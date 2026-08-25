import json
from pathlib import Path

import jsonschema
import pytest


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
