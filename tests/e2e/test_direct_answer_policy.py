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


@pytest.mark.parametrize(
    "request_text",
    (
        "What is the capital of France?",
        "Format this date as YYYY-MM-DD.",
        "Translate hello into Spanish.",
        "What is 7 plus 8?",
        "Convert this heading to title case.",
        "Define photosynthesis in one sentence.",
        "Alphabetize these three names.",
        "How many minutes are in two hours?",
        "Rewrite this sentence in the passive voice.",
        "Return the first item in this list.",
    ),
)
def test_simple_bounded_requests_stay_direct(request_text: str) -> None:
    assert request_text

    decision = route_request(RoutingRequest(complexity="simple"), PROTOCOLS)

    assert decision.action == "direct_answer"
    assert decision.protocol_ids == ()


@pytest.mark.parametrize(
    "request_text",
    (
        "Explain recursion normally.",
        "Analyze the trade-offs in this design.",
        "This is complex; choose whatever framework you want.",
        "Give me several perspectives on this ordinary question.",
        "Research is not requested; reason from the supplied facts.",
    ),
)
def test_specialized_protocols_are_not_inferred_without_specific_intent(
    request_text: str,
) -> None:
    assert request_text

    decision = route_request(
        RoutingRequest(primary_role="reason", complexity="complex"), PROTOCOLS
    )

    assert decision.action == "direct_answer"
    assert decision.protocol_ids == ()
    assert "AMBIGUOUS_PRIMARY_ROLE" in decision.reason_codes
