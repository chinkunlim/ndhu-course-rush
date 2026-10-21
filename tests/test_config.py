"""Tests for configuration loader."""

from __future__ import annotations

import os
import tempfile
import unittest
from unittest import mock

from ndhu_course_rush.config import AppConfig, load_legacy_config


class ConfigLoaderTest(unittest.TestCase):
    """Test configuration loading and precedence rules."""

    def test_load_legacy_config_default_values(self) -> None:
        """Verify default fallback values when files do not exist."""
        cfg = load_legacy_config(config_file="non_existent.txt", env_file="non_existent.env")
        self.assertIn("LOGIN_URL", cfg)
        self.assertIn("https://sys.ndhu.edu.tw", cfg["LOGIN_URL"])

    def test_load_legacy_config_file(self) -> None:
        """Verify legacy config.txt format parsing."""
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f:
            f.write("USERNAME=test_user_411\nPASSWORD=secret_pass\n")
            tmp_name = f.name

        try:
            cfg = load_legacy_config(config_file=tmp_name, env_file="non_existent.env")
            self.assertEqual(cfg["USERNAME"], "test_user_411")
            self.assertEqual(cfg["PASSWORD"], "secret_pass")
        finally:
            if os.path.exists(tmp_name):
                os.remove(tmp_name)

    def test_load_legacy_config_env_priority(self) -> None:
        """Verify OS environment variables take highest precedence."""
        env_vars = {"NDHU_USERNAME": "env_user_999", "NDHU_PASSWORD": "env_secret"}
        with mock.patch.dict(os.environ, env_vars):
            cfg = load_legacy_config(config_file="non_existent.txt", env_file="non_existent.env")
            self.assertEqual(cfg["USERNAME"], "env_user_999")
            self.assertEqual(cfg["PASSWORD"], "env_secret")

    def test_load_app_config(self) -> None:
        """Verify modern AppConfig initialization and defaults."""
        cfg = AppConfig()
        self.assertEqual(cfg.app_env, "development")
        self.assertEqual(cfg.rush_delay, 0.05)
        self.assertEqual(cfg.query_delay, 0.15)
        self.assertIn("subjselect", cfg.login_url)


if __name__ == "__main__":
    unittest.main()
