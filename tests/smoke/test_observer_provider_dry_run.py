from smoke.observer_provider_dry_run import run_observer_provider_dry_run


def test_observer_provider_dry_run_returns_safe_local_report():
    report = run_observer_provider_dry_run()

    assert "Observer provider dry-run complete." in report
    assert "provider_id=local" in report
    assert "observer_name=default" in report
    assert "model=local-deterministic-v0" in report
    assert "output=local_observation task_id=smoke-provider-local" in report
    assert "task_type=memo_cleanup" in report
    assert "private prompt text" not in report
