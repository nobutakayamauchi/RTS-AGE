"""Build observer provider registries from explicit configuration.

This module creates local-only adapter instances from safe configuration. It does
not perform runtime provider work.
"""

from __future__ import annotations

from core.observer_gate.local_adapter import LocalObserverProviderAdapter
from core.observer_gate.provider_config import (
    ObserverProviderAdapterConfig,
    ObserverProviderConfig,
)
from core.observer_gate.provider_registry import ObserverProviderRegistry


class ObserverProviderRegistryBuildError(ValueError):
    """Raised when provider registry construction is not supported."""


def build_observer_provider_registry_from_config(
    config: ObserverProviderConfig,
) -> ObserverProviderRegistry:
    """Build a provider registry from enabled local adapter configuration."""
    registry = ObserverProviderRegistry()
    for adapter_config in config.enabled_configs():
        adapter = _create_adapter(adapter_config)
        registry = registry.with_adapter(adapter)
    return registry


def _create_adapter(
    adapter_config: ObserverProviderAdapterConfig,
) -> LocalObserverProviderAdapter:
    if adapter_config.adapter_kind != "local":
        raise ObserverProviderRegistryBuildError(
            f"unsupported observer provider adapter kind: {adapter_config.adapter_kind}"
        )

    return LocalObserverProviderAdapter(
        provider_id=adapter_config.provider_id,
        observer_name=adapter_config.observer_name,
        model=adapter_config.model or "local-deterministic-v0",
    )
