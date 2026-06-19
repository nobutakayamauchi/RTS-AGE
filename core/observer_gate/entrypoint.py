import os
from collections.abc import Mapping
from pathlib import Path

from .models import ObserverDecision, TaskInput
from .policy_loader import load_observer_policy
from .router import route_observer

OBSERVER_GATE_ENABLED_ENV = "RTS_AGE_OBSERVER_GATE_ENABLED"
DEFAULT_POLICY_PATH = Path("specs/multi_observer_v0.yaml")
_TRUE_VALUES = {"1", "true", "yes", "on"}


def is_observer_gate_enabled(env: Mapping[str, str] | None = None) -> bool:
    values = os.environ if env is None else env
    return values.get(OBSERVER_GATE_ENABLED_ENV, "").lower() in _TRUE_VALUES


def evaluate_observer_gate(
    task_input: TaskInput,
    policy_path: str | Path = DEFAULT_POLICY_PATH,
    enabled: bool | None = None,
) -> ObserverDecision:
    """Evaluate the observer gate behind an explicit feature flag.

    Disabled mode does not read policy files and always returns a default observer
    decision. Enabled mode reads the YAML policy and routes deterministically.
    """
    if enabled is None:
        enabled = is_observer_gate_enabled()

    if not enabled:
        return ObserverDecision(
            task_id=task_input.task_id,
            task_type="observer_gate_disabled",
            selected_observer="default",
            score=0,
            should_use_fusion=False,
            reasons=["observer gate disabled"],
        )

    policy = load_observer_policy(policy_path)
    return route_observer(task_input, policy)
