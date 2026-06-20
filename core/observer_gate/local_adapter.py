"""Local observer provider adapter for deterministic dry-runs.

This adapter does not call external services, Fusion, or any provider runtime.
It returns deterministic observation metadata for local testing only.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.observer_gate.provider_adapter import (
    ObserverProviderRequest,
    ObserverProviderResponse,
)


@dataclass(frozen=True)
class LocalObserverProviderAdapter:
    """Deterministic local adapter for observer-provider dry-runs."""

    provider_id: str = "local"
    observer_name: str = "default"
    model: str = "local-deterministic-v0"

    def observe(self, request: ObserverProviderRequest) -> ObserverProviderResponse:
        """Return a deterministic observation without exposing request text."""
        output = " ".join(
            (
                "local_observation",
                f"task_id={request.task_id}",
                f"task_type={request.task_type}",
            )
        )
        return ObserverProviderResponse(
            provider_id=self.provider_id,
            observer_name=self.observer_name,
            output=output,
            model=self.model,
        )


def create_local_observer_provider_adapter() -> LocalObserverProviderAdapter:
    """Return the default local observer provider adapter."""
    return LocalObserverProviderAdapter()
