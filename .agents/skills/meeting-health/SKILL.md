---
name: meeting-health
description: Use when the user wants to analyze meetings, calendar events, collaborators, or workday schedule patterns against Apple Health or Apple Watch heart-rate data. Trigger for phrases like "meeting health", "meeting fitness", "calendar heart rate", "meeting stress load", "which meetings raise my heart rate", "Apple Watch meetings", or "analyze my calendar with Apple Health".
---

# Meeting Health

Analyze calendar events against Apple Health heart-rate data and produce a private, caveated meeting health report.

## Scope

Use this skill for personal calendar analysis that combines:

- Calendar events with start and end times.
- Apple Health `heartRate` samples, ideally recorded by Apple Watch.
- Optional context from `restingHeartRate`, `heartRateVariabilitySDNN`, `sleepAnalysis`, `stepCount`, `activeEnergyBurned`, and `workout`.

This skill ports the core methodology from Eric Porres's "Your Calendar Has a Heart Rate" workflow to Apple Health users:

- Join wearable heart-rate samples to calendar meeting windows.
- Compare each meeting with a 30-minute pre-meeting baseline.
- Rank activating, calming, and high-variance meetings.
- Roll up daily Meeting Stress Load.
- Look for attendee, organizer, recurring-meeting, and time-of-day patterns.
- Turn the results into personal calendar coaching.

Do not present results as medical advice, mental-health diagnosis, employee evaluation, or objective proof that another person caused a physiological response.

## Run Modes

Choose the smallest mode that answers the user.

1. Feasibility check
   - Use for first runs, unclear connector access, or broad date ranges.
   - Report whether Apple Health `heartRate` and calendar data are available and dense enough.
   - Do not produce meeting rankings yet.

2. Private full report
   - Use when the user explicitly asks for analysis or a report.
   - It may include real meeting titles and names only if the user asked for a private report.
   - Keep raw data local to the thread/tool context.

3. Sanitized shareable report
   - Use only when the user asks for shareable output.
   - Remove exact dates, names, emails, meeting titles, links, locations, descriptions, and raw event logs.
   - Replace people and events with stable aliases and categories.

## Default Workflow

1. Confirm the analysis window.
   - If the user gives no range, use the last 14 complete days.
   - Use the user's local timezone when available.
   - Prefer a feasibility check before a full report when this is the first run.

2. Check health-data coverage.
   - Verify that Apple Health has `heartRate` data for the requested range.
   - Prefer Apple Watch samples when source metadata is available.
   - If sample density is sparse, say so before running a detailed report.
   - Check optional metrics only when they improve interpretation.

3. Pull calendar events.
   - Retrieve title, start, end, organizer, attendees, response status, recurrence, transparency, location, and meeting link metadata when available.
   - Exclude all-day events, declined events, transparent holds, focus blocks, reminders, travel, decompression blocks, and events shorter than 5 minutes unless the user asks to include them.
   - Keep private identifiers out of any shareable output.

4. Build meeting windows.
   - For each event, define the meeting window from event start to event end.
   - Ignore meetings with no heart-rate samples unless reporting data gaps.
   - Flag overlapping meetings instead of double-counting heart-rate samples across multiple meetings.
   - For overlapping meetings, either exclude them from rankings or mark confidence as low unless one event is clearly the primary meeting.

5. Build baselines.
   - Default baseline: 30 minutes before meeting start, `[start - 30m, start)`.
   - Exclude overlapping meetings, travel blocks, workouts, and obvious movement periods when possible.
   - If the baseline has too few samples, fall back to same-day non-meeting work-hour baseline and mark the fallback.
   - If no credible baseline exists, exclude the meeting from rankings and report the data gap.

6. Normalize heart-rate samples.
   - Apple Health samples can be irregular rather than exactly per-minute.
   - Use raw samples directly for averages.
   - When sample density supports it, optionally bucket samples by minute and average multiple samples in the same minute.
   - Do not silently interpolate missing minutes. If interpolation is used for a chart, label it as display-only.

7. Calculate meeting metrics.
   - `baseline_avg_hr`: average heart rate during the baseline window.
   - `baseline_std_hr`: standard deviation during the baseline window.
   - `meeting_avg_hr`: average heart rate during the meeting window.
   - `meeting_max_hr`: maximum heart rate during the meeting window.
   - `hr_delta`: `meeting_avg_hr - baseline_avg_hr`.
   - `elevated_share`: share of meeting samples above `baseline_avg_hr + baseline_std_hr`.
   - `sample_count`: number of heart-rate samples used for the meeting.
   - `baseline_sample_count`: number of samples used for the baseline.
   - `meeting_stress_load`: `max(hr_delta, 0)` for the meeting.
   - `duration_weighted_load`: optional improvement, `max(hr_delta, 0) * duration_minutes / 30`.

8. Assign confidence.
   - High: meeting and baseline both have enough samples, no major overlap, no obvious movement/workout confounder.
   - Medium: adequate samples with minor gaps or mild confounders.
   - Low: sparse samples, overlapping meetings, fallback baseline, or likely movement/workout confounder.
   - Never rank low-confidence meetings above high-confidence meetings without saying why.

9. Aggregate results.
   - By meeting title or recurring event.
   - By attendee, only when attendee data is available and privacy-safe.
   - By organizer.
   - By day.
   - By time of day.
   - By meeting category when titles can be classified safely.

10. Match the source methodology's main findings.
   - Top activating meetings.
   - Calming meetings.
   - Daily Meeting Stress Load.
   - Collaborator or attendee effects.
   - High-variance collaborators or recurring meetings.
   - Time-of-day periodization recommendations.
   - Simpson's-paradox checks when day-level and meeting-window results disagree.

11. Create visualizations when useful.
   - Use deterministic charting for quantitative visuals, such as a chart widget, plotting library, spreadsheet chart, SVG, or Mermaid diagram built from computed metrics.
   - Do not use image generation for numeric charts, axis labels, rankings, or exact values.
   - Use image generation only for optional conceptual or editorial visuals, such as a privacy-safe "calendar as training plan" illustration, and clearly separate it from measured results.
   - For private reports, charts may use real event titles and people only when the user asked for a private report.
   - For shareable reports, charts must anonymize names, titles, exact dates, locations, links, and raw timestamps.
   - Every quantitative chart should state the baseline method, whether elevated share is sample-based or minute-based, and any confidence caveat.

12. Interpret carefully.
   - Prefer language like "associated with", "appears activating", "appears calming", and "may be a recovery meeting".
   - Call out confounders: sleep, caffeine, workouts, walking, illness, medication, speaking, high-stakes presentation, room temperature, sensor gaps, or missing samples.
   - Highlight variance as a finding when a person or recurring meeting has both high and low deltas.
   - Do not claim the calendar caused the heart-rate pattern.

## Report Format

Produce a concise Markdown report unless the user asks for another format.

Use this structure for private reports:

```md
# Meeting Health Report

## Executive Summary

## Data Coverage

## Method

## Top Activating Meetings

## Calming Meetings

## Daily Meeting Stress Load

## Visualizations

## Collaborator and Recurring Meeting Patterns

## Time-of-Day Patterns

## High-Variance Findings

## Calendar Recommendations

## Caveats

## Appendix: Included and Excluded Data
```

Include tables for the main rankings. Prefer anonymized people names in shareable reports.

Recommended quantitative visuals:

- Meeting heart-rate timeline: heart-rate samples overlaid with baseline average and elevated threshold for one selected meeting.
- Activating and calming meetings: bar chart of `hr_delta`, grouped or annotated by confidence.
- Daily Meeting Stress Load: bar or line chart by day.
- Time-of-day pattern: heatmap or small table showing average `hr_delta` and load by time block.
- Collaborator or recurring-meeting pattern: dot plot of average `hr_delta` versus range, sized by meeting count.
- Data coverage: sample-count chart by day or window so sparse data is visible.

## Privacy Rules

- Treat raw health and calendar data as private.
- Do not commit raw exports, event lists, names, emails, locations, links, screenshots, or exact meeting logs.
- Ask before creating a shareable report with identifiable people or meeting titles.
- For public examples, anonymize people, organizations, locations, exact dates, and titles.
- Do not infer private attributes about attendees.

## Success Criteria

A successful run should clearly state:

- The date range analyzed.
- Whether `heartRate` coverage was sufficient.
- The number of calendar events fetched.
- The number of meetings included and excluded.
- The main exclusion reasons.
- The baseline method used.
- Whether elevated share means minute share or sample share.
- Which visualizations were created, if any, and whether they are deterministic charts or conceptual generated images.
- The highest-confidence findings.
- The main caveats and skipped checks.
- Whether the output is private or sanitized/shareable.

## Suggested Prompts

```text
$meeting-health
Check if my Apple Health heart-rate data is dense enough for a meeting health report over the last 14 complete days.
```

```text
$meeting-health
Create a private meeting health report for the last 30 days. Use a 30-minute pre-meeting baseline and anonymize attendees in the final summary.
```

```text
$meeting-health
Find recurring meetings that appear consistently activating or calming. Keep the output local and privacy-safe.
```

```text
$meeting-health
Create a shareable version of the report with people, titles, exact dates, locations, and links removed.
```

```text
$meeting-health
Create a private meeting health report with charts for daily Meeting Stress Load, top activating meetings, and time-of-day patterns. Use generated imagery only for an optional conceptual cover image, not for data charts.
```
