# Local state templates

Create only these three files in the chosen project's `.sensible-vibes/`.
Replace bracketed values with actual evidence or “Not specified.” Keep the two
status lines unformatted and near the top; the restoration hook reads them.
Do not replace existing state with a fresh template.

## profile.md

```markdown
# Learner Profile

Learning mode: active
Onboarding: complete

## Project
Situation: [New / Existing / Known]
Building: [project purpose]
Codebase familiarity: [answer]
Learning scope: [entire system / parts we touch / mixed]

## Experience
Overall programming: [answer]
Stack familiarity: [per-technology answers if given]

## Goals
Primary: [answer]
Capability goal: [optional answer]

## Preferences
Checkpoint frequency: Normal
Question style: Open-ended
Implementation style: AI writes code

## Strong Concepts
No demonstrated understanding recorded yet.

## Developing Concepts
None recorded yet.

## Revisit
None recorded yet.
```

## progress.md

```markdown
# Learning Progress

No learning events recorded yet.
```

As learning occurs, add a `## Topic` with concise bullets under Introduced,
Demonstrated understanding, and Needs reinforcement. Record reasoning evidence,
not quotations of a whole exchange. Consolidate repeated entries. Keep each
topic independently readable so it can be loaded without the whole file.
While waiting on a decision review, keep a short `## Pending decision` section
with the proposed approach and what reply is awaited. Remove it once resolved.
Include the checkpoint's decision name and stage: awaiting reasoning, choice
confirmation, or implementation approval. Record confirmed choices in the map
without claiming they are implemented. Keep any proposed coding scope explicit.

## project-map.md

```markdown
# Project Map

## Purpose
[What this software does.]

## Components
[Components, responsibilities, and supporting file paths.]

## Main Flow
[Compact text diagram with labeled arrows. Mark unknowns and distinguish proposed,
chosen, and implemented components.]

## Data and Trust Boundaries
[Storage, ownership, auth, external services; unknown when unverified.]

## Build and Deployment
[Commands and configuration paths verified in the repository.]

## Unknowns
[What still needs inspection or a decision.]
```
