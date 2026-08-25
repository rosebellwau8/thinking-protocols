from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator

from thinking_protocols.errors import ProtocolParseError
from thinking_protocols.protocols import Protocol, load_protocol


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
    validator = Draft202012Validator(protocol_schema)
    known_capabilities = set(capability_schema.get("examples", ()))
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
                    code="PROTOCOL_SCHEMA_ERROR",
                    path=f"{relative_path}::{_metadata_path(error.absolute_path)}",
                    message=error.message,
                )
            )
        if not schema_errors:
            records.append(_ProtocolRecord(protocol, relative_path))

    issues.extend(
        _cross_reference_issues(records, known_artifacts, known_capabilities)
    )
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


def _cross_reference_issues(
    records: list[_ProtocolRecord],
    known_artifacts: set[str],
    known_capabilities: set[str],
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

        capabilities = metadata["capabilities"]
        for field in ("required", "optional"):
            for index, capability in enumerate(capabilities[field]):
                if capability not in known_capabilities:
                    issues.append(
                        ValidationIssue(
                            code="UNKNOWN_CAPABILITY",
                            path=(
                                f"{record.relative_path}::"
                                f"metadata.capabilities.{field}[{index}]"
                            ),
                            message=f"Unknown capability: {capability}",
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
