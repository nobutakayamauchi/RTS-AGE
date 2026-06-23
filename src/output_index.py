"""Output manifest writer for generated RTS Adapt Engine artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp for output index records."""
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest for a local file."""
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_file_entry(path: Path) -> dict[str, Any]:
    """Build a JSON-serializable file entry for a generated file."""
    return {
        "path": str(path),
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
    }


def build_output_manifest(
    *,
    input_path: Path,
    generated_paths: tuple[Path, ...],
    execution_log_path: Path | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Build a manifest describing generated local output files."""
    record: dict[str, Any] = {
        "schema_version": "rts-adapt-engine.output-manifest.v0.1",
        "created_at": created_at or utc_timestamp(),
        "input_file": str(input_path),
        "generated_files": [build_file_entry(path) for path in generated_paths],
        "generated_file_count": len(generated_paths),
        "external_api_calls": False,
        "publishing": False,
        "sending": False,
        "credentials_required": False,
        "review_required": True,
    }
    if execution_log_path is not None:
        record["execution_log_file"] = str(execution_log_path)
    return record


def write_output_manifest(path: Path, record: dict[str, Any]) -> Path:
    """Write the output manifest as stable JSON and return its path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True)
    path.write_text(serialized.rstrip() + "\n", encoding="utf-8")
    return path
