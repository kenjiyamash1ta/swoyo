import tomllib
from pathlib import Path

config_path = Path(__file__).parent.parent / "cfg" / "config.toml"

def read_cfg(path = config_path) -> dict:
    with open(path, "rb") as f:
        config = tomllib.load(f)
    return config