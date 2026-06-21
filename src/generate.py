"""RTS Adapt Engine v0.1 scaffold command.

This is intentionally scaffold-only. It validates the local file layout and prints
an operator-facing status message. Generation logic is introduced in later PRs.
"""

from __future__ import annotations

from pathlib import Path

INPUT_PATH = Path("inputs/daily_input.md")
OUTPUT_DIR = Path("outputs")
LOG_DIR = Path("logs")


def ensure_scaffold_paths() -> None:
    """Ensure local scaffold directories exist without external side effects."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    """Run the scaffold-only local command."""
    ensure_scaffold_paths()

    if not INPUT_PATH.is_file():
        print(f"missing_input={INPUT_PATH}")
        return 1

    print("RTS Adapt Engine v0.1 scaffold ready.")
    print(f"input_path={INPUT_PATH}")
    print(f"output_dir={OUTPUT_DIR}")
    print(f"log_dir={LOG_DIR}")
    print("generation_not_implemented=true")
    print("external_api_calls=false")
    print("publishing=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
