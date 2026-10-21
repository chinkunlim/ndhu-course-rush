#!/usr/bin/env python3
"""NDHU Course Selector - 向後相容根目錄進入點腳本.

此腳本保留原先 `auto_login.py` 的進入點與函式介面，底層轉發調用 `ndhu_course_selector` 核心模組。
使用方式：
    python auto_login.py
    uv run auto_login.py
"""

import sys
from ndhu_course_selector.cli import main
from ndhu_course_selector.tools.config import load_config as read_config
from ndhu_course_selector.core.auth import perform_login
from ndhu_course_selector.core.browser import create_browser_session

if __name__ == "__main__":
    sys.exit(main())
