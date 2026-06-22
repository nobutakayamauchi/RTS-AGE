"""Tests for RTS Adapt Engine daily input parsing."""

from __future__ import annotations

from src.section_parser import SUPPORTED_SECTIONS, parse_daily_input


def test_parse_daily_input_extracts_supported_sections():
    markdown = """# 今日の現状
車中で作業中。

# 次にやること
- parserを作る

# 言ってはいけないこと
秘密情報は出さない。
"""

    parsed = parse_daily_input(markdown)

    assert parsed.sections["今日の現状"] == "車中で作業中。"
    assert parsed.sections["次にやること"] == "- parserを作る"
    assert parsed.sections["言ってはいけないこと"] == "秘密情報は出さない。"
    assert "今日やったこと" in parsed.missing_sections
    assert "今日の現状" in parsed.present_sections


def test_parse_daily_input_tolerates_missing_sections():
    parsed = parse_daily_input("# 今日の現状\n最小入力。\n")

    assert parsed.sections == {"今日の現状": "最小入力。"}
    assert len(parsed.missing_sections) == len(SUPPORTED_SECTIONS) - 1


def test_parse_daily_input_preserves_unknown_sections_and_preamble():
    markdown = """前置きメモ

# 未定義セクション
ここはまだ正式対応外。

# 今日の現状
通常セクション。
"""

    parsed = parse_daily_input(markdown)

    assert parsed.preamble == "前置きメモ"
    assert parsed.unknown_sections == {"未定義セクション": "ここはまだ正式対応外。"}
    assert parsed.sections["今日の現状"] == "通常セクション。"
