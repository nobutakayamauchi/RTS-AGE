"""Read observer decision JSONL logs without exposing request text."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ObserverDecisionLogEntry:
    timestamp: str
    task_id: str
    task_type: str
    selected_observer: str
    score: int
    should_use_fusion: bool
    reasons: list[str]


def read_observer_decision_log(
    path: str | Path,
    limit: int = 20,
) -> list[ObserverDecisionLogEntry]:
    """Read the latest observer decision log entries.

    Invalid lines are skipped so a partially written JSONL file does not break
    inspection. Request text and metadata are intentionally ignored even if a
    future writer accidentally includes them.
    """
    if limit <= 0:
        return []

    log_path = Path(path)
    if not log_path.exists():
        return []

    entries: list[ObserverDecisionLogEntry] = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        entry = _entry_from_json_line(line)
        if entry is not None:
            entries.append(entry)

    return entries[-limit:]


def format_observer_decision_log_entries(
    entries: list[ObserverDecisionLogEntry],
) -> str:
    """Format observer decisions as a compact human-readable report."""
    if not entries:
        return "No observer decision log entries found."

    lines: list[str] = []
    for entry in entries:
        reasons = ", ".join(entry.reasons) if entry.reasons else "none"
        lines.append(
            " | ".join(
                [
                    entry.timestamp,
                    f"task_id={entry.task_id}",
                    f"type={entry.task_type}",
                    f"observer={entry.selected_observer}",
                    f"score={entry.score}",
                    f"fusion={entry.should_use_fusion}",
                    f"reasons={reasons}",
                ]
            )
        )
    return "\n".join(lines)


def _entry_from_json_line(line: str) -> ObserverDecisionLogEntry | None:
    try:
        raw = json.loads(line)
    except json.JSONDecodeError:
        return None

    if not isinstance(raw, dict):
        return None

    try:
        return ObserverDecisionLogEntry(
            timestamp=_string_field(raw, "timestamp"),
            task_id=_string_field(raw, "task_id"),
            task_type=_string_field(raw, "task_type"),
            selected_observer=_string_field(raw, "selected_observer"),
            score=int(raw["score"]),
            should_use_fusion=bool(raw["should_use_fusion"]),
            reasons=_string_list_field(raw, "reasons"),
        )
    except KeyError, TypeError, ValueError:
        return None


def _string_field(raw: dict[str, Any], key: str) -> str:
    value = raw[key]
    if not isinstance(value, str):
        raise TypeError(f"expected string field: {key}")
    return value


def _string_list_field(raw: dict[str, Any], key: str) -> list[str]:
    value = raw[key]
    if not isinstance(value, list):
        raise TypeError(f"expected list field: {key}")
    return [str(item) for item in value]
