from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
import yaml

from thinking_protocols.errors import ProtocolParseError
from thinking_protocols.protocols import Protocol, load_protocol


BASE_EVAL_CATEGORIES = frozenset(
    {
        "should_trigger",
        "should_not_trigger",
        "missing_input",
        "early_stop",
        "unsafe_or_sensitive",
    }
)


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    path: str
    message: str


@dataclass(frozen=True, slots=True)
class ValidationResult:
    issues: tuple[ValidationIssue, ...]

    @property
    def is_valid(self) -> bool:
        return not self.issues

    @property
    def valid(self) -> bool:
        return self.is_valid


@dataclass(frozen=True, slots=True)
class _ProtocolRecord:
    protocol: Protocol
    relative_path: str


def validate_repository(root: Path | str) -> ValidationResult:
    repository_root = Path(root)
    issues: list[ValidationIssue] = []

    protocol_schema = _load_json(repository_root / "schemas" / "protocol.schema.json")
    capability_schema = _load_json(repository_root / "schemas" / "capability.schema.json")
    registry = Registry().with_resource(
        capability_schema["$id"], Resource.from_contents(capability_schema)
    )
    validator = Draft202012Validator(protocol_schema, registry=registry)
    known_artifacts = _artifact_names(repository_root / "schemas" / "artifacts")

    records: list[_ProtocolRecord] = []
    for path in _protocol_paths(repository_root):
        relative_path = path.relative_to(repository_root).as_posix()
        try:
            protocol = load_protocol(path)
        except ProtocolParseError as error:
            issues.append(
                ValidationIssue(
                    code="PROTOCOL_PARSE_ERROR",
                    path=relative_path,
                    message=str(error),
                )
            )
            continue

        schema_errors = sorted(
            validator.iter_errors(protocol.metadata),
            key=lambda error: tuple(str(part) for part in error.absolute_path),
        )
        for error in schema_errors:
            issues.append(
                ValidationIssue(
                    code=_schema_issue_code(error),
                    path=f"{relative_path}::{_metadata_path(error.absolute_path)}",
                    message=error.message,
                )
            )
        if not schema_errors:
            records.append(_ProtocolRecord(protocol, relative_path))

    issues.extend(
        _cross_reference_issues(records, known_artifacts)
    )
    evals_schema_path = repository_root / "schemas" / "evals.schema.json"
    if evals_schema_path.is_file():
        issues.extend(_eval_issues(records, _load_json(evals_schema_path)))
    return ValidationResult(tuple(sorted(issues, key=_issue_sort_key)))


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _protocol_paths(root: Path) -> list[Path]:
    protocol_root = root / "protocols"
    if not protocol_root.exists():
        return []
    return sorted(
        path
        for path in protocol_root.glob("*/PROTOCOL.md")
        if not path.parent.name.startswith("_")
    )


def _artifact_names(schema_dir: Path) -> set[str]:
    if not schema_dir.exists():
        return set()
    return {
        path.name.removesuffix(".schema.json")
        for path in schema_dir.glob("*.schema.json")
        if not path.name.startswith("envelope.")
    }


def _metadata_path(parts: Iterable[object]) -> str:
    path = "metadata"
    for part in parts:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f".{part}"
    return path


def _schema_issue_code(error: Any) -> str:
    path = list(error.absolute_path)
    if (
        error.validator == "enum"
        and len(path) >= 3
        and path[0] == "capabilities"
        and path[1] in {"required", "optional"}
    ):
        return "UNKNOWN_CAPABILITY"
    return "PROTOCOL_SCHEMA_ERROR"


def _cross_reference_issues(
    records: list[_ProtocolRecord],
    known_artifacts: set[str],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    ids: dict[str, list[_ProtocolRecord]] = defaultdict(list)
    producers: dict[str, list[_ProtocolRecord]] = defaultdict(list)

    for record in records:
        metadata = record.protocol.metadata
        ids[metadata["id"]].append(record)

        for field, code in (
            ("consumes", "UNKNOWN_CONSUMED_ARTIFACT"),
            ("produces", "UNKNOWN_PRODUCED_ARTIFACT"),
        ):
            for index, artifact in enumerate(metadata[field]):
                if artifact not in known_artifacts:
                    issues.append(
                        ValidationIssue(
                            code=code,
                            path=f"{record.relative_path}::metadata.{field}[{index}]",
                            message=f"Unknown Artifact contract: {artifact}",
                        )
                    )

        for artifact in metadata["produces"]:
            if artifact in known_artifacts:
                producers[artifact].append(record)

    for protocol_id, duplicate_records in sorted(ids.items()):
        for duplicate in duplicate_records[1:]:
            issues.append(
                ValidationIssue(
                    code="DUPLICATE_PROTOCOL_ID",
                    path=f"{duplicate.relative_path}::metadata.id",
                    message=f"Duplicate Protocol id: {protocol_id}",
                )
            )

    for artifact, producer_records in sorted(producers.items()):
        if len(producer_records) < 2:
            continue
        priorities = [
            int(record.protocol.metadata.get("routing_priority", 0))
            for record in producer_records
        ]
        highest = max(priorities)
        if highest == 0 or priorities.count(highest) > 1:
            producer_ids = sorted(
                str(record.protocol.metadata["id"]) for record in producer_records
            )
            issues.append(
                ValidationIssue(
                    code="AMBIGUOUS_ARTIFACT_PRODUCER",
                    path=f"artifacts/{artifact}",
                    message=(
                        f"Artifact has no unique highest-priority producer: "
                        f"{', '.join(producer_ids)}"
                    ),
                )
            )

    return issues


def _issue_sort_key(issue: ValidationIssue) -> tuple[str, str, str]:
    return issue.path, issue.code, issue.message


def _eval_issues(
    records: list[_ProtocolRecord], evals_schema: dict[str, Any]
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    validator = Draft202012Validator(evals_schema)
    for record in records:
        evals_path = record.protocol.path.parent / "evals.yaml"
        relative_path = f"{record.relative_path.rsplit('/', 1)[0]}/evals.yaml"
        if not evals_path.is_file():
            issues.append(
                ValidationIssue(
                    code="MISSING_EVALS",
                    path=relative_path,
                    message="Protocol is missing evals.yaml",
                )
            )
            continue
        try:
            evals = yaml.safe_load(evals_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as error:
            issues.append(
                ValidationIssue(
                    code="EVALS_PARSE_ERROR",
                    path=relative_path,
                    message=f"Could not parse evals.yaml: {error}",
                )
            )
            continue
        schema_errors = sorted(
            validator.iter_errors(evals),
            key=lambda error: tuple(str(part) for part in error.absolute_path),
        )
        for error in schema_errors:
            issues.append(
                ValidationIssue(
                    code="EVALS_SCHEMA_ERROR",
                    path=f"{relative_path}::{_eval_path(error.absolute_path)}",
                    message=error.message,
                )
            )
        if not schema_errors:
            if evals["protocol_id"] != record.protocol.metadata["id"]:
                issues.append(
                    ValidationIssue(
                        code="EVALS_PROTOCOL_MISMATCH",
                        path=f"{relative_path}::protocol_id",
                        message="evals.yaml protocol_id does not match Protocol id",
                    )
                )
            required_categories = set(BASE_EVAL_CATEGORIES)
            metadata = record.protocol.metadata
            if metadata["capabilities"]["required"]:
                required_categories.add("missing_required_capability")
            roles = {
                metadata["epistemic_role"]["primary"],
                *metadata["epistemic_role"]["secondary"],
            }
            if "research" in roles:
                required_categories.add("evidence_conflict")
            actual_categories = {case["category"] for case in evals["cases"]}
            for category in sorted(required_categories - actual_categories):
                issues.append(
                    ValidationIssue(
                        code="MISSING_EVAL_CATEGORY",
                        path=f"{relative_path}::evals.cases",
                        message=f"Protocol evals are missing category: {category}",
                    )
                )
    return issues


def _eval_path(parts: Iterable[object]) -> str:
    path = "evals"
    for part in parts:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f".{part}"
    return path
