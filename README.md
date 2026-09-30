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

```text
You:
  Build a reading list I can share with friends, but only I can edit.

Claude:
  | ✦ 🧠 BUILD CHECKPOINT - Who can change a shared list |
  | :--- |
  | Friends need to read the list without being able to change it. |
  | **How would you make sure only the owner can edit?** |

[Claude waits for your reasoning before responding.]

You:
  I'd check on the server that the person making the change owns the list.

Claude:
  That puts the check somewhere visitors can't change it. We'd need to
  check every request that changes the list, even if the UI hides the edit button.

  ────────────────────────────────────────────────────────────

  ✦ 💬 DECISION CHECKPOINT - Who can change a shared list

  Proposed: check ownership on the server before allowing a change. This keeps
  friends' viewing access separate from editing. Edits must pass through the server.

  If confirmed, we'll record this access rule. Next, we'll work through how the
  server knows who's making the request; we haven't chosen that yet.

  ❯ 1. Confirm and continue
       This approach makes sense to me; move to the next piece.
    2. Discuss
       Ask questions or clarify anything that doesn't make sense before deciding.
```

You don't need to know the answer already. Claude can explain unfamiliar concepts, sketch the relevant pieces, and help you tackle a smaller question. You stay involved in forming the plan. Answer in plain English; ask for more help or say “skip” whenever you want.

Describing what you want sets the requirements. Build Checkpoints ask you to work
out how it should function; a feature preference doesn't approve an architecture.

**Confirm and continue** means the approach makes sense to you and you're ready for the next design decision. **Implement this step** writes the specific code Claude just described. **Discuss** gives you room to ask questions, clarify anything confusing, or explore alternatives before deciding.

When Claude proposes additional implementation details, it separates them from your
decisions in a short list or table explaining each addition and why it matters.
You can question or change any item before proceeding.

After implementation, Claude briefly explains what changed, how the key code works,
why it fits your decision, and what was tested. Ask to dig deeper anywhere it's unclear.

Small diagrams help you trace data, understand relationships, and see how the system fits together.

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

## Upgrading from SensibleVibes

The plugin and marketplace are now named `vibe-wise`. In Claude Code, run:

```text
/plugin marketplace remove sensible-vibes
/plugin marketplace add nykooi1/vibe-wise
/plugin install vibe-wise@vibe-wise
```

Removing the old marketplace uninstalls its plugin. Restart Claude, then use
`/vibe-wise:learn`. Existing `.sensible-vibes/` notes are reused in place; keep their
Git ignore rule. New projects use `.vibe-wise/`. If both directories exist at the
same location, `.vibe-wise/` takes precedence; files aren't merged automatically.

## License

[MIT](LICENSE). You can use, modify, and share this software, including commercially. Keep the license notice with copies. The software comes without a warranty.
