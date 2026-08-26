from pathlib import Path

import yaml

from thinking_protocols.protocols import load_protocol
from thinking_protocols.registry import (
    is_registry_current,
    render_registry,
    write_registry,
)


ROOT = Path(__file__).parents[1]


def registry_document() -> dict[str, object]:
    return yaml.safe_load(render_registry(ROOT).decode("utf-8"))


def test_registry_has_one_record_per_protocol_in_id_order() -> None:
    records = registry_document()["protocols"]
    ids = [record["id"] for record in records]

    assert ids == sorted(ids)
    assert len(ids) == len(set(ids)) == 12


def test_registry_records_canonical_metadata_and_effective_priority() -> None:
    records = registry_document()["protocols"]

    for record in records:
        assert record["version"] == "0.1.0"
        assert record["lifecycle"] == "draft"
        assert record["routing_priority"] == 0
        assert record["secondary_roles"] == sorted(record["secondary_roles"])
        assert record["required_capabilities"] == sorted(
            record["required_capabilities"]
        )
        assert record["consumes"] == sorted(record["consumes"])
        assert record["produces"] == sorted(record["produces"])


def test_registry_source_digests_match_canonical_protocols() -> None:
    records = {record["id"]: record for record in registry_document()["protocols"]}

    for path in sorted((ROOT / "protocols").glob("*/PROTOCOL.md")):
        if path.parent.name.startswith("_"):
            continue
        protocol = load_protocol(path)
        assert records[protocol.metadata["id"]]["source_digest"] == protocol.digest


def test_registry_rendering_is_byte_deterministic() -> None:
    assert render_registry(ROOT) == render_registry(ROOT)


def test_stale_generated_registry_is_detected(tmp_path: Path) -> None:
    output = tmp_path / "registry.yaml"
    assert write_registry(ROOT, output)
    assert is_registry_current(ROOT, output)

    output.write_bytes(b"stale\n")

    assert not is_registry_current(ROOT, output)
