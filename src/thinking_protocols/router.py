from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

from thinking_protocols.protocols import Protocol


RoutingAction = Literal["direct_answer", "run_protocol", "request_input", "blocked"]


@dataclass(frozen=True, slots=True)
class RoutingRequest:
    explicit_protocol: str | None = None
    desired_artifact: str | None = None
    primary_role: str | None = None
    available_artifacts: frozenset[str] = frozenset()
    available_capabilities: frozenset[str] = frozenset()
    allow_iterative: bool = False
    complexity: Literal["simple", "complex"] = "simple"


@dataclass(frozen=True, slots=True)
class RoutingDecision:
    action: RoutingAction
    protocol_ids: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()
    missing_capabilities: tuple[str, ...] = ()


def route_request(
    request: RoutingRequest, protocols: Iterable[Protocol]
) -> RoutingDecision:
    available = tuple(sorted(protocols, key=_protocol_id))

    if request.explicit_protocol is not None:
        target = next(
            (
                protocol
                for protocol in available
                if _protocol_id(protocol) == request.explicit_protocol
            ),
            None,
        )
        if target is None:
            return RoutingDecision(
                action="blocked", reason_codes=("UNKNOWN_EXPLICIT_PROTOCOL",)
            )
        selected, prerequisite_reason = _add_one_prerequisite(
            target, available, request.available_artifacts
        )
        if isinstance(selected, RoutingDecision):
            return selected
        reasons = ("EXPLICIT_PROTOCOL",) + prerequisite_reason
        return _apply_requirements(request, selected, reasons)

    if request.complexity == "simple" and request.desired_artifact is None:
        return RoutingDecision(
            action="direct_answer", reason_codes=("SIMPLE_DIRECT_ANSWER",)
        )

    if request.desired_artifact in request.available_artifacts:
        return RoutingDecision(
            action="direct_answer", reason_codes=("ARTIFACT_ALREADY_AVAILABLE",)
        )

    target: Protocol | None = None
    reasons: tuple[str, ...] = ()
    if request.desired_artifact is not None:
        producers = tuple(
            protocol
            for protocol in available
            if request.desired_artifact in protocol.metadata["produces"]
        )
        selection = _select_artifact_producer(producers)
        if isinstance(selection, RoutingDecision):
            return selection
        if selection is None:
            return RoutingDecision(
                action="blocked", reason_codes=("NO_ARTIFACT_PRODUCER",)
            )
        target, used_priority = selection
        reasons = ("EXACT_ARTIFACT_PRODUCER",)
        if used_priority:
            reasons += ("HIGHEST_ROUTING_PRIORITY",)
    elif request.primary_role is not None:
        role_matches = tuple(
            protocol
            for protocol in available
            if protocol.metadata["epistemic_role"]["primary"] == request.primary_role
        )
        if not role_matches:
            return RoutingDecision(
                action="direct_answer", reason_codes=("NO_PROTOCOL_MATCH",)
            )
        target = role_matches[0]
        reasons = ("PRIMARY_ROLE_MATCH",)
        if len(role_matches) > 1:
            reasons += ("ROLE_TIE_LEXICOGRAPHIC",)
    else:
        return RoutingDecision(
            action="direct_answer", reason_codes=("DIRECT_ANSWER_DEFAULT",)
        )

    selected, prerequisite_reason = _add_one_prerequisite(
        target, available, request.available_artifacts
    )
    if isinstance(selected, RoutingDecision):
        return selected
    return _apply_requirements(request, selected, reasons + prerequisite_reason)


def _add_one_prerequisite(
    target: Protocol,
    protocols: tuple[Protocol, ...],
    available_artifacts: frozenset[str],
) -> tuple[tuple[Protocol, ...] | RoutingDecision, tuple[str, ...]]:
    missing_artifacts = sorted(
        set(target.metadata["consumes"]) - set(available_artifacts)
    )
    for artifact in missing_artifacts:
        producers = tuple(
            protocol
            for protocol in protocols
            if artifact in protocol.metadata["produces"]
            and _protocol_id(protocol) != _protocol_id(target)
        )
        if not producers:
            continue
        selection = _select_artifact_producer(producers)
        if isinstance(selection, RoutingDecision):
            return (
                RoutingDecision(
                    action="blocked",
                    reason_codes=("AMBIGUOUS_PREREQUISITE_PRODUCER",),
                ),
                (),
            )
        if selection is not None:
            prerequisite, _used_priority = selection
            return (prerequisite, target), ("ONE_PREREQUISITE_ADDED",)
    return (target,), ()


def _select_artifact_producer(
    producers: tuple[Protocol, ...],
) -> tuple[Protocol, bool] | RoutingDecision | None:
    if not producers:
        return None
    if len(producers) == 1:
        return producers[0], False

    highest = max(_routing_priority(protocol) for protocol in producers)
    highest_producers = tuple(
        protocol
        for protocol in producers
        if _routing_priority(protocol) == highest
    )
    if len(highest_producers) != 1:
        return RoutingDecision(
            action="blocked",
            reason_codes=("AMBIGUOUS_ARTIFACT_PRODUCER",),
        )
    return highest_producers[0], True


def _apply_requirements(
    request: RoutingRequest,
    selected: tuple[Protocol, ...],
    reasons: tuple[str, ...],
) -> RoutingDecision:
    protocol_ids = tuple(_protocol_id(protocol) for protocol in selected)
    required_capabilities = {
        capability
        for protocol in selected
        for capability in protocol.metadata["capabilities"]["required"]
    }
    missing = tuple(sorted(required_capabilities - set(request.available_capabilities)))
    if missing:
        return RoutingDecision(
            action="blocked",
            protocol_ids=protocol_ids,
            reason_codes=reasons + ("MISSING_REQUIRED_CAPABILITY",),
            missing_capabilities=missing,
        )

    if not request.allow_iterative and any(
        protocol.metadata["interaction"]["mode"] == "iterative"
        for protocol in selected
    ):
        return RoutingDecision(
            action="request_input",
            protocol_ids=protocol_ids,
            reason_codes=reasons + ("ITERATIVE_CONSENT_REQUIRED",),
        )

    return RoutingDecision(
        action="run_protocol",
        protocol_ids=protocol_ids,
        reason_codes=reasons,
    )


def _protocol_id(protocol: Protocol) -> str:
    return str(protocol.metadata["id"])


def _routing_priority(protocol: Protocol) -> int:
    return int(protocol.metadata.get("routing_priority", 0))
