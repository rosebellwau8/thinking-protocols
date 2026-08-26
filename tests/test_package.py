from pathlib import Path
import tomllib

import thinking_protocols


ROOT = Path(__file__).parents[1]


def test_package_exposes_version() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert thinking_protocols.__version__ == "0.2.0"
    assert project["project"]["version"] == thinking_protocols.__version__
