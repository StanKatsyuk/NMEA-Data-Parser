import yaml

from pathlib import Path

# Resolve the current dir's parent to fetch the config
current_dir = Path(__file__).resolve().parent
CONFIG_PATH = current_dir.parent / "configs" / "config.yaml"


if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Config file does not exist at {CONFIG_PATH} - Check provided path")

class BaseIO:
    def __init__(self, config_path: str = CONFIG_PATH.as_posix()):
        if config_path is None:
            config_path = CONFIG_PATH.as_posix()
        self.config_path = config_path

    def load_from_config(self, protocol: str) -> dict:
        """
        Loads IO settings from the configuration file for the specified protocol.

        This method reads the configuration settings for the specified protocol
        from the YAML configuration file located at `self.config_path`.

        Args:
            protocol (str): The protocol for which to load configuration settings.

        Returns:
            dict: Dictionary containing IO configuration settings for the specified protocol.
        """
        with open(self.config_path, 'r') as file:
            config_data = yaml.safe_load(file)
            return config_data[protocol]
