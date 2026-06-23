"""Tests for RTS Adapt Engine draft output generators."""

from __future__ import annotations

from src.generators.line_message import build_line_message
from src.generators.note_draft import build_note_draft
from src.generators.video_script import build_video_script
from src.generators.x_posts import build_x_posts
from src.section_parser import parse_daily_input


SAMPLE_INPUT = """# 今日の現状
車中で開発を続けている。

# 今日やったこと
AGEの境界整理を終えた。

# 詰まっていること
手順が崩れるとミスが連鎖する。

# 次にやること
下書き生成を実装する。

# 使いたいネタ
人間が確認できる形で出す。

# 言いたいこと
AIは作業を消すのではなく、確認可能な形に分解する道具だ。

# 言ってはいけないこと
秘密の合言葉

# 出力したい媒体
X, note, LINE, video

# 今日の温度感
落ち着いて、でも前に進める。

# 売りたい商品・サービス
Breakpoint Consulting

# 誘導したい行動
相談導線を見る。

# LINE公式でやりたいこと
短い案内と無料配布への誘導。

# 無料配布物
簡易チェックリスト

# 相談導線
プロフィールのリンク

# 注意事項
断定しすぎない。
"""


def _parsed():
    return parse_daily_input(SAMPLE_INPUT)


def test_build_x_posts_returns_three_reviewable_drafts():
    output = build_x_posts(_parsed())

    assert "# X Post Drafts" in output
    assert output.count("## Draft") == 3
    assert "review" in output.lower() or "要確認" in output
    assert "秘密の合言葉" not in output


def test_build_note_draft_contains_article_parts_and_cta():
    output = build_note_draft(_parsed())

    assert "# Note Draft" in output
    assert "## Title" in output
    assert "## Body" in output
    assert "## CTA" in output
    assert "相談導線を見る。" in output
    assert "Human review is required" in output
    assert "秘密の合言葉" not in output


def test_build_line_message_is_reviewable_and_not_sent():
    output = build_line_message(_parsed())

    assert "# LINE Message Draft" in output
    assert "review_required: true" in output
    assert "sending: false" in output
    assert "external_api_calls: false" in output
    assert "簡易チェックリスト" in output
    assert "秘密の合言葉" not in output


def test_build_video_script_contains_hook_main_points_and_closing():
    output = build_video_script(_parsed())

    assert "# Video Script Draft" in output
    assert "## Hook" in output
    assert "## Main Points" in output
    assert "## Closing" in output
    assert "## CTA" in output
    assert "Human review is required" in output
    assert "秘密の合言葉" not in output
