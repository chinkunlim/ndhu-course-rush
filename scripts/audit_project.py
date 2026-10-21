#!/usr/bin/env python3
"""Antigravity Project Compliance Auditor.

Validates that a project conforms to the legacy directory layout and governance requirements.
"""

from __future__ import annotations

import os
import sys

REQUIRED_FILES = [
    "pyproject.toml",
    ".python-version",
    ".gitignore",
    ".env.example",
    "LICENSE",
    "README.md",
    "AGENTS.md",
    "CHANGELOG.md",
]

REQUIRED_DIRS = [
    "docs",
    "tests",
]


def audit() -> int:
    """Audit project structure against required files and folders.

    Returns:
        0 if audit passes, 1 otherwise.
    """
    missing_files = [f for f in REQUIRED_FILES if not os.path.exists(f)]
    missing_dirs = [d for d in REQUIRED_DIRS if not os.path.exists(d)]

    print("================ 專案標準合規審計報告 ================")
    if not missing_files and not missing_dirs:
        print("✅ 100% 通過！本專案結構與文件規格完全符合標準。")
        return 0
    if missing_files:
        print(f"❌ 缺少必備核心檔案: {missing_files}")
    if missing_dirs:
        print(f"❌ 缺少必備標準目錄: {missing_dirs}")
    return 1


if __name__ == "__main__":
    sys.exit(audit())
