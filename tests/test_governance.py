from pathlib import Path


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
