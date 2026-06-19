"""Provider adapter interfaces for observer execution boundaries.

This module defines types only. It does not call external providers, Fusion, or
any provider registry.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class ObserverProviderRequest:
    """A request that can be passed to a future observer provider adapter."""

    task_id: str
    task_type: str
    prompt: str
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ObserverProviderResponse:
    """A successful response from an observer provider adapter."""

    provider_id: str
    observer_name: str
    output: str
    model: str | None = None


@dataclass(frozen=True)
class ObserverProviderError:
    """A structured provider adapter failure without raising adapter internals."""

    provider_id: str
    observer_name: str
    reason: str
    retryable: bool = False


ObserverProviderResult = ObserverProviderResponse | ObserverProviderError


class ObserverProviderAdapter(Protocol):
    """Protocol implemented by future observer provider adapters."""

    @property
    def provider_id(self) -> str:
        """Stable adapter identifier, such as local, openai, claude, or fusion."""

    @property
    def observer_name(self) -> str:
        """Human-facing observer name used in routing and reports."""

    def observe(self, request: ObserverProviderRequest) -> ObserverProviderResult:
        """Return an observer result for the request.

        Implementations must keep external calls behind explicit configuration.
        """
