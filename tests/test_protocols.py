import hashlib
from pathlib import Path

import pytest

from thinking_protocols.errors import ProtocolParseError
from thinking_protocols.protocols import load_protocol


def write_protocol(tmp_path: Path, source: str) -> Path:
    path = tmp_path / "PROTOCOL.md"
    path.write_text(source, encoding="utf-8", newline="")
    return path


def test_loads_frontmatter_body_and_source_digest(tmp_path: Path) -> None:
    source = "---\nid: example\nversion: 0.1.0\n---\n\n# Procedure\n\nDo the work.\n"
    path = write_protocol(tmp_path, source)

    protocol = load_protocol(path)

    assert protocol.metadata == {"id": "example", "version": "0.1.0"}
    assert protocol.body == "# Procedure\n\nDo the work."
    assert len(protocol.digest) == 64
    assert protocol.digest == hashlib.sha256(source.encode("utf-8")).hexdigest()


def test_digest_is_identical_for_lf_and_crlf_sources(tmp_path: Path) -> None:
    normalized = "---\nid: example\n---\n\n# Procedure\n"
    lf_path = tmp_path / "lf.md"
    crlf_path = tmp_path / "crlf.md"
    lf_path.write_bytes(normalized.encode("utf-8"))
    crlf_path.write_bytes(normalized.replace("\n", "\r\n").encode("utf-8"))

    lf_protocol = load_protocol(lf_path)
    crlf_protocol = load_protocol(crlf_path)

    expected = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    assert lf_protocol.digest == expected
    assert crlf_protocol.digest == expected


def test_rejects_missing_frontmatter(tmp_path: Path) -> None:
    path = write_protocol(tmp_path, "# Procedure\n")

    with pytest.raises(ProtocolParseError, match="frontmatter") as error:
        load_protocol(path)

    assert str(path) in str(error.value)


def test_rejects_invalid_yaml(tmp_path: Path) -> None:
    path = write_protocol(tmp_path, "---\nid: [unterminated\n---\n\n# Procedure\n")

    with pytest.raises(ProtocolParseError, match="YAML") as error:
        load_protocol(path)

    assert str(path) in str(error.value)


def test_rejects_empty_body(tmp_path: Path) -> None:
    path = write_protocol(tmp_path, "---\nid: example\n---\n\n   \n")

    with pytest.raises(ProtocolParseError, match="body") as error:
        load_protocol(path)

    assert str(path) in str(error.value)
