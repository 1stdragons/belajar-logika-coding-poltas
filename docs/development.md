# Development

V1 is a Claude Code skill, Markdown instructions, and one read-only Python hook.
There are no packages to install. Python 3.8+ is sufficient for the hook and tests.

## Local checks

```sh
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
claude plugin validate skills
python3 -B -m unittest discover -s tests -v
git diff --check
```

The tests execute the registered hook command with real JSON stdin in temporary
projects. They cover activation, restoration, partial onboarding, paused mode,
subdirectories, repository/worktree boundaries, missing/invalid files, symlinks,
bounded context, and read-only behavior. They do not prove teaching quality.

## Conversation smoke tests

Use an authenticated Claude Code session and temporary copies of projects.
Launch with `claude --plugin-dir /absolute/path/to/sensible-vibes`.

1. **Fresh project:** Run `/sensible-vibes:learn`. Choose a new project, describe
   a small CLI, and accept preference defaults. Check that all three state files
   are created, the map separates proposed from implemented components, and no
   understanding is marked demonstrated without evidence. Choice questions must
   use native pickers with one question per screen; no questionnaire dump or
   failed shell check for a missing state directory.
2. **Existing unfamiliar repository:** Use a separate copy of a real repository.
   Choose the existing-repository flow. Confirm Claude reads actual entry points
   and configuration, gives an accurate short map before familiarity questions,
   asks whole-system versus focused scope, and doesn't invent a frontend/database.
3. **Checkpoint → implementation:** Ask for a meaningful feature, such as durable
   storage or retrying an external request. Confirm Claude asks one reasoning
   question under a title naming the decision, before suggesting its own solution
   or implementing the decision. Give a partial answer; check that
   it refines the answer, names the coding scope, and offers Implement this step /
   Discuss first. Select Discuss
   first, ask for clarification or propose an alternative, and confirm it stays
   paused and updates the approach if needed. Select Implement this step;
   check it writes the code and records only evidenced learning. Restart while a
   decision review is pending and confirm it preserves that pause.
4. **Skip and adaptation:** Say “I don't know” or “skip.” Confirm Claude explains
   the approach and offers the decision review without quizzing again. “Just
   implement it” should proceed. Make a trivial edit and confirm no checkpoint. After demonstrating
   a concept, check that later questions address new decisions rather than repeat it.
5. **Lifecycle:** Restart, resume, `/clear`, and `/compact`. Confirm preferences,
   the map, and mastered concepts survive without repeated onboarding. Pause
   learning, restart, and confirm it stays paused; invoke Learn to resume.
6. **Guided foundations:** With a beginner profile and a new project, check that
   stack, storage, and deployment remain visible open decisions. Ask what an
   unfamiliar term means while answering a checkpoint. Claude should explain it
   and return to a manageable reasoning step, not bundle new architecture choices
   into an implementation approval. Use different projects to avoid overfitting.
   A design-only review should offer Use this choice / Discuss first. Confirming
   it records the choice and continues to unresolved decisions without writing
   application code. Implementation approval must name a concrete coding scope.

Do not commit `.sensible-vibes/` or test transcripts. The plugin recommends an
ignore rule during onboarding, but changes `.gitignore` only after telling the
user and receiving their instruction to make the edit.

## Design and official references

Verified against current first-party documentation on 2026-09-28:

- [Plugin creation](https://code.claude.com/docs/en/plugins/create): standard
  component directories and `--plugin-dir` for local loading.
- [Skills](https://code.claude.com/docs/en/skills): the command is
  `/sensible-vibes:learn`. Explicit invocation starts onboarding; the hook restores
  behavior in later sessions only where a learner profile already exists.
- [Hooks](https://code.claude.com/docs/en/hooks): `SessionStart` sources include
  `startup`, `resume`, `clear`, `compact`, and `fork`. The hook emits
  `hookSpecificOutput.additionalContext`, keeping it below the 10,000-character
  limit. It embeds behavior and bounded profile/map excerpts, plus pending-decision
  markers and a progress topic index; Claude reads full relevant notes when necessary.
- [Marketplace creation](https://code.claude.com/docs/en/plugin-marketplaces):
  the small catalog points to this repository's plugin root. The GitHub install
  instructions work after these files are published to the remote repository.
- [Anthropic's learning-output-style plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/learning-output-style):
  inspected its SessionStart configuration and context injection. SensibleVibes
  supplies its own reasoning-first instructions and leaves implementation to AI.

No `PreCompact` hook is needed: it doesn't provide an opportunity for Claude to
save learning notes through `additionalContext`. Save notes at meaningful events
and restore them through `SessionStart` with source `compact`. Unsaved reasoning
can still be lost if a session ends before Claude writes it; the hook doesn't
infer progress from transcripts. State writes are performed by Claude using
normal permissions, so denied writes should be reported rather than called saved.

Keep V1 local and terminal-native. No backend, analytics, accounts, separate LLM
calls, scoring engine, or custom UI. Saved context is processed by Claude Code
under the user's existing data settings.

## V1 verification

Tested on 2026-09-28 with Claude Code 2.1.240:

- Plugin, marketplace, and skill validation passed; installation in an isolated
  local marketplace configuration succeeded.
- All 16 hook tests passed, including simulated compact/clear/resume events.
- Live Claude sessions completed fresh-project onboarding and orientation of an
  unfamiliar copy of this repository. A new session restored saved preferences.
- The fresh-project session asked about persistence, reviewed the learner's JSON
  storage proposal, waited through clarification (the choice was initially named
  Ask a question; now Discuss first), then wrote
  the CLI after Implement. Its five generated CLI/storage tests passed locally.

Those initial live tests used print mode with file tools and covered the plain-text
choice fallback. For 0.1.1, additional checks on Claude Code 2.1.284 verified the
native first-question picker and Enter selection in an interactive terminal.
The following prompt asked only for the project description. A separate beginner
conversation kept foundational choices open, asked a named checkpoint, and returned
to that checkpoint after explaining unfamiliar concepts, without implementing.

For 0.1.2, a live design-review check offered Use this choice / Discuss first and
explicitly described recording the choice and moving to the next decision without
writing code. This check used print mode's text fallback.

All 16 hook tests still pass. The actual `/compact` command still needs an
interactive smoke test. Checkpoint quality remains model-dependent; these examples
verify observed behavior, not a guarantee for every conversation.
