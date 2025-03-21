import pytest
from src.config import read_cfg

def test_read_cfg(tmp_path):
    config_content = """
    username = "user"
    password = "pass"
    host = "localhost"
    port = "4010"
    """
    config_file = tmp_path / "config.toml"
    config_file.write_text(config_content)

    config = read_cfg(config_file)

    
    assert config["host"] == "localhost"
    assert config["port"] == "4010"
    assert config["username"] == "user"
    assert config["password"] == "pass"

def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_cfg("nonexistent.toml")