import os
from typer.testing import CliRunner

from earthscope_cli.main import app
from earthscope_cli.util import APP_DIR

runner = CliRunner()


def test_login():
    result = runner.invoke(app, "sso login".split())
    assert result.exit_code == 0
    assert "Successful login" in result.stdout
    assert APP_DIR.exists()
    assert APP_DIR.is_dir()
    assert len(os.listdir(APP_DIR)) > 0
    assert (APP_DIR / "sso_tokens.json").exists()


# def test_refresh():
#     result = runner.invoke(app, "sso refresh".split())
