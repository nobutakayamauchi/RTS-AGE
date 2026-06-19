from pathlib import Path

from smoke.observer_gate_dry_run import run_observer_gate_dry_run


def test_observer_gate_dry_run_writes_log_and_returns_report(tmp_path: Path):
    log_path = tmp_path / "observer_decisions.dry_run.jsonl"

    report = run_observer_gate_dry_run(log_path)

    assert log_path.exists()
    assert "Observer gate dry-run complete." in report
    assert "task_id=smoke-observer-gate-1" in report
    assert "selected_observer=" in report
    assert "score=" in report
    assert "should_use_fusion=" in report
    assert "text" not in report


def test_observer_gate_dry_run_accepts_low_risk_task(tmp_path: Path):
    log_path = tmp_path / "observer_decisions.dry_run.jsonl"

    report = run_observer_gate_dry_run(
        log_path,
        task_id="smoke-low-risk",
        task_text="メモを整理して",
    )

    assert "task_id=smoke-low-risk" in report
    assert "selected_observer=default" in report
