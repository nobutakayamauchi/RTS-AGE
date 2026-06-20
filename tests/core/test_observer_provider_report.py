from core.observer_gate.provider_adapter import (
    ObserverProviderError,
    ObserverProviderResponse,
)
from core.observer_gate.provider_report import (
    format_observer_provider_result,
    format_observer_provider_results,
)


def test_format_observer_provider_response():
    response = ObserverProviderResponse(
        provider_id="local",
        observer_name="default",
        output="local_observation task_id=task-1 task_type=memo_cleanup",
        model="local-model",
    )

    report = format_observer_provider_result(response)

    assert report == (
        "status=ok | provider_id=local | observer_name=default | "
        "model=local-model | "
        "output=local_observation task_id=task-1 task_type=memo_cleanup"
    )


def test_format_observer_provider_response_uses_unknown_model_when_missing():
    response = ObserverProviderResponse(
        provider_id="local",
        observer_name="default",
        output="local_observation task_id=task-1 task_type=memo_cleanup",
    )

    report = format_observer_provider_result(response)

    assert "model=unknown" in report


def test_format_observer_provider_error():
    error = ObserverProviderError(
        provider_id="remote",
        observer_name="remote",
        reason="not configured",
        retryable=True,
    )

    report = format_observer_provider_result(error)

    assert report == (
        "status=error | provider_id=remote | observer_name=remote | "
        "retryable=true | reason=not configured"
    )


def test_format_observer_provider_results():
    response = ObserverProviderResponse(
        provider_id="local",
        observer_name="default",
        output="local_observation task_id=task-1 task_type=memo_cleanup",
    )
    error = ObserverProviderError(
        provider_id="remote",
        observer_name="remote",
        reason="not configured",
    )

    report = format_observer_provider_results([response, error])

    assert "status=ok" in report
    assert "status=error" in report
    assert "\n" in report


def test_format_observer_provider_results_empty_state():
    report = format_observer_provider_results([])

    assert report == "No observer provider results."


def test_format_observer_provider_result_does_not_add_prompt_text():
    response = ObserverProviderResponse(
        provider_id="local",
        observer_name="default",
        output="local_observation task_id=task-1 task_type=memo_cleanup",
    )

    report = format_observer_provider_result(response)

    assert "private prompt text" not in report
