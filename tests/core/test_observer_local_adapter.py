from core.observer_gate.local_adapter import (
    LocalObserverProviderAdapter,
    create_local_observer_provider_adapter,
)
from core.observer_gate.provider_adapter import (
    ObserverProviderRequest,
    ObserverProviderResponse,
)
from core.observer_gate.provider_registry import empty_observer_provider_registry


def test_local_observer_provider_adapter_defaults():
    adapter = create_local_observer_provider_adapter()

    assert adapter.provider_id == "local"
    assert adapter.observer_name == "default"
    assert adapter.model == "local-deterministic-v0"


def test_local_observer_provider_adapter_returns_deterministic_response():
    adapter = LocalObserverProviderAdapter()
    request = ObserverProviderRequest(
        task_id="task-1",
        task_type="memo_cleanup",
        prompt="sensitive prompt text",
        metadata={"source": "test"},
    )

    response = adapter.observe(request)

    assert response == ObserverProviderResponse(
        provider_id="local",
        observer_name="default",
        output="local_observation task_id=task-1 task_type=memo_cleanup",
        model="local-deterministic-v0",
    )
    assert request.prompt not in response.output
    assert "source" not in response.output


def test_local_observer_provider_adapter_can_be_registered():
    adapter = create_local_observer_provider_adapter()
    registry = empty_observer_provider_registry().with_adapter(adapter)
    request = ObserverProviderRequest(
        task_id="task-2",
        task_type="paid_delivery",
        prompt="review deliverable",
    )

    response = registry.require("local").observe(request)

    assert isinstance(response, ObserverProviderResponse)
    assert response.provider_id == "local"
    assert response.observer_name == "default"
    assert response.output == "local_observation task_id=task-2 task_type=paid_delivery"
    assert response.model == "local-deterministic-v0"
