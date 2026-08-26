from pathlib import Path

from thinking_protocols.protocols import Protocol, load_protocol
from thinking_protocols.router import RoutingRequest, route_request


ROOT = Path(__file__).parents[1]


def pilot_protocols() -> tuple[Protocol, ...]:
    return tuple(
        load_protocol(path)
        for path in sorted((ROOT / "protocols").glob("*/PROTOCOL.md"))
        if not path.parent.name.startswith("_")
    )


def synthetic_protocol(
    protocol_id: str,
    *,
    produces: tuple[str, ...] = (),
    consumes: tuple[str, ...] = (),
    primary_role: str = "reason",
    priority: int = 0,
    required_capabilities: tuple[str, ...] = (),
    interaction_mode: str = "one_shot",
) -> Protocol:
    metadata = {
        "id": protocol_id,
        "routing_priority": priority,
        "epistemic_role": {"primary": primary_role, "secondary": []},
        "interaction": {"mode": interaction_mode},
        "capabilities": {"required": list(required_capabilities)},
        "consumes": list(consumes),
        "produces": list(produces),
    }
    return Protocol(Path(f"{protocol_id}.md"), metadata, "Procedure", "0" * 64)


def test_simple_question_returns_direct_answer() -> None:
    decision = route_request(RoutingRequest(), pilot_protocols())

    assert decision.action == "direct_answer"
    assert decision.protocol_ids == ()


def test_explicit_protocol_request_is_honored() -> None:
    request = RoutingRequest(
        explicit_protocol="fact-checking",
        available_capabilities=frozenset({"web.search"}),
    )

    decision = route_request(request, pilot_protocols())

    assert decision.action == "run_protocol"
    assert decision.protocol_ids == ("fact-checking",)


def test_desired_artifact_selects_its_producer() -> None:
    request = RoutingRequest(
        desired_artifact="clarified_problem.v1",
        complexity="complex",
        allow_iterative=True,
    )

    decision = route_request(request, pilot_protocols())

    assert decision.action == "run_protocol"
    assert decision.protocol_ids == ("socratic-questioning",)


def test_unique_highest_priority_selects_exact_artifact_producer() -> None:
    protocols = (
        synthetic_protocol("lower", produces=("result.v1",), priority=1),
        synthetic_protocol("higher", produces=("result.v1",), priority=10),
    )
    request = RoutingRequest(desired_artifact="result.v1", complexity="complex")

    decision = route_request(request, protocols)

    assert decision.action == "run_protocol"
    assert decision.protocol_ids == ("higher",)
    assert "HIGHEST_ROUTING_PRIORITY" in decision.reason_codes


def test_tied_highest_artifact_producers_are_blocked() -> None:
    protocols = (
        synthetic_protocol("alpha", produces=("result.v1",), priority=10),
        synthetic_protocol("beta", produces=("result.v1",), priority=10),
    )
    request = RoutingRequest(desired_artifact="result.v1", complexity="complex")

    decision = route_request(request, protocols)

    assert decision.action == "blocked"
    assert decision.protocol_ids == ()
    assert "AMBIGUOUS_ARTIFACT_PRODUCER" in decision.reason_codes


def test_existing_artifact_is_not_reproduced() -> None:
    request = RoutingRequest(
        desired_artifact="verified_claims.v1",
        available_artifacts=frozenset({"verified_claims.v1"}),
        available_capabilities=frozenset({"web.search"}),
        complexity="complex",
    )

    decision = route_request(request, pilot_protocols())

    assert decision.action == "direct_answer"
    assert decision.protocol_ids == ()
    assert "ARTIFACT_ALREADY_AVAILABLE" in decision.reason_codes


def test_only_one_missing_artifact_prerequisite_is_added() -> None:
    protocols = (
        synthetic_protocol("first-input", produces=("first.v1",)),
        synthetic_protocol("second-input", produces=("second.v1",)),
        synthetic_protocol(
            "target",
            produces=("target.v1",),
            consumes=("second.v1", "first.v1"),
        ),
    )
    request = RoutingRequest(desired_artifact="target.v1", complexity="complex")

    decision = route_request(request, protocols)

    assert decision.action == "run_protocol"
    assert decision.protocol_ids == ("first-input", "target")
    assert len(decision.protocol_ids) == 2


def test_missing_required_capability_blocks_without_substitution() -> None:
    request = RoutingRequest(
        desired_artifact="verified_claims.v1",
        complexity="complex",
    )

    decision = route_request(request, pilot_protocols())

    assert decision.action == "blocked"
    assert decision.protocol_ids == ("fact-checking",)
    assert decision.missing_capabilities == ("web.search",)


def test_iterative_protocol_requires_user_consent() -> None:
    request = RoutingRequest(explicit_protocol="socratic-questioning")

    decision = route_request(request, pilot_protocols())

    assert decision.action == "request_input"
    assert decision.protocol_ids == ("socratic-questioning",)
    assert "ITERATIVE_CONSENT_REQUIRED" in decision.reason_codes


def test_primary_role_ties_prefer_direct_answer_to_specialized_guessing() -> None:
    protocols = (
        synthetic_protocol("zeta", primary_role="decide"),
        synthetic_protocol("alpha", primary_role="decide"),
    )
    request = RoutingRequest(primary_role="decide", complexity="complex")

    decision = route_request(request, protocols)

    assert decision.action == "direct_answer"
    assert decision.protocol_ids == ()
    assert "AMBIGUOUS_PRIMARY_ROLE" in decision.reason_codes


def test_no_routing_decision_contains_more_than_two_protocols() -> None:
    requests = (
        RoutingRequest(),
        RoutingRequest(explicit_protocol="fact-checking"),
        RoutingRequest(
            desired_artifact="experiment_plan.v1",
            complexity="complex",
        ),
        RoutingRequest(primary_role="decide", complexity="complex"),
    )

    for request in requests:
        assert len(route_request(request, pilot_protocols()).protocol_ids) <= 2


def test_priority_cannot_override_higher_precedence_or_requirements() -> None:
    explicit = synthetic_protocol("explicit", produces=("result.v1",), priority=0)
    high = synthetic_protocol("high", produces=("result.v1",), priority=100)
    explicit_decision = route_request(
        RoutingRequest(
            explicit_protocol="explicit",
            desired_artifact="result.v1",
            complexity="complex",
        ),
        (explicit, high),
    )
    assert explicit_decision.protocol_ids == ("explicit",)

    direct_decision = route_request(
        RoutingRequest(primary_role="reason", complexity="simple"),
        (high,),
    )
    assert direct_decision.action == "direct_answer"
    assert direct_decision.protocol_ids == ()

    capability_bound = synthetic_protocol(
        "capability-bound",
        produces=("capability_result.v1",),
        priority=100,
        required_capabilities=("web.search",),
    )
    capability_decision = route_request(
        RoutingRequest(
            desired_artifact="capability_result.v1", complexity="complex"
        ),
        (capability_bound,),
    )
    assert capability_decision.action == "blocked"
    assert capability_decision.missing_capabilities == ("web.search",)

    iterative = synthetic_protocol(
        "iterative",
        produces=("iterative_result.v1",),
        priority=100,
        interaction_mode="iterative",
    )
    consent_decision = route_request(
        RoutingRequest(desired_artifact="iterative_result.v1", complexity="complex"),
        (iterative,),
    )
    assert consent_decision.action == "request_input"
    assert "ITERATIVE_CONSENT_REQUIRED" in consent_decision.reason_codes
