import json
from pathlib import Path

from jsonschema import Draft202012Validator
import yaml

from thinking_protocols.protocols import load_protocol
from thinking_protocols.validation import validate_repository


ROOT = Path(__file__).parents[1]
PROTOCOL_ROOT = ROOT / "protocols"
PROTOCOL_IDS = {
    "socratic-questioning",
    "fact-checking",
    "steelman-both-sides",
    "minimum-experiment",
    "dual-layer-explanation",
    "reverse-engineering",
    "horizontal-vertical-analysis",
    "expert-panel",
    "first-principles",
    "cross-domain-transfer",
    "talent-discovery",
    "life-design",
}
REQUIRED_EVAL_CATEGORIES = {
    "should_trigger",
    "should_not_trigger",
    "missing_input",
    "early_stop",
    "unsafe_or_sensitive",
}


def protocol_paths() -> list[Path]:
    return sorted(
        path
        for path in PROTOCOL_ROOT.glob("*/PROTOCOL.md")
        if not path.parent.name.startswith("_")
    )


def test_repository_contains_exactly_the_twelve_valid_protocols() -> None:
    protocols = [load_protocol(path) for path in protocol_paths()]

    assert {protocol.metadata["id"] for protocol in protocols} == PROTOCOL_IDS
    assert validate_repository(ROOT).is_valid


def test_protocol_evals_have_valid_structure_and_required_categories() -> None:
    schema = json.loads(
        (ROOT / "schemas" / "evals.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)

    for path in protocol_paths():
        protocol_id = path.parent.name
        evals_path = path.parent / "evals.yaml"
        evals = yaml.safe_load(evals_path.read_text(encoding="utf-8"))
        validator.validate(evals)
        categories = {case["category"] for case in evals["cases"]}
        assert evals["protocol_id"] == protocol_id
        assert REQUIRED_EVAL_CATEGORIES <= categories
        protocol = load_protocol(path)
        if protocol.metadata["capabilities"]["required"]:
            assert "missing_required_capability" in categories
        roles = {
            protocol.metadata["epistemic_role"]["primary"],
            *protocol.metadata["epistemic_role"]["secondary"],
        }
        if "research" in roles:
            assert "evidence_conflict" in categories


def test_each_protocol_has_an_example_and_artifact_examples_are_valid() -> None:
    for path in protocol_paths():
        protocol = load_protocol(path)
        produced = protocol.metadata["produces"]
        examples = sorted(
            example
            for example in (path.parent / "examples").glob("*")
            if example.is_file()
        )
        assert examples
        if produced:
            assert len(produced) == 1
            artifact = produced[0]
            schema = json.loads(
                (ROOT / "schemas" / "artifacts" / f"{artifact}.schema.json").read_text(
                    encoding="utf-8"
                )
            )
            json_examples = [example for example in examples if example.suffix == ".json"]
            assert len(json_examples) == 1
            instance = json.loads(json_examples[0].read_text(encoding="utf-8"))
            Draft202012Validator(schema).validate(instance)


def test_new_terminal_protocols_do_not_add_artifact_or_persistent_state() -> None:
    new_ids = PROTOCOL_IDS - {
        "socratic-questioning",
        "fact-checking",
        "steelman-both-sides",
        "minimum-experiment",
    }

    for path in protocol_paths():
        protocol = load_protocol(path)
        if protocol.metadata["id"] not in new_ids:
            continue
        assert protocol.metadata["produces"] == []
        assert protocol.metadata["state"].get("lifetime") != "persistent"


def test_research_and_sensitive_protocol_contracts_are_explicit() -> None:
    protocols = {
        protocol.metadata["id"]: protocol
        for protocol in (load_protocol(path) for path in protocol_paths())
    }

    for protocol_id in ("horizontal-vertical-analysis", "cross-domain-transfer"):
        metadata = protocols[protocol_id].metadata
        assert metadata["capabilities"]["required"] == ["web.search"]
        assert metadata["capabilities"]["on_missing"] == "block"

    for protocol_id in ("talent-discovery", "life-design"):
        metadata = protocols[protocol_id].metadata
        assert metadata["interaction"] == {"mode": "iterative", "max_turns": 8}
        assert metadata["state"] == {
            "required": True,
            "lifetime": "conversation",
        }

    explanation = protocols["dual-layer-explanation"].metadata
    assert explanation["interaction"]["mode"] == "one_shot"
    assert explanation["capabilities"]["required"] == []
