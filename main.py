#!/usr/bin/env python3
"""NDHU Course Rush - Root execution entrypoint.

Usage:
    uv run python main.py
"""

from __future__ import annotations

import sys

from ndhu_course_rush.entrypoints.cli import main

if __name__ == "__main__":
    sys.exit(main())
