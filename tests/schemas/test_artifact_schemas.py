import json
from pathlib import Path

import jsonschema
import pytest
from jsonschema import ValidationError


ROOT = Path(__file__).parents[2]
SCHEMA_DIR = ROOT / "schemas" / "artifacts"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "artifacts"
ARTIFACT_TYPES = (
    "clarified_problem",
    "claim_set",
    "verified_claims",
    "option_set",
    "decision_context",
    "decision_memo",
    "experiment_plan",
)


@pytest.mark.parametrize("artifact_type", ARTIFACT_TYPES)
def test_artifact_fixture_matches_versioned_schema(artifact_type: str) -> None:
    schema_path = SCHEMA_DIR / f"{artifact_type}.v1.schema.json"
    fixture_path = FIXTURE_DIR / f"{artifact_type}.v1.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

    jsonschema.validate(instance=fixture, schema=schema)


@pytest.mark.parametrize("artifact_type", ARTIFACT_TYPES)
def test_artifact_schema_rejects_unknown_top_level_properties(
    artifact_type: str,
) -> None:
    schema = json.loads(
        (SCHEMA_DIR / f"{artifact_type}.v1.schema.json").read_text(encoding="utf-8")
    )
    fixture = json.loads(
        (FIXTURE_DIR / f"{artifact_type}.v1.json").read_text(encoding="utf-8")
    )
    fixture["unexpected"] = True

    with pytest.raises(ValidationError):
        jsonschema.validate(instance=fixture, schema=schema)


@pytest.mark.parametrize("artifact_type", ARTIFACT_TYPES)
def test_artifact_schema_rejects_missing_required_payload_fields(
    artifact_type: str,
) -> None:
    schema = json.loads(
        (SCHEMA_DIR / f"{artifact_type}.v1.schema.json").read_text(encoding="utf-8")
    )
    fixture = json.loads(
        (FIXTURE_DIR / f"{artifact_type}.v1.json").read_text(encoding="utf-8")
    )
    required_field = schema["properties"]["payload"]["required"][0]
    del fixture["payload"][required_field]

    with pytest.raises(ValidationError):
        jsonschema.validate(instance=fixture, schema=schema)


def test_option_set_requires_two_distinct_options() -> None:
    schema = json.loads(
        (SCHEMA_DIR / "option_set.v1.schema.json").read_text(encoding="utf-8")
    )
    fixture = json.loads(
        (FIXTURE_DIR / "option_set.v1.json").read_text(encoding="utf-8")
    )
    fixture["payload"]["options"] = ["Same option", "Same option"]

    with pytest.raises(ValidationError):
        jsonschema.validate(instance=fixture, schema=schema)
