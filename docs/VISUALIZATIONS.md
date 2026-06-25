# Visualizations

Visuals are useful for this workflow, but they need a clean boundary.

Use deterministic charts for measured data. Use generated images only for optional conceptual art or sanitized explainer images.

## Default Chart Set

For a full private report, prefer these charts when the data supports them:

1. Meeting heart-rate timeline
   - Shows raw or minute-bucketed `heartRate` samples for one selected meeting.
   - Includes meeting window, baseline average, and elevated threshold.
   - Best for explaining a single high-confidence finding.

2. Top activating and calming meetings
   - Bar chart of `hr_delta`.
   - Show confidence by color, marker, or adjacent label.
   - Use private titles only in private reports.

3. Daily Meeting Stress Load
   - Bar or line chart by day.
   - Include included-meeting count or low-confidence count when useful.
   - Do not imply a universal safe threshold.

4. Time-of-day pattern
   - Heatmap or grouped bar chart by morning, midday, afternoon, and evening.
   - Use average `hr_delta`, total load, and meeting count.

5. Collaborator or recurring-meeting variance
   - Dot plot with average `hr_delta` on one axis and `hr_delta` range on the other.
   - Size points by meeting count when possible.
   - Label shareable versions with aliases or categories only.

6. Data coverage
   - Sample count by day or by included/excluded window.
   - Use this when Apple Health density is uneven.

## Deterministic Chart Requirements

Quantitative charts must be produced from computed metric tables, not from prompts alone.

Acceptable methods include:

- A chart widget or report artifact when available.
- A local plotting library.
- A spreadsheet chart from sanitized aggregate tables.
- Hand-authored SVG from exact aggregate values.
- Mermaid only for workflows or method diagrams, not precise numeric charts.

Every quantitative chart should show or caption:

- Date range or sanitized range.
- Baseline method.
- Heart-rate grain: raw sample, sample bucket, or minute bucket.
- Whether elevated share is sample share or minute share.
- Confidence caveat when relevant.
- Sanitization status.

## Image Generation Rules

Generated images are allowed only for non-quantitative visuals.

Good uses:

- A sanitized cover image for a shareable report.
- A generic "calendar as training plan" illustration.
- A conceptual diagram of activation, recovery, and load, without measured values.

Do not use generated images for:

- Heart-rate line charts.
- Bar charts.
- Heatmaps.
- Axes, labels, values, or exact rankings.
- Any visual that appears to encode the user's private health or calendar data.

Generated image prompts must avoid:

- Real names.
- Company names.
- Meeting titles.
- Exact dates or times.
- Email addresses.
- Calendar links.
- Health values or exact chart labels.

## Private Versus Shareable Labels

Private charts may use real labels only when the user explicitly asked for a private report.

Shareable charts must replace:

- Person names with `Contact A`, `Contact B`, etc.
- Meeting titles with categories.
- Exact dates with relative labels such as `Day 1`.
- Locations and links with nothing.

## Recommended Shareable Visual Set

For a shareable report, prefer:

- Daily Meeting Stress Load by `Day 1`, `Day 2`, etc.
- Meeting category `hr_delta` chart.
- Time-of-day heatmap.
- Conceptual generated cover image, optional.
- Data-coverage note instead of raw sample chart when coverage itself could reveal private behavior.

