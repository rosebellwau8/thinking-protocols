from __future__ import annotations

import argparse
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from typing import Sequence

from thinking_protocols.adapters import build_adapter
from thinking_protocols.registry import write_registry
from thinking_protocols.validation import validate_repository


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="thinking-protocols")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="Validate the Protocol repository")
    subparsers.add_parser("build-registry", help="Build generated/registry.yaml")
    build_parser = subparsers.add_parser("build", help="Build an Adapter")
    build_parser.add_argument("--adapter", choices=("generic", "codex"), required=True)
    subparsers.add_parser(
        "check-generated", help="Check tracked generated output without overwriting it"
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if args.command == "validate":
        result = validate_repository(root)
        for issue in result.issues:
            print(f"{issue.code} {issue.path}: {issue.message}", file=sys.stderr)
        return 0 if result.is_valid else 1
    if args.command == "build-registry":
        write_registry(root)
        return 0
    if args.command == "build":
        build_adapter(root, args.adapter)
        return 0
    if args.command == "check-generated":
        return 0 if check_generated(root) else 1
    parser.error(f"unknown command: {args.command}")
    return 2


def check_generated(root: Path | str) -> bool:
    repository_root = Path(root)
    with TemporaryDirectory(prefix="thinking-protocols-") as temporary:
        temporary_root = Path(temporary)
        generated_registry = temporary_root / "generated" / "registry.yaml"
        write_registry(repository_root, generated_registry)
        generic_output = temporary_root / "dist" / "generic"
        codex_output = temporary_root / "dist" / "codex"
        build_adapter(repository_root, "generic", generic_output)
        build_adapter(repository_root, "codex", codex_output)

        return (
            _same_file(
                repository_root / "generated" / "registry.yaml",
                generated_registry,
            )
            and _same_tree(repository_root / "dist" / "generic", generic_output)
            and _same_tree(repository_root / "dist" / "codex", codex_output)
        )


def _same_file(actual: Path, expected: Path) -> bool:
    return actual.is_file() and actual.read_bytes() == expected.read_bytes()


def _same_tree(actual: Path, expected: Path) -> bool:
    actual_files = {
        path.relative_to(actual).as_posix(): path.read_bytes()
        for path in actual.rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    }
    expected_files = {
        path.relative_to(expected).as_posix(): path.read_bytes()
        for path in expected.rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    }
    return actual_files == expected_files


if __name__ == "__main__":
    raise SystemExit(main())
