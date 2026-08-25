from pathlib import Path


class ProtocolParseError(ValueError):
    """Raised when a Protocol source cannot be parsed."""

    def __init__(self, path: Path, message: str) -> None:
        self.path = Path(path)
        super().__init__(f"{self.path}: {message}")

