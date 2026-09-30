# Notion-style notes app demo

Rehearse the learning flow from the playground conversation: define the scope,
explore folder deletion, propose the data relationships, and discuss sign-in.
The scenario uses paraphrased learner inputs and synthetic notes. It includes no
private transcript, credentials, or generated application source.

The original conversation loaded VibeWise 0.1.23 and had an existing starter.
This demo loads the current checkout and starts clean, so the current card titles
and wording apply. Expect the same learning opportunities, not identical replies
or checkpoint ordering. No changes to the plugin's teaching prompts are needed.

## Start a fresh recording

From the VibeWise repository, in a terminal with Claude Code installed and signed in:

```sh
python3 scripts/notion_demo.py prepare --launch
```

The helper creates a new temporary project and launches interactive Claude with
this checkout. It skips user/project/local settings and external MCP configuration
to keep other installed plugins out of the rehearsal. Managed settings still apply.
It doesn't reset or modify your existing playground. No dependencies or database
are installed, and you don't need to run `git init`.

In Claude, enter `/vibe-wise:learn`. Choose **New project**, describe a Notion-style
notes app, choose **Beginner**, then **Use defaults**. Stack familiarity can wait
until you choose a stack.

Use these responses when the relevant question comes up. Follow the actual
conversation; don't paste the whole script or jump past a question you don't
understand. Claude may need a different follow-up.

| Moment | Learner input | What to look for |
| :--- | :--- | :--- |
| Scope | “Sign in, create/read/edit/delete private notes, and organize them in folders.” | Requirements get clarified without choosing a stack. |
| Folder behavior | “A note can be in several folders. Folders can't contain folders. Deleting a folder should delete its notes.” | A concrete example reveals that a shared note could disappear from another folder too. |
| Revise the rule | “Keep it in any other folders. If none are left, leave it outside every folder.” | Your revision changes the requirements. Claude leaves the representation for you to propose. |
| Main flow | “The browser sends the note to our backend, which checks who I am and saves it in a database. Later it loads my notes.” | Feedback examines responsibilities and gaps in your proposal. |
| Privacy | “Send a session key. The backend checks it, then checks the note's owner against that user. Browser-only checks could be bypassed.” | Reasoning is evaluated before confirming the access design. |
| Data model | “Use a links table with note_id and folder_id. Deleting a folder removes link rows, not notes.” | Claude evaluates your relationship model instead of supplying it first. |
| Sign-in | “We should store a hashed password, not the password itself.” | Missing concepts are explained; additional details remain labeled as proposals. |
| Discuss an addition | Select **Discuss**: “What is a salt, and why does it help?” | The agent explains and keeps implementation paused. |
| Zoom out | “Can we trace the whole design so far?” | A system diagram distinguishes your choices from open questions. |

Choose **Confirm and continue** only when the displayed design makes sense to you.
It records the choice; it doesn't authorize implementation. If recording ends
here, you've shown the reasoning and discussion loop. To continue building, choose
the remaining technology decisions and approve one concrete scope with
**Implement this step**. Expect an implementation report afterward. Dependency
setup, Docker, and app implementation are outside the automated scenes below.

Each `prepare` makes a new project. For another take, exit Claude and run the
command again. `/vibe-wise:reset` resets learning notes but keeps application
code, so it isn't a clean-project reset. Run folders remain in the system temp
directory for inspection; save anything you want to keep before your OS cleans it.

## Rehearse a specific scene

```sh
python3 scripts/notion_demo.py prepare --scene folders --launch
python3 scripts/notion_demo.py prepare --scene data-model --launch
python3 scripts/notion_demo.py prepare --scene sign-in --launch
```

These start with **synthetic saved decisions** to skip earlier conversation.
The helper prints the first message to send. When filming a shortcut, describe
where you're picking up; these fixtures aren't evidence of earlier learner reasoning.
Omit `--launch` to prepare only and print the launch commands.

## Run conversation checks

These use your signed-in Claude account and consume usage. Each invocation gets
a `--max-budget-usd` limit (default 1) and a 180-second timeout; multi-turn scenes
invoke Claude more than once. They use the configured default model and record
its reported name. Use `--claude /path/to/claude` if it isn't on PATH.

```sh
python3 scripts/notion_demo.py check --scene fresh
python3 scripts/notion_demo.py check --scene folders
python3 scripts/notion_demo.py check --scene data-model
python3 scripts/notion_demo.py check --scene sign-in
```

The runner resumes the same session for each learner turn. It exposes file tools
and the Skill tool, but no shell, network tools, or native question picker. This
tests the text fallback; use the interactive demo to review pickers and rendering.
It stops on CLI failures, budget exhaustion, or application files appearing before
approval. Those mechanical checks do **not** establish that the teaching was good.

Every run prints its artifact directory:

```text
vibe-wise-notion-<unique>/
├── project/           Empty project or synthetic .vibe-wise notes
├── run.json           Scene, plugin version, guide hashes, session ID
├── review.json        Human-review criteria for that scene
├── turn-01.json       Learner input, visible response, tools, model, result
└── conversation.txt   Visible conversation across completed turns
```

Review the conversation and saved notes against `review.json`. Check that no
future solution appears before a learner attempt and that proposed additions
haven't become confirmed choices without approval. Future scripted answers and
review criteria aren't copied into the project or included in the model prompts.

Don't preserve mistakes from the original as expected answers. In particular,
flag unsupported absolutes about database access or data types, praise without
evaluation, and claims that one architecture is required merely for learning.
Avoid exact wording snapshots: a different, sound follow-up should still pass review.

The runner and fixtures live in the repo; generated conversations stay outside it.
The regular unit tests validate fixture isolation and runner failure handling
without invoking Claude:

```sh
python3 -B -m unittest discover -s tests -v
```

## Initial verification

On 2026-09-30, all four live scenes completed without creating application files
before approval. These runs preceded the separate Implementation checkpoint label.
Fresh onboarding asked only the project-situation question. The
staged reasoning scenes emitted the current Build checkpoint table with padding
rows, and the data-model scene waited for the learner's links-table proposal.

Human review found differences from the original: the folder scene repeated a
clarification after the learner revised the deletion rule, and sign-in asked a
further reasoning question instead of immediately presenting proposed additions.
The later request for an explanation received one, but this run did not exercise
a native Discuss picker or the proposed-additions table. Those remain interactive
review points, not claimed passes. The 42 unit tests validate the tooling and
existing hook/reset behavior; they do not grade the conversations.

## Example: discussing an unfamiliar detail

This condensed adaptation of the original sign-in discussion shows why **Discuss**
matters. It illustrates the interaction, not an exact transcript or a required
password-storage design. The folder example in the [README](../../README.md#what-it-feels-like)
shows Build, Decision, and Implementation checkpoints together.

**Claude:**

```text
╭────────────────────────────────────────────────────────────────────╮
│ ✦ Build checkpoint: Password storage                               │
├────────────────────────────────────────────────────────────────────┤
│ What would you store so we can check someone's password when they  │
│ sign in?                                                           │
╰────────────────────────────────────────────────────────────────────╯
```

**You:**

```text
A hashed password, not the password itself.
```

**Claude:**

A hash lets us verify a password without storing the original. Password storage
also needs a method designed to make repeated guesses expensive, and a unique
salt so equal passwords don't produce equal stored hashes.

**✦ Decision checkpoint: Password storage**

Your proposal: store a password hash. Details to discuss before confirming:

| Detail | Proposal | Why it matters |
| --- | --- | --- |
| Hashing method | Use a password-hashing library with scrypt | Makes each guess expensive |
| Salt | Let the library generate a fresh random salt per password | Prevents reuse of precomputed guesses across users |

```text
❯ 1. Confirm and continue
     This approach makes sense to me; move to the next piece.
  2. Discuss
     Ask questions or clarify anything that doesn't make sense before deciding.
```

**You:**

```text
Discuss. What is a salt?
```

**Claude:**

Extra random data mixed into the password before hashing. Two people with the
same password get different hashes because their salts differ. We store the salt
alongside the hash so we can repeat the check at sign-in; it doesn't need to be secret.

The hashing method and salt handling are still proposals. We haven't confirmed
them or started implementing.

An Implementation checkpoint comes when a specific coding step is ready. It can
confirm the design and authorize that step together; don't add a separate Decision
checkpoint just to repeat the same approval.
