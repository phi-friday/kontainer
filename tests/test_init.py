from __future__ import annotations

import sys
from pathlib import Path

if sys.version_info < (3, 11):
    import tomli as toml  # type: ignore
else:
    import toml  # type: ignore


def test_version():
    from kontainer import __version__

    root = Path(__file__).parent.parent
    pyproject = root / "pyproject.toml"
    with pyproject.open("rb") as f:
        data = toml.load(f)

    assert data["tool"]["poetry"]["version"] == __version__
