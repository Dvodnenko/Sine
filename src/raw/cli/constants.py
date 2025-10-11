from pathlib import Path


DAEMON_PID_PATH = Path("/tmp/raw.pid")
CONFIG_PATH = Path.home() / ".config" / "raw" / "config.json"
DEFAULT_CONFIG = {
    "data_file_path": f"sqlite:///{Path.home()}/.raw.sqlite",
}
