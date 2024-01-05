"""Test web server."""

# std
from pathlib import Path

# lib
from webtest import TestApp

# pkg
from attrbox import AttrDict
from inkfill import __main__ as server

PATH_EXAMPLES = Path(__file__).parent.parent / "src" / "inkfill" / "examples"
"""Path to examples directory."""


def test_server() -> None:
    """Run the main endpoints."""
    app = TestApp(server.app)
    server.args = AttrDict(config=PATH_EXAMPLES / "corporate-letter" / "letter.toml")
    server.setup_config()
    server.setup_jinja()

    assert app.get("/").status_code == 200
    assert app.get("/doc/0").status_code == 200
    assert app.get("/static/index.less").status_code == 200
    assert app.get("/does-not-exist", expect_errors=True).status_code == 404
