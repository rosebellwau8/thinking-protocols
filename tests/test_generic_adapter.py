from pathlib import Path

from thinking_protocols.adapters import build_adapter
from thinking_protocols.protocols import load_protocol


ROOT = Path(__file__).parents[1]


def pilot_protocols():
    return [
        load_protocol(path)
        for path in sorted((ROOT / "protocols").glob("*/PROTOCOL.md"))
        if not path.parent.name.startswith("_")
    ]


def test_generic_build_contains_one_complete_prompt_per_protocol(tmp_path: Path) -> None:
    output = tmp_path / "generic"

    written = build_adapter(ROOT, "generic", output)

    assert {path.name for path in written} == {
        f"{protocol.metadata['id']}.md" for protocol in pilot_protocols()
    }
    for protocol in pilot_protocols():
        rendered = (output / f"{protocol.metadata['id']}.md").read_text(
            encoding="utf-8"
        )
        assert protocol.body in rendered
        assert f"source_version: {protocol.metadata['version']}" in rendered
        assert f"source_digest: {protocol.digest}" in rendered
        for capability in protocol.metadata["capabilities"]["required"]:
            assert capability in rendered
        for stop_condition in protocol.metadata["stop_conditions"]:
            assert stop_condition in rendered


def test_generic_build_is_byte_identical_and_write_only_when_changed(
    tmp_path: Path,
) -> None:
    output = tmp_path / "generic"
    first_paths = build_adapter(ROOT, "generic", output)
    first_bytes = {path.name: path.read_bytes() for path in first_paths}
    first_mtimes = {path.name: path.stat().st_mtime_ns for path in first_paths}

    second_paths = build_adapter(ROOT, "generic", output)

    assert {path.name: path.read_bytes() for path in second_paths} == first_bytes
    assert {path.name: path.stat().st_mtime_ns for path in second_paths} == first_mtimes
    assert all(b"\r\n" not in content for content in first_bytes.values())
