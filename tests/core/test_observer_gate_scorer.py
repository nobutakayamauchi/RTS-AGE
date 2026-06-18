from core.observer_gate.models import ObserverPolicy, TaskClassification
from core.observer_gate.scorer import score_fusion_need


def _policy() -> ObserverPolicy:
    return ObserverPolicy(
        fusion_trigger_score=7,
        risk_weights={
            'paid_delivery': 3,
            'public_release': 2,
            'legal_or_money': 3,
            'security': 3,
            'unclear_requirements': 2,
            'multi_domain': 2,
            'high_failure_cost': 2,
        },
        blocklist={
            'simple_rewrite',
            'memo_cleanup',
            'x_post_generation',
            'draft_only',
            'trivial_code_edit',
        },
    )


def test_scores_risk_flags():
    classification = TaskClassification(
        task_id='1',
        task_type='paid_delivery',
        flags={'paid_delivery', 'public_release', 'multi_domain'},
    )
    score, reasons = score_fusion_need(classification, _policy())
    assert score == 7
    assert 'paid_delivery: +3' in reasons


def test_blocklist_forces_zero_score():
    classification = TaskClassification(
        task_id='2',
        task_type='x_post_generation',
        flags={'x_post_generation', 'public_release'},
    )
    score, reasons = score_fusion_need(classification, _policy())
    assert score == 0
    assert reasons == ['blocklisted task_type: x_post_generation']


def test_unknown_flags_are_ignored():
    classification = TaskClassification(
        task_id='3',
        task_type='general',
        flags={'unknown'},
    )
    score, reasons = score_fusion_need(classification, _policy())
    assert score == 0
    assert reasons == []
