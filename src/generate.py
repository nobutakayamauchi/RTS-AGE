"""RTS Adapt Engine v0.1 local generation command.

This command validates the local file layout, reads the daily input, parses
supported Markdown sections, writes a context summary, writes deterministic
reviewable draft outputs, and writes a human review checklist. It does not call
external APIs or publish content.
"""

from __future__ import annotations

from pathlib import Path

from src.generators.line_message import build_line_message
from src.generators.note_draft import build_note_draft
from src.generators.video_script import build_video_script
from src.generators.x_posts import build_x_posts
from src.input_reader import InputReadError, read_daily_input
from src.normalizer import build_context_summary
from src.review.checklist import build_review_checklist
from src.section_parser import ParsedDailyInput, parse_daily_input

INPUT_PATH = Path("inputs/daily_input.md")
OUTPUT_DIR = Path("outputs")
LOG_DIR = Path("logs")
CONTEXT_SUMMARY_PATH = OUTPUT_DIR / "context_summary.md"
X_POSTS_PATH = OUTPUT_DIR / "x_posts.md"
NOTE_DRAFT_PATH = OUTPUT_DIR / "note_draft.md"
LINE_MESSAGE_PATH = OUTPUT_DIR / "line_message.md"
VIDEO_SCRIPT_PATH = OUTPUT_DIR / "video_script.md"
REVIEW_CHECKLIST_PATH = OUTPUT_DIR / "review_checklist.md"


DRAFT_OUTPUTS: tuple[tuple[Path, str], ...] = (
    (X_POSTS_PATH, "x_posts"),
    (NOTE_DRAFT_PATH, "note_draft"),
    (LINE_MESSAGE_PATH, "line_message"),
    (VIDEO_SCRIPT_PATH, "video_script"),
)


def ensure_scaffold_paths() -> None:
    """Ensure local scaffold directories exist without external side effects."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def write_markdown(path: Path, content: str) -> None:
    """Write Markdown content locally."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_context_summary(summary: str) -> None:
    """Write the normalized context summary locally."""
    write_markdown(CONTEXT_SUMMARY_PATH, summary)


def build_draft_outputs(parsed: ParsedDailyInput) -> dict[Path, str]:
    """Build deterministic draft outputs for supported platforms."""
    return {
        X_POSTS_PATH: build_x_posts(parsed),
        NOTE_DRAFT_PATH: build_note_draft(parsed),
        LINE_MESSAGE_PATH: build_line_message(parsed),
        VIDEO_SCRIPT_PATH: build_video_script(parsed),
    }


def write_draft_outputs(parsed: ParsedDailyInput) -> tuple[Path, ...]:
    """Write deterministic draft outputs and return written paths."""
    draft_outputs = build_draft_outputs(parsed)
    written_paths: list[Path] = []

    for path, content in draft_outputs.items():
        write_markdown(path, content)
        written_paths.append(path)

    return tuple(written_paths)


def write_review_checklist(
    parsed: ParsedDailyInput,
    draft_paths: tuple[Path, ...],
) -> Path:
    """Write a human review checklist for generated draft outputs."""
    checklist = build_review_checklist(parsed, draft_paths)
    write_markdown(REVIEW_CHECKLIST_PATH, checklist)
    return REVIEW_CHECKLIST_PATH


def main() -> int:
    """Run the local parser, context normalizer, draft generators, and checklist."""
    ensure_scaffold_paths()

    try:
        daily_input = read_daily_input(INPUT_PATH)
    except InputReadError as exc:
        print(f"input_error={exc}")
        return 1

    parsed = parse_daily_input(daily_input)
    context_summary = build_context_summary(parsed)
    write_context_summary(context_summary)
    written_draft_paths = write_draft_outputs(parsed)
    review_checklist_path = write_review_checklist(parsed, written_draft_paths)

    print("RTS Adapt Engine v0.1 draft generators ready.")
    print(f"input_path={INPUT_PATH}")
    print(f"context_summary_path={CONTEXT_SUMMARY_PATH}")
    for path in written_draft_paths:
        print(f"draft_output_path={path}")
    print(f"review_checklist_path={review_checklist_path}")
    print(f"output_dir={OUTPUT_DIR}")
    print(f"log_dir={LOG_DIR}")
    print(f"present_sections={len(parsed.present_sections)}")
    print(f"missing_sections={len(parsed.missing_sections)}")
    print(f"unknown_sections={len(parsed.unknown_sections)}")
    print("draft_generation_implemented=true")
    print("review_checklist_implemented=true")
    print("external_api_calls=false")
    print("publishing=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
