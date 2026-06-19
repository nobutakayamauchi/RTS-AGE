import json
import sys
from pathlib import Path

from cli.entrypoints import observer_log


def _write_jsonl(path: Path, records: list[dict]):
    path.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records),
        encoding="utf-8",
    )


def test_observer_log_prints_recent_entries(
    monkeypatch,
    tmp_path: Path,
    capsys,
):
    log_path = tmp_path / "observer_decisions.jsonl"
    _write_jsonl(
        log_path,
        [
            {
                "timestamp": "2026-06-19T00:01:00+00:00",
                "task_id": "1",
                "task_type": "security",
                "selected_observer": "fusion",
                "score": 7,
                "should_use_fusion": True,
                "reasons": ["security: +3"],
                "text": "must not be printed",
            }
        ],
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["observer-log", "--path", str(log_path), "--limit", "5"],
    )

    observer_log()

    output = capsys.readouterr().out
    assert "task_id=1" in output
    assert "observer=fusion" in output
    assert "must not be printed" not in output
    assert "text" not in output


def test_observer_log_handles_missing_file(monkeypatch, tmp_path: Path, capsys):
    missing_path = tmp_path / "missing.jsonl"
    monkeypatch.setattr(
        sys,
        "argv",
        ["observer-log", "--path", str(missing_path)],
    )

    observer_log()

    output = capsys.readouterr().out
    assert "No observer decision log entries found." in output


def test_observer_log_summary_prints_aggregate_report(
    monkeypatch,
    tmp_path: Path,
    capsys,
):
    log_path = tmp_path / "observer_decisions.jsonl"
    _write_jsonl(
        log_path,
        [
            {
                "timestamp": "2026-06-19T00:01:00+00:00",
                "task_id": "1",
                "task_type": "security",
                "selected_observer": "fusion",
                "score": 7,
                "should_use_fusion": True,
                "reasons": ["security: +3"],
                "text": "must not be printed",
            },
            {
                "timestamp": "2026-06-19T00:02:00+00:00",
                "task_id": "2",
                "task_type": "memo_cleanup",
                "selected_observer": "default",
                "score": 0,
                "should_use_fusion": False,
                "reasons": ["blocklist: memo_cleanup"],
                "metadata": {"must": "not be printed"},
            },
        ],
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["observer-log", "--path", str(log_path), "--limit", "5", "--summary"],
    )

    observer_log()

    output = capsys.readouterr().out
    assert "Observer decision report" in output
    assert "total=2" in output
    assert "fusion_count=1" in output
    assert "default_count=1" in output
    assert "average_score=3.50" in output
    assert "security:1" in output
    assert "must not be printed" not in output
    assert "metadata" not in output
