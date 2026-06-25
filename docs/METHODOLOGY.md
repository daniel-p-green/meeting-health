# Methodology

This document defines the analysis contract for the Meeting Health skill. It is designed to preserve the core of the Whoop-plus-calendar method described in Eric Porres's "Your Calendar Has a Heart Rate", while adapting it honestly for Apple Health and Apple Watch data.

The goal is personal calendar reflection. The output is not medical advice, a stress diagnosis, or an employee-evaluation tool.

## Source Method Parity

The source workflow combined wearable heart-rate data, calendar events, a 30-minute baseline, meeting-level rankings, attendee scoring, daily load, and training-plan-style recommendations.

This skill should preserve those elements:

- Wearable heart-rate samples joined to calendar meeting windows.
- 30-minute baseline before each meeting.
- Meeting-level `hr_delta`.
- Elevated share above baseline plus one standard deviation.
- Daily Meeting Stress Load.
- Attendee, organizer, and recurring-meeting rollups when privacy-safe.
- High-variance findings where the spread matters more than the average.
- Time-of-day recommendations that treat the calendar like a training plan.
- Deterministic visuals that make the measured patterns inspectable.

## Apple Health Adaptation

Whoop data may be available as a dense stream. Apple Health `heartRate` data can be irregular, even when recorded by Apple Watch.

Use these rules:

- Prefer Apple Watch `heartRate` samples when source metadata is available.
- Use raw samples for statistical averages.
- Bucket to minute-level only when sample density supports it.
- Do not silently interpolate missing heart-rate minutes.
- If a chart uses interpolation for readability, label it as display-only and do not use it for rankings.
- If data is sparse, say "elevated sample share" rather than "elevated minute share".

## Calendar Event Filtering

Include events that are plausible meetings:

- Timed events lasting at least 5 minutes.
- Accepted or owner-created meetings.
- Events with attendees, organizer metadata, or meeting links when available.
- Recurring meetings and one-off meetings.

Exclude by default:

- All-day events.
- Declined events.
- Transparent events.
- Focus blocks.
- Travel blocks.
- Decompression or recovery holds.
- Reminders and tasks.
- Events with no usable heart-rate samples.
- Events where no credible baseline can be constructed.

Report exclusions by reason.

## Meeting Window

For each included event:

```text
meeting_window = [event_start, event_end)
```

If meetings overlap:

- Flag the overlap.
- Do not double-count the same heart-rate samples across multiple ranked meetings.
- If one event is clearly a hold or transparent event, exclude the hold.
- If two real meetings overlap, mark confidence as low or exclude both from ranked findings.

## Baseline Window

Default baseline:

```text
baseline_window = [event_start - 30 minutes, event_start)
```

Clean the baseline by excluding:

- Other meeting windows.
- Workouts.
- Travel blocks.
- Obvious movement periods when `stepCount`, `activeEnergyBurned`, or workout data supports that call.

Fallback baseline:

- Same-day non-meeting work-hour baseline.
- Use only when the default baseline lacks enough samples.
- Mark the meeting as fallback-baseline and reduce confidence.

If no credible baseline exists, exclude the meeting from rankings and list it under data gaps.

## Core Metrics

For each meeting:

```text
baseline_avg_hr = avg(heartRate samples in cleaned baseline_window)
baseline_std_hr = stddev(heartRate samples in cleaned baseline_window)
meeting_avg_hr = avg(heartRate samples in meeting_window)
meeting_max_hr = max(heartRate samples in meeting_window)
hr_delta = meeting_avg_hr - baseline_avg_hr
elevated_threshold = baseline_avg_hr + baseline_std_hr
elevated_share = count(meeting heartRate samples > elevated_threshold) / meeting sample_count
meeting_stress_load = max(hr_delta, 0)
duration_weighted_load = max(hr_delta, 0) * duration_minutes / 30
```

`meeting_stress_load` preserves source-method parity: a daily sum of positive meeting deltas. `duration_weighted_load` is an optional improvement for comparing short and long meetings, but should not replace the source-parity metric unless clearly labeled.

## Confidence Labels

Use confidence labels so sparse Apple Watch data does not look more precise than it is.

High confidence:

- Meeting and baseline both have adequate samples for their duration.
- No major event overlap.
- No workout or obvious movement confounder.
- Default pre-meeting baseline used.

Medium confidence:

- Sample count is usable but not dense.
- Minor gaps or mild movement confounders.
- Small overlap that does not materially affect the window.

Low confidence:

- Sparse samples.
- Fallback baseline.
- Overlapping real meetings.
- Likely workout, walking, travel, illness, or sensor confounder.

Do not hide low-confidence findings, but do not lead with them unless the user asks for raw exploration.

## Rollups

Daily:

- Sum `meeting_stress_load`.
- Also report number of included meetings and low-confidence meetings.
- Avoid universal thresholds. A value like 20 bpm-sessions may be a useful personal benchmark for one person, not a general rule.

Recurring meeting:

- Group by recurring event id when available.
- Otherwise group by normalized title only in private output.
- In shareable output, group by category or alias.

Attendee and organizer:

- Include only when attendee/organizer metadata is available and privacy-safe.
- For each person, report meeting count, average `hr_delta`, median `hr_delta`, range, high-confidence count, and caveats.
- Avoid ranking people as causes. Use "meetings involving Contact A were associated with..."

Time of day:

- Compare morning, midday, afternoon, and evening meetings.
- Use this to suggest calendar periodization: high-activation work, recovery meetings, moderate collaboration, and cool-down blocks.

## High-Variance And Simpson's-Paradox Checks

High variance is a finding.

Flag a collaborator, organizer, or recurring meeting when:

- It appears in at least three included meetings.
- Its `hr_delta` range is large enough to change the interpretation.
- It has both activating and calming examples.

Check for Simpson's paradox:

- Compare day-level load on days involving a person or recurring meeting against meeting-window deltas for that same person or meeting.
- If day-level and meeting-level patterns point in opposite directions, explain the split instead of forcing one answer.

## Recommendations

Recommendations should be practical calendar-design suggestions:

- Put activating meetings where the user has capacity.
- Separate high-load meetings with recovery blocks.
- Cluster calming or recovery meetings when useful.
- Avoid back-to-back high-activation meetings.
- Preserve high-variance meetings but add prep, notes, or recovery rather than labeling them bad.

Do not recommend medical interventions.

## Visualization Rules

Use visuals to make the analysis easier to inspect, not more dramatic than the data supports.

Quantitative visuals must be deterministic:

- Chart widgets.
- Plots generated from computed tables.
- Spreadsheet charts.
- SVG or PNG charts created from exact values.
- Mermaid diagrams for method flow, not numeric findings.

Do not use image generation for:

- Ranked bar charts.
- Numeric axes.
- Exact labels or values.
- Heart-rate traces.
- Heatmaps derived from private calendar or health data.

Image generation may be used only for optional non-quantitative visuals:

- A conceptual cover image for a sanitized report.
- A privacy-safe illustration of "calendar as training plan".
- A generic explainer graphic that contains no real names, dates, event titles, links, or measured values.

Every chart should include:

- Baseline method.
- Sample or minute grain.
- Confidence caveat when relevant.
- Sanitized labels when the report is shareable.

See `docs/VISUALIZATIONS.md` for recommended chart types.

## Report Requirements

Every full report must include:

- Date range.
- Timezone.
- Health-data coverage.
- Calendar-event coverage.
- Included and excluded meeting counts.
- Baseline method.
- Whether elevated share is sample-based or minute-based.
- Visualizations created and whether they are deterministic charts or conceptual generated images.
- Highest-confidence findings.
- Main caveats.
- Privacy status: private or sanitized/shareable.
