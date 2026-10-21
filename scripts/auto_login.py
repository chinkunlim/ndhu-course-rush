#!/usr/bin/env python3
"""NDHU Course Rush - Backward compatibility entrypoint script.

Usage:
    uv run scripts/auto_login.py
"""

from __future__ import annotations

import sys
from ndhu_course_rush.config import load_config, load_legacy_config
from ndhu_course_rush.entrypoints.cli import main
from ndhu_course_rush.services import create_browser_session, perform_login

read_config = load_legacy_config

__all__ = [
    "create_browser_session",
    "load_config",
    "main",
    "perform_login",
    "read_config",
]

if __name__ == "__main__":
    sys.exit(main())
