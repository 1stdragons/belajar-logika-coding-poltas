# SensibleVibes

**You build. AI writes.**

A Claude Code plugin that helps you learn how to build software while AI writes the code. At meaningful decisions, Claude asks how you'd approach the problem, refines the approach with you, then writes the implementation when you're ready.

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
You: Add Stripe subscriptions.

Claude: ✦ BUILD CHECKPOINT - Handling duplicate payment events
Stripe can deliver the same event more than once.
How would you prevent it from updating a subscription twice?

You: Save the event ID and check whether we already handled it?

Claude: Yes—that's the idea behind idempotency.

✦ DECISION REVIEW - Handling duplicate payment events
We'll save the event ID and update the subscription in one
transaction, so concurrent deliveries can't process it twice.

1. Implement
2. Discuss first
```

Answer in plain English. If you're unsure, say “I don't know” or “skip,” and Claude explains the approach. Before implementing a checkpoint decision, choose **Implement** or **Discuss first** to ask questions, raise concerns, or explore alternatives. Claude writes the code.

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
