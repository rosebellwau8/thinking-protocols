from copy import deepcopy
from pathlib import Path
import shutil

import yaml

from thinking_protocols.validation import validate_repository


PROJECT_ROOT = Path(__file__).parents[1]
KNOWN_ARTIFACTS = (
    "clarified_problem.v1",
    "claim_set.v1",
    "verified_claims.v1",
    "option_set.v1",
    "decision_context.v1",
    "decision_memo.v1",
    "experiment_plan.v1",
)


def base_metadata(protocol_id: str = "example-protocol") -> dict[str, object]:
    return {
        "id": protocol_id,
        "version": "0.1.0",
        "lifecycle": "draft",
        "source_category": "validation_fixture",
        "epistemic_role": {"primary": "clarify", "secondary": []},
        "interaction": {"mode": "one_shot"},
        "state": {"required": False},
        "capabilities": {
            "required": ["web.search"],
            "optional": ["files.read"],
            "on_missing": "block",
        },
        "inputs": {"required": ["user_request"], "optional": []},
        "consumes": ["option_set.v1"],
        "produces": ["clarified_problem.v1"],
        "phases": [{"id": "assess", "objective": "Assess the request."}],
        "stop_conditions": ["The output contract is satisfied."],
        "use_when": ["The request needs clarification."],
        "avoid_when": ["The request is already precise."],
        "safety": ["Do not request hidden chain-of-thought."],
        "source": {"relationship": "original", "references": []},
    }


def make_repository(tmp_path: Path) -> Path:
    root = tmp_path / "repository"
    artifact_dir = root / "schemas" / "artifacts"
    artifact_dir.mkdir(parents=True)
    shutil.copy(PROJECT_ROOT / "schemas" / "protocol.schema.json", root / "schemas")
    shutil.copy(PROJECT_ROOT / "schemas" / "capability.schema.json", root / "schemas")
    for artifact in KNOWN_ARTIFACTS:
        (artifact_dir / f"{artifact}.schema.json").write_text("{}", encoding="utf-8")
    return root


def add_protocol(root: Path, directory: str, metadata: dict[str, object]) -> Path:
    path = root / "protocols" / directory / "PROTOCOL.md"
    path.parent.mkdir(parents=True)
    frontmatter = yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True)
    path.write_text(f"---\n{frontmatter}---\n\n# Procedure\n", encoding="utf-8")
    return path


def issue_codes(root: Path) -> set[str]:
    return {issue.code for issue in validate_repository(root).issues}


def test_valid_protocol_repository(tmp_path: Path) -> None:
    root = make_repository(tmp_path)
    add_protocol(root, "example", base_metadata())

    result = validate_repository(root)

    assert result.is_valid
    assert result.issues == ()


def test_protocol_schema_error_has_stable_path(tmp_path: Path) -> None:
    root = make_repository(tmp_path)
    metadata = base_metadata()
    metadata["version"] = "not-semver"
    add_protocol(root, "example", metadata)

    result = validate_repository(root)

    issue = next(issue for issue in result.issues if issue.code == "PROTOCOL_SCHEMA_ERROR")
    assert issue.path == "protocols/example/PROTOCOL.md::metadata.version"


def test_unknown_consumed_artifact_is_reported(tmp_path: Path) -> None:
    root = make_repository(tmp_path)
    metadata = base_metadata()
    metadata["consumes"] = ["missing_input.v1"]
    add_protocol(root, "example", metadata)

    assert "UNKNOWN_CONSUMED_ARTIFACT" in issue_codes(root)


def test_unknown_produced_artifact_is_reported(tmp_path: Path) -> None:
    root = make_repository(tmp_path)
    metadata = base_metadata()
    metadata["produces"] = ["missing_output.v1"]
    add_protocol(root, "example", metadata)

    assert "UNKNOWN_PRODUCED_ARTIFACT" in issue_codes(root)


def test_unknown_capability_is_reported(tmp_path: Path) -> None:
    root = make_repository(tmp_path)
    metadata = base_metadata()
    metadata["capabilities"] = {
        "required": ["web.fetch"],
        "optional": [],
        "on_missing": "block",
    }
    add_protocol(root, "example", metadata)

    assert "UNKNOWN_CAPABILITY" in issue_codes(root)


def test_duplicate_protocol_id_is_reported(tmp_path: Path) -> None:
    root = make_repository(tmp_path)
    add_protocol(root, "first", base_metadata("same-id"))
    add_protocol(root, "second", base_metadata("same-id"))

    assert "DUPLICATE_PROTOCOL_ID" in issue_codes(root)


def test_duplicate_producer_without_priority_is_ambiguous(tmp_path: Path) -> None:
    root = make_repository(tmp_path)
    add_protocol(root, "first", base_metadata("first-producer"))
    add_protocol(root, "second", base_metadata("second-producer"))

    assert "AMBIGUOUS_ARTIFACT_PRODUCER" in issue_codes(root)


def test_unique_highest_routing_priority_resolves_duplicate_producer(tmp_path: Path) -> None:
    root = make_repository(tmp_path)
    first = deepcopy(base_metadata("first-producer"))
    first["routing_priority"] = 10
    second = deepcopy(base_metadata("second-producer"))
    second["routing_priority"] = 5
    add_protocol(root, "first", first)
    add_protocol(root, "second", second)

    assert "AMBIGUOUS_ARTIFACT_PRODUCER" not in issue_codes(root)


def test_explicit_priority_beats_an_omitted_zero_priority(tmp_path: Path) -> None:
    root = make_repository(tmp_path)
    preferred = deepcopy(base_metadata("preferred-producer"))
    preferred["routing_priority"] = 1
    add_protocol(root, "preferred", preferred)
    add_protocol(root, "default", base_metadata("default-producer"))

    assert "AMBIGUOUS_ARTIFACT_PRODUCER" not in issue_codes(root)


def test_equal_highest_routing_priorities_remain_ambiguous(tmp_path: Path) -> None:
    root = make_repository(tmp_path)
    first = deepcopy(base_metadata("first-producer"))
    first["routing_priority"] = 10
    second = deepcopy(base_metadata("second-producer"))
    second["routing_priority"] = 10
    add_protocol(root, "first", first)
    add_protocol(root, "second", second)

    assert "AMBIGUOUS_ARTIFACT_PRODUCER" in issue_codes(root)


def test_malformed_evals_are_reported_structurally(tmp_path: Path) -> None:
    root = make_repository(tmp_path)
    shutil.copy(PROJECT_ROOT / "schemas" / "evals.schema.json", root / "schemas")
    protocol_path = add_protocol(root, "example", base_metadata())
    (protocol_path.parent / "evals.yaml").write_text(
        "protocol_id: example-protocol\ncases:\n  - category: should_trigger\n",
        encoding="utf-8",
    )

    assert "EVALS_SCHEMA_ERROR" in issue_codes(root)
