"""Tests for RTS Adapt Engine review checklist generation."""

from __future__ import annotations

from pathlib import Path

from src.review.checklist import build_review_checklist
from src.section_parser import parse_daily_input


SAMPLE_INPUT = """# 今日の現状
下書き生成まで進んだ。

# 言ってはいけないこと
利用者の個人情報は書かない。

# 出力したい媒体
X, note, LINE, video

# 今日の温度感
落ち着いて確認する。

# 売りたい商品・サービス
Breakpoint Consulting

# 誘導したい行動
相談導線を見る。

# 注意事項
断定しすぎない。送信前に確認する。

# 未定義セクション
追加の観察メモ。
"""


def test_build_review_checklist_includes_required_safety_flags():
    parsed = parse_daily_input(SAMPLE_INPUT)

    checklist = build_review_checklist(parsed)

    assert "# Review Checklist" in checklist
    assert "review_required: true" in checklist
    assert "approval_required: true" in checklist
    assert "publishing: false" in checklist
    assert "sending: false" in checklist
    assert "external_api_calls: false" in checklist
    assert "credentials_required: false" in checklist


def test_build_review_checklist_references_draft_paths_and_boundaries():
    parsed = parse_daily_input(SAMPLE_INPUT)
    draft_paths = (
        Path("outputs/x_posts.md"),
        Path("outputs/note_draft.md"),
        Path("outputs/line_message.md"),
        Path("outputs/video_script.md"),
    )

    checklist = build_review_checklist(parsed, draft_paths)

    assert "- outputs/x_posts.md" in checklist
    assert "- outputs/note_draft.md" in checklist
    assert "- outputs/line_message.md" in checklist
    assert "- outputs/video_script.md" in checklist
    assert "利用者の個人情報は書かない。" in checklist
    assert "断定しすぎない。送信前に確認する。" in checklist
    assert "unknown_sections: 1" in checklist


def test_build_review_checklist_keeps_decision_as_manual_gate():
    parsed = parse_daily_input(SAMPLE_INPUT)

    checklist = build_review_checklist(parsed)

    assert "approve_for_manual_use" in checklist
    assert "revise_before_use" in checklist
    assert "reject_output" in checklist
    assert "This checklist is itself a review artifact." in checklist
