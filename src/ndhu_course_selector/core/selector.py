"""Course selection execution and rate-limiting strategy."""

import time
import random
from typing import Dict, List, Any
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from ndhu_course_selector.core.parser import parse_markdown_priorities


def execute_course_selection(
    page: Page,
    alert_msg_box: Dict[str, Any],
    course_data: List[Dict[str, Any]],
    md_filename: str = "courses_info.md"
) -> bool:
    """Interacts with user for selection strategy and clicks add buttons accordingly."""
    row_count = len(course_data)
    print("\n=============================================")
    user_input = input(
        f"準備好後，請選擇操作：\n"
        f"1. 輸入 Y：按照網頁預設順序全自動點擊\n"
        f"2. 輸入 2：讀取您修改過的 {md_filename} 裡面的排序\n"
        f"3. 輸入 N：取消並結束程式\n"
        f"請輸入： "
    )
    user_input_upper = user_input.strip().upper()

    priority_map: List[Dict[str, int]] = []
    if user_input_upper == "N":
        print("⚠️ 已取消操作，即將關閉瀏覽器。")
        return False
    elif user_input_upper == "":
        print("⚠️ 未輸入任何指令，取消加選。")
        return False
    elif user_input_upper == "Y":
        priority_map = [{"priority": idx + 1, "index": i} for idx, i in enumerate(range(row_count))]
    elif user_input_upper == "2":
        print(f"▶️ 正在從 {md_filename} 讀取您的自訂順序...")
        priority_map = parse_markdown_priorities(md_filename)
        if not priority_map:
            print(f"⚠️ 找不到任何填寫了數字的「搶課順序」！請確認您有在 {md_filename} 最左側欄位填寫數字，取消操作。")
            return False
    else:
        print("⚠️ 輸入無效 (請輸入 Y, 2, 或 N)，取消操作。")
        return False

    extracted_indices = [item["index"] for item in priority_map]
    print(f"\n▶️ 將嚴格按照此順序開始加選 (顯示的數字為您選擇的「原編號」): {extracted_indices}")

    # 3. Click buttons in order
    for item in priority_map:
        priority = item["priority"]
        i = item["index"]

        if i < 0 or i >= row_count:
            print(f"   ⚠️ [第 {priority} 順位] 原編號 {i} 不在範圍內，跳過。")
            continue

        current_row = page.locator("#ContentPlaceHolder1_grd_subjs tr:has(td)").nth(i)
        first_cell = current_row.locator("td").first
        action_btn = first_cell.locator("button, input[type='button'], input[type='submit'], a").first

        # Stage 1: Click button
        try:
            action_btn.wait_for(state="visible", timeout=500)
            code_str = course_data[i]["code"] if i < len(course_data) else ""
            print(f"   ⏳ [第 {priority} 順位] 正在點擊原編號 {i} ({code_str}) 的加選按鈕...")

            alert_msg_box["text"] = None
            action_btn.click()
        except PlaywrightTimeoutError:
            print(f"   ⚠️ [第 {priority} 順位] 原編號 {i} 沒有可點擊的加選按鈕，跳過。")
            continue

        # Stage 2: Handle popup / dialog
        popup_closed = False
        for _ in range(10):
            if alert_msg_box["text"] is not None:
                print(f"   ✅ [第 {priority} 順位] 已自動確認系統彈窗提示: {alert_msg_box['text']}")
                popup_closed = True
                break
            time.sleep(0.1)

        if not popup_closed:
            try:
                modal_btn = page.locator(".ui-dialog:visible .ui-dialog-buttonset button").first
                modal_btn.wait_for(state="visible", timeout=1000)
                modal_btn.click()
                print(f"   ✅ [第 {priority} 順位] 已成功點擊並關閉網頁對話框。")
            except PlaywrightTimeoutError:
                print(f"   ✅ [第 {priority} 順位] 沒有偵測到需要關閉的對話框。")

        # Stage 3: Human-like delay
        human_delay = random.uniform(0.08, 0.20)
        print(f"   ⏳ 人性化延遲: 等待 {human_delay:.3f} 秒...\n")
        time.sleep(human_delay)

    return True
