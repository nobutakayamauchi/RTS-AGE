from core.observer_gate.classifier import classify_task


def test_classifies_japanese_paid_delivery():
    result = classify_task('1', 'この納品物の見積をレビューして')
    assert result.task_type == 'legal_or_money'
    assert 'paid_delivery' in result.flags
    assert 'legal_or_money' in result.flags


def test_classifies_security_review():
    result = classify_task('2', 'セキュリティとcredential漏洩を確認して')
    assert result.task_type == 'security'
    assert 'security' in result.flags


def test_classifies_x_post_as_blocklisted():
    result = classify_task('3', 'X投稿を10個作って')
    assert result.task_type == 'x_post_generation'
    assert 'x_post_generation' in result.flags


def test_classifies_memo_cleanup_as_blocklisted():
    result = classify_task('4', 'メモ整理をして')
    assert result.task_type == 'memo_cleanup'
    assert 'memo_cleanup' in result.flags


def test_classifies_general_when_no_keywords():
    result = classify_task('5', 'hello world')
    assert result.task_type == 'general'
    assert result.flags == set()
