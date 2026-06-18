from .models import ObserverPolicy, TaskClassification


def score_fusion_need(
    classification: TaskClassification,
    policy: ObserverPolicy,
) -> tuple[int, list[str]]:
    """Calculate whether a task deserves special observer review.

    The scorer is deterministic and cheap. It does not call external APIs.
    Blocklisted task types are forced to score 0 even if risk flags are present.
    """
    if policy.is_blocklisted(classification.task_type):
        return 0, [f"blocklisted task_type: {classification.task_type}"]

    score = 0
    reasons: list[str] = []

    for flag in sorted(classification.flags):
        weight = policy.weight_for(flag)
        if weight <= 0:
            continue
        score += weight
        reasons.append(f"{flag}: +{weight}")

    return score, reasons
