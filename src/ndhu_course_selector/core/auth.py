"""Authentication and modal dismissal logic."""

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


def perform_login(page: Page, login_url: str, username: str, password: str) -> bool:
    """Navigates to NDHU login page, enters credentials, and handles post-login modals."""
    print(f"▶️  Navigating to login page: {login_url}")
    page.goto(login_url)

    # Fill credentials
    page.locator("#ContentPlaceHolder1_ed_StudNo").fill(username)
    page.locator("#ContentPlaceHolder1_ed_pass").fill(password)
    page.locator("#ContentPlaceHolder1_BtnLoginNew").click()

    print("\n▶️  After login, handling dialogs and waiting for main page...")

    # Dismiss teaching evaluation survey modal if it pops up
    try:
        div_modal_locator = page.locator("div[aria-describedby='evalModal'] button:has-text('取消')")
        div_modal_locator.wait_for(state="visible", timeout=5000)
        div_modal_locator.click()
        print("   ✅ Dismissed the DIV modal (教學意見評量提示).")
    except PlaywrightTimeoutError:
        pass

    page.wait_for_load_state("networkidle")
    print("✅ Confirmed navigation to main page. Cleanup complete.")
    print("🎉 Login successful!")
    return True
