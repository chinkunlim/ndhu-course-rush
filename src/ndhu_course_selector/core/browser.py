"""Browser lifecycle and Playwright management."""

from contextlib import contextmanager
from typing import Dict, Generator, Tuple
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page


@contextmanager
def create_browser_session(headless: bool = False) -> Generator[Tuple[Page, Dict[str, str], Browser], None, None]:
    """Context manager for launching headed Chrome and managing native dialogs."""
    print("▶️  Launching Chrome browser (Playwright)...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, channel="chrome")
        context = browser.new_context()
        page = context.new_page()

        # Shared container for native alert messages
        alert_msg_box = {"text": None}

        def handle_dialog(dialog):
            try:
                alert_msg_box["text"] = dialog.message
                dialog.accept()
            except Exception:
                pass

        page.on("dialog", handle_dialog)

        try:
            yield page, alert_msg_box, browser
        finally:
            print("▶️  Closing browser session...")
            try:
                page.remove_listener("dialog", handle_dialog)
            except Exception:
                pass
            try:
                context.close()
                browser.close()
            except Exception:
                pass
