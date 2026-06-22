"""Markdown section parser for RTS Adapt Engine v0.1."""

from __future__ import annotations

from dataclasses import dataclass

SUPPORTED_SECTIONS: tuple[str, ...] = (
    "今日の現状",
    "今日やったこと",
    "詰まっていること",
    "次にやること",
    "使いたいネタ",
    "参考URL",
    "言いたいこと",
    "言ってはいけないこと",
    "出力したい媒体",
    "今日の温度感",
    "売りたい商品・サービス",
    "誘導したい行動",
    "LINE公式でやりたいこと",
    "無料配布物",
    "相談導線",
    "注意事項",
)


@dataclass(frozen=True)
class ParsedDailyInput:
    """Parsed Markdown sections from the daily input file."""

    sections: dict[str, str]
    unknown_sections: dict[str, str]
    preamble: str = ""

    @property
    def present_sections(self) -> tuple[str, ...]:
        """Return supported sections that were present in the input."""
        return tuple(name for name in SUPPORTED_SECTIONS if name in self.sections)

    @property
    def missing_sections(self) -> tuple[str, ...]:
        """Return supported sections that were not present in the input."""
        return tuple(name for name in SUPPORTED_SECTIONS if name not in self.sections)


def _normalize_heading(line: str) -> str | None:
    stripped = line.strip()
    if not stripped.startswith("#"):
        return None

    heading = stripped.lstrip("#").strip()
    return heading or None


def parse_daily_input(markdown_text: str) -> ParsedDailyInput:
    """Parse top-level Markdown headings into supported and unknown sections.

    Missing sections are tolerated. Unknown sections are preserved separately so
    later PRs can decide how to use or report them.
    """
    supported_set = set(SUPPORTED_SECTIONS)
    sections: dict[str, list[str]] = {}
    unknown_sections: dict[str, list[str]] = {}
    preamble_lines: list[str] = []
    current_heading: str | None = None

    for line in markdown_text.splitlines():
        heading = _normalize_heading(line)
        if heading is not None:
            current_heading = heading
            target = sections if heading in supported_set else unknown_sections
            target.setdefault(heading, [])
            continue

        if current_heading is None:
            preamble_lines.append(line)
            continue

        target = sections if current_heading in supported_set else unknown_sections
        target.setdefault(current_heading, []).append(line)

    return ParsedDailyInput(
        sections={key: "\n".join(value).strip() for key, value in sections.items()},
        unknown_sections={
            key: "\n".join(value).strip() for key, value in unknown_sections.items()
        },
        preamble="\n".join(preamble_lines).strip(),
    )
