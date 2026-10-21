"""Course selection execution and rate-limiting strategy."""

from __future__ import annotations

import logging
import random
import time
from collections.abc import Sequence
from typing import Any

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from ndhu_course_rush.services.parser import parse_markdown_priorities

logger = logging.getLogger(__name__)


def resolve_priority_map(
    choice: str,
    row_count: int,
    md_filename: str = "courses_info.md",
) -> list[dict[str, int]] | None:
    """Resolve selection priority order based on user choice.

    Args:
        choice: Selected strategy ('Y', '2', or 'N').
        row_count: Total number of courses available.
        md_filename: Markdown filename containing priority ranking.

    Returns:
        List of priority mappings, or None if cancelled or invalid.
    """
    clean_choice = choice.strip().upper()
    if clean_choice == "Y":
        return [{"priority": idx + 1, "index": i} for idx, i in enumerate(range(row_count))]
    if clean_choice == "2":
        logger.info("Reading priority order from %s", md_filename)
        priorities = parse_markdown_priorities(md_filename)
        return priorities if priorities else None
    logger.info("Course selection cancelled or invalid input: %s", clean_choice)
    return None


def _dismiss_action_dialog(page: Page, alert_box: dict[str, Any]) -> None:
    """Dismiss native alert or jQuery dialog after an action click.

    Args:
        page: Playwright Page instance.
        alert_box: Container for native alert message handling.
    """
    for _ in range(10):
        if alert_box.get("text") is not None:
            logger.info("System alert confirmed: %s", alert_box["text"])
            return
        time.sleep(0.05)
    try:
        modal_btn = page.locator(".ui-dialog:visible .ui-dialog-buttonset button").first
        modal_btn.wait_for(state="visible", timeout=1000)
        modal_btn.click()
        logger.info("jQuery dialog dismissed")
    except PlaywrightTimeoutError:
        logger.debug("No modal dialog detected after action click")


def _click_course_action(row: Locator, alert_box: dict[str, Any], page: Page) -> bool:
    """Find and click the selection button within a table row.

    Args:
        row: Table row locator.
        alert_box: Container for native alert messages.
        page: Playwright Page instance.

    Returns:
        True if the button was clicked and handled.
    """
    first_cell = row.locator("td").first
    action_btn = first_cell.locator("button, input[type='button'], input[type='submit'], a").first
    try:
        action_btn.wait_for(state="visible", timeout=500)
        alert_box["text"] = None
        action_btn.click()
        _dismiss_action_dialog(page, alert_box)
        return True
    except PlaywrightTimeoutError:
        logger.warning("No clickable action button in row")
        return False


def execute_course_selection(
    page: Page,
    alert_box: dict[str, Any],
    course_data: Sequence[Any],
    priority_map: Sequence[dict[str, int]] | None = None,
) -> bool:
    """Execute course selection according to priority mapping.

    Args:
        page: Playwright Page instance.
        alert_box: Container for native dialog interception.
        course_data: List of Course models or dictionaries.
        priority_map: Optional pre-defined priority list. If None, reads from courses_info.md.

    Returns:
        True if execution completed, False if cancelled or empty.
    """
    row_count = len(course_data)
    if priority_map is None:
        priority_map = resolve_priority_map("2", row_count)
    if not priority_map:
        logger.warning("No priority mapping available for selection")
        return False

    logger.info("Executing selection for %d courses in priority order", len(priority_map))
    for item in priority_map:
        priority, i = item["priority"], item["index"]
        if i < 0 or i >= row_count:
            logger.warning("[#%d] Index %d out of bounds, skipping", priority, i)
            continue
        current_row = page.locator("#ContentPlaceHolder1_grd_subjs tr:has(td)").nth(i)
        logger.info("[#%d] Clicking selection button for course index %d", priority, i)
        _click_course_action(current_row, alert_box, page)
        human_delay = random.uniform(0.08, 0.20)
        time.sleep(human_delay)

    return True
