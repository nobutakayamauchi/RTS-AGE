"""RTS Adapt Engine v0.1 scaffold command.

This command validates the local file layout, reads the daily input, and parses
supported Markdown sections. Draft generation is introduced in later PRs.
"""

from __future__ import annotations

from pathlib import Path

from src.input_reader import InputReadError, read_daily_input
from src.section_parser import parse_daily_input

INPUT_PATH = Path("inputs/daily_input.md")
OUTPUT_DIR = Path("outputs")
LOG_DIR = Path("logs")


def ensure_scaffold_paths() -> None:
    """Ensure local scaffold directories exist without external side effects."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    """Run the local input-reader and section-parser scaffold command."""
    ensure_scaffold_paths()

    try:
        daily_input = read_daily_input(INPUT_PATH)
    except InputReadError as exc:
        print(f"input_error={exc}")
        return 1

    parsed = parse_daily_input(daily_input)

    print("RTS Adapt Engine v0.1 input parser ready.")
    print(f"input_path={INPUT_PATH}")
    print(f"output_dir={OUTPUT_DIR}")
    print(f"log_dir={LOG_DIR}")
    print(f"present_sections={len(parsed.present_sections)}")
    print(f"missing_sections={len(parsed.missing_sections)}")
    print(f"unknown_sections={len(parsed.unknown_sections)}")
    print("generation_not_implemented=true")
    print("external_api_calls=false")
    print("publishing=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
