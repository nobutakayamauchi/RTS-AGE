from core.observer_gate.local_adapter import LocalObserverProviderAdapter
from core.observer_gate.provider_adapter import (
    ObserverProviderRequest,
    ObserverProviderResponse,
)
from core.observer_gate.provider_config import (
    ObserverProviderAdapterConfig,
    ObserverProviderConfig,
)
from core.observer_gate.provider_registry_builder import (
    ObserverProviderRegistryBuildError,
    build_observer_provider_registry_from_config,
)


def test_build_observer_provider_registry_from_empty_config():
    registry = build_observer_provider_registry_from_config(ObserverProviderConfig())

    assert registry.provider_ids() == ()
    assert registry.get("local") is None


def test_build_observer_provider_registry_from_enabled_local_config():
    config = ObserverProviderConfig(
        adapters=(
            ObserverProviderAdapterConfig(
                provider_id="local",
                observer_name="default",
                enabled=True,
                adapter_kind="local",
                model="local-model",
            ),
        )
    )

    registry = build_observer_provider_registry_from_config(config)
    adapter = registry.require("local")

    assert isinstance(adapter, LocalObserverProviderAdapter)
    assert adapter.provider_id == "local"
    assert adapter.observer_name == "default"
    assert adapter.model == "local-model"


def test_build_observer_provider_registry_ignores_disabled_config():
    config = ObserverProviderConfig(
        adapters=(
            ObserverProviderAdapterConfig(
                provider_id="local",
                observer_name="default",
                enabled=False,
                adapter_kind="local",
            ),
        )
    )

    registry = build_observer_provider_registry_from_config(config)

    assert registry.provider_ids() == ()
    assert registry.get("local") is None


def test_built_local_registry_can_return_observation_without_prompt_leak():
    config = ObserverProviderConfig(
        adapters=(
            ObserverProviderAdapterConfig(
                provider_id="local",
                observer_name="default",
                enabled=True,
                adapter_kind="local",
            ),
        )
    )
    registry = build_observer_provider_registry_from_config(config)
    request = ObserverProviderRequest(
        task_id="task-1",
        task_type="memo_cleanup",
        prompt="private prompt text",
    )

    response = registry.require("local").observe(request)

    assert isinstance(response, ObserverProviderResponse)
    assert response.output == "local_observation task_id=task-1 task_type=memo_cleanup"
    assert request.prompt not in response.output


def test_build_observer_provider_registry_rejects_enabled_unsupported_kind():
    config = ObserverProviderConfig(
        adapters=(
            ObserverProviderAdapterConfig(
                provider_id="remote",
                observer_name="remote",
                enabled=True,
                adapter_kind="remote",
            ),
        )
    )

    try:
        build_observer_provider_registry_from_config(config)
    except ObserverProviderRegistryBuildError as exc:
        assert "unsupported observer provider adapter kind: remote" in str(exc)
    else:
        raise AssertionError("Expected unsupported adapter kind to raise build error")


def test_build_observer_provider_registry_allows_disabled_unsupported_kind():
    config = ObserverProviderConfig(
        adapters=(
            ObserverProviderAdapterConfig(
                provider_id="remote",
                observer_name="remote",
                enabled=False,
                adapter_kind="remote",
            ),
        )
    )

    registry = build_observer_provider_registry_from_config(config)

    assert registry.provider_ids() == ()
