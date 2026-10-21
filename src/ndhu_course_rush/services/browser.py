"""Browser lifecycle and Playwright management."""

from __future__ import annotations

import logging
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from playwright.sync_api import Browser, Dialog, Page, sync_playwright

logger = logging.getLogger(__name__)


def _create_dialog_handler(alert_box: dict[str, str | None]) -> Any:
    """Create a dialog event handler that captures the message and accepts.

    Args:
        alert_box: Dictionary holding the latest dialog text.

    Returns:
        Callable handler for Playwright dialog events.
    """

    def handler(dialog: Dialog) -> None:
        """Handle incoming native dialog event.

        Args:
            dialog: Playwright dialog event instance.
        """
        try:
            alert_box["text"] = dialog.message
            logger.info("Native dialog received: %s", dialog.message)
            dialog.accept()
        except Exception as exc:
            logger.debug("Dialog dismiss error: %s", exc)

    return handler


@contextmanager
def create_browser_session(
    headless: bool = False,
    channel: str | None = "chrome",
) -> Generator[tuple[Page, dict[str, str | None], Browser], None, None]:
    """Launch a browser session with native dialog interception.

    Args:
        headless: Whether to run the browser in headless mode.
        channel: Specific browser channel (e.g. 'chrome' or None for bundled chromium).

    Yields:
        Tuple of (Page, alert_msg_box dict, Browser).
    """
    logger.info("Launching Playwright browser (headless=%s, channel=%s)", headless, channel)
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=headless, channel=channel)
        except Exception as exc:
            logger.warning("Failed to launch with channel=%s (%s), falling back to chromium", channel, exc)
            browser = p.chromium.launch(headless=headless)

        context = browser.new_context()
        page = context.new_page()
        alert_msg_box: dict[str, str | None] = {"text": None}
        dialog_handler = _create_dialog_handler(alert_msg_box)
        page.on("dialog", dialog_handler)

        try:
            yield page, alert_msg_box, browser
        finally:
            logger.info("Closing browser session")
            try:
                page.remove_listener("dialog", dialog_handler)
            except Exception:
                pass
            try:
                context.close()
                browser.close()
            except Exception:
                pass
