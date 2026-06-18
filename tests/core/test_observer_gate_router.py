from core.observer_gate.models import ObserverPolicy, TaskInput
from core.observer_gate.router import route_observer, should_use_fusion


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


def test_should_use_fusion_when_score_reaches_threshold():
    assert should_use_fusion(7, _policy()) is True


def test_should_not_use_fusion_below_threshold():
    assert should_use_fusion(6, _policy()) is False


def test_routes_high_risk_task_to_fusion():
    task = TaskInput('1', '顧客納品用の公開営業LPをレビューして')
    decision = route_observer(task, _policy())
    assert decision.selected_observer == 'fusion'
    assert decision.should_use_fusion is True
    assert decision.score >= 7


def test_routes_blocklisted_task_to_default():
    task = TaskInput('2', 'X投稿を10個作って')
    decision = route_observer(task, _policy())
    assert decision.selected_observer == 'default'
    assert decision.should_use_fusion is False
    assert decision.score == 0
