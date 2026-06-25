# AGENTS.md

These instructions apply to this repository.

## Project Goal

This repo packages a public, privacy-safe Codex skill for analyzing Apple Health heart-rate data against calendar meetings.

## Defaults

- Keep the repo small, readable, and installable.
- Preserve privacy by default. Do not add real health data, calendar exports, email addresses, meeting titles, or screenshots.
- Keep claims honest. This is a personal reflection and calendar-design workflow, not a medical, diagnostic, or employee-evaluation product.
- Prefer instruction-first skill design unless deterministic scripts clearly improve reliability.
- If adding scripts, include tests or sample fixtures with synthetic data only.

## Public Content Rules

- Reference Eric Porres's original post as inspiration, not as affiliation or endorsement.
- Avoid implying this repo reproduces his private dataset or exact implementation.
- Do not publish sensitive local connector details.
- Use synthetic examples for documentation.

## Verification

Before considering changes done:

- Confirm `README.md` explains install, use, requirements, privacy, and caveats.
- Confirm `.agents/skills/meeting-fitness/SKILL.md` has valid YAML front matter with `name` and `description`.
- Confirm no raw data or secrets are present.

