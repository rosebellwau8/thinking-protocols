import json
from pathlib import Path

from thinking_protocols.adapters import build_adapter
from thinking_protocols.conformance import check_codex_conformance


ROOT = Path(__file__).parents[1]
START = "<!-- thinking-protocols-invariants\n"
END = "\nthinking-protocols-invariants -->"


def test_codex_build_is_semantically_conformant(tmp_path: Path) -> None:
    output = tmp_path / "codex"
    build_adapter(ROOT, "codex", output)

    assert check_codex_conformance(ROOT, output) == ()


def test_conformance_reports_exact_semantic_path_on_drift(tmp_path: Path) -> None:
    output = tmp_path / "codex"
    build_adapter(ROOT, "codex", output)
    skill = output / "skills" / "socratic-questioning" / "SKILL.md"
    source = skill.read_text(encoding="utf-8")
    before, remainder = source.split(START, maxsplit=1)
    raw_invariants, after = remainder.split(END, maxsplit=1)
    invariants = json.loads(raw_invariants)
    invariants["interaction"]["mode"] = "one_shot"
    skill.write_text(
        before
        + START
        + json.dumps(invariants, sort_keys=True, separators=(",", ":"))
        + END
        + after,
        encoding="utf-8",
        newline="",
    )

    issues = check_codex_conformance(ROOT, output)

    assert any(issue.path == "interaction.mode" for issue in issues)
