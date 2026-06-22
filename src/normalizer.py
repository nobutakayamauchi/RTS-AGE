"""Context normalizer for RTS Adapt Engine v0.1.

The normalizer converts parsed daily input into a deterministic Markdown context
summary. It does not generate platform drafts and does not call external APIs.
"""

from __future__ import annotations

from src.section_parser import ParsedDailyInput

EMPTY_VALUE = "_未入力_"

SECTION_LABELS: tuple[tuple[str, str], ...] = (
    ("今日の現状", "Current situation"),
    ("今日やったこと", "Completed work"),
    ("詰まっていること", "Blockers"),
    ("次にやること", "Next actions"),
    ("使いたいネタ", "Source material"),
    ("参考URL", "Reference URLs"),
    ("言いたいこと", "Core message"),
    ("言ってはいけないこと", "Do-not-say boundary"),
    ("出力したい媒体", "Requested outputs"),
    ("今日の温度感", "Tone"),
    ("売りたい商品・サービス", "Offer"),
    ("誘導したい行動", "Call to action"),
    ("LINE公式でやりたいこと", "LINE intent"),
    ("無料配布物", "Free resource"),
    ("相談導線", "Consultation path"),
    ("注意事項", "Cautions"),
)


def _value(parsed: ParsedDailyInput, section_name: str) -> str:
    value = parsed.sections.get(section_name, "").strip()
    return value or EMPTY_VALUE


def _format_block(title: str, body: str) -> str:
    return f"## {title}\n\n{body.strip() or EMPTY_VALUE}\n"


def build_context_summary(parsed: ParsedDailyInput) -> str:
    """Build a deterministic context summary Markdown document."""
    blocks = ["# Context Summary", ""]

    blocks.append(
        _format_block(
            "Input Coverage",
            "\n".join(
                [
                    f"- present_sections: {len(parsed.present_sections)}",
                    f"- missing_sections: {len(parsed.missing_sections)}",
                    f"- unknown_sections: {len(parsed.unknown_sections)}",
                ]
            ),
        )
    )

    for section_name, label in SECTION_LABELS:
        blocks.append(_format_block(label, _value(parsed, section_name)))

    if parsed.preamble:
        blocks.append(_format_block("Preamble", parsed.preamble))

    if parsed.unknown_sections:
        unknown_lines: list[str] = []
        for name, body in parsed.unknown_sections.items():
            unknown_lines.append(f"### {name}")
            unknown_lines.append("")
            unknown_lines.append(body or EMPTY_VALUE)
            unknown_lines.append("")
        blocks.append(_format_block("Unknown Sections", "\n".join(unknown_lines)))

    blocks.append(
        _format_block(
            "Safety Boundary",
            "\n".join(
                [
                    "- draft_generation: not_implemented",
                    "- external_api_calls: false",
                    "- publishing: false",
                    "- credentials_required: false",
                    "- review_required: true",
                ]
            ),
        )
    )

    return "\n".join(block.rstrip() for block in blocks).rstrip() + "\n"
