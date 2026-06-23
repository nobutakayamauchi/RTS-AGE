"""Deterministic LINE message draft generator."""

from __future__ import annotations

from src.section_parser import ParsedDailyInput

EMPTY_VALUE = "未入力"


def _section(parsed: ParsedDailyInput, name: str) -> str:
    return parsed.sections.get(name, "").strip() or EMPTY_VALUE


def _compact(value: str, limit: int = 80) -> str:
    normalized = " ".join(part.strip() for part in value.splitlines() if part.strip())
    if not normalized:
        return EMPTY_VALUE
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "…"


def build_line_message(parsed: ParsedDailyInput) -> str:
    """Build a short reviewable LINE message draft."""
    situation = _compact(_section(parsed, "今日の現状"), 70)
    line_intent = _compact(_section(parsed, "LINE公式でやりたいこと"), 70)
    free_resource = _compact(_section(parsed, "無料配布物"), 70)
    consultation_path = _compact(_section(parsed, "相談導線"), 70)
    cta = _compact(_section(parsed, "誘導したい行動"), 70)

    return f"""# LINE Message Draft

## Message

こんにちは。\n{situation}\n\n{line_intent}\n\n無料配布: {free_resource}\n相談導線: {consultation_path}\n\n次の行動: {cta}\n\n※この文面は下書きです。送信前に必ず人間が確認してください。

## Status

review_required: true
sending: false
external_api_calls: false
"""
