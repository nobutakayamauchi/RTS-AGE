"""Deterministic review checklist generator."""

from __future__ import annotations

from pathlib import Path

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


def _format_paths(paths: tuple[Path, ...] | None) -> str:
    if not paths:
        return "- 未指定"
    return "\n".join(f"- {path}" for path in paths)


def build_review_checklist(
    parsed: ParsedDailyInput,
    draft_paths: tuple[Path, ...] | None = None,
) -> str:
    """Build a human review checklist for generated draft outputs."""
    do_not_say = _compact(_section(parsed, "言ってはいけないこと"))
    cautions = _compact(_section(parsed, "注意事項"))
    requested_outputs = _compact(_section(parsed, "出力したい媒体"))
    tone = _compact(_section(parsed, "今日の温度感"))
    offer = _compact(_section(parsed, "売りたい商品・サービス"))
    cta = _compact(_section(parsed, "誘導したい行動"))

    return f"""# Review Checklist

## Review status

- review_required: true
- approval_required: true
- publishing: false
- sending: false
- external_api_calls: false
- credentials_required: false

## Draft outputs to review

{_format_paths(draft_paths)}

## Required checks

- [ ] Confirm drafts match requested outputs: {requested_outputs}
- [ ] Confirm tone matches: {tone}
- [ ] Confirm offer is represented accurately: {offer}
- [ ] Confirm CTA is clear and not pushy: {cta}
- [ ] Confirm do-not-say boundary is not present in public drafts: {do_not_say}
- [ ] Confirm cautions are respected: {cautions}
- [ ] Confirm no private credentials, API keys, or connector secrets are included.
- [ ] Confirm no auto-publish or auto-send behavior was triggered.

## Unknown section review

- unknown_sections: {len(parsed.unknown_sections)}

## Decision

- [ ] approve_for_manual_use
- [ ] revise_before_use
- [ ] reject_output

## Note

This checklist is itself a review artifact. It is not a public draft.
"""
