# SensibleVibes

**You build. AI writes.**

A Claude Code plugin that puts learning first while AI writes the code. You work through each meaningful build decision: Claude asks how you'd approach it **before suggesting a solution**, waits for your reasoning, then helps refine it. You review the approach together before Claude implements it.

Built for junior or aspiring engineers under pressure to ship with AI. Practice planning how the pieces fit together, anticipating failures, and checking the result—while keeping ownership of the decisions.

## Get started

You need [Claude Code](https://code.claude.com/docs/en/setup) and Python 3 (`python3` on your PATH).

In Claude Code, run:

```text
/plugin marketplace add nykooi1/sensible-vibes
/plugin install sensible-vibes@sensible-vibes
```

Restart Claude Code in the project you want to work on, then run:

```text
/sensible-vibes:learn
```

Setup asks one question at a time. Use the arrow keys and Enter for choices; pick **Use defaults** to skip preference setup. Then ask Claude to build something. Starting fresh or joining an unfamiliar repository both work. For an existing repository, Claude first inspects the code and sketches a small system map.

## What it feels like

```text
You: Build a reading list I can share with friends, but only I can edit.

Claude:
────────────────────────────────────────────────────────────

✦ ✦ ✦ BUILD CHECKPOINT - Who can change a shared list ✦ ✦ ✦

Friends need to read the list without being able to change it.

How would you make sure only the owner can edit?

[Claude waits for your reasoning before offering an approach.]

You: I'd check on the server that the person making the change owns the list.

Claude: That puts the check somewhere visitors can't change it. We'd need to
check every request that changes the list, even if the UI hides the edit button.

────────────────────────────────────────────────────────────

✦ ✦ ✦ DECISION REVIEW - Who can change a shared list ✦ ✦ ✦

We'll check ownership on the server before allowing a change. Friends' viewing
access won't grant editing access. That means edits must pass through the server.

If confirmed, we'll record this access rule. Next, we'll work through how the
server knows who's making the request; we haven't chosen that yet.

❯ 1. Use this choice
  2. Discuss first
```

You don't need to know the answer already. Claude can explain unfamiliar concepts, sketch the relevant pieces, and help you tackle a smaller question. You stay involved in forming the plan. Answer in plain English; ask for more help or say “skip” whenever you want.

**Use this choice** records a design decision and continues planning. **Implement this step** writes the specific code Claude just described. **Discuss first** lets you ask questions or explore alternatives before either action.

Small diagrams help you trace data, understand relationships, and see how the system fits together.

## Make it yours

- “Use fewer checkpoints.”
- “Focus on backend architecture.”
- “Use multiple-choice questions.”
- “Just implement this one.”
- “Pause learning.” Resume with `/sensible-vibes:learn`.

Preferences, learning notes, and a project map live in `.sensible-vibes/` in your project. Learning mode resumes in future sessions and after compaction. Add `.sensible-vibes/` to your `.gitignore` to keep your notes out of Git; the plugin won't change it silently.

No extra account, backend, or telemetry. Saved notes are included in Claude's context, so your normal Claude Code data settings still apply.

## Try a local checkout

Before this version is published, or to develop locally, launch Claude from your project with an absolute path to this checkout:

```sh
claude --plugin-dir /absolute/path/to/sensible-vibes
```

Then run `/sensible-vibes:learn`. [Development and testing](docs/development.md).

## License

[MIT](LICENSE). You can use, modify, and share this software, including commercially. Keep the license notice with copies. The software comes without a warranty.
