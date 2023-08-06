import os
from typer.testing import CliRunner

from earthscope_cli.main import app
from earthscope_cli.util import APP_DIR

runner = CliRunner()


def test_m2m_login():
    result = runner.invoke(app, "m2m login".split())
    assert result.exit_code == 0
    assert "Successful login" in result.stdout
    assert APP_DIR.exists()
    assert APP_DIR.is_dir()
    assert len(os.listdir(APP_DIR)) > 0
    assert (APP_DIR / "m2m_tokens.json").exists()


def test_user_lookup():
    result = runner.invoke(
        app,
        "user lookup --id google-oauth2|115207392315468355758 --id google-oauth2|112775405674935392870".split(),
    )
    assert result.exit_code == 0
