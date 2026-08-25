from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Any

import yaml

from thinking_protocols.errors import ProtocolParseError


@dataclass(frozen=True)
class Protocol:
    path: Path
    metadata: dict[str, Any]
    body: str
    digest: str


def load_protocol(path: Path | str) -> Protocol:
    protocol_path = Path(path)

    try:
        source_bytes = protocol_path.read_bytes()
        source = source_bytes.decode("utf-8")
    except (OSError, UnicodeError) as error:
        raise ProtocolParseError(
            protocol_path, f"could not read UTF-8 source: {error}"
        ) from error

    normalized = source.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.startswith("---\n"):
        raise ProtocolParseError(protocol_path, "missing leading YAML frontmatter")

    remainder = normalized[4:]
    if "\n---\n" not in remainder:
        raise ProtocolParseError(protocol_path, "missing closing YAML frontmatter")

    frontmatter, markdown = remainder.split("\n---\n", maxsplit=1)
    try:
        metadata = yaml.safe_load(frontmatter)
    except yaml.YAMLError as error:
        raise ProtocolParseError(protocol_path, f"invalid YAML frontmatter: {error}") from error

    if not isinstance(metadata, dict):
        raise ProtocolParseError(protocol_path, "YAML frontmatter must be a mapping")

    body = markdown.strip()
    if not body:
        raise ProtocolParseError(protocol_path, "Markdown body must not be empty")

    return Protocol(
        path=protocol_path,
        metadata=metadata,
        body=body,
        digest=hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
    )
