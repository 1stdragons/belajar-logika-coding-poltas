"""Prepare an isolated demo or run opt-in, planning-only Claude conversation checks."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import uuid


ROOT = Path(__file__).resolve().parents[1]
SCENARIO = ROOT / "tests/scenarios/notion-dupe.json"
FILE_TOOLS = "Read,Glob,Grep,Write,Edit,Skill"


def load_scenario():
    return json.loads(SCENARIO.read_text(encoding="utf-8"))


def prepare(scene_name, parent=None):
    scenario = load_scenario()
    scene = scenario["scenes"][scene_name]
    run = Path(tempfile.mkdtemp(prefix="vibe-wise-notion-", dir=parent))
    project = run / "project"
    project.mkdir()
    if scene["files"]:
        state = project / ".vibe-wise"
        state.mkdir()
        (state / "profile.md").write_text(scenario["profile"], encoding="utf-8")
        for name, content in scene["files"].items():
            (state / name).write_text(content, encoding="utf-8")
    # These instructions and future learner answers stay OUTSIDE the demo project.
    metadata = {
        "scene": scene_name,
        "plugin_version": json.loads((ROOT / ".claude-plugin/plugin.json").read_text())["version"],
        "plugin_root": str(ROOT),
        "scenario_sha256": hashlib.sha256(SCENARIO.read_bytes()).hexdigest(),
        "guide_hashes": {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted((ROOT / "skills/learn").glob("*.md"))
        },
        "session_id": str(uuid.uuid4()),
    }
    (run / "run.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (run / "review.json").write_text(json.dumps(scene["review"], indent=2) + "\n")
    return run, scene, metadata


def base_command(claude):
    return [claude, "--plugin-dir", str(ROOT), "--setting-sources", "",
            "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']


def environment():
    return {**os.environ, "CLAUDE_CODE_AUTO_CONNECT_IDE": "false"}


def summarize_output(stdout):
    """Keep visible responses and tool calls; omit hidden reasoning and init details."""
    texts, calls, model, result = [], [], None, None
    for line in stdout.splitlines():
        row = json.loads(line)
        if row.get("type") == "system" and row.get("subtype") == "init":
            model = row.get("model")
        if row.get("type") == "assistant":
            for block in row.get("message", {}).get("content", []):
                if block.get("type") == "text":
                    texts.append(block["text"])
                elif block.get("type") == "tool_use":
                    calls.append({"name": block["name"], "input": block.get("input", {})})
        if row.get("type") == "result":
            result = row.get("subtype")
    return {"assistant": "\n\n".join(texts), "tools": calls,
            "model": model, "result": result}


def application_files(project):
    # Planning scenes may only create/update their learning notes.
    return sorted(str(p.relative_to(project)) for p in project.rglob("*")
                  if p.is_file() and p.relative_to(project).parts[0] != ".vibe-wise")


def check(run, scene, metadata, claude, budget, timeout):
    project = run / "project"
    transcript = []
    for number, prompt in enumerate(scene["turns"], 1):
        print("Turn {}/{}".format(number, len(scene["turns"])), flush=True)
        command = base_command(claude) + [
            "--print", "--tools", FILE_TOOLS, "--allowedTools", FILE_TOOLS,
            "--permission-mode", "dontAsk", "--output-format", "stream-json",
            "--verbose", "--max-budget-usd", str(budget),
            "--session-id" if number == 1 else "--resume", metadata["session_id"], prompt,
        ]
        completed = subprocess.run(command, cwd=project, env=environment(),
                                   capture_output=True, text=True, timeout=timeout)
        # Save errors locally, even if a failed process didn't produce valid JSON.
        if completed.stderr:
            (run / "turn-{:02d}.stderr.txt".format(number)).write_text(completed.stderr)
        output = summarize_output(completed.stdout)
        output["user"] = prompt
        output["exit_code"] = completed.returncode
        output["application_files"] = application_files(project)
        (run / "turn-{:02d}.json".format(number)).write_text(
            json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        transcript.append("You:\n{}\n\nClaude:\n{}\n".format(prompt, output["assistant"]))
        (run / "conversation.txt").write_text("\n".join(transcript), encoding="utf-8")
        print(output["assistant"], flush=True)
        if completed.returncode or output["result"] != "success" or not output["assistant"]:
            raise RuntimeError("Claude did not finish successfully; inspect the run artifacts.")
        if output["application_files"]:
            raise RuntimeError("Application files appeared before approval: " +
                               ", ".join(output["application_files"]))
    print("\nMechanical checks passed: completed turns; no application files created.")
    print("Teaching quality still needs review against review.json and the demo guide.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "check"))
    parser.add_argument("--scene", choices=tuple(load_scenario()["scenes"]), default="fresh")
    parser.add_argument("--launch", action="store_true", help="Open interactive Claude after prepare")
    parser.add_argument("--claude", default="claude", help="Claude executable name or path")
    parser.add_argument("--budget", type=float, default=1.0,
                        help="Pass this --max-budget-usd to each check invocation (default: 1)")
    parser.add_argument("--timeout", type=int, default=180, help="Seconds allowed per check turn")
    args = parser.parse_args()
    if args.budget <= 0 or args.timeout <= 0:
        parser.error("budget and timeout must be positive")
    if args.action == "check" and args.launch:
        parser.error("--launch is only for prepare")
    if (args.action == "check" or args.launch) and not shutil.which(args.claude):
        parser.error("Claude executable not found; set --claude to its path")
    run, scene, metadata = prepare(args.scene)
    print("Run folder: " + str(run), flush=True)
    print("Project: " + str(run / "project"), flush=True)
    try:
        if args.action == "check":
            check(run, scene, metadata, args.claude, args.budget, args.timeout)
        else:
            command = base_command(args.claude)
            print("\n" + shlex.join(["cd", str(run / "project")]))
            print(shlex.join(command))
            print("\nFirst message: " + scene["turns"][0], flush=True)
            if args.launch:
                return subprocess.call(command, cwd=run / "project", env=environment())
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        print("Check failed: {}\nArtifacts: {}".format(error, run), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
