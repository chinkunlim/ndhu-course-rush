"""Authentication and post-login modal dismissal logic."""

from __future__ import annotations

import logging

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)


def _dismiss_survey_modal(page: Page) -> None:
    """Dismiss teaching evaluation survey modal if it appears after login.

    Args:
        page: Playwright Page instance.
    """
    try:
        modal_btn = page.locator("div[aria-describedby='evalModal'] button:has-text('取消')")
        modal_btn.wait_for(state="visible", timeout=5000)
        modal_btn.click()
        logger.info("Dismissed teaching evaluation modal")
    except PlaywrightTimeoutError:
        logger.debug("No survey modal detected")


def perform_login(page: Page, login_url: str, username: str, password: str) -> bool:
    """Navigate to NDHU login page, submit credentials, and dismiss modals.

    Args:
        page: Playwright Page instance.
        login_url: Course selection system login URL.
        username: Student ID username.
        password: Password for account.

    Returns:
        True if login submission and navigation completed.
    """
    logger.info("Navigating to login page: %s (user=%s)", login_url, username)
    page.goto(login_url)

    # Fill credentials and submit
    page.locator("#ContentPlaceHolder1_ed_StudNo").fill(username)
    page.locator("#ContentPlaceHolder1_ed_pass").fill(password)
    page.locator("#ContentPlaceHolder1_BtnLoginNew").click()

    logger.info("Handling post-login dialogs and waiting for main page")
    _dismiss_survey_modal(page)
    page.wait_for_load_state("networkidle")
    logger.info("Login confirmed, navigation complete")
    return True
