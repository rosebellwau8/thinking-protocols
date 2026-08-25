import json
from pathlib import Path

from jsonschema import Draft202012Validator
import yaml

from thinking_protocols.protocols import load_protocol
from thinking_protocols.validation import validate_repository


ROOT = Path(__file__).parents[1]
PROTOCOL_ROOT = ROOT / "protocols"
PILOT_IDS = {
    "socratic-questioning",
    "fact-checking",
    "steelman-both-sides",
    "minimum-experiment",
}
REQUIRED_EVAL_CATEGORIES = {
    "should_trigger",
    "should_not_trigger",
    "missing_input",
    "early_stop",
    "unsafe_or_sensitive",
}


def pilot_paths() -> list[Path]:
    return sorted(
        path
        for path in PROTOCOL_ROOT.glob("*/PROTOCOL.md")
        if not path.parent.name.startswith("_")
    )


def test_repository_contains_exactly_the_four_valid_pilots() -> None:
    protocols = [load_protocol(path) for path in pilot_paths()]

    assert {protocol.metadata["id"] for protocol in protocols} == PILOT_IDS
    assert validate_repository(ROOT).is_valid


def test_pilot_evals_have_valid_structure_and_required_categories() -> None:
    schema = json.loads(
        (ROOT / "schemas" / "evals.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)

    for path in pilot_paths():
        protocol_id = path.parent.name
        evals_path = path.parent / "evals.yaml"
        evals = yaml.safe_load(evals_path.read_text(encoding="utf-8"))
        validator.validate(evals)
        categories = {case["category"] for case in evals["cases"]}
        assert evals["protocol_id"] == protocol_id
        assert REQUIRED_EVAL_CATEGORIES <= categories
        if protocol_id == "fact-checking":
            assert "missing_required_capability" in categories


def test_each_pilot_example_matches_its_produced_artifact_schema() -> None:
    for path in pilot_paths():
        protocol = load_protocol(path)
        produced = protocol.metadata["produces"]
        assert len(produced) == 1
        artifact = produced[0]
        schema = json.loads(
            (ROOT / "schemas" / "artifacts" / f"{artifact}.schema.json").read_text(
                encoding="utf-8"
            )
        )
        examples = sorted((path.parent / "examples").glob("*.json"))
        assert len(examples) == 1
        instance = json.loads(examples[0].read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(instance)
