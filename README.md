# VibeWise

**You build. AI writes.**

A Claude Code plugin that puts learning first while AI writes the code. You work through each meaningful build decision: Claude **asks for your approach first**, then gives feedback, explains unfamiliar concepts, and asks follow-ups where needed. Your reasoning shapes the design. You review the approach together before Claude implements it.

Built for junior or aspiring engineers under pressure to ship with AI. Practice planning how the pieces fit together, anticipating failures, and checking the result—while keeping ownership of the decisions.

## Get started

You need [Claude Code](https://code.claude.com/docs/en/setup) and Python 3 (`python3` on your PATH).

In Claude Code, run:

```text
/plugin marketplace add nykooi1/vibe-wise
/plugin install vibe-wise@vibe-wise
```

Restart Claude Code in the project you want to work on, then run:

```text
/vibe-wise:learn
```

Setup asks one question at a time. Use the arrow keys and Enter for choices; pick **Use defaults** to skip preference setup. Then ask Claude to build something. Starting fresh or joining an unfamiliar repository both work. For an existing repository, Claude first inspects the code and sketches a small system map.

## What it feels like

A condensed example adapted from a real notes-app learning session. Later
implementation steps are illustrative; intervening design discussions are omitted.

**You:**

```text
A note can be in several folders. Deleting a folder should delete its notes.
```

**Claude:**

---

**✦ Build checkpoint: Deleting a shared note**

"Trip ideas" is in both Travel and Summer. Deleting it removes it from both.

When someone deletes Travel, what should happen to that note in Summer?

**You:**

```text
Keep it in Summer. If it has no folders left, keep the note outside any folder.
```

**Claude:**

That separates deleting a folder from deleting a note.

---

**✦ Build checkpoint: Connecting notes and folders**

How would you represent which folders a note belongs to, without copying the note?

**You:**

```text
A links table with note_id and folder_id. Deleting a folder removes its links,
not the notes.
```

**Claude:**

Each link records one membership. Several links can point to the same note;
a note with no links is unfiled.

`notes ← folder links → folders`

---

**✦ Decision checkpoint: Folder membership**

Proposed: store notes once and track folder membership in a links table.
Deleting a folder removes its links and keeps the notes. This supports multiple
folders per note; loading a folder's notes needs a lookup through those links.

Confirming records this design. We still need to work through access rules
and technology choices before writing code.

```text
❯ 1. Confirm and continue
     This approach makes sense to me; move to the next piece.
  2. Discuss
     Ask questions or clarify anything that doesn't make sense before deciding.
```

**You:**

```text
Confirm and continue.
```

*Later, after the remaining choices for this step are worked through...*

**Claude:**

---

**✦ Implementation checkpoint: Folder membership**

I'll add the agreed tables and folder-deletion operation, then test that deleting
a folder preserves its notes and their membership in other folders.
This step builds storage behavior; the UI comes later.

```text
❯ 1. Implement this step
     This approach makes sense to me; write the code for this step.
  2. Discuss
     Ask questions or clarify anything that doesn't make sense before deciding.
```

**You:**

```text
Implement this step.
```

*Claude writes the code and runs the tests.*

**Claude:**

---

**✦ Implementation report: Folder membership**

- Added the schema migration: each membership references one note and one folder.
- Added folder deletion: removes the folder and its links, preserving note content.
- Added and ran tests for shared notes and notes left without a folder; both passed.

You don't need to know the answer already. Claude can explain unfamiliar concepts, sketch the relevant pieces, and help you tackle a smaller question. You stay involved in forming the plan. Answer in plain English; ask for more help or say “skip” whenever you want.

Describing what you want sets the requirements. Build Checkpoints ask you to work
out how it should function; a feature preference doesn't approve an architecture.

| Checkpoint | What happens |
| --- | --- |
| **Build** | You reason through how to approach the problem with Claude. |
| **Decision** | Review the design. **Confirm and continue** records it and continues planning; no code yet. |
| **Implementation** | Review the specific code changes. **Implement this step** authorizes Claude to make them. |

These aren't three mandatory stops. When ready to code, the Implementation
checkpoint also confirms the design, skipping a separate Decision checkpoint.
Both confirmations offer **Discuss** to ask questions, clarify anything confusing,
or explore alternatives before deciding.

When Claude proposes additional implementation details, it separates them from your
decisions in a short list or table explaining each addition and why it matters.
You can question or change any item before proceeding.

After implementation, Claude briefly explains what changed, how the key code works,
why it fits your decision, any tests it added or updated and what they cover, and
which checks ran with their results. Ask to dig deeper anywhere it's unclear.

Small diagrams help you trace data, understand relationships, and see how the system fits together.

[Recreate the notes-app demo](docs/demos/notion-dupe.md), including discussing
password storage and questioning details Claude proposes.

## Make it yours

Experience changes the support you get, not your ownership of decisions:

| Level | Teaching approach |
| --- | --- |
| Beginner | Explain unfamiliar pieces, use diagrams, ask smaller reasoning questions. |
| Intermediate | Less introductory context; explore interactions and tradeoffs. |
| Advanced | Probe difficult constraints, failure modes, and design assumptions. |

Everyone reasons first. Claude adapts to what you demonstrate and how familiar you
are with the stack. Checkpoint frequency—Light, Normal, or Frequent—is separate.

- “Use fewer checkpoints.”
- “Focus on backend architecture.”
- “Use multiple-choice questions.”
- “Just implement this one.”
- “Pause learning.” Resume with `/vibe-wise:learn`.

Preferences, learning notes, and a project map live in `.vibe-wise/` in your project. Learning mode resumes in future sessions and after compaction. Add `.vibe-wise/` to your `.gitignore` to keep your notes out of Git; the plugin won't change it silently.

No extra account, backend, or telemetry. Saved notes are included in Claude's context, so your normal Claude Code data settings still apply.

To start learning this project from scratch, run `/vibe-wise:reset`. It shows the
project and asks **Cancel / Reset learning**. After confirmation, it backs up your
profile, progress, and project map inside the notes directory's `backups/` folder,
then restarts onboarding. Source code and other projects stay untouched. To change
your experience level or preferences, just tell Claude; no reset is needed.

## Updating

For automatic updates, open `/plugin` → **Marketplaces** → **vibe-wise** →
**Enable auto-update**. Auto-update is off by default for third-party marketplaces.
Claude Code notifies you after an update; restart Claude Code to load the new version.

To update manually, run these in your terminal:

```sh
claude plugin marketplace update vibe-wise
claude plugin update vibe-wise@vibe-wise
```

Then restart Claude Code. Your project learning notes stay intact; no reset is needed.
Run `claude plugin list` to check the installed version.
[More about plugin updates](https://code.claude.com/docs/en/discover-plugins#keep-plugins-updated).

## Try a local checkout

Before this version is published, or to develop locally, launch Claude from your project with an absolute path to this checkout:

```sh
claude --plugin-dir /absolute/path/to/vibe-wise
```

Then run `/vibe-wise:learn`. [Development and testing](docs/development.md).

## License

[MIT](LICENSE). You can use, modify, and share this software, including commercially. Keep the license notice with copies. The software comes without a warranty.
