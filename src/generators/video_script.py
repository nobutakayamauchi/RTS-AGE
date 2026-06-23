"""Deterministic video script draft generator."""

from __future__ import annotations

from src.section_parser import ParsedDailyInput

EMPTY_VALUE = "未入力"


def _section(parsed: ParsedDailyInput, name: str) -> str:
    return parsed.sections.get(name, "").strip() or EMPTY_VALUE


def _compact(value: str, limit: int = 120) -> str:
    normalized = " ".join(part.strip() for part in value.splitlines() if part.strip())
    if not normalized:
        return EMPTY_VALUE
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "…"


def build_video_script(parsed: ParsedDailyInput) -> str:
    """Build a short reviewable video script draft."""
    situation = _compact(_section(parsed, "今日の現状"))
    blocker = _compact(_section(parsed, "詰まっていること"))
    material = _compact(_section(parsed, "使いたいネタ"))
    core_message = _compact(_section(parsed, "言いたいこと"))
    next_action = _compact(_section(parsed, "次にやること"))
    cta = _compact(_section(parsed, "誘導したい行動"))

    return f"""# Video Script Draft

## Hook

今の状況を一言で言うと、{situation}

## Main Points

1. 今日の詰まり: {blocker}
2. 使えるネタ: {material}
3. 伝えたいこと: {core_message}

## Closing

次は、{next_action}

## CTA

{cta}

## Review status

This is a draft script. Human review is required before recording, publishing, or sending.
"""
