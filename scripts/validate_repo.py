#!/usr/bin/env python3
"""Validate the public Meeting Health skill package."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "CONTRIBUTING.md",
    "AGENTS.md",
    "LICENSE",
    ".agents/skills/meeting-health/SKILL.md",
    "docs/METHODOLOGY.md",
    "docs/VISUALIZATIONS.md",
    "docs/REPORT_TEMPLATE.md",
    "fixtures/README.md",
    "fixtures/synthetic_calendar_events.csv",
    "fixtures/synthetic_heart_rate.csv",
]

README_KEYWORDS = [
    "Install",
    "Requirements",
    "Recommended First Run",
    "Privacy",
    "Interpretation Caveats",
    "Contributing",
    "License",
    "Apple Watch",
    "Meeting Stress Load",
    "deterministic charts",
]

SKILL_KEYWORDS = [
    "heartRate",
    "30 minutes",
    "baseline_avg_hr",
    "baseline_std_hr",
    "meeting_stress_load",
    "Simpson",
    "sanitized",
    "visualizations",
    "image generation",
]

METHODOLOGY_KEYWORDS = [
    "Source Method Parity",
    "Apple Health Adaptation",
    "Calendar Event Filtering",
    "Core Metrics",
    "Visualization Rules",
    "High-Variance",
    "Simpson",
]

SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\b[A-Za-z0-9._%+-]+@(?!example\.com\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    re.compile(r"https://(?:meet|teams|zoom|calendly|calendar|mail|drive)\.[^\s)]+", re.IGNORECASE),
]

TEXT_SUFFIXES = {".md", ".txt", ".py", ".sh", ".csv", ".gitignore"}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def tracked_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or path.is_dir():
            continue
        if path.suffix in TEXT_SUFFIXES or path.name == ".gitignore":
            files.append(path)
    return files


def check_required_files() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            fail(f"missing required file: {rel}")


def check_front_matter() -> None:
    text = read(".agents/skills/meeting-health/SKILL.md")
    if not text.startswith("---\n"):
        fail("skill is missing opening YAML front matter fence")
    end = text.find("\n---\n", 4)
    if end == -1:
        fail("skill is missing closing YAML front matter fence")
    front = text[4:end]
    fields = {}
    for line in front.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    for key in ("name", "description"):
        if not fields.get(key):
            fail(f"skill front matter missing {key}")
    if fields["name"] != "meeting-health":
        fail("skill name must be meeting-health")


def check_keywords() -> None:
    readme = read("README.md")
    skill = read(".agents/skills/meeting-health/SKILL.md")
    methodology = read("docs/METHODOLOGY.md")
    for keyword in README_KEYWORDS:
        if keyword not in readme:
            fail(f"README missing keyword/section: {keyword}")
    for keyword in SKILL_KEYWORDS:
        if keyword not in skill:
            fail(f"skill missing methodology keyword: {keyword}")
    for keyword in METHODOLOGY_KEYWORDS:
        if keyword not in methodology:
            fail(f"methodology missing keyword/section: {keyword}")


def check_fixtures() -> None:
    calendar_path = ROOT / "fixtures/synthetic_calendar_events.csv"
    hr_path = ROOT / "fixtures/synthetic_heart_rate.csv"

    with calendar_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 3:
        fail("calendar fixture should include at least three synthetic rows")
    required_calendar_fields = {"event_id", "title", "start", "end", "organizer", "category"}
    if not required_calendar_fields.issubset(rows[0]):
        fail("calendar fixture missing required columns")
    for row in rows:
        if "@" in ",".join(row.values()):
            fail("calendar fixture must not contain email addresses")

    with hr_path.open(newline="", encoding="utf-8") as handle:
        hr_rows = list(csv.DictReader(handle))
    if len(hr_rows) < 10:
        fail("heart-rate fixture should include enough synthetic samples")
    required_hr_fields = {"timestamp", "heart_rate", "source"}
    if not required_hr_fields.issubset(hr_rows[0]):
        fail("heart-rate fixture missing required columns")
    for row in hr_rows:
        try:
            value = int(row["heart_rate"])
        except ValueError as exc:
            fail(f"heart-rate fixture has non-integer value: {exc}")
        if value < 35 or value > 220:
            fail("heart-rate fixture value outside plausible synthetic range")


def check_privacy_hygiene() -> None:
    for path in tracked_text_files():
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            match = pattern.search(text)
            if match:
                fail(f"privacy/secret-like pattern in {rel}: {match.group(0)[:80]}")


def main() -> None:
    check_required_files()
    check_front_matter()
    check_keywords()
    check_fixtures()
    check_privacy_hygiene()
    print("meeting-health repo validation passed")


if __name__ == "__main__":
    main()
