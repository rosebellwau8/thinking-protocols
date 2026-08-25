from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from thinking_protocols.protocols import Protocol, load_protocol
from thinking_protocols.validation import validate_repository


def render_registry(root: Path | str) -> bytes:
    repository_root = Path(root)
    validation = validate_repository(repository_root)
    if not validation.is_valid:
        codes = ", ".join(issue.code for issue in validation.issues)
        raise ValueError(f"Cannot build an invalid Protocol repository: {codes}")

    document = {
        "schema_version": "v1",
        "protocols": [
            _registry_record(protocol)
            for protocol in sorted(
                _load_repository_protocols(repository_root),
                key=lambda item: item.metadata["id"],
            )
        ],
    }
    rendered = yaml.safe_dump(
        document,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=4096,
        line_break="\n",
    )
    return rendered.replace("\r\n", "\n").encode("utf-8")


def write_registry(
    root: Path | str, output_path: Path | str | None = None
) -> bool:
    repository_root = Path(root)
    output = (
        Path(output_path)
        if output_path is not None
        else repository_root / "generated" / "registry.yaml"
    )
    rendered = render_registry(repository_root)
    if output.is_file() and output.read_bytes() == rendered:
        return False
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(rendered)
    return True


def is_registry_current(
    root: Path | str, output_path: Path | str | None = None
) -> bool:
    repository_root = Path(root)
    output = (
        Path(output_path)
        if output_path is not None
        else repository_root / "generated" / "registry.yaml"
    )
    return output.is_file() and output.read_bytes() == render_registry(repository_root)


def _load_repository_protocols(root: Path) -> list[Protocol]:
    protocol_root = root / "protocols"
    return [
        load_protocol(path)
        for path in sorted(protocol_root.glob("*/PROTOCOL.md"))
        if not path.parent.name.startswith("_")
    ]


def _registry_record(protocol: Protocol) -> dict[str, Any]:
    metadata = protocol.metadata
    return {
        "id": metadata["id"],
        "version": metadata["version"],
        "lifecycle": metadata["lifecycle"],
        "primary_role": metadata["epistemic_role"]["primary"],
        "secondary_roles": sorted(metadata["epistemic_role"]["secondary"]),
        "interaction_mode": metadata["interaction"]["mode"],
        "routing_priority": int(metadata.get("routing_priority", 0)),
        "required_capabilities": sorted(metadata["capabilities"]["required"]),
        "consumes": sorted(metadata["consumes"]),
        "produces": sorted(metadata["produces"]),
        "source_digest": protocol.digest,
    }

