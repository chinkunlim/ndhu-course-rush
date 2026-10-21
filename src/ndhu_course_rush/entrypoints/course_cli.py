"""Backward-compatible command-line interface module.

Delegates to ndhu_course_rush.entrypoints.cli.
"""

from __future__ import annotations

import sys

from ndhu_course_rush.entrypoints.cli import main

__all__ = ["main"]

if __name__ == "__main__":
    sys.exit(main())
