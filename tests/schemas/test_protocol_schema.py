import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource


ROOT = Path(__file__).parents[2]
SCHEMA_PATH = ROOT / "schemas" / "protocol.schema.json"
CAPABILITY_SCHEMA_PATH = ROOT / "schemas" / "capability.schema.json"
FIXTURES = ROOT / "tests" / "fixtures" / "protocols"


def load_frontmatter(path: Path) -> dict[str, object]:
    source = path.read_text(encoding="utf-8")
    assert source.startswith("---\n")
    frontmatter, _body = source[4:].split("\n---\n", maxsplit=1)
    metadata = yaml.safe_load(frontmatter)
    assert isinstance(metadata, dict)
    return metadata


def load_validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    capability_schema = json.loads(CAPABILITY_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator.check_schema(capability_schema)
    registry = Registry().with_resource(
        capability_schema["$id"], Resource.from_contents(capability_schema)
    )
    return Draft202012Validator(schema, registry=registry)


def test_valid_protocol_frontmatter_matches_schema() -> None:
    load_validator().validate(load_frontmatter(FIXTURES / "valid.md"))


def test_iterative_protocol_requires_a_stop_condition() -> None:
    with pytest.raises(ValidationError):
        load_validator().validate(load_frontmatter(FIXTURES / "invalid_iterative.md"))


def test_protocol_capabilities_use_the_canonical_vocabulary() -> None:
    metadata = load_frontmatter(FIXTURES / "valid.md")
    metadata["capabilities"]["required"] = ["web.fetch"]

    with pytest.raises(ValidationError):
        load_validator().validate(metadata)
