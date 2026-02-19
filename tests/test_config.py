import os
import yaml
import pytest
from pathlib import Path
from gcp_chirp.config import ConfigManager, DEFAULT_CONFIG

def test_config_manager_initialization(tmp_path):
    manager = ConfigManager(config_dir=tmp_path)
    assert manager.all == DEFAULT_CONFIG

def test_config_manager_save_load(tmp_path):
    config_file = tmp_path / "settings.yaml"
    
    manager = ConfigManager(config_dir=tmp_path)
    manager.set("project_id", "test-project")
    manager.set("auto_play", True)
    manager.save()
    
    assert config_file.exists()
    
    # New manager instance should load saved values
    new_manager = ConfigManager(config_dir=tmp_path)
    assert new_manager.get("project_id") == "test-project"
    assert new_manager.get("auto_play") is True

def test_config_manager_get_default(tmp_path):
    manager = ConfigManager(config_dir=tmp_path)
    assert manager.get("non_existent", "fallback") == "fallback"
