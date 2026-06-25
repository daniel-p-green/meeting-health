# Meeting Fitness Skill

A Codex skill for analyzing how calendar events line up with Apple Health heart-rate data.

This repo packages a repeatable workflow for a private "meeting fitness" report: join timestamped calendar events with Apple Health `heartRate` samples, compare each meeting against a nearby baseline, and summarize which meetings appear activating, calming, or variable.

The idea is inspired by Eric Porres's post, ["Your Calendar Has a Heart Rate"](https://promptedbyeric.substack.com/p/your-calendar-has-a-heart-rate), which describes using wearable data and calendar data to test whether meetings leave a measurable physiological trace.

## What This Is

This is a Codex skill, not a hosted app and not a medical device.

Use it when you want Codex to:

- Check whether Apple Health has enough `heartRate` data for analysis.
- Pull calendar events for a selected date range.
- Compare meeting heart rate against a pre-meeting baseline.
- Produce a private report with meeting-level and day-level patterns.
- Keep health and calendar data local unless you explicitly export a sanitized report.

## What It Produces

The skill guides Codex toward a report with:

- Meeting HR delta: average meeting heart rate minus baseline heart rate.
- Elevated-minute share: percent of meeting samples above baseline plus one standard deviation.
- Meeting Stress Load: sum of positive HR deltas across meetings in a day.
- Calming meetings: meetings with consistent negative HR deltas.
- High-variance collaborators or recurring meetings.
- Calendar coaching recommendations with caveats.

## Install

Codex can discover repo-scoped skills from `.agents/skills` inside a repository.

Clone the repo, open it in Codex, then mention the skill:

```text
$meeting-fitness
Analyze my last 14 days of meetings against Apple Health heart rate.
```

You can also copy the skill folder into your user skills directory:

```bash
mkdir -p "$HOME/.agents/skills"
cp -R .agents/skills/meeting-fitness "$HOME/.agents/skills/"
```

Restart Codex if the skill does not appear immediately.

## Requirements

You need:

- Codex with access to this repository.
- Apple Health data synced into a connector Codex can use.
- Calendar access, such as Google Calendar, available to Codex.
- Enough heart-rate samples during work hours to make meeting windows meaningful.

For Apple Watch users, the key HealthKit metric is `heartRate`. Helpful supporting metrics include `restingHeartRate`, `heartRateVariabilitySDNN`, `sleepAnalysis`, `stepCount`, and `activeEnergyBurned`.

## Recommended First Run

Start with a narrow feasibility check:

```text
$meeting-fitness
Check whether my Apple Health heart-rate data and calendar events are sufficient for a 14-day meeting fitness report. Do not generate the full report yet.
```

If coverage looks good, run:

```text
$meeting-fitness
Create a private meeting fitness report for the last 14 days. Use a 30-minute pre-meeting baseline, exclude overlapping calendar time from the baseline when possible, and anonymize attendee names in the final report.
```

## Method

For each meeting:

1. Pull event metadata: title, start, end, organizer, attendees, and recurrence when available.
2. Pull `heartRate` samples for the event window and a nearby baseline window.
3. Prefer a 30-minute baseline before the meeting.
4. Exclude other meeting time, workouts, and obvious movement spikes when the data supports it.
5. Compute average baseline HR, average meeting HR, HR delta, sample count, and elevated-minute share.
6. Aggregate by day, recurring meeting, attendee, organizer, and time of day.
7. Present results with uncertainty, missing-data notes, and privacy-safe recommendations.

## Privacy

This workflow touches sensitive health and calendar data. Treat outputs as private by default.

Before sharing:

- Remove attendee names, email addresses, meeting titles, locations, and exact timestamps.
- Replace people with stable aliases such as `Contact A`.
- Replace event titles with categories such as `1:1`, `sales call`, or `team meeting`.
- Keep raw Apple Health exports out of git.
- Avoid publishing claims about other people based on one person's physiology.

## Interpretation Caveats

Heart rate is not a clean stress label. It can move because of caffeine, sleep, illness, medication, workouts, walking between meetings, room temperature, posture, speaking, or excitement.

Use this as a personal reflection and calendar-design tool. Do not use it to rank employees, diagnose health conditions, or make performance decisions about other people.

## Repo Layout

```text
.agents/skills/meeting-fitness/SKILL.md  # The Codex skill
README.md                                # Public repo guide
AGENTS.md                                # Contributor instructions
LICENSE                                  # MIT license
```

## OpenAI Codex Notes

OpenAI's Codex docs describe skills as reusable workflow packages with a `SKILL.md` file plus optional scripts and references. They also note that repo-scoped skills can be checked into `.agents/skills` inside a repository, which is the layout used here.

Reference: [OpenAI Codex skills documentation](https://developers.openai.com/codex/skills).

## Status

Early public scaffold. The current version is intentionally instruction-first so it can adapt to the user's available Apple Health and calendar connectors.
