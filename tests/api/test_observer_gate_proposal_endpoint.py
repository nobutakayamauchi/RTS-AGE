import pytest

from api.models.observer_gate import ObserverGateProposalRequest
from api.routes import propose_observer_gate
from core.observer_gate.entrypoint import OBSERVER_GATE_ENABLED_ENV


@pytest.mark.asyncio
async def test_observer_gate_proposal_endpoint_defaults_to_disabled(monkeypatch):
    monkeypatch.delenv(OBSERVER_GATE_ENABLED_ENV, raising=False)
    request = ObserverGateProposalRequest(
        task_id="1",
        text="顧客納品用の公開営業LPをレビューして",
    )

    response = await propose_observer_gate(request)

    assert response.mode == "proposal"
    assert response.observer_gate_enabled is False
    assert response.selected_observer == "default"
    assert response.should_use_fusion is False
    assert response.score == 0
    assert response.task_type == "observer_gate_disabled"


@pytest.mark.asyncio
async def test_observer_gate_proposal_endpoint_routes_when_enabled(monkeypatch):
    monkeypatch.setenv(OBSERVER_GATE_ENABLED_ENV, "true")
    request = ObserverGateProposalRequest(
        task_id="2",
        text="顧客納品用の公開営業LPをレビューして",
    )

    response = await propose_observer_gate(request)

    assert response.mode == "proposal"
    assert response.observer_gate_enabled is True
    assert response.selected_observer == "fusion"
    assert response.should_use_fusion is True
    assert response.score >= 7


@pytest.mark.asyncio
async def test_observer_gate_proposal_endpoint_respects_blocklist(monkeypatch):
    monkeypatch.setenv(OBSERVER_GATE_ENABLED_ENV, "true")
    request = ObserverGateProposalRequest(
        task_id="3",
        text="X投稿を10個作って",
    )

    response = await propose_observer_gate(request)

    assert response.mode == "proposal"
    assert response.observer_gate_enabled is True
    assert response.selected_observer == "default"
    assert response.should_use_fusion is False
    assert response.score == 0
