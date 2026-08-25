from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from thinking_protocols.protocols import Protocol, load_protocol


INVARIANT_START = "<!-- thinking-protocols-invariants\n"
INVARIANT_END = "\nthinking-protocols-invariants -->"


@dataclass(frozen=True, slots=True)
class ConformanceIssue:
    protocol_id: str
    path: str
    message: str


def canonical_invariants(protocol: Protocol) -> dict[str, Any]:
    metadata = protocol.metadata
    return {
        "id": metadata["id"],
        "version": metadata["version"],
        "interaction": deepcopy(metadata["interaction"]),
        "state": deepcopy(metadata["state"]),
        "capabilities": {
            "required": sorted(metadata["capabilities"]["required"]),
            "optional": sorted(metadata["capabilities"]["optional"]),
            "on_missing": metadata["capabilities"]["on_missing"],
        },
        "consumes": sorted(metadata["consumes"]),
        "produces": sorted(metadata["produces"]),
        "phases": deepcopy(metadata["phases"]),
        "stop_conditions": deepcopy(metadata["stop_conditions"]),
        "safety": deepcopy(metadata["safety"]),
    }


def check_codex_conformance(
    root: Path | str, output_dir: Path | str | None = None
) -> tuple[ConformanceIssue, ...]:
    repository_root = Path(root)
    destination = (
        Path(output_dir)
        if output_dir is not None
        else repository_root / "dist" / "codex"
    )
    issues: list[ConformanceIssue] = []
    for protocol in _load_protocols(repository_root):
        protocol_id = str(protocol.metadata["id"])
        path = destination / "skills" / protocol_id / "SKILL.md"
        if not path.is_file():
            issues.append(
                ConformanceIssue(protocol_id, "file", f"Missing generated skill: {path}")
            )
            continue
        try:
            actual = extract_invariants(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
            issues.append(
                ConformanceIssue(
                    protocol_id,
                    "invariants",
                    f"Could not parse invariant block: {error}",
                )
            )
            continue
        _compare(
            canonical_invariants(protocol),
            actual,
            "",
            protocol_id,
            issues,
        )
    return tuple(sorted(issues, key=lambda issue: (issue.protocol_id, issue.path)))


def extract_invariants(source: str) -> dict[str, Any]:
    if INVARIANT_START not in source or INVARIANT_END not in source:
        raise ValueError("missing invariant block markers")
    _before, remainder = source.split(INVARIANT_START, maxsplit=1)
    raw, _after = remainder.split(INVARIANT_END, maxsplit=1)
    invariants = json.loads(raw)
    if not isinstance(invariants, dict):
        raise ValueError("invariant block must contain a JSON object")
    return invariants


def _load_protocols(root: Path) -> list[Protocol]:
    return sorted(
        (
            load_protocol(path)
            for path in (root / "protocols").glob("*/PROTOCOL.md")
            if not path.parent.name.startswith("_")
        ),
        key=lambda protocol: protocol.metadata["id"],
    )


def _compare(
    expected: Any,
    actual: Any,
    path: str,
    protocol_id: str,
    issues: list[ConformanceIssue],
) -> None:
    if isinstance(expected, dict) and isinstance(actual, dict):
        for key in sorted(set(expected) | set(actual)):
            child_path = f"{path}.{key}" if path else key
            if key not in expected:
                issues.append(
                    ConformanceIssue(protocol_id, child_path, "Unexpected semantic field")
                )
            elif key not in actual:
                issues.append(
                    ConformanceIssue(protocol_id, child_path, "Missing semantic field")
                )
            else:
                _compare(expected[key], actual[key], child_path, protocol_id, issues)
        return
    if isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            issues.append(
                ConformanceIssue(
                    protocol_id,
                    path,
                    f"List length drift: expected {len(expected)}, got {len(actual)}",
                )
            )
        for index, (expected_item, actual_item) in enumerate(zip(expected, actual)):
            _compare(
                expected_item,
                actual_item,
                f"{path}[{index}]",
                protocol_id,
                issues,
            )
        return
    if expected != actual:
        issues.append(
            ConformanceIssue(
                protocol_id,
                path,
                f"Semantic drift: expected {expected!r}, got {actual!r}",
            )
        )
