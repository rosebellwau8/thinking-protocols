from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined
import yaml

from thinking_protocols.protocols import Protocol, load_protocol
from thinking_protocols.validation import validate_repository


def build_adapter(
    root: Path | str,
    adapter_id: str,
    output_dir: Path | str | None = None,
) -> tuple[Path, ...]:
    repository_root = Path(root)
    validation = validate_repository(repository_root)
    if not validation.is_valid:
        codes = ", ".join(issue.code for issue in validation.issues)
        raise ValueError(f"Cannot build an invalid Protocol repository: {codes}")

    adapter_root = repository_root / "adapters" / adapter_id
    manifest = _load_manifest(adapter_root / "adapter.yaml")
    if manifest["id"] != adapter_id:
        raise ValueError(f"Adapter manifest id does not match directory: {adapter_id}")
    destination = (
        Path(output_dir)
        if output_dir is not None
        else repository_root / manifest["output"]
    )
    template_path = Path(manifest["template"])
    environment = Environment(
        loader=FileSystemLoader(adapter_root),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
        newline_sequence="\n",
    )
    template = environment.get_template(template_path.as_posix())

    outputs: list[Path] = []
    for protocol in _load_protocols(repository_root):
        relative_output = _output_path(adapter_id, protocol)
        output = destination / relative_output
        rendered = template.render(
            protocol=protocol,
            metadata=protocol.metadata,
            adapter=manifest,
        )
        content = _normalize_lf(rendered).rstrip("\n") + "\n"
        _write_if_changed(output, content.encode("utf-8"))
        outputs.append(output)
    return tuple(outputs)


def _load_manifest(path: Path) -> dict[str, Any]:
    manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError(f"Adapter manifest must be a mapping: {path}")
    return manifest


def _load_protocols(root: Path) -> list[Protocol]:
    return sorted(
        (
            load_protocol(path)
            for path in (root / "protocols").glob("*/PROTOCOL.md")
            if not path.parent.name.startswith("_")
        ),
        key=lambda protocol: protocol.metadata["id"],
    )


def _output_path(adapter_id: str, protocol: Protocol) -> Path:
    protocol_id = protocol.metadata["id"]
    if adapter_id == "generic":
        return Path(f"{protocol_id}.md")
    if adapter_id == "codex":
        return Path("skills") / protocol_id / "SKILL.md"
    raise ValueError(f"Unsupported Adapter: {adapter_id}")


def _normalize_lf(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n")


def _write_if_changed(path: Path, content: bytes) -> None:
    if path.is_file() and path.read_bytes() == content:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
