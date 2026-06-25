# Contributing

Thanks for helping improve Meeting Health.

This is an open-source Codex skill package for personal calendar reflection with Apple Health and Apple Watch data. The project is MIT licensed, and forks, issues, and pull requests are welcome.

## Good Contributions

Useful improvements include:

- Better Apple Health sample-density checks.
- More precise calendar-event filtering.
- Deterministic chart examples built from computed metrics.
- Synthetic fixtures for sparse data, overlaps, missing baselines, and movement confounders.
- Clearer privacy-safe report templates.
- Better documentation for installing and running the skill.

## Privacy Rules

Do not contribute real private data.

Do not add:

- Apple Health exports.
- Calendar exports.
- Meeting titles from real calendars.
- Names, email addresses, locations, meeting links, or screenshots.
- Connector payloads.
- Reports based on identifiable people.

Use synthetic examples only.

## Interpretation Rules

Keep claims careful.

This project is for personal reflection and calendar design. It is not:

- Medical advice.
- A diagnostic tool.
- A mental-health assessment.
- An employee-evaluation product.
- Proof that another person caused a physiological response.

Prefer language like "associated with", "appears activating", and "appears calming".

## Validation

Before opening a pull request, run:

```bash
scripts/check.sh
```

The validator checks the public package contract, YAML front matter, required docs, synthetic fixtures, and basic privacy hygiene.

## License

By contributing, you agree that your contribution will be licensed under the MIT License.
