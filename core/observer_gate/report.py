"""Summarize observer decision logs without exposing request text."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from core.observer_gate.log_reader import ObserverDecisionLogEntry


@dataclass(frozen=True)
class ObserverDecisionReport:
    total: int
    fusion_count: int
    default_count: int
    average_score: float
    task_type_counts: dict[str, int]
    observer_counts: dict[str, int]
    top_reasons: list[tuple[str, int]]


def summarize_observer_decisions(
    entries: list[ObserverDecisionLogEntry],
    top_reason_limit: int = 5,
) -> ObserverDecisionReport:
    """Summarize observer decisions into aggregate routing metrics."""
    if not entries:
        return ObserverDecisionReport(
            total=0,
            fusion_count=0,
            default_count=0,
            average_score=0.0,
            task_type_counts={},
            observer_counts={},
            top_reasons=[],
        )

    observer_counts = Counter(entry.selected_observer for entry in entries)
    task_type_counts = Counter(entry.task_type for entry in entries)
    reason_counts = Counter(reason for entry in entries for reason in entry.reasons)
    total_score = sum(entry.score for entry in entries)

    return ObserverDecisionReport(
        total=len(entries),
        fusion_count=sum(1 for entry in entries if entry.should_use_fusion),
        default_count=observer_counts.get("default", 0),
        average_score=round(total_score / len(entries), 2),
        task_type_counts=dict(task_type_counts),
        observer_counts=dict(observer_counts),
        top_reasons=reason_counts.most_common(max(top_reason_limit, 0)),
    )


def format_observer_decision_report(report: ObserverDecisionReport) -> str:
    """Format an observer decision report for human review."""
    if report.total == 0:
        return "No observer decision log entries found."

    lines = [
        "Observer decision report",
        f"total={report.total}",
        f"fusion_count={report.fusion_count}",
        f"default_count={report.default_count}",
        f"average_score={report.average_score:.2f}",
        f"task_types={_format_counts(report.task_type_counts)}",
        f"observers={_format_counts(report.observer_counts)}",
        f"top_reasons={_format_reason_counts(report.top_reasons)}",
    ]
    return "\n".join(lines)


def _format_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "none"
    return ", ".join(f"{key}:{value}" for key, value in sorted(counts.items()))


def _format_reason_counts(reason_counts: list[tuple[str, int]]) -> str:
    if not reason_counts:
        return "none"
    return ", ".join(f"{reason}:{count}" for reason, count in reason_counts)
