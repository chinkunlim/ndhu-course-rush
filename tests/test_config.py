"""Tests for configuration loader."""

import os
import tempfile
from ndhu_course_selector.tools.config import load_config


def test_load_config_default_values():
    """Verify default fallback values when files do not exist."""
    cfg = load_config(config_file="non_existent.txt", env_file="non_existent.env")
    assert "LOGIN_URL" in cfg
    assert "https://sys.ndhu.edu.tw" in cfg["LOGIN_URL"]


def test_load_config_legacy_file(monkeypatch):
    """Verify legacy config.txt format parsing."""
    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f:
        f.write("USERNAME=test_user_411\nPASSWORD=secret_pass\n")
        tmp_name = f.name

    try:
        cfg = load_config(config_file=tmp_name, env_file="non_existent.env")
        assert cfg["USERNAME"] == "test_user_411"
        assert cfg["PASSWORD"] == "secret_pass"
    finally:
        if os.path.exists(tmp_name):
            os.remove(tmp_name)


def test_load_config_env_priority(monkeypatch):
    """Verify OS environment variables take highest precedence."""
    monkeypatch.setenv("NDHU_USERNAME", "env_user_999")
    monkeypatch.setenv("NDHU_PASSWORD", "env_secret")

    cfg = load_config(config_file="non_existent.txt", env_file="non_existent.env")
    assert cfg["USERNAME"] == "env_user_999"
    assert cfg["PASSWORD"] == "env_secret"
