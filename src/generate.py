"""RTS Adapt Engine v0.1 local generation command.

This command validates the local file layout, reads the daily input, parses
supported Markdown sections, and writes a context summary. Platform draft
generation is introduced in later PRs.
"""

from __future__ import annotations

from pathlib import Path

from src.input_reader import InputReadError, read_daily_input
from src.normalizer import build_context_summary
from src.section_parser import parse_daily_input

INPUT_PATH = Path("inputs/daily_input.md")
OUTPUT_DIR = Path("outputs")
LOG_DIR = Path("logs")
CONTEXT_SUMMARY_PATH = OUTPUT_DIR / "context_summary.md"


def ensure_scaffold_paths() -> None:
    """Ensure local scaffold directories exist without external side effects."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def write_context_summary(summary: str) -> None:
    """Write the normalized context summary locally."""
    CONTEXT_SUMMARY_PATH.write_text(summary, encoding="utf-8")


def main() -> int:
    """Run the local parser and context normalizer command."""
    ensure_scaffold_paths()

    try:
        daily_input = read_daily_input(INPUT_PATH)
    except InputReadError as exc:
        print(f"input_error={exc}")
        return 1

    parsed = parse_daily_input(daily_input)
    context_summary = build_context_summary(parsed)
    write_context_summary(context_summary)

    print("RTS Adapt Engine v0.1 context normalizer ready.")
    print(f"input_path={INPUT_PATH}")
    print(f"context_summary_path={CONTEXT_SUMMARY_PATH}")
    print(f"output_dir={OUTPUT_DIR}")
    print(f"log_dir={LOG_DIR}")
    print(f"present_sections={len(parsed.present_sections)}")
    print(f"missing_sections={len(parsed.missing_sections)}")
    print(f"unknown_sections={len(parsed.unknown_sections)}")
    print("draft_generation_not_implemented=true")
    print("external_api_calls=false")
    print("publishing=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
