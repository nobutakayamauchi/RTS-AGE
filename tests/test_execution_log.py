"""Tests for RTS Adapt Engine local execution logging."""

from __future__ import annotations

import json
from pathlib import Path

from src.execution.log import append_execution_record, build_execution_record
from src.section_parser import parse_daily_input


SAMPLE_INPUT = """# 今日の現状
下書きとレビュー表が生成できる。

# 次にやること
実行記録を残す。

# 未定義セクション
追加メモ。
"""


def test_build_execution_record_is_json_serializable_and_safe():
    parsed = parse_daily_input(SAMPLE_INPUT)

    record = build_execution_record(
        input_path=Path("inputs/daily_input.md"),
        context_summary_path=Path("outputs/context_summary.md"),
        draft_paths=(
            Path("outputs/x_posts.md"),
            Path("outputs/note_draft.md"),
        ),
        review_checklist_path=Path("outputs/review_checklist.md"),
        parsed=parsed,
        created_at="2026-06-23T00:00:00Z",
    )

    assert record["schema_version"] == "rts-adapt-engine.execution-log.v0.1"
    assert record["created_at"] == "2026-06-23T00:00:00Z"
    assert record["status"] == "completed"
    assert record["input_path"] == "inputs/daily_input.md"
    assert "outputs/context_summary.md" in record["output_paths"]
    assert "outputs/review_checklist.md" in record["output_paths"]
    assert record["present_sections"] == 2
    assert record["unknown_sections"] == 1
    assert record["external_api_calls"] is False
    assert record["publishing"] is False
    assert record["sending"] is False
    assert record["credentials_required"] is False
    assert record["review_required"] is True

    json.dumps(record, ensure_ascii=False, sort_keys=True)


def test_append_execution_record_writes_one_jsonl_line(tmp_path):
    parsed = parse_daily_input(SAMPLE_INPUT)
    record = build_execution_record(
        input_path=Path("inputs/daily_input.md"),
        context_summary_path=Path("outputs/context_summary.md"),
        draft_paths=(Path("outputs/x_posts.md"),),
        review_checklist_path=Path("outputs/review_checklist.md"),
        parsed=parsed,
        created_at="2026-06-23T00:00:00Z",
    )
    log_path = tmp_path / "logs" / "execution_log.jsonl"

    written_path = append_execution_record(log_path, record)

    assert written_path == log_path
    lines = log_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    loaded = json.loads(lines[0])
    assert loaded["schema_version"] == "rts-adapt-engine.execution-log.v0.1"
    assert loaded["review_checklist_path"] == "outputs/review_checklist.md"
