"""Course table parsing and markdown synchronization."""

from __future__ import annotations

import logging
import re
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from ndhu_course_rush.domain.models import Course

logger = logging.getLogger(__name__)


def _poll_alert_message(alert_box: dict[str, Any]) -> str | None:
    """Wait briefly for native dialog text.

    Args:
        alert_box: Shared dict containing dialog text.

    Returns:
        Captured text or None.
    """
    for _ in range(20):
        if alert_box.get("text") is not None:
            text = str(alert_box["text"]).replace("\n", " ")
            return text
        time.sleep(0.05)
    return None


def _dismiss_jquery_dialog(page: Page) -> str:
    """Extract and dismiss jQuery UI dialog if present.

    Args:
        page: Playwright Page instance.

    Returns:
        Extracted dialog text.
    """
    try:
        dialog_content = page.locator(".ui-dialog:visible .ui-dialog-content").first
        if dialog_content.is_visible(timeout=500):
            text = dialog_content.inner_text().strip().replace("\n", " ")
            ok_btn = page.locator(".ui-dialog:visible .ui-dialog-buttonset button").first
            ok_btn.click()
            return text
    except Exception:
        pass
    return "未知"


def _query_enrolled_count(page: Page, code_el: Locator, alert_box: dict[str, Any]) -> int:
    """Click course code link and parse enrolled student count from dialog.

    Args:
        page: Playwright Page instance.
        code_el: Locator for the course code link.
        alert_box: Shared dict containing native dialog text.

    Returns:
        Number of enrolled students.
    """
    alert_box["text"] = None
    code_el.click()
    text = _poll_alert_message(alert_box) or _dismiss_jquery_dialog(page)
    numbers = re.findall(r"\d+", text)
    return int(numbers[-1]) if numbers else 0


def _parse_row(page: Page, index: int, alert_box: dict[str, Any]) -> Course:
    """Parse one table row into a Course object.

    Args:
        page: Playwright Page instance.
        index: Zero-based row index.
        alert_box: Shared dict containing dialog text.

    Returns:
        Populated Course object.
    """
    row = page.locator("#ContentPlaceHolder1_grd_subjs tr:has(td)").nth(index)
    code_el = row.locator("td:nth-child(2) a")
    name_el = row.locator("td:nth-child(3)")
    limit_el = row.locator("td:nth-child(10)")

    code_text = code_el.inner_text().strip()
    name_text = name_el.inner_text().strip().split("\n")[0]
    limit_text = limit_el.inner_text().strip()
    limit_int = int(limit_text) if limit_text.isdigit() else 0

    enrolled = _query_enrolled_count(page, code_el, alert_box)
    remaining = max(0, limit_int - enrolled)
    logger.info(
        "[%d] %s - %s (limit=%d, enrolled=%d, remaining=%d)",
        index,
        code_text,
        name_text,
        limit_int,
        enrolled,
        remaining,
    )
    return Course(
        index=index,
        code=code_text,
        name=name_text,
        limit=limit_int,
        enrolled=enrolled,
        remaining=remaining,
    )


def query_and_parse_courses(
    page: Page,
    alert_box: dict[str, Any],
    md_filename: str = "courses_info.md",
) -> list[Course]:
    """Click 'Query Pre-scheduled Courses', extract data, and export to markdown.

    Args:
        page: Playwright Page instance.
        alert_box: Container for native alert message handling.
        md_filename: Output markdown file name.

    Returns:
        List of parsed Course models.
    """
    logger.info("Starting course query on NDHU portal")
    query_btn = page.locator("#ContentPlaceHolder1_Button7")
    query_btn.wait_for(state="visible", timeout=5000)
    query_btn.click()

    page.wait_for_load_state("networkidle")
    table = page.locator("#ContentPlaceHolder1_grd_subjs")
    table.wait_for(state="visible", timeout=10000)

    try:
        table.locator("tr:has(td)").first.wait_for(state="visible", timeout=5000)
    except PlaywrightTimeoutError:
        pass

    row_count = table.locator("tr:has(td)").count()
    logger.info("Course table loaded with %d rows", row_count)

    courses = [_parse_row(page, i, alert_box) for i in range(row_count)]
    write_courses_markdown(courses, md_filename)
    return courses


def _format_markdown_row(item: Any) -> str:
    """Format one course record into a markdown table row.

    Args:
        item: Course model or dictionary containing course fields.

    Returns:
        Markdown table row string.
    """
    idx = getattr(item, "index", item["index"] if isinstance(item, dict) else 0)
    code = getattr(item, "code", item["code"] if isinstance(item, dict) else "")
    limit = getattr(item, "limit", item["limit"] if isinstance(item, dict) else 0)
    enrolled = getattr(item, "enrolled", item["enrolled"] if isinstance(item, dict) else 0)
    remaining = getattr(item, "remaining", item["remaining"] if isinstance(item, dict) else 0)
    name = getattr(item, "name", item["name"] if isinstance(item, dict) else "")
    return f"|  | **{idx}** | `{code}` | {limit} | {enrolled} | **{remaining}** | {name} |\n"


def write_courses_markdown(
    courses: Sequence[Any],
    filename: str = "courses_info.md",
) -> None:
    """Write course data into standard markdown table format.

    Args:
        courses: Sequence of Course models or dictionaries.
        filename: Destination markdown file path.
    """
    usage_note = (
        "> 數字越小代表越優先搶，不想選的課程請保持空白即可。"
        "排好後記得存檔，然後在終端機輸入 `2` 載入此設定。\n\n"
    )
    lines = [
        "# 預排課程與人數清單\n\n",
        "> 💡 **使用說明**：請在最左邊的「搶課順序」欄位填寫數字（例如 1, 2, 3...）。\n",
        usage_note,
        "| 搶課順序 | 原編號 | 課程代碼 | 限修人數 | 已選人數 | 剩餘空位 | 課程名稱 |\n",
        "| :---: | :---: | :--- | :---: | :---: | :---: | :--- |\n",
    ]
    lines.extend(_format_markdown_row(c) for c in courses)
    content = "".join(lines)
    try:
        Path(filename).write_text(content, encoding="utf-8")
        logger.info("Course info exported to markdown: %s", filename)
    except Exception as exc:
        logger.warning("Failed to write course markdown file: %s", exc)


def parse_markdown_priorities(filepath: str) -> list[dict[str, int]]:
    """Parse user-configured priority rankings from markdown table.

    Args:
        filepath: Path to courses_info.md.

    Returns:
        Sorted list of priority dictionaries: [{'priority': int, 'index': int}, ...].
    """
    path = Path(filepath)
    if not path.is_file():
        return []
    priorities: list[dict[str, int]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "原編號" in stripped or ":---" in stripped:
            continue
        parts = stripped.split("|")
        if len(parts) < 3:
            continue
        p_str = parts[1].replace("*", "").strip()
        i_str = parts[2].replace("*", "").strip()
        if p_str.isdigit() and i_str.isdigit():
            priorities.append({"priority": int(p_str), "index": int(i_str)})
    priorities.sort(key=lambda x: x["priority"])
    return priorities
