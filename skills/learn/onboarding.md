# First-time onboarding

Keep this conversational and short. Accept free-form answers, batch related
preferences, and reuse information the user already supplied. Do not quiz during
onboarding. The user may accept defaults or skip questions; mark unknowns honestly.

Tell the user: “I'll keep your preferences and a small project map in
`.sensible-vibes/` here. I recommend adding it to `.gitignore` so your learning
notes stay out of Git.” Do not edit `.gitignore` unless the user wants the edit;
announce it before making it. Explain that AI writes the code by default, and
after each checkpoint the user can choose Implement or Discuss first.

## Project situation

Ask: “What are we doing? A. Starting a new project; B. Working in an existing
repository; C. Continuing a project I already know.”
Skip this question only if the user has already stated their situation. An empty
folder alone is not an answer. Ask this first, before the preference batch.

- **New:** Ask what they are building (unless already known). Establish the
  intended product; proposed architecture is a proposal, not an existing system.
- **Existing:** Before asking about architecture familiarity, inspect the repo.
  Read project guidance, README, directory structure, dependency manifests,
  entry points, routing, data/schema layer, auth, external integrations, and
  deployment configuration. Exclude generated/vendor directories and secret
  values. Follow one representative flow; this is orientation, not an audit.
  Create the initial map with file-path evidence, unknowns, and major boundaries.
  Present a concise flow and key external services. Then ask codebase familiarity
  (basically new / worked in it a little / know it well) and learning scope
  (entire system / mostly parts we touch / a mix). Never assume a web app stack.
- **Known:** Ask familiarity with the current architecture. Do a brief inspection
  to maintain an evidence-based map, avoiding introductory teaching they don't
  need. Infer or ask desired scope if it isn't clear.

## Preferences

Ask these in a compact conversational batch, not an eight-turn questionnaire:

- Overall programming experience: Beginner / Some experience / Comfortable /
  Advanced.
- Familiarity with this project's stack: New / Some experience / Comfortable /
  Advanced. Accept distinctions across technologies.
- Main learning goals: systems end to end / architecture / backend / frontend /
  debugging / infrastructure and deployment / engineering fundamentals / all.
- Checkpoint frequency: Light / **Normal** / Frequent.
- Question style: **Open-ended** / Multiple choice / Mixed.
- Implementation: **AI writes code** / Mix of AI and me / More hands-on coding.
- Optional: “What do you hope to become capable of?”

Offer “use the defaults” for the bold preferences. Do not silently fill in
experience or goals. If skipped, record “Not specified” and adapt from evidence.

Use state-templates.md to save answers and the map. If setup spans turns, save
known answers with `Onboarding: incomplete` and a short `Remaining onboarding`
list so a restart can resume it. Mark complete when the user finishes or chooses
to proceed with defaults. Never label self-reported experience as demonstrated
understanding. Summarize the chosen preferences in one sentence and start building.
