from pathlib import Path

from thinking_protocols.protocols import load_protocol
from thinking_protocols.router import RoutingRequest, route_request


ROOT = Path(__file__).parents[2]
PROTOCOLS = tuple(
    load_protocol(path)
    for path in sorted((ROOT / "protocols").glob("*/PROTOCOL.md"))
    if not path.parent.name.startswith("_")
)


def test_verified_claims_without_web_search_blocks_without_substitution() -> None:
    decision = route_request(
        RoutingRequest(desired_artifact="verified_claims.v1", complexity="complex"),
        PROTOCOLS,
    )

    assert decision.action == "blocked"
    assert decision.protocol_ids == ("fact-checking",)
    assert decision.missing_capabilities == ("web.search",)
