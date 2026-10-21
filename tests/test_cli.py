"""Unit tests for the CLI entrypoint."""

from __future__ import annotations

import io
import os
import unittest
from contextlib import redirect_stdout
from unittest import mock

from ndhu_course_rush.config.settings import AppConfig
from ndhu_course_rush.entrypoints.cli import _validate_credentials, build_parser, main


class CliEntrypointTest(unittest.TestCase):
    """Test CLI argument parsing and validation logic."""

    def test_build_parser_defaults(self) -> None:
        """Parser sets default flags properly."""
        parser = build_parser()
        args = parser.parse_args([])
        self.assertFalse(args.headless)
        self.assertFalse(args.query_only)
        self.assertFalse(args.non_interactive)
        self.assertEqual(args.md_file, "courses_info.md")

    def test_validate_credentials_missing(self) -> None:
        """Missing credentials returns False."""
        cfg = AppConfig(ndhu_username="", ndhu_password="")
        out = io.StringIO()
        with redirect_stdout(out):
            valid = _validate_credentials(cfg)
        self.assertFalse(valid)
        self.assertIn("未找到學號", out.getvalue())

    def test_validate_credentials_present(self) -> None:
        """Present credentials returns True."""
        cfg = AppConfig(ndhu_username="411383000", ndhu_password="secret_password")
        self.assertTrue(_validate_credentials(cfg))

    def test_main_exits_when_no_credentials(self) -> None:
        """Main exits with error code 1 when credentials missing."""
        out = io.StringIO()
        env_overrides = {"NDHU_USERNAME": "", "NDHU_PASSWORD": "", "LOG_TO_FILE": "false"}
        with mock.patch.dict(os.environ, env_overrides, clear=True), redirect_stdout(out):
            code = main([])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
