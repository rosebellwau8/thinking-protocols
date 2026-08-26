from pathlib import Path

import pytest

from thinking_protocols.protocols import load_protocol
from thinking_protocols.router import RoutingRequest, route_request


ROOT = Path(__file__).parents[2]
PROTOCOLS = tuple(
    load_protocol(path)
    for path in sorted((ROOT / "protocols").glob("*/PROTOCOL.md"))
    if not path.parent.name.startswith("_")
)
NEW_PROTOCOL_IDS = (
    "cross-domain-transfer",
    "dual-layer-explanation",
    "expert-panel",
    "first-principles",
    "horizontal-vertical-analysis",
    "life-design",
    "reverse-engineering",
    "talent-discovery",
)


@pytest.mark.parametrize("protocol_id", NEW_PROTOCOL_IDS)
def test_explicit_new_protocol_requests_are_honored(protocol_id: str) -> None:
    decision = route_request(
        RoutingRequest(
            explicit_protocol=protocol_id,
            available_capabilities=frozenset({"web.search"}),
            allow_iterative=True,
        ),
        PROTOCOLS,
    )

    assert decision.action == "run_protocol"
    assert decision.protocol_ids == (protocol_id,)


@pytest.mark.parametrize(
    "protocol_id", ("horizontal-vertical-analysis", "cross-domain-transfer")
)
def test_research_protocols_block_without_required_search(protocol_id: str) -> None:
    decision = route_request(
        RoutingRequest(explicit_protocol=protocol_id, allow_iterative=True), PROTOCOLS
    )

    assert decision.action == "blocked"
    assert decision.protocol_ids == (protocol_id,)
    assert decision.missing_capabilities == ("web.search",)


@pytest.mark.parametrize("protocol_id", ("talent-discovery", "life-design"))
def test_self_exploration_protocols_require_consent(protocol_id: str) -> None:
    decision = route_request(
        RoutingRequest(explicit_protocol=protocol_id), PROTOCOLS
    )

    assert decision.action == "request_input"
    assert decision.protocol_ids == (protocol_id,)
    assert "ITERATIVE_CONSENT_REQUIRED" in decision.reason_codes
