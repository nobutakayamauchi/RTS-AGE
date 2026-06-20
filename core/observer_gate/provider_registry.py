"""Registry for observer provider adapters.

This registry stores adapter instances only. It does not call external
providers, Fusion, or any provider runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.observer_gate.provider_adapter import ObserverProviderAdapter


@dataclass(frozen=True)
class ObserverProviderRegistry:
    """Immutable registry for observer provider adapters."""

    adapters: dict[str, ObserverProviderAdapter] = field(default_factory=dict)

    def provider_ids(self) -> tuple[str, ...]:
        """Return registered provider IDs in stable order."""
        return tuple(sorted(self.adapters))

    def get(self, provider_id: str) -> ObserverProviderAdapter | None:
        """Return a provider adapter by ID, if registered."""
        return self.adapters.get(provider_id)

    def require(self, provider_id: str) -> ObserverProviderAdapter:
        """Return a provider adapter or raise a clear lookup error."""
        adapter = self.get(provider_id)
        if adapter is None:
            raise KeyError(f"Observer provider adapter not registered: {provider_id}")
        return adapter

    def with_adapter(
        self,
        adapter: ObserverProviderAdapter,
    ) -> ObserverProviderRegistry:
        """Return a new registry with the adapter registered by provider ID."""
        return ObserverProviderRegistry(
            adapters={**self.adapters, adapter.provider_id: adapter}
        )


def empty_observer_provider_registry() -> ObserverProviderRegistry:
    """Return an empty observer provider registry."""
    return ObserverProviderRegistry()
