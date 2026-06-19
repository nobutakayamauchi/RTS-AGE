"""Pydantic models for observer gate proposal endpoints."""

from typing import Literal

from pydantic import BaseModel, Field


class ObserverGateProposalRequest(BaseModel):
    task_id: str = Field(min_length=1)
    text: str = Field(min_length=1)


class ObserverGateProposalResponse(BaseModel):
    mode: Literal["proposal"] = "proposal"
    observer_gate_enabled: bool
    task_id: str
    task_type: str
    selected_observer: str
    score: int
    should_use_fusion: bool
    reasons: list[str]
