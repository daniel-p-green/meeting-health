# Meeting Health

A Codex skill for Apple Watch users who want to compare calendar meetings with Apple Health heart-rate data.

Meeting Health joins calendar events with HealthKit `heartRate` samples, compares each meeting with a 30-minute pre-meeting baseline, and produces a private report on which meetings appear activating, calming, or variable.

The project is inspired by Eric Porres's post, ["Your Calendar Has a Heart Rate"](https://promptedbyeric.substack.com/p/your-calendar-has-a-heart-rate). His post describes a Whoop-plus-calendar workflow for analyzing meetings as a kind of training load. This repo ports that idea to Apple Health and Apple Watch users. It is not affiliated with Eric Porres, MeetingScience, Logitech, Whoop, or Apple, and it does not reproduce Eric's private data or exact implementation.

## What It Does

Use the skill when you want Codex to:

- Check whether Apple Health has enough Apple Watch `heartRate` samples for analysis.
- Pull calendar events for a selected date range.
- Compare each meeting against a 30-minute baseline before the meeting.
- Calculate meeting HR delta, elevated share, and daily Meeting Stress Load.
- Find activating, calming, and high-variance meetings.
- Roll up patterns by day, recurring meeting, attendee, organizer, category, and time of day.
- Create deterministic charts from computed metrics.
- Keep the report private unless you explicitly ask for a sanitized version.

Generated images are allowed only for optional conceptual art, such as a cover image for a sanitized report. They are never used for measured charts, rankings, axes, or values.

## What Carries Over From The Whoop Method

Eric's workflow used a Whoop stream, Google Workspace calendar data, a per-minute join, 47 meetings, 137 attendees, and a 30-minute baseline comparison. Meeting Health keeps the core method and adapts the data handling for Apple Health.

| Method element | Whoop workflow | Meeting Health |
| --- | --- | --- |
| Wearable source | Whoop heart-rate stream | Apple Health `heartRate`, ideally from Apple Watch |
| Calendar source | Google Workspace calendar | Any Codex-accessible calendar connector, usually Google Calendar |
| Join grain | Per-minute meeting windows | Raw samples or minute buckets, depending on Apple Health density |
| Baseline | 30 minutes before meeting | 30 minutes before meeting, with overlaps removed when possible |
| Meeting score | Meeting HR above baseline | `hr_delta = meeting_avg_hr - baseline_avg_hr` |
| Elevated share | Minutes above baseline plus one standard deviation | Dense data: minute share. Sparse data: sample share, clearly labeled |
| Daily load | Sum of positive meeting deltas | Daily Meeting Stress Load |
| People patterns | Attendee and collaborator effects | Attendee, organizer, and recurring-meeting rollups when privacy-safe |
| Output | Meeting fitness report | Private Codex report, with optional sanitized summary |

## Apple Health Differences

Apple Health is not always a clean per-minute stream. Even Apple Watch `heartRate` samples can be irregular. The skill treats that as part of the analysis instead of hiding it.

It adds:

- A feasibility check before a full report.
- Sample-density checks and confidence labels.
- Overlap handling so the same heart-rate samples are not counted twice.
- Optional movement and workout checks using `stepCount`, `activeEnergyBurned`, and `workout`.
- Optional sleep and recovery context using `sleepAnalysis`, `restingHeartRate`, and `heartRateVariabilitySDNN`.
- A Simpson's-paradox check when day-level and meeting-level patterns disagree.
- A visualization contract: quantitative charts are deterministic; generated images are conceptual only.
- Synthetic fixtures and a validator so the public repo can be tested without real health or calendar data.

## Install

Codex can discover repo-scoped skills from `.agents/skills` inside a repository.

Clone the repo, open it in Codex, then mention the skill:

```text
$meeting-health
Analyze my last 14 days of meetings against Apple Health heart rate.
```

You can also copy the skill folder into your user skills directory:

```bash
mkdir -p "$HOME/.agents/skills"
cp -R .agents/skills/meeting-health "$HOME/.agents/skills/"
```

Restart Codex if the skill does not appear immediately.

## Requirements

You need:

- Codex with access to this repository or a user-installed copy of the skill.
- Apple Health data synced into a connector Codex can use.
- Apple Watch heart-rate samples in HealthKit `heartRate`.
- Calendar access, such as Google Calendar, available to Codex.
- Enough heart-rate samples during meeting windows and baseline windows to make comparisons meaningful.

Helpful HealthKit metrics include `restingHeartRate`, `heartRateVariabilitySDNN`, `sleepAnalysis`, `stepCount`, `activeEnergyBurned`, and `workout`.

## Recommended First Run

Start with a feasibility check:

```text
$meeting-health
Check whether my Apple Health heart-rate data and calendar events are sufficient for a 14-day meeting health report. Do not generate the full report yet.
```

If coverage looks usable, run a private report:

```text
$meeting-health
Create a private meeting health report for the last 14 complete days. Use a 30-minute pre-meeting baseline, exclude overlapping calendar time from the baseline when possible, and anonymize attendee names in the final report.
```

For a shareable version, ask for sanitization:

```text
$meeting-health
Create a sanitized shareable summary from the private report. Remove exact dates, meeting titles, locations, links, names, and emails.
```

For charts:

```text
$meeting-health
Create a private meeting health report with deterministic charts for daily Meeting Stress Load, top activating meetings, and time-of-day patterns. If you add generated imagery, use it only as a conceptual cover image.
```

## Method

For each meeting, the skill should:

1. Pull event metadata: title, start, end, organizer, attendees, response status, transparency, recurrence, location, and meeting-link metadata when available.
2. Exclude all-day events, declined events, transparent holds, focus blocks, reminders, travel, decompression blocks, and events shorter than 5 minutes unless the user asks to include them.
3. Pull `heartRate` samples for the meeting window and the nearby baseline window.
4. Prefer a 30-minute baseline before the meeting.
5. Exclude other meeting time, workouts, travel, and obvious movement spikes when the data supports it.
6. Compute average baseline HR, baseline standard deviation, average meeting HR, HR delta, sample count, elevated share, and confidence.
7. Aggregate by day, recurring meeting, attendee, organizer, category, and time of day.
8. Flag high-variance people or recurring meetings instead of forcing them into "good" or "bad" labels.
9. Create deterministic charts when they help the user inspect the pattern.
10. Present findings with uncertainty, missing-data notes, and privacy-safe recommendations.

See [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for formulas, [docs/VISUALIZATIONS.md](docs/VISUALIZATIONS.md) for chart rules, and [docs/REPORT_TEMPLATE.md](docs/REPORT_TEMPLATE.md) for the report shape.

## Validation

Run the repo check:

```bash
scripts/check.sh
```

The validator checks:

- README coverage for install, use, requirements, privacy, caveats, contribution, and license.
- Skill YAML front matter.
- Required methodology, visualization, and report-template docs.
- Synthetic fixtures.
- Basic privacy and secret hygiene for tracked files.

It does not query Apple Health or Calendar. Live connector testing happens inside Codex when a user runs the skill.

## Current Proof

This repo has been tested with:

- The local package validator.
- Synthetic fixtures for baseline, HR delta, elevated share, Meeting Stress Load, exclusions, and deterministic SVG chart output.
- A live feasibility check confirming that Apple Health `heartRate`, Apple Watch samples, and calendar events can be reached from one Codex environment.

That is enough to treat this as a usable v0 skill package. It is not proof that every user's connectors, watch data, or calendar shape will work without adjustment.

## Privacy

This workflow touches health and calendar data. Treat outputs as private by default.

Before sharing:

- Remove attendee names, email addresses, meeting titles, locations, links, descriptions, and exact timestamps.
- Replace people with stable aliases such as `Contact A`.
- Replace event titles with categories such as `1:1`, `sales call`, `team meeting`, or `presentation rehearsal`.
- Keep raw Apple Health exports and calendar exports out of git.
- Do not publish claims about other people based on one person's physiology.

## Interpretation Caveats

Heart rate is not a clean stress label. It can move because of caffeine, sleep, illness, medication, workouts, walking between meetings, room temperature, posture, speaking, excitement, or sensor gaps.

Use this as a personal reflection and calendar-design tool. Do not use it to rank employees, diagnose health conditions, or make performance decisions about other people.

## Contributing

This is open source under the MIT License. Forks, issues, and pull requests are welcome.

Useful improvements include:

- Better Apple Health density checks.
- More accurate calendar filtering.
- Deterministic chart examples.
- Synthetic fixtures for edge cases.
- Clearer privacy-safe report patterns.

Please keep contributions privacy-safe. Do not add real Apple Health exports, calendar exports, meeting titles, names, email addresses, screenshots, connector payloads, or generated reports based on real people.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT. See [LICENSE](LICENSE).

## Repo Layout

```text
.agents/skills/meeting-health/SKILL.md   # The Codex skill
docs/METHODOLOGY.md                      # Formula and workflow contract
docs/VISUALIZATIONS.md                   # Chart and image-generation rules
docs/REPORT_TEMPLATE.md                  # Private and shareable report shape
fixtures/                                # Synthetic examples only
scripts/check.sh                         # Local validation wrapper
scripts/validate_repo.py                 # Repo contract checks
README.md                                # Public repo guide
CONTRIBUTING.md                          # Contribution guidelines
AGENTS.md                                # Contributor instructions
LICENSE                                  # MIT license
```

## Status

Public v0. The skill is ready for careful use and forking. Live analysis still depends on each user's Apple Health and calendar connector setup.
