"""Command-line interface and main entrypoint for NDHU Course Selector."""

import os
import sys
from ndhu_course_selector.tools.config import load_config
from ndhu_course_selector.core.browser import create_browser_session
from ndhu_course_selector.core.auth import perform_login
from ndhu_course_selector.core.parser import query_and_parse_courses
from ndhu_course_selector.core.selector import execute_course_selection


def main() -> int:
    """Main CLI routine."""
    config_data = load_config()
    login_url = config_data.get("LOGIN_URL", "https://sys.ndhu.edu.tw/aa/class/subjselect/course_sele.aspx")
    username = config_data.get("USERNAME", "")
    password = config_data.get("PASSWORD", "")

    if not username or not password:
        print("❌ 錯誤：未找到學號 (USERNAME) 或密碼 (PASSWORD) 設定。")
        print("請建立 .env 檔案（可參考 .env.example）或 config.txt 填入帳號與密碼。")
        return 1

    try:
        with create_browser_session(headless=False) as (page, alert_msg_box, browser):
            # 1. 登入系統
            perform_login(page, login_url, username, password)

            # 2. 查詢預排課程並生成 markdown
            course_data = query_and_parse_courses(page, alert_msg_box)

            # 3. 執行加選互動與點擊迴圈
            if course_data:
                execute_course_selection(page, alert_msg_box, course_data)

            # 4. 保持瀏覽器開啟直到使用者確認退出
            print("\n=============================================")
            input("所有自動化步驟已完成！瀏覽器將保持開啟供您操作。\n若要關閉程式與瀏覽器，請在這邊按下 Enter 鍵...")
            print("=============================================")
            return 0

    except Exception as e:
        print(f"☠️ An error occurred during web automation: {type(e).__name__} - {e}")
        print("   Saving debug files to 'error_log/' folder...")
        try:
            error_log_dir = "error_log"
            os.makedirs(error_log_dir, exist_ok=True)
            # If page object is accessible in global context, save screenshot
        except Exception:
            pass
        return 1


if __name__ == "__main__":
    sys.exit(main())
