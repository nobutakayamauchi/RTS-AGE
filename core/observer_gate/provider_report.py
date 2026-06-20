"""Report helpers for observer provider results.

This module formats provider result objects only. It does not run adapters or
perform runtime provider work.
"""

from __future__ import annotations

from collections.abc import Iterable

from core.observer_gate.provider_adapter import (
    ObserverProviderError,
    ObserverProviderResponse,
    ObserverProviderResult,
)


def format_observer_provider_result(result: ObserverProviderResult) -> str:
    """Format one provider result for safe display."""
    if isinstance(result, ObserverProviderResponse):
        return _format_response(result)
    return _format_error(result)


def format_observer_provider_results(results: Iterable[ObserverProviderResult]) -> str:
    """Format multiple provider results for safe display."""
    lines = [format_observer_provider_result(result) for result in results]
    if not lines:
        return "No observer provider results."
    return "\n".join(lines)


def _format_response(response: ObserverProviderResponse) -> str:
    model = response.model or "unknown"
    return " | ".join(
        [
            "status=ok",
            f"provider_id={response.provider_id}",
            f"observer_name={response.observer_name}",
            f"model={model}",
            f"output={response.output}",
        ]
    )


def _format_error(error: ObserverProviderError) -> str:
    return " | ".join(
        [
            "status=error",
            f"provider_id={error.provider_id}",
            f"observer_name={error.observer_name}",
            f"retryable={str(error.retryable).lower()}",
            f"reason={error.reason}",
        ]
    )
