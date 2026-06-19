"""Dry-run smoke script for the observer gate workflow.

This script exercises the safe local observer gate path only. It does not call
external providers, Fusion, or the provider registry.
"""

from pathlib import Path

from core.observer_gate.entrypoint import evaluate_observer_gate
from core.observer_gate.log_reader import (
    format_observer_decision_log_entries,
    read_observer_decision_log,
)
from core.observer_gate.models import TaskInput

DEFAULT_TASK_TEXT = "顧客納品用の公開営業LPをレビューして"


def run_observer_gate_dry_run(
    log_path: str | Path,
    task_id: str = "smoke-observer-gate-1",
    task_text: str = DEFAULT_TASK_TEXT,
) -> str:
    """Run one safe observer gate decision and return a formatted report."""
    log_file = Path(log_path)
    task_input = TaskInput(task_id=task_id, text=task_text)

    decision = evaluate_observer_gate(
        task_input,
        enabled=True,
        log_decision=True,
        log_path=log_file,
    )
    entries = read_observer_decision_log(log_file, limit=1)
    report = format_observer_decision_log_entries(entries)

    return "\n".join(
        [
            "Observer gate dry-run complete.",
            f"task_id={decision.task_id}",
            f"selected_observer={decision.selected_observer}",
            f"score={decision.score}",
            f"should_use_fusion={decision.should_use_fusion}",
            "",
            report,
        ]
    )


def main() -> None:
    report = run_observer_gate_dry_run("logs/observer_decisions.dry_run.jsonl")
    print(report)


if __name__ == "__main__":
    main()
