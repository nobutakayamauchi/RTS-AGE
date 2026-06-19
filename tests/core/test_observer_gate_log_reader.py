import json
from pathlib import Path

from core.observer_gate.log_reader import (
    format_observer_decision_log_entries,
    read_observer_decision_log,
)


def _write_jsonl(path: Path, records: list[dict]):
    path.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records),
        encoding="utf-8",
    )


def test_read_observer_decision_log_returns_empty_for_missing_file(tmp_path: Path):
    assert read_observer_decision_log(tmp_path / "missing.jsonl") == []


def test_read_observer_decision_log_returns_latest_entries(tmp_path: Path):
    log_path = tmp_path / "observer_decisions.jsonl"
    _write_jsonl(
        log_path,
        [
            {
                "timestamp": "2026-06-19T00:00:00+00:00",
                "task_id": "1",
                "task_type": "general",
                "selected_observer": "default",
                "score": 0,
                "should_use_fusion": False,
                "reasons": ["low risk"],
            },
            {
                "timestamp": "2026-06-19T00:01:00+00:00",
                "task_id": "2",
                "task_type": "security",
                "selected_observer": "fusion",
                "score": 7,
                "should_use_fusion": True,
                "reasons": ["security: +3", "high_failure_cost: +2"],
            },
        ],
    )

    entries = read_observer_decision_log(log_path, limit=1)

    assert len(entries) == 1
    assert entries[0].task_id == "2"
    assert entries[0].selected_observer == "fusion"
    assert entries[0].should_use_fusion is True


def test_read_observer_decision_log_skips_invalid_lines(tmp_path: Path):
    log_path = tmp_path / "observer_decisions.jsonl"
    log_path.write_text(
        "not-json\n"
        + json.dumps(
            {
                "timestamp": "2026-06-19T00:01:00+00:00",
                "task_id": "2",
                "task_type": "security",
                "selected_observer": "fusion",
                "score": 7,
                "should_use_fusion": True,
                "reasons": ["security: +3"],
                "text": "must not be surfaced",
            }
        ),
        encoding="utf-8",
    )

    entries = read_observer_decision_log(log_path)

    assert len(entries) == 1
    assert entries[0].task_id == "2"


def test_format_observer_decision_log_entries_hides_request_text(tmp_path: Path):
    log_path = tmp_path / "observer_decisions.jsonl"
    _write_jsonl(
        log_path,
        [
            {
                "timestamp": "2026-06-19T00:01:00+00:00",
                "task_id": "2",
                "task_type": "security",
                "selected_observer": "fusion",
                "score": 7,
                "should_use_fusion": True,
                "reasons": ["security: +3"],
                "text": "secret request body",
            }
        ],
    )

    report = format_observer_decision_log_entries(read_observer_decision_log(log_path))

    assert "task_id=2" in report
    assert "observer=fusion" in report
    assert "secret request body" not in report
    assert "text" not in report


def test_format_observer_decision_log_entries_handles_empty_entries():
    assert format_observer_decision_log_entries([]) == (
        "No observer decision log entries found."
    )
