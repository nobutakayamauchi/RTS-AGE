"""Dry-run smoke script with observer decision summary output.

This script stays on the safe local path. It does not call external providers,
Fusion, the provider registry, or task execution.
"""

from pathlib import Path

from core.observer_gate.entrypoint import evaluate_observer_gate
from core.observer_gate.log_reader import (
    format_observer_decision_log_entries,
    read_observer_decision_log,
)
from core.observer_gate.models import TaskInput
from core.observer_gate.report import (
    format_observer_decision_report,
    summarize_observer_decisions,
)

DEFAULT_HIGH_RISK_TASK_TEXT = "顧客納品用の公開営業LPをレビューして"
DEFAULT_LOW_RISK_TASK_TEXT = "メモを整理して"


def run_observer_gate_summary_dry_run(log_path: str | Path) -> str:
    """Run safe observer gate decisions and return raw plus summary output."""
    log_file = Path(log_path)
    decisions = [
        evaluate_observer_gate(
            TaskInput(task_id="smoke-summary-high-risk", text=DEFAULT_HIGH_RISK_TASK_TEXT),
            enabled=True,
            log_decision=True,
            log_path=log_file,
        ),
        evaluate_observer_gate(
            TaskInput(task_id="smoke-summary-low-risk", text=DEFAULT_LOW_RISK_TASK_TEXT),
            enabled=True,
            log_decision=True,
            log_path=log_file,
        ),
    ]
    entries = read_observer_decision_log(log_file, limit=len(decisions))
    raw_report = format_observer_decision_log_entries(entries)
    summary_report = format_observer_decision_report(
        summarize_observer_decisions(entries)
    )

    return "\n".join(
        [
            "Observer gate summary dry-run complete.",
            "",
            "Raw decisions",
            raw_report,
            "",
            summary_report,
        ]
    )


def main() -> None:
    report = run_observer_gate_summary_dry_run(
        "logs/observer_decisions.summary_dry_run.jsonl"
    )
    print(report)


if __name__ == "__main__":
    main()
