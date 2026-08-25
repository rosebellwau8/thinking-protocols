from pathlib import Path

import yaml

from thinking_protocols.adapters import build_adapter
from thinking_protocols.protocols import load_protocol


ROOT = Path(__file__).parents[1]


def pilot_protocols():
    return [
        load_protocol(path)
        for path in sorted((ROOT / "protocols").glob("*/PROTOCOL.md"))
        if not path.parent.name.startswith("_")
    ]


def frontmatter(source: str) -> dict[str, object]:
    assert source.startswith("---\n")
    raw, _body = source[4:].split("\n---\n", maxsplit=1)
    metadata = yaml.safe_load(raw)
    assert isinstance(metadata, dict)
    return metadata


def test_codex_build_emits_discoverable_skill_per_protocol(tmp_path: Path) -> None:
    output = tmp_path / "codex"

    paths = build_adapter(ROOT, "codex", output)

    assert {path.relative_to(output).as_posix() for path in paths} == {
        "skills/fact-checking/SKILL.md",
        "skills/minimum-experiment/SKILL.md",
        "skills/socratic-questioning/SKILL.md",
        "skills/steelman-both-sides/SKILL.md",
    }
    for protocol in pilot_protocols():
        path = output / "skills" / protocol.metadata["id"] / "SKILL.md"
        source = path.read_text(encoding="utf-8")
        discovery = frontmatter(source)
        assert discovery["name"] == protocol.metadata["id"]
        assert discovery["description"]
        assert discovery["metadata"]["source_version"] == protocol.metadata["version"]
        assert discovery["metadata"]["source_digest"] == protocol.digest
        assert discovery["metadata"]["required_capabilities"] == sorted(
            protocol.metadata["capabilities"]["required"]
        )
        assert protocol.body in source
        assert "## Stop Conditions" in source
        assert "## Artifact Contract" in source
        for condition in protocol.metadata["stop_conditions"]:
            assert condition in source


def test_codex_build_is_byte_deterministic(tmp_path: Path) -> None:
    output = tmp_path / "codex"
    first = build_adapter(ROOT, "codex", output)
    first_bytes = {path.relative_to(output): path.read_bytes() for path in first}

    second = build_adapter(ROOT, "codex", output)

    assert {path.relative_to(output): path.read_bytes() for path in second} == first_bytes
    assert all(b"\r\n" not in content for content in first_bytes.values())

