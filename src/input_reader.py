"""Input reader for RTS Adapt Engine v0.1.

The reader is intentionally small and local-only. It reads a Markdown input file
from disk and does not call external services.
"""

from __future__ import annotations

from pathlib import Path


class InputReadError(RuntimeError):
    """Raised when the local input file cannot be read."""


def read_daily_input(path: str | Path = "inputs/daily_input.md") -> str:
    """Read the daily input Markdown file as UTF-8 text."""
    input_path = Path(path)
    if not input_path.is_file():
        raise InputReadError(f"Daily input file not found: {input_path}")

    try:
        return input_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise InputReadError(f"Could not read daily input file: {input_path}") from exc
