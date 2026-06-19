from pathlib import Path

from core.observer_gate.entrypoint import (
    OBSERVER_GATE_ENABLED_ENV,
    evaluate_observer_gate,
    is_observer_gate_enabled,
)
from core.observer_gate.models import TaskInput

POLICY_TEXT = """
version: 0.1

fusion_trigger_score: 7

risk_weights:
  paid_delivery: 3
  public_release: 2
  legal_or_money: 3
  security: 3
  unclear_requirements: 2
  multi_domain: 2
  model_disagreement: 2
  high_failure_cost: 2

blocklist:
  - simple_rewrite
  - memo_cleanup
  - x_post_generation
  - draft_only
  - trivial_code_edit

observers:
  default:
    provider: nvidia_nim
    role: cheap_observer

  fusion:
    provider: open_router
    model: openrouter/fusion
    role: special_observer

logging:
  path: logs/observer_decisions.jsonl
"""


def test_is_observer_gate_enabled_reads_true_values():
    assert is_observer_gate_enabled({OBSERVER_GATE_ENABLED_ENV: "true"}) is True
    assert is_observer_gate_enabled({OBSERVER_GATE_ENABLED_ENV: "1"}) is True


def test_is_observer_gate_enabled_defaults_to_false():
    assert is_observer_gate_enabled({}) is False


def test_disabled_entrypoint_returns_default_without_policy_file():
    task = TaskInput(task_id="1", text="顧客納品用の公開営業LPをレビューして")

    decision = evaluate_observer_gate(
        task,
        policy_path="missing-policy.yaml",
        enabled=False,
    )

    assert decision.selected_observer == "default"
    assert decision.should_use_fusion is False
    assert decision.score == 0
    assert decision.task_type == "observer_gate_disabled"


def test_enabled_entrypoint_routes_using_policy(tmp_path: Path):
    policy_path = tmp_path / "policy.yaml"
    policy_path.write_text(POLICY_TEXT, encoding="utf-8")
    task = TaskInput(task_id="2", text="顧客納品用の公開営業LPをレビューして")

    decision = evaluate_observer_gate(task, policy_path=policy_path, enabled=True)

    assert decision.selected_observer == "fusion"
    assert decision.should_use_fusion is True
    assert decision.score >= 7


def test_enabled_entrypoint_respects_blocklist(tmp_path: Path):
    policy_path = tmp_path / "policy.yaml"
    policy_path.write_text(POLICY_TEXT, encoding="utf-8")
    task = TaskInput(task_id="3", text="X投稿を10個作って")

    decision = evaluate_observer_gate(task, policy_path=policy_path, enabled=True)

    assert decision.selected_observer == "default"
    assert decision.should_use_fusion is False
    assert decision.score == 0
