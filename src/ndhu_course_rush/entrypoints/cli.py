"""Command-line interface and main entrypoint for NDHU Course Rush.

Usage:
    uv run ndhu-course-rush
    uv run python main.py
"""

from __future__ import annotations

import argparse
import logging
import sys

from ndhu_course_rush.config import AppConfig, load_config, setup_logging
from ndhu_course_rush.services import (
    create_browser_session,
    execute_course_selection,
    perform_login,
    query_and_parse_courses,
)

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Construct command-line argument parser.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(description="NDHU Course Rush Automation & Inspection System")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument(
        "--query-only", action="store_true", help="Only query and export course info without selecting"
    )
    parser.add_argument(
        "--non-interactive", action="store_true", help="Do not wait for user input at completion"
    )
    parser.add_argument("--md-file", default="courses_info.md", help="Markdown file for course priorities")
    return parser


def _validate_credentials(config: AppConfig) -> bool:
    """Check that student credentials are provided.

    Args:
        config: Application configuration.

    Returns:
        True if username and password are non-empty.
    """
    if not config.ndhu_username or not config.ndhu_password:
        print("❌ 錯誤：未找到學號 (NDHU_USERNAME) 或密碼 (NDHU_PASSWORD) 設定。")
        print("請建立 .env 檔案（參考 .env.example）填入帳號與密碼。")
        return False
    return True


def _run_workflow(config: AppConfig, args: argparse.Namespace) -> int:
    """Execute the core browser workflow.

    Args:
        config: Application configuration.
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 on success, 1 on failure).
    """
    logger.info("Starting browser automation session (headless=%s)", args.headless)
    try:
        with create_browser_session(headless=args.headless) as (page, alert_box, _browser):
            # 1. 登入系統
            perform_login(page, config.login_url, config.ndhu_username, config.ndhu_password)

            # 2. 查詢預排課程並生成 markdown
            courses = query_and_parse_courses(page, alert_box, md_filename=args.md_file)
            print(f"✅ 成功查詢並載入 {len(courses)} 門預排課程。")

            # 3. 執行加選互動與點擊
            if courses and not args.query_only:
                execute_course_selection(page, alert_box, courses)

            if not args.non_interactive:
                print("\n=============================================")
                input("所有自動化步驟已完成！按 Enter 鍵關閉瀏覽器...")
                print("=============================================")
        return 0
    except Exception as exc:
        logger.exception("Web automation failed: %s", exc)
        print(f"☠️ 執行過程中發生錯誤: {type(exc).__name__} - {exc}")
        return 1


def main(argv: list[str] | None = None) -> int:
    """Main CLI entrypoint.

    Args:
        argv: Command-line arguments; defaults to sys.argv[1:].

    Returns:
        Process exit code.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    config = load_config()
    setup_logging(config.log_level, config.logs_dir if config.log_to_file else None)
    logger.info("ndhu-course-rush started (env=%s)", config.app_env)

    if not _validate_credentials(config):
        return 1

    return _run_workflow(config, args)


if __name__ == "__main__":
    sys.exit(main())
