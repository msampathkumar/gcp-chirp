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

def test_say_missing_input(mocker, tmp_path):
    mocker.patch("gcp_chirp.config.Path.home", return_value=tmp_path)
    result = runner.invoke(app, ["say"])
    assert result.exit_code == 1
    assert "provide either a text argument or a --file path" in result.stdout

def test_say_with_file(mocker, tmp_path):
    mocker.patch("gcp_chirp.config.Path.home", return_value=tmp_path)
    mocker.patch.dict("os.environ", {"GOOGLE_CLOUD_PROJECT": "test-project"}, clear=True)
    
    # Mock TTS synthesis to avoid real calls
    mocker.patch("gcp_chirp.cli.ChirpTTS.synthesize", return_value="output.mp3")
    
    # Create a dummy file
    test_file = tmp_path / "input.txt"
    test_file.write_text("Hello from file")
    
    result = runner.invoke(app, ["say", "--file", str(test_file), "--no-play"])
    assert result.exit_code == 0
    assert "Success" in result.stdout
