from core.observer_gate.models import (
    ObserverDecision,
    ObserverPolicy,
    TaskClassification,
    TaskInput,
)


def test_task_input_creation():
    task = TaskInput(task_id="1", text="hello")
    assert task.task_id == "1"


def test_classification_flags():
    c = TaskClassification(task_id="1", task_type="paid_delivery", flags={"paid"})
    assert "paid" in c.flags


def test_policy_blocklist():
    p = ObserverPolicy(7, blocklist={"memo_cleanup"})
    assert p.is_blocklisted("memo_cleanup")


def test_policy_weight():
    p = ObserverPolicy(7, risk_weights={"security": 3})
    assert p.weight_for("security") == 3


def test_decision_creation():
    d = ObserverDecision("1", "security", "fusion", 10, True)
    assert d.should_use_fusion is True
