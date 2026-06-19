from core.observer_gate.provider_adapter import (
    ObserverProviderError,
    ObserverProviderRequest,
    ObserverProviderResponse,
)


def test_observer_provider_request_keeps_prompt_in_memory_only():
    request = ObserverProviderRequest(
        task_id="task-1",
        task_type="paid_delivery",
        prompt="顧客納品用のレビューをして",
        metadata={"source": "test"},
    )

    assert request.task_id == "task-1"
    assert request.task_type == "paid_delivery"
    assert request.prompt == "顧客納品用のレビューをして"
    assert request.metadata == {"source": "test"}


def test_observer_provider_response_represents_success():
    response = ObserverProviderResponse(
        provider_id="local",
        observer_name="default",
        output="ok",
        model="local-rule",
    )

    assert response.provider_id == "local"
    assert response.observer_name == "default"
    assert response.output == "ok"
    assert response.model == "local-rule"


def test_observer_provider_error_represents_safe_failure():
    error = ObserverProviderError(
        provider_id="fusion",
        observer_name="fusion",
        reason="not configured",
        retryable=False,
    )

    assert error.provider_id == "fusion"
    assert error.observer_name == "fusion"
    assert error.reason == "not configured"
    assert error.retryable is False
