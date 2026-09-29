# Development

V1 uses Claude Code skills, Markdown instructions, one read-only Python hook,
and a small Python helper for confirmed learning resets.
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
Rename coverage verifies that `.sensible-vibes/` notes restore without migration,
`.vibe-wise/` takes precedence at the same location, and legacy lookup preserves
repository boundaries, nearest-state selection, and symlink rejection.
Reset tests cover read-only preview, confirmed backup/reset, stale confirmation,
legacy and partial notes, nested projects, repeated backups, rejected symlinks,
backup/write failures, and restoring incomplete onboarding after reset.

## Conversation smoke tests

Use an authenticated Claude Code session and temporary copies of projects.
Launch with `claude --plugin-dir /absolute/path/to/vibe-wise`.

1. **Fresh project:** Run `/vibe-wise:learn`. Choose a new project, describe
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
   Decision Checkpoint is pending and confirm it preserves that pause.
4. **Skip and adaptation:** Say “I'm completely lost.” Confirm Claude explains
   the relevant pieces and returns one manageable reasoning step, without dumping
   a complete plan or repeatedly demanding guesses. Ask for an explanation or say “skip”; it should
   explain and proceed to a Decision Checkpoint without demanding another attempt. “Just
   implement it” should proceed. Make a trivial edit and confirm no checkpoint. After demonstrating
   a concept, check that later questions address new decisions rather than repeat it.
5. **Lifecycle:** Restart, resume, `/clear`, and `/compact`. Confirm preferences,
   the map, and mastered concepts survive without repeated onboarding. Pause
   learning, restart, and confirm it stays paused; invoke Learn to resume.
6. **Guided foundations:** With a beginner profile and a new project, check that
   essential capabilities are established and preserved when selecting a platform;
   stack, storage, and deployment must remain visible open decisions. Ask what an
   unfamiliar term means while answering a checkpoint. Claude should explain it
   and return to a manageable reasoning step, not bundle new architecture choices
   into an implementation approval. Use different projects to avoid overfitting.
   A design-only Decision Checkpoint should offer Confirm approach / Discuss first. Confirming
   it records the choice and continues to unresolved decisions without writing
   application code. Implementation approval must name a concrete coding scope.
7. **Preference versus reasoning:** Answer a checkpoint with a tentative preference
   and no rationale. Claude should ask one focused question about implications or
   tradeoffs, not invent the learner's reasoning, praise mastery, or immediately
   present confirmation buttons. Verify that this holds across different projects.
8. **Diagrams:** During orientation or a system check, confirm a compact terminal
   diagram shows real components and labeled flows. Unknowns and proposals must
   stay explicit; diagrams before reasoning must not silently decide the solution.
   Build and Decision Checkpoints should start with a divider and bold named title
   with three `✦` stars on each side and a consistent icon (🧠 Build, 💬 Decision,
   🔎 System),
   followed by brief context and a bold question (or native picker), with no
   trailing paragraphs obscuring the point where the learner should respond.
9. **Clarification without steering:** Ask about an unfamiliar concept mid-decision.
   Claude should clarify it, correct any misleading framing, and return to one
   question about the project's requirements or constraints. It should not replace
   reasoning with a solution menu, bundle independent choices, or steer toward an
   architecture because it offers more learning opportunities.
10. **Learning first:** With default preferences, make an ordinary build request.
    Before any recommendation, solution menu, revealing diagram, dependency install,
    or application scaffold, Claude must ask for the learner's approach and wait.
    Answer, then check that refinement doesn't silently decide the next problem.
    Test unfamiliar concepts with neutral background, and familiar concepts with
    a new tradeoff: neither should remove the learner's turn to reason. Explicitly
    requesting a suggestion, multiple choice, or a skip should still be respected.

11. **Experience levels:** Setup offers Beginner / Intermediate / Advanced for
    experience and stack familiarity. Compare the same decision across profiles:
    background and question depth should adapt, while every level still reasons
    before suggestions. An advanced learner unfamiliar with the stack should get
    grounding when needed. Existing Some experience / Comfortable profiles should
    resume with intermediate guidance, without rewriting history or re-onboarding.
    Experience must not change the saved checkpoint frequency.

12. **Evaluation and concise confirmation:** Give a confident but flawed proposal;
    Claude should name the violated constraint rather than praise confidence.
    Give a sound proposal; it should explain why and combine feedback with a concise
    Decision Checkpoint, without redundant questions. Compare two viable approaches:
    tradeoffs should be tied to the project, not a claim of one correct answer.
    The checkpoint describes a proposal until confirmed and must not invent an
    unresolved issue. No code should be written before implementation approval.

13. **Reset:** In a temporary project with saved learning notes, invoke
    `/vibe-wise:reset`. Confirm it shows the absolute project and state paths and
    asks Cancel / Reset learning. Cancel must leave all files unchanged. Invoke
    again and confirm: original notes must exist in the reported backup, the
    active profile must be incomplete, and onboarding must ask fresh questions
    rather than reuse old preferences. Repeat with legacy notes and after restart.
    If notes change during confirmation, Claude must preview and confirm again.

14. **Requirements versus design:** Give a product requirement without proposing
    a mechanism. Claude should record the requirement, then invite a concrete
    design attempt before offering a solution or confirmation. It must not count
    the requirement as demonstrated engineering understanding. Combine a near-term
    single-user pilot with future public availability; Claude should preserve both
    rather than invent a contradiction or choose the storage layout itself. Ask
    for grounding: the response should clarify concepts and return an open design
    step, not give the complete design and quiz the learner on recalling it.
    Check that this applies across boundaries, stack, storage location, database
    model, data structures, and deployment. Reasoning about one operation must not
    silently approve the remaining foundational choices; keep them in the map.
    Ask for a model of components, entities, relationships, and flows. Diagrams
    should clarify the learner's model, preserving unknown links until discussed,
    rather than present a complete architecture for the learner to rubber-stamp.
15. **Implementation report:** After an approved step, Claude should explain the
    changed files, important code mechanics, connection to the learner's design,
    and actual verification results. Keep it concise, with optional deeper detail;
    avoid a line-by-line lecture or another mandatory approval. New design choices
    discovered during implementation still need a reasoning checkpoint.
    Feedback should be factual and specific, with no personal praise, hype, or
    congratulatory filler. Corrections should be direct without belittling.

Do not commit `.vibe-wise/` or test transcripts. The plugin recommends an
ignore rule during onboarding, but changes `.gitignore` only after telling the
user and receiving their instruction to make the edit.

## Design and official references

Verified against current first-party documentation on 2026-09-28:

- [Plugin creation](https://code.claude.com/docs/en/plugins/create): standard
  component directories and `--plugin-dir` for local loading.
- [Skills](https://code.claude.com/docs/en/skills): the command is
  `/vibe-wise:learn`. Explicit invocation starts onboarding; the hook restores
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
  inspected its SessionStart configuration and context injection. VibeWise
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

For 0.1.4, a tentative preference with no rationale triggered a follow-up question
instead of confirmation buttons or application code. The first run omitted its
checkpoint heading; after clarifying that follow-ups keep a heading, the repeat
used a named checkpoint. These checks establish that the interaction paused, not
that a complete session will consistently teach good engineering judgment.

All 16 hook tests still pass. The actual `/compact` command still needs an
interactive smoke test. Checkpoint quality remains model-dependent; these examples
verify observed behavior, not a guarantee for every conversation.

For 0.1.9, a live print-mode session with default preferences paused an ordinary
build request before suggesting a stack or writing application code. Its initial
scope question bundled multiple details; the instructions now explicitly limit
requirements gathering to one focused question too. After scope confirmation,
“I'm completely lost” received an incomplete end-to-end diagram and a plain-English
question about the missing flow. Claude left language, storage, and indexing open,
and changed only learning notes. This verifies the observed grounding behavior;
the revised requirements-question pacing still needs a fresh-session check.

For 0.1.13, the VibeWise rename passes all 21 hook tests and plugin, marketplace,
and skill validation. New notes use `.vibe-wise/`; existing `.sensible-vibes/`
notes remain in place and are restored by the renamed plugin.

For 0.1.14, reset uses a read-only preview and an explicit confirmation before
calling the helper with that snapshot's token. Backups stay inside the selected
state directory so its existing ignore rule applies. Only the three learning
notes are replaced. A replacement failure may leave a partial reset; the helper
reports failure and the backup path, and the skill stops instead of onboarding.
All 35 tests and plugin, marketplace, and skill validation pass.
A live print-mode smoke test verified the text confirmation fallback: preview
changed no notes, explicit Reset learning backed up all three originals, and
Claude asked the first onboarding question without carrying forward old preferences.
The fixture's source file stayed unchanged. Reset's native picker still needs an
interactive check; the existing Learn picker was verified in earlier testing.

For 0.1.15, print-mode checks during prompt revision kept a public-access
requirement separate from architecture approval and reflected a learner-proposed
data model without choosing the remaining stack or storage. Grounding responses
were still too expansive, motivating the shorter behavior instructions.
A final check with the shortened prompt implemented an explicitly approved
write-then-replace file update, verified successful saves and preservation of the
original after a serialization failure, and explained the code and its connection
to the learner's decision. The report used three top-level bullets but expanded
them into nested detail: brevity remains inconsistent. These checks exercise
individual interactions, not a guarantee of teaching quality across a full session.
