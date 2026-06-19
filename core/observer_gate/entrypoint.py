import os
from collections.abc import Mapping
from pathlib import Path

from .logger import append_observer_decision
from .models import ObserverDecision, TaskInput
from .policy_loader import load_observer_policy
from .router import route_observer

OBSERVER_GATE_ENABLED_ENV = "RTS_AGE_OBSERVER_GATE_ENABLED"
OBSERVER_GATE_LOG_ENABLED_ENV = "RTS_AGE_OBSERVER_GATE_LOG_ENABLED"
OBSERVER_GATE_LOG_PATH_ENV = "RTS_AGE_OBSERVER_GATE_LOG_PATH"
DEFAULT_POLICY_PATH = Path("specs/multi_observer_v0.yaml")
DEFAULT_LOG_PATH = Path("logs/observer_decisions.jsonl")
_TRUE_VALUES = {"1", "true", "yes", "on"}


def is_observer_gate_enabled(env: Mapping[str, str] | None = None) -> bool:
    values = os.environ if env is None else env
    return values.get(OBSERVER_GATE_ENABLED_ENV, "").lower() in _TRUE_VALUES


def is_observer_gate_logging_enabled(env: Mapping[str, str] | None = None) -> bool:
    values = os.environ if env is None else env
    return values.get(OBSERVER_GATE_LOG_ENABLED_ENV, "").lower() in _TRUE_VALUES


def get_observer_gate_log_path(env: Mapping[str, str] | None = None) -> Path:
    values = os.environ if env is None else env
    configured_path = values.get(OBSERVER_GATE_LOG_PATH_ENV, "")
    if configured_path:
        return Path(configured_path)
    return DEFAULT_LOG_PATH


def evaluate_observer_gate(
    task_input: TaskInput,
    policy_path: str | Path = DEFAULT_POLICY_PATH,
    enabled: bool | None = None,
    log_decision: bool | None = None,
    log_path: str | Path | None = None,
) -> ObserverDecision:
    """Evaluate the observer gate behind explicit feature flags.

    Disabled mode does not read policy files and always returns a default observer
    decision. Enabled mode reads the YAML policy and routes deterministically.
    Optional logging writes only routing metadata, never task text.
    """
    if enabled is None:
        enabled = is_observer_gate_enabled()

    if not enabled:
        decision = ObserverDecision(
            task_id=task_input.task_id,
            task_type="observer_gate_disabled",
            selected_observer="default",
            score=0,
            should_use_fusion=False,
            reasons=["observer gate disabled"],
        )
    else:
        policy = load_observer_policy(policy_path)
        decision = route_observer(task_input, policy)

    if log_decision is None:
        log_decision = is_observer_gate_logging_enabled()

    if log_decision:
        append_observer_decision(
            decision,
            path=log_path if log_path is not None else get_observer_gate_log_path(),
        )

    return decision
