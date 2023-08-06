import configparser
from pathlib import Path


class Config:
    """
    Class for configuration operations.
    """

    def set_config(self,
                   username: str,
                   password: str,
                   path: Path) -> Path:
        """Set app configuartion."""

        cfg = configparser.ConfigParser()
        cfg["credentials"] = {
            "username": username,
            "password": password
        }
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w") as file:
                cfg.write(file)
        except OSError as err:
            raise ValueError from err

        return path

    def get_config(self, config_file: Path) -> Path:
        """Return the content of the config file."""
        config_parser = configparser.ConfigParser()
        config_parser.read(config_file)
        return (config_parser["credentials"]["username"],
                config_parser["credentials"]["password"])
