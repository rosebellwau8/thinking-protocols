from pathlib import Path

from thinking_protocols import cli
from thinking_protocols.validation import ValidationIssue, ValidationResult


ROOT = Path(__file__).parents[1]


def test_cli_success_commands_exit_zero() -> None:
    assert cli.main(["--root", str(ROOT), "validate"]) == 0
    assert cli.main(["--root", str(ROOT), "build-registry"]) == 0
    assert cli.main(["--root", str(ROOT), "build", "--adapter", "generic"]) == 0
    assert cli.main(["--root", str(ROOT), "build", "--adapter", "codex"]) == 0
    assert cli.main(["--root", str(ROOT), "check-generated"]) == 0


def test_cli_validation_failure_exits_one(monkeypatch) -> None:
    result = ValidationResult(
        (ValidationIssue("TEST_ERROR", "protocols/test", "intentional"),)
    )
    monkeypatch.setattr(cli, "validate_repository", lambda _root: result)

    assert cli.main(["--root", str(ROOT), "validate"]) == 1


def test_cli_stale_generated_failure_exits_one(monkeypatch) -> None:
    monkeypatch.setattr(cli, "check_generated", lambda _root: False)

    assert cli.main(["--root", str(ROOT), "check-generated"]) == 1
