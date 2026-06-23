"""Deterministic note draft generator."""

from __future__ import annotations

from src.section_parser import ParsedDailyInput

EMPTY_VALUE = "未入力"


def _section(parsed: ParsedDailyInput, name: str) -> str:
    return parsed.sections.get(name, "").strip() or EMPTY_VALUE


def _compact(value: str, limit: int = 140) -> str:
    normalized = " ".join(part.strip() for part in value.splitlines() if part.strip())
    if not normalized:
        return EMPTY_VALUE
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "…"


def build_note_draft(parsed: ParsedDailyInput) -> str:
    """Build a reviewable note article draft."""
    situation = _section(parsed, "今日の現状")
    completed = _section(parsed, "今日やったこと")
    blockers = _section(parsed, "詰まっていること")
    next_actions = _section(parsed, "次にやること")
    source_material = _section(parsed, "使いたいネタ")
    core_message = _section(parsed, "言いたいこと")
    offer = _section(parsed, "売りたい商品・サービス")
    cta = _section(parsed, "誘導したい行動")
    cautions = _section(parsed, "注意事項")

    title_seed = _compact(core_message if core_message != EMPTY_VALUE else situation, 48)

    return f"""# Note Draft

## Title

{title_seed}

## Lead

{_compact(situation)}

## Body

### What changed today

{completed}

### Current blocker

{blockers}

### Source material

{source_material}

### Main message

{core_message}

### Next step

{next_actions}

## Offer

{offer}

## CTA

{cta}

## Review cautions

{cautions}

## Publishing status

This is a draft. Human review is required before publishing.
"""
