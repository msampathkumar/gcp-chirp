from typer.testing import CliRunner
from gcp_chirp.cli import app
import pytest

runner = CliRunner()

def test_config_show_defaults(mocker, tmp_path):
    # Mock config path
    mocker.patch("gcp_chirp.config.Path.home", return_value=tmp_path)
    
    result = runner.invoke(app, ["config", "--show"])
    assert result.exit_code == 0
    assert "default_voice" in result.stdout

def test_list_command_no_project_error(mocker, tmp_path):
    # Mock home and make sure config is empty
    mocker.patch("gcp_chirp.config.Path.home", return_value=tmp_path)
    mocker.patch.dict("os.environ", {}, clear=True)
    
    # We need to re-init config manager or mock it
    from gcp_chirp.cli import config_manager
    config_manager.set("project_id", "")
    
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 1
    assert "Project ID is not set" in result.stdout
