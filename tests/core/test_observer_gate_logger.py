import json

from core.observer_gate.logger import append_observer_decision
from core.observer_gate.models import ObserverDecision


def test_append_observer_decision_writes_jsonl(tmp_path):
    path = tmp_path / 'observer_decisions.jsonl'
    decision = ObserverDecision(
        task_id='1',
        task_type='security',
        selected_observer='fusion',
        score=8,
        should_use_fusion=True,
        reasons=['security: +3'],
    )

    append_observer_decision(decision, path)

    lines = path.read_text(encoding='utf-8').splitlines()
    assert len(lines) == 1

    record = json.loads(lines[0])
    assert record['task_id'] == '1'
    assert record['task_type'] == 'security'
    assert record['selected_observer'] == 'fusion'
    assert record['score'] == 8
    assert record['should_use_fusion'] is True
    assert record['reasons'] == ['security: +3']
    assert 'timestamp' in record
