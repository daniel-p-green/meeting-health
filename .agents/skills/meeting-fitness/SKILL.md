---
name: meeting-fitness
description: Use when the user wants to analyze meetings, calendar events, collaborators, or workday schedule patterns against Apple Health heart-rate data. Trigger for phrases like "meeting fitness", "calendar heart rate", "meeting stress load", "which meetings raise my heart rate", or "analyze my calendar with Apple Health".
---

# Meeting Fitness

Analyze calendar events against Apple Health heart-rate data and produce a private, caveated meeting fitness report.

## Scope

Use this skill for personal calendar analysis that combines:

- Calendar events with start and end times.
- Apple Health `heartRate` samples.
- Optional context from `restingHeartRate`, `heartRateVariabilitySDNN`, `sleepAnalysis`, `stepCount`, `activeEnergyBurned`, and workouts.

Do not present results as medical advice, mental-health diagnosis, employee evaluation, or objective proof that another person caused a physiological response.

## Default Workflow

1. Confirm the analysis window.
   - If the user gives no range, use the last 14 complete days.
   - Use the user's local timezone when available.
   - Prefer a feasibility check before a full report when this is the first run.

2. Check health-data coverage.
   - Verify that Apple Health has `heartRate` data for the requested range.
   - If sample density is sparse, say so before running a detailed report.
   - Check optional metrics only when they improve interpretation.

3. Pull calendar events.
   - Retrieve title, start, end, organizer, attendees, recurrence, location, and meeting link metadata when available.
   - Exclude all-day events, declined events, focus blocks, reminders, and events shorter than 5 minutes unless the user asks to include them.
   - Keep private identifiers out of any shareable output.

4. Build meeting windows.
   - For each event, define the meeting window from event start to event end.
   - Ignore meetings with no heart-rate samples unless reporting data gaps.
   - Flag overlaps instead of double-counting heart-rate samples across overlapping meetings.

5. Build baselines.
   - Default baseline: 30 minutes before meeting start.
   - Exclude overlapping meetings from the baseline when possible.
   - Exclude workouts or obvious movement periods when supporting data is available.
   - If the baseline has too few samples, fall back to same-day non-meeting work-hour baseline and mark the fallback.

6. Calculate meeting metrics.
   - `baseline_avg_hr`: average heart rate during the baseline window.
   - `meeting_avg_hr`: average heart rate during the meeting window.
   - `hr_delta`: `meeting_avg_hr - baseline_avg_hr`.
   - `elevated_minute_share`: share of meeting samples above `baseline_avg_hr + baseline_std_hr`.
   - `sample_count`: number of heart-rate samples used.
   - `meeting_stress_load`: `max(hr_delta, 0)` for the meeting.

7. Aggregate results.
   - By meeting title or recurring event.
   - By attendee, only when attendee data is available and privacy-safe.
   - By organizer.
   - By day.
   - By time of day.
   - By meeting category when titles can be classified safely.

8. Interpret carefully.
   - Prefer language like "associated with", "appears activating", and "appears calming".
   - Call out confounders: sleep, caffeine, workouts, walking, illness, medication, speaking, high-stakes presentation, or missing samples.
   - Highlight variance as a finding when a person or recurring meeting has both high and low deltas.

## Report Format

Produce a concise Markdown report unless the user asks for another format.

Use this structure:

```md
# Meeting Fitness Report

## Executive Summary

## Data Coverage

## Top Activating Meetings

## Calming Meetings

## Daily Meeting Stress Load

## Collaborator and Recurring Meeting Patterns

## Calendar Recommendations

## Caveats

## Appendix: Method
```

Include tables for the main rankings. Prefer anonymized people names in shareable reports.

## Privacy Rules

- Treat raw health and calendar data as private.
- Do not commit raw exports, event lists, names, emails, or exact meeting logs.
- Ask before creating a shareable report with identifiable people or meeting titles.
- For public examples, anonymize people, organizations, locations, exact dates, and titles.
- Do not infer private attributes about attendees.

## Success Criteria

A successful run should clearly state:

- The date range analyzed.
- Whether `heartRate` coverage was sufficient.
- The number of meetings included and excluded.
- The baseline method used.
- The highest-confidence findings.
- The main caveats and skipped checks.

## Suggested Prompts

```text
$meeting-fitness
Check if my Apple Health heart-rate data is dense enough for a meeting fitness report over the last 14 days.
```

```text
$meeting-fitness
Create a private meeting fitness report for the last 30 days. Use a 30-minute pre-meeting baseline and anonymize attendees.
```

```text
$meeting-fitness
Find recurring meetings that appear consistently activating or calming. Keep the output local and privacy-safe.
```

