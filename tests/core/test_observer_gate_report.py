from core.observer_gate.log_reader import ObserverDecisionLogEntry
from core.observer_gate.report import (
    format_observer_decision_report,
    summarize_observer_decisions,
)


def test_summarize_observer_decisions_empty():
    report = summarize_observer_decisions([])

    assert report.total == 0
    assert report.fusion_count == 0
    assert report.default_count == 0
    assert report.average_score == 0.0
    assert report.task_type_counts == {}
    assert report.observer_counts == {}
    assert report.top_reasons == []
    assert format_observer_decision_report(report) == (
        "No observer decision log entries found."
    )


def test_summarize_observer_decisions_aggregates_entries():
    entries = [
        ObserverDecisionLogEntry(
            timestamp="2026-06-19T00:00:00+00:00",
            task_id="1",
            task_type="paid_delivery",
            selected_observer="fusion",
            score=7,
            should_use_fusion=True,
            reasons=["paid_delivery: +3", "public_release: +2"],
        ),
        ObserverDecisionLogEntry(
            timestamp="2026-06-19T00:01:00+00:00",
            task_id="2",
            task_type="memo_cleanup",
            selected_observer="default",
            score=0,
            should_use_fusion=False,
            reasons=["blocklist: memo_cleanup"],
        ),
        ObserverDecisionLogEntry(
            timestamp="2026-06-19T00:02:00+00:00",
            task_id="3",
            task_type="paid_delivery",
            selected_observer="fusion",
            score=5,
            should_use_fusion=True,
            reasons=["paid_delivery: +3"],
        ),
    ]

    report = summarize_observer_decisions(entries)

    assert report.total == 3
    assert report.fusion_count == 2
    assert report.default_count == 1
    assert report.average_score == 4.0
    assert report.task_type_counts == {"paid_delivery": 2, "memo_cleanup": 1}
    assert report.observer_counts == {"fusion": 2, "default": 1}
    assert report.top_reasons[0] == ("paid_delivery: +3", 2)


def test_format_observer_decision_report_does_not_include_request_text():
    report = summarize_observer_decisions(
        [
            ObserverDecisionLogEntry(
                timestamp="2026-06-19T00:00:00+00:00",
                task_id="secret-task",
                task_type="paid_delivery",
                selected_observer="fusion",
                score=7,
                should_use_fusion=True,
                reasons=["paid_delivery: +3"],
            )
        ]
    )

    output = format_observer_decision_report(report)

    assert "Observer decision report" in output
    assert "total=1" in output
    assert "fusion_count=1" in output
    assert "paid_delivery:1" in output
    assert "secret text" not in output
    assert "metadata" not in output
