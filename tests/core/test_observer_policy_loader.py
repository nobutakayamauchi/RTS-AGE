from pathlib import Path

import pytest

from core.observer_gate.policy_loader import (
    ObserverPolicyLoadError,
    load_observer_policy,
    observer_policy_from_text,
)


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


def test_observer_policy_from_text_loads_score_and_weights():
    policy = observer_policy_from_text(POLICY_TEXT)
    assert policy.fusion_trigger_score == 7
    assert policy.weight_for("paid_delivery") == 3
    assert policy.weight_for("security") == 3


def test_observer_policy_from_text_loads_blocklist():
    policy = observer_policy_from_text(POLICY_TEXT)
    assert policy.is_blocklisted("memo_cleanup")
    assert policy.is_blocklisted("x_post_generation")


def test_load_observer_policy_reads_file(tmp_path: Path):
    policy_path = tmp_path / "policy.yaml"
    policy_path.write_text(POLICY_TEXT, encoding="utf-8")

    policy = load_observer_policy(policy_path)

    assert policy.fusion_trigger_score == 7
    assert policy.weight_for("high_failure_cost") == 2


def test_invalid_policy_raises_error():
    with pytest.raises(ObserverPolicyLoadError):
        observer_policy_from_text("version: 0.1\n")
