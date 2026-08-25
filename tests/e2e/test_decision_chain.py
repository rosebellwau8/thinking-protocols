from pathlib import Path

from thinking_protocols.protocols import load_protocol
from thinking_protocols.router import RoutingRequest, route_request


ROOT = Path(__file__).parents[2]
PROTOCOLS = tuple(
    load_protocol(path)
    for path in sorted((ROOT / "protocols").glob("*/PROTOCOL.md"))
    if not path.parent.name.startswith("_")
)


def test_artifact_driven_decision_chain_selects_only_the_next_producer() -> None:
    stages = (
        ("clarified_problem.v1", "socratic-questioning"),
        ("verified_claims.v1", "fact-checking"),
        ("decision_memo.v1", "steelman-both-sides"),
        ("experiment_plan.v1", "minimum-experiment"),
    )
    available: set[str] = set()

    for artifact, expected_protocol in stages:
        decision = route_request(
            RoutingRequest(
                desired_artifact=artifact,
                available_artifacts=frozenset(available),
                available_capabilities=frozenset({"web.search"}),
                allow_iterative=True,
                complexity="complex",
            ),
            PROTOCOLS,
        )
        assert decision.action == "run_protocol"
        assert decision.protocol_ids == (expected_protocol,)
        available.add(artifact)
