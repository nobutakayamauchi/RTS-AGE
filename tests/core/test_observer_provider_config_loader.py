import json

from core.observer_gate.provider_config_loader import (
    ObserverProviderConfigError,
    load_observer_provider_config_from_json_file,
    load_observer_provider_config_from_mapping,
)


def test_load_observer_provider_config_from_empty_mapping():
    config = load_observer_provider_config_from_mapping({})

    assert config.provider_ids() == ()
    assert config.enabled_provider_ids() == ()
    assert config.enabled_configs() == ()


def test_load_observer_provider_config_from_mapping():
    config = load_observer_provider_config_from_mapping(
        {
            "adapters": [
                {
                    "provider_id": "local",
                    "observer_name": "default",
                    "enabled": True,
                    "adapter_kind": "local",
                    "model": "local-deterministic-v0",
                },
                {
                    "provider_id": "fusion",
                    "observer_name": "fusion",
                    "enabled": False,
                    "adapter_kind": "special",
                },
            ]
        }
    )

    assert config.provider_ids() == ("local", "fusion")
    assert config.enabled_provider_ids() == ("local",)
    assert config.require("local").adapter_kind == "local"
    assert config.require("local").model == "local-deterministic-v0"
    assert config.require("fusion").model is None


def test_load_observer_provider_config_replaces_duplicate_provider_id():
    config = load_observer_provider_config_from_mapping(
        {
            "adapters": [
                {
                    "provider_id": "local",
                    "observer_name": "default",
                },
                {
                    "provider_id": "local",
                    "observer_name": "replacement",
                    "enabled": True,
                },
            ]
        }
    )

    assert config.provider_ids() == ("local",)
    assert config.require("local").observer_name == "replacement"
    assert config.enabled_provider_ids() == ("local",)


def test_load_observer_provider_config_from_json_file(tmp_path):
    path = tmp_path / "provider_config.json"
    path.write_text(
        json.dumps(
            {
                "adapters": [
                    {
                        "provider_id": "local",
                        "observer_name": "default",
                        "enabled": True,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    config = load_observer_provider_config_from_json_file(path)

    assert config.provider_ids() == ("local",)
    assert config.enabled_provider_ids() == ("local",)


def test_load_observer_provider_config_rejects_invalid_root(tmp_path):
    path = tmp_path / "provider_config.json"
    path.write_text(json.dumps([]), encoding="utf-8")

    try:
        load_observer_provider_config_from_json_file(path)
    except ObserverProviderConfigError as exc:
        assert "provider config root must be an object" in str(exc)
    else:
        raise AssertionError("Expected invalid root to raise config error")


def test_load_observer_provider_config_rejects_invalid_adapter_list():
    try:
        load_observer_provider_config_from_mapping({"adapters": "local"})
    except ObserverProviderConfigError as exc:
        assert "adapters must be a list" in str(exc)
    else:
        raise AssertionError("Expected invalid adapters to raise config error")


def test_load_observer_provider_config_rejects_missing_provider_id():
    try:
        load_observer_provider_config_from_mapping(
            {"adapters": [{"observer_name": "default"}]}
        )
    except ObserverProviderConfigError as exc:
        assert "adapters[0].provider_id must be a string" in str(exc)
    else:
        raise AssertionError("Expected missing provider_id to raise config error")


def test_load_observer_provider_config_rejects_invalid_enabled_type():
    try:
        load_observer_provider_config_from_mapping(
            {
                "adapters": [
                    {
                        "provider_id": "local",
                        "observer_name": "default",
                        "enabled": "yes",
                    }
                ]
            }
        )
    except ObserverProviderConfigError as exc:
        assert "adapters[0].enabled must be a bool" in str(exc)
    else:
        raise AssertionError("Expected invalid enabled to raise config error")
