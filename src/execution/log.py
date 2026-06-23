"""Append-only local execution log writer."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.section_parser import ParsedDailyInput


def utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp for execution records."""
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _path_strings(paths: tuple[Path, ...]) -> list[str]:
    return [str(path) for path in paths]


def build_execution_record(
    *,
    input_path: Path,
    context_summary_path: Path,
    draft_paths: tuple[Path, ...],
    review_checklist_path: Path,
    parsed: ParsedDailyInput,
    created_at: str | None = None,
    status: str = "completed",
) -> dict[str, Any]:
    """Build a JSON-serializable local execution record."""
    output_paths = (context_summary_path, *draft_paths, review_checklist_path)

    return {
        "schema_version": "rts-adapt-engine.execution-log.v0.1",
        "created_at": created_at or utc_timestamp(),
        "status": status,
        "input_path": str(input_path),
        "output_paths": _path_strings(output_paths),
        "context_summary_path": str(context_summary_path),
        "draft_output_paths": _path_strings(draft_paths),
        "review_checklist_path": str(review_checklist_path),
        "present_sections": len(parsed.present_sections),
        "missing_sections": len(parsed.missing_sections),
        "unknown_sections": len(parsed.unknown_sections),
        "external_api_calls": False,
        "publishing": False,
        "sending": False,
        "credentials_required": False,
        "review_required": True,
    }


def append_execution_record(log_path: Path, record: dict[str, Any]) -> Path:
    """Append one execution record as JSONL and return the log path."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(record, ensure_ascii=False, sort_keys=True)
    with log_path.open("a", encoding="utf-8") as file_handle:
        file_handle.write(serialized + "\n")
    return log_path
