from pathlib import Path

from smoke.observer_gate_summary_dry_run import run_observer_gate_summary_dry_run


def test_observer_gate_summary_dry_run_outputs_raw_and_summary(tmp_path: Path):
    log_path = tmp_path / "observer_decisions.summary_dry_run.jsonl"

    report = run_observer_gate_summary_dry_run(log_path)

    assert log_path.exists()
    assert "Observer gate summary dry-run complete." in report
    assert "Raw decisions" in report
    assert "Observer decision report" in report
    assert "total=2" in report
    assert "fusion_count=" in report
    assert "default_count=" in report
    assert "average_score=" in report
    assert "task_types=" in report
    assert "observers=" in report
    assert "top_reasons=" in report
    assert "smoke-summary-high-risk" in report
    assert "smoke-summary-low-risk" in report
    assert "text" not in report
    assert "metadata" not in report
