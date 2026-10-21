"""Tests for Markdown parsing and priority extraction."""

import os
import tempfile
from ndhu_course_selector.core.parser import parse_markdown_priorities, write_courses_markdown


SAMPLE_MD = """# 預排課程與人數清單

> 說明文字...

| 搶課順序 | 原編號 | 課程代碼 | 限修人數 | 已選人數 | 剩餘空位 | 課程名稱 |
| :---: | :---: | :--- | :---: | :---: | :---: | :--- |
| 0 | **0** | `CP__30000` | 30 | 19 | **11** | 團體諮商 |
| 2 | **1** | `CP__30210` | 60 | 13 | **47** | 心理學研究法 |
|   | **2** | `CP__31000` | 60 | 9 | **51** | 生涯諮商 |
| 1 | **3** | `CP__33400` | 60 | 16 | **44** | 親師合作 |
"""


def test_parse_markdown_priorities():
    """Verify parsing and sorting of user priorities from Markdown table."""
    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f:
        f.write(SAMPLE_MD)
        tmp_name = f.name

    try:
        priorities = parse_markdown_priorities(tmp_name)
        assert len(priorities) == 3
        # Should be sorted: priority 0 (index 0), priority 1 (index 3), priority 2 (index 1)
        assert priorities[0] == {"priority": 0, "index": 0}
        assert priorities[1] == {"priority": 1, "index": 3}
        assert priorities[2] == {"priority": 2, "index": 1}
    finally:
        if os.path.exists(tmp_name):
            os.remove(tmp_name)


def test_write_courses_markdown():
    """Verify writing course data into markdown format."""
    dummy_data = [
        {
            "index": 0,
            "code": "TEST_101",
            "name": "測試課程",
            "limit": 50,
            "enrolled": 20,
            "remaining": 30
        }
    ]
    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f:
        tmp_name = f.name

    try:
        write_courses_markdown(dummy_data, tmp_name)
        with open(tmp_name, "r", encoding="utf-8") as f:
            content = f.read()
        assert "TEST_101" in content
        assert "測試課程" in content
        assert "搶課順序" in content
    finally:
        if os.path.exists(tmp_name):
            os.remove(tmp_name)
