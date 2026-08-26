from pathlib import Path

import yaml


ROOT = Path(__file__).parents[1]


def test_governance_and_provenance_files_exist() -> None:
    required = (
        "README.md",
        "NOTICE.md",
        "docs/architecture.md",
        "docs/versioning.md",
        "sources/kazike-12-prompts/source.yaml",
        "sources/kazike-12-prompts/notes.md",
    )

    missing = [path for path in required if not (ROOT / path).is_file()]

    assert not missing, f"Missing governance files: {missing}"


def test_third_party_prompt_body_is_not_stored() -> None:
    assert not (ROOT / "sources/kazike-12-prompts/original.md").exists()


def test_source_record_maps_all_protocols_without_storing_source_text() -> None:
    source_root = ROOT / "sources" / "kazike-12-prompts"
    source = yaml.safe_load((source_root / "source.yaml").read_text(encoding="utf-8"))
    protocol_ids = {
        path.parent.name
        for path in (ROOT / "protocols").glob("*/PROTOCOL.md")
        if not path.parent.name.startswith("_")
    }

    assert source["relationship"] == "inspiration_for_independent_rewrite"
    assert source["rights_status"] == "third_party_not_licensed_by_this_repository"
    assert source["full_text_stored"] is False
    assert set(source["protocol_mappings"]) == protocol_ids
    assert {path.name for path in source_root.iterdir()} == {"notes.md", "source.yaml"}
