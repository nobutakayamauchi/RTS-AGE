"""Tests for RTS Adapt Engine context normalization."""

from __future__ import annotations

from src.normalizer import build_context_summary
from src.section_parser import parse_daily_input


def test_build_context_summary_includes_core_sections():
    parsed = parse_daily_input(
        """# 今日の現状
車中で作業中。

# 詰まっていること
手順が崩れる。

# 次にやること
- normalizerを作る

# 言ってはいけないこと
秘密情報は出さない。
"""
    )

    summary = build_context_summary(parsed)

    assert "# Context Summary" in summary
    assert "## Current situation" in summary
    assert "車中で作業中。" in summary
    assert "## Blockers" in summary
    assert "手順が崩れる。" in summary
    assert "## Next actions" in summary
    assert "- normalizerを作る" in summary
    assert "## Do-not-say boundary" in summary
    assert "秘密情報は出さない。" in summary


def test_build_context_summary_reports_coverage_and_safety_boundary():
    parsed = parse_daily_input("# 今日の現状\n最小入力。\n")

    summary = build_context_summary(parsed)

    assert "- present_sections: 1" in summary
    assert "- missing_sections: 15" in summary
    assert "- unknown_sections: 0" in summary
    assert "- external_api_calls: false" in summary
    assert "- publishing: false" in summary
    assert "- review_required: true" in summary


def test_build_context_summary_preserves_unknown_sections_and_preamble():
    parsed = parse_daily_input(
        """前置きメモ

# 未定義セクション
ここは正式対応外。

# 今日の現状
通常セクション。
"""
    )

    summary = build_context_summary(parsed)

    assert "## Preamble" in summary
    assert "前置きメモ" in summary
    assert "## Unknown Sections" in summary
    assert "### 未定義セクション" in summary
    assert "ここは正式対応外。" in summary
