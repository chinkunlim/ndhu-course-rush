#!/usr/bin/env python3
"""Antigravity Project Compliance Auditor
Validates that a project conforms to the Antigravity standard directory layout
and documentation governance requirements.
"""
import os
import sys

REQUIRED_FILES = [
    "pyproject.toml",
    ".python-version",
    ".gitignore",
    ".env.example",
    "Makefile",
    "LICENSE",
    ".cursorrules",
    "README.md",
    "AGENTS.md",
    "WORKFLOW_GUIDE.md",
    "CHANGELOG.md",
    "DECISIONS.md",
    "KNOWN_ISSUES.md"
]

REQUIRED_DIRS = [
    ".vscode",
    ".github/workflows",
    "docs",
    "tests",
    "evals",
    "conversations/raw",
    "conversations/summaries"
]

FORBIDDEN_DUPLICATES = [
    "docs/CHANGELOG.md",
    "docs/DECISIONS.md",
    "docs/KNOWN_ISSUES.md",
    "OPERATIONS.md",
    "docs/STRUCTURE.md",
    "agent.md"
]

def audit():
    missing_files = [f for f in REQUIRED_FILES if not os.path.exists(f)]
    missing_dirs = [d for d in REQUIRED_DIRS if not os.path.exists(d)]
    found_duplicates = [dup for dup in FORBIDDEN_DUPLICATES if os.path.exists(dup)]
    
    print("================ 專案標準合規審計報告 ================")
    if not missing_files and not missing_dirs and not found_duplicates:
        print("✅ 100% 通過！本專案結構與文件規格完全符合 Antigravity 標準。")
        return 0
    else:
        if missing_files:
            print(f"❌ 缺少必備核心檔案: {missing_files}")
        if missing_dirs:
            print(f"❌ 缺少必備標準目錄: {missing_dirs}")
        if found_duplicates:
            print(f"⚠️ 發現重複或應收斂之舊檔案: {found_duplicates}")
        return 1

if __name__ == "__main__":
    sys.exit(audit())
