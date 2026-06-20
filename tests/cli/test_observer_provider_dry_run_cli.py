from cli.entrypoints import observer_provider_dry_run


def test_observer_provider_dry_run_cli_prints_safe_report(capsys):
    observer_provider_dry_run()

    output = capsys.readouterr().out

    assert "Observer provider dry-run complete." in output
    assert "status=ok" in output
    assert "provider_id=local" in output
    assert "observer_name=default" in output
    assert "model=local-deterministic-v0" in output
    assert "output=local_observation task_id=smoke-provider-local" in output
    assert "task_type=memo_cleanup" in output
    assert "private prompt text" not in output
