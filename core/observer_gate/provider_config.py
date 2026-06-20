"""Configuration models for observer provider adapters.

This module defines configuration data only. It does not create adapters, call
external providers, call Fusion, or execute tasks.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ObserverProviderAdapterConfig:
    """Configuration for one observer provider adapter."""

    provider_id: str
    observer_name: str
    enabled: bool = False
    adapter_kind: str = "stub"
    model: str | None = None


@dataclass(frozen=True)
class ObserverProviderConfig:
    """Configuration collection for observer provider adapters."""

    adapters: tuple[ObserverProviderAdapterConfig, ...] = ()

    def provider_ids(self) -> tuple[str, ...]:
        """Return configured provider IDs in stable order."""
        return tuple(adapter.provider_id for adapter in self.adapters)

    def enabled_provider_ids(self) -> tuple[str, ...]:
        """Return enabled provider IDs in stable order."""
        return tuple(
            adapter.provider_id for adapter in self.adapters if adapter.enabled
        )

    def enabled_configs(self) -> tuple[ObserverProviderAdapterConfig, ...]:
        """Return enabled adapter configs in stable order."""
        return tuple(adapter for adapter in self.adapters if adapter.enabled)

    def get(self, provider_id: str) -> ObserverProviderAdapterConfig | None:
        """Return adapter config by provider ID, if configured."""
        for adapter in self.adapters:
            if adapter.provider_id == provider_id:
                return adapter
        return None

    def require(self, provider_id: str) -> ObserverProviderAdapterConfig:
        """Return adapter config or raise a clear lookup error."""
        adapter = self.get(provider_id)
        if adapter is None:
            raise KeyError(f"Observer provider adapter config not found: {provider_id}")
        return adapter

    def with_adapter_config(
        self,
        adapter_config: ObserverProviderAdapterConfig,
    ) -> ObserverProviderConfig:
        """Return a new config with this adapter config added or replaced."""
        adapters = tuple(
            adapter
            for adapter in self.adapters
            if adapter.provider_id != adapter_config.provider_id
        )
        return ObserverProviderConfig(adapters=(*adapters, adapter_config))


def empty_observer_provider_config() -> ObserverProviderConfig:
    """Return an empty observer provider adapter config."""
    return ObserverProviderConfig()
