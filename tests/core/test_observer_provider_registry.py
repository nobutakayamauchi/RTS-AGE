from dataclasses import dataclass

from core.observer_gate.provider_adapter import (
    ObserverProviderRequest,
    ObserverProviderResponse,
)
from core.observer_gate.provider_registry import empty_observer_provider_registry


@dataclass(frozen=True)
class FakeObserverAdapter:
    provider_id: str
    observer_name: str

    def observe(self, request: ObserverProviderRequest) -> ObserverProviderResponse:
        return ObserverProviderResponse(
            provider_id=self.provider_id,
            observer_name=self.observer_name,
            output=f"observed:{request.task_id}",
            model="fake-model",
        )


def test_empty_observer_provider_registry_has_no_adapters():
    registry = empty_observer_provider_registry()

    assert registry.provider_ids() == ()
    assert registry.get("local") is None


def test_observer_provider_registry_registers_adapter_immutably():
    registry = empty_observer_provider_registry()
    adapter = FakeObserverAdapter(provider_id="local", observer_name="default")

    updated = registry.with_adapter(adapter)

    assert registry.provider_ids() == ()
    assert updated.provider_ids() == ("local",)
    assert updated.get("local") == adapter
    assert updated.require("local") == adapter


def test_observer_provider_registry_replaces_existing_provider_id():
    registry = empty_observer_provider_registry()
    first = FakeObserverAdapter(provider_id="local", observer_name="default")
    second = FakeObserverAdapter(provider_id="local", observer_name="replacement")

    updated = registry.with_adapter(first).with_adapter(second)

    assert updated.provider_ids() == ("local",)
    assert updated.require("local") == second


def test_observer_provider_registry_raises_for_missing_required_adapter():
    registry = empty_observer_provider_registry()

    try:
        registry.require("missing")
    except KeyError as exc:
        assert "Observer provider adapter not registered: missing" in str(exc)
    else:
        raise AssertionError("Expected missing adapter lookup to raise KeyError")


def test_registered_adapter_can_observe_without_registry_calling_it():
    registry = empty_observer_provider_registry().with_adapter(
        FakeObserverAdapter(provider_id="local", observer_name="default")
    )
    request = ObserverProviderRequest(
        task_id="task-1",
        task_type="memo_cleanup",
        prompt="メモを整理して",
    )

    response = registry.require("local").observe(request)

    assert response.provider_id == "local"
    assert response.observer_name == "default"
    assert response.output == "observed:task-1"
    assert response.model == "fake-model"
