from core.observer_gate.provider_config import (
    ObserverProviderAdapterConfig,
    empty_observer_provider_config,
)


def test_empty_observer_provider_config_has_no_adapters():
    config = empty_observer_provider_config()

    assert config.provider_ids() == ()
    assert config.enabled_provider_ids() == ()
    assert config.enabled_configs() == ()
    assert config.get("local") is None


def test_observer_provider_adapter_config_defaults_to_disabled_stub():
    adapter_config = ObserverProviderAdapterConfig(
        provider_id="local",
        observer_name="default",
    )

    assert adapter_config.provider_id == "local"
    assert adapter_config.observer_name == "default"
    assert adapter_config.enabled is False
    assert adapter_config.adapter_kind == "stub"
    assert adapter_config.model is None


def test_observer_provider_config_tracks_enabled_adapters():
    config = empty_observer_provider_config()
    config = config.with_adapter_config(
        ObserverProviderAdapterConfig(
            provider_id="local",
            observer_name="default",
            enabled=True,
            adapter_kind="local",
            model="rule-based",
        )
    )
    config = config.with_adapter_config(
        ObserverProviderAdapterConfig(
            provider_id="fusion",
            observer_name="fusion",
            enabled=False,
            adapter_kind="special",
        )
    )

    assert config.provider_ids() == ("local", "fusion")
    assert config.enabled_provider_ids() == ("local",)
    assert config.require("local").model == "rule-based"
    assert config.require("fusion").enabled is False


def test_observer_provider_config_replaces_existing_provider_id():
    config = empty_observer_provider_config()
    config = config.with_adapter_config(
        ObserverProviderAdapterConfig(
            provider_id="local",
            observer_name="default",
            enabled=False,
        )
    )
    config = config.with_adapter_config(
        ObserverProviderAdapterConfig(
            provider_id="local",
            observer_name="replacement",
            enabled=True,
        )
    )

    assert config.provider_ids() == ("local",)
    assert config.require("local").observer_name == "replacement"
    assert config.enabled_provider_ids() == ("local",)


def test_observer_provider_config_raises_for_missing_required_config():
    config = empty_observer_provider_config()

    try:
        config.require("missing")
    except KeyError as exc:
        assert "Observer provider adapter config not found: missing" in str(exc)
    else:
        raise AssertionError("Expected missing adapter config to raise KeyError")
