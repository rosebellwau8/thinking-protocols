import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError


ROOT = Path(__file__).parents[2]
SCHEMA_PATH = ROOT / "schemas" / "evals.schema.json"


def test_evidence_conflict_case_is_a_runnable_behavior() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    document = {
        "protocol_id": "research-protocol",
        "cases": [
            {
                "id": "conflicting_sources",
                "category": "evidence_conflict",
                "input": "Two scope-matched primary sources disagree.",
                "expected": "run_protocol",
            }
        ],
    }

    validator.validate(document)
    document["cases"][0]["expected"] = "blocked"
    with pytest.raises(ValidationError):
        validator.validate(document)
