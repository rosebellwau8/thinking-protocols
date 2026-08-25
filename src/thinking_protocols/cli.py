from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from thinking_protocols.registry import write_registry


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="thinking-protocols")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("build-registry", help="Build generated/registry.yaml")
    args = parser.parse_args(argv)

    if args.command == "build-registry":
        write_registry(Path.cwd())
        return 0
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
