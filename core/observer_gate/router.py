from .classifier import classify_task
from .models import ObserverDecision, ObserverPolicy, TaskInput
from .scorer import score_fusion_need


def should_use_fusion(score: int, policy: ObserverPolicy) -> bool:
    return score >= policy.fusion_trigger_score


def route_observer(task_input: TaskInput, policy: ObserverPolicy) -> ObserverDecision:
    classification = classify_task(task_input.task_id, task_input.text)
    score, score_reasons = score_fusion_need(classification, policy)
    use_fusion = should_use_fusion(score, policy)

    selected_observer = policy.fusion_observer if use_fusion else policy.default_observer

    reasons = [*classification.reasons, *score_reasons]

    return ObserverDecision(
        task_id=task_input.task_id,
        task_type=classification.task_type,
        selected_observer=selected_observer,
        score=score,
        should_use_fusion=use_fusion,
        reasons=reasons,
    )
