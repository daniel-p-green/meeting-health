# Report Template

Use this shape for full private reports. For shareable reports, remove names, titles, exact dates, links, locations, descriptions, and raw event logs.

```md
# Meeting Health Report

## Executive Summary

- Date range:
- Timezone:
- Report status: Private
- Best-supported finding:
- Main caveat:

## Data Coverage

| Source | Coverage | Notes |
| --- | ---: | --- |
| Apple Health `heartRate` |  |  |
| Calendar events fetched |  |  |
| Meetings included |  |  |
| Meetings excluded |  |  |

## Method

- Baseline:
- Heart-rate grain:
- Elevated-share definition:
- Movement/workout handling:
- Overlap handling:
- Confidence labels:

## Top Activating Meetings

| Rank | Meeting | Avg HR delta | Elevated share | Samples | Confidence | Notes |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 |  |  |  |  |  |  |

## Calming Meetings

| Rank | Meeting | Avg HR delta | Elevated share | Samples | Confidence | Notes |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 |  |  |  |  |  |  |

## Daily Meeting Stress Load

| Day | Included meetings | Meeting Stress Load | Duration-weighted load | Confidence notes |
| --- | ---: | ---: | ---: | --- |
|  |  |  |  |  |

## Visualizations

| Visual | Type | Data source | Privacy status | Notes |
| --- | --- | --- | --- | --- |
| Daily Meeting Stress Load | Deterministic chart | Aggregated day-level metrics | Private or sanitized |  |
| Top activating meetings | Deterministic chart | Meeting-level metrics | Private or sanitized |  |
| Conceptual cover image | Generated image, optional | No measured data | Sanitized only | Must not contain names, dates, or values |

## Collaborator And Recurring Meeting Patterns

| Pattern | Meetings | Avg HR delta | Range | Confidence | Interpretation |
| --- | ---: | ---: | ---: | --- | --- |
|  |  |  |  |  |  |

## Time-of-Day Patterns

| Time block | Meetings | Avg HR delta | Meeting Stress Load | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Morning |  |  |  |  |
| Midday |  |  |  |  |
| Afternoon |  |  |  |  |
| Evening |  |  |  |  |

## High-Variance Findings

List recurring meetings, attendees, or organizers where the range matters more than the average.

## Calendar Recommendations

1. 
2. 
3. 

## Caveats

- Heart rate is not a direct stress label.
- Results can be affected by sleep, caffeine, illness, medication, workouts, walking, speaking, excitement, temperature, and sensor gaps.
- Attendee and organizer patterns are associations, not causes.

## Appendix: Included And Excluded Data

Summarize counts and exclusion reasons. Do not paste raw private event logs into shareable reports.
```
