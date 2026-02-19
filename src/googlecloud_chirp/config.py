import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional

# These are defaults, but the class can take customs
CONFIG_DIR = Path.home() / ".googlecloud-chirp"
CONFIG_FILE = CONFIG_DIR / "settings.yaml"

DEFAULT_CONFIG = {
    "project_id": "",
    "default_voice": "en-US-Chirp3-HD-A",
    "default_language": "en-US",
    "output_dir": ".",
    "auto_play": False,
    "output_template": "speech_{timestamp}.mp3"
}

class ConfigManager:
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or (Path.home() / ".googlecloud-chirp")
        self.config_file = self.config_dir / "settings.yaml"
        self._config: Dict[str, Any] = DEFAULT_CONFIG.copy()
        self.load()

    def _ensure_config_dir(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    file_config = yaml.safe_load(f)
                    if file_config:
                        self._config.update(file_config)
            except Exception:
                pass

    def save(self):
        self._ensure_config_dir()
        with open(self.config_file, "w") as f:
            yaml.safe_dump(self._config, f)

    def get(self, key: str, default: Any = None) -> Any:
        value = self._config.get(key)
        
        # Special handling for project_id to check environment variables
        if key == "project_id" and not value:
            value = os.environ.get("GOOGLE_CLOUD_PROJECT")
            
        return value if value is not None else default

    def set(self, key: str, value: Any):
        self._config[key] = value

    def reset(self):
        """Resets the configuration to defaults."""
        self._config = DEFAULT_CONFIG.copy()
        self.save()

    @property
    def all(self) -> Dict[str, Any]:
        return self._config.copy()
