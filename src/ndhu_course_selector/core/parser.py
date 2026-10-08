"""Course table parsing and markdown synchronization."""

import os
import re
import time
import random
from typing import Dict, List, Any
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


def query_and_parse_courses(
    page: Page,
    alert_msg_box: Dict[str, Any],
    md_filename: str = "courses_info.md"
) -> List[Dict[str, Any]]:
    """Clicks 'Query Pre-scheduled Courses', scrapes capacity, and exports to markdown."""
    print("\n▶️  開始處理預排課程...")
    
    # 1. Click Query Button
    query_btn = page.locator("#ContentPlaceHolder1_Button7")
    query_btn.wait_for(state="visible", timeout=5000)
    query_btn.click()
    print("   ✅ 已點擊「查詢預排課程」")

    print("   ⏳ 等待表格資料載入中...")
    time.sleep(1)
    page.wait_for_load_state("networkidle")

    # 2. Wait for table
    table = page.locator("#ContentPlaceHolder1_grd_subjs")
    table.wait_for(state="visible", timeout=10000)

    try:
        table.locator("tr:has(td)").first.wait_for(state="visible", timeout=5000)
    except PlaywrightTimeoutError:
        pass

    time.sleep(0.5)
    row_count = table.locator("tr:has(td)").count()
    print(f"   ✅ 表格已載入，共有 {row_count} 列資料。準備依序查詢已選課人數...")

    course_data = []
    for i in range(row_count):
        current_row = page.locator("#ContentPlaceHolder1_grd_subjs tr:has(td)").nth(i)
        code_el = current_row.locator("td:nth-child(2) a")
        name_el = current_row.locator("td:nth-child(3)")
        limit_el = current_row.locator("td:nth-child(10)")

        code_text = code_el.inner_text().strip()
        name_text = name_el.inner_text().strip().split("\n")[0]
        limit_text = limit_el.inner_text().strip()

        try:
            limit_int = int(limit_text)
        except ValueError:
            limit_int = 0

        # Query enrolled count via dialog
        alert_msg_box["text"] = None
        code_el.click()

        enrolled_text = "未知"
        for _ in range(30):
            if alert_msg_box["text"] is not None:
                enrolled_text = alert_msg_box["text"].replace("\n", " ")
                break
            time.sleep(0.05)

        if alert_msg_box["text"] is None:
            try:
                dialog_content = page.locator(".ui-dialog:visible .ui-dialog-content").first
                if dialog_content.is_visible(timeout=500):
                    enrolled_text = dialog_content.inner_text().strip().replace("\n", " ")
                    ok_btn = page.locator(".ui-dialog:visible .ui-dialog-buttonset button").first
                    ok_btn.click()
            except Exception:
                pass

        enrolled_int = 0
        numbers = re.findall(r"\d+", enrolled_text)
        if numbers:
            enrolled_int = int(numbers[-1])

        remaining_seats = max(0, limit_int - enrolled_int)

        course_data.append({
            "index": i,
            "code": code_text,
            "name": name_text,
            "limit": limit_int,
            "enrolled": enrolled_int,
            "remaining": remaining_seats
        })

        print(f"   [{i}] {code_text} - {name_text}")
        print(f"       -> [系統訊息擷取] {enrolled_text}")
        print(f"       -> 限修: {limit_int}, 已選: {enrolled_int}, 空位: {remaining_seats}")

        time.sleep(random.uniform(0.5, 1.5))

    # Write courses_info.md
    write_courses_markdown(course_data, md_filename)
    return course_data


def write_courses_markdown(course_data: List[Dict[str, Any]], filename: str = "courses_info.md") -> None:
    """Writes course data into standard markdown table format."""
    md_content = "# 預排課程與人數清單\n\n"
    md_content += "> 💡 **使用說明**：請在最左邊的「搶課順序」欄位填寫數字（例如 1, 2, 3...）。\n"
    md_content += "> 數字越小代表越優先搶，不想選的課程請保持空白即可。排好後記得存檔，然後在終端機輸入 `2` 載入此設定。\n\n"
    md_content += "| 搶課順序 | 原編號 | 課程代碼 | 限修人數 | 已選人數 | 剩餘空位 | 課程名稱 |\n"
    md_content += "| :---: | :---: | :--- | :---: | :---: | :---: | :--- |\n"
    for c in course_data:
        md_content += f"|  | **{c['index']}** | `{c['code']}` | {c['limit']} | {c['enrolled']} | **{c['remaining']}** | {c['name']} |\n"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"\n✅ 課程資訊已成功輸出至 markdown 檔案: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"\n⚠️ 無法寫入 markdown 檔案: {e}")


def parse_markdown_priorities(filepath: str) -> List[Dict[str, int]]:
    """Parses priority mapping from courses_info.md file.

    Returns a sorted list of dicts: [{'priority': int, 'index': int}, ...]
    """
    priority_map: List[Dict[str, int]] = []
    if not os.path.exists(filepath):
        return priority_map

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("|") and "原編號" not in line and ":---" not in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    priority_str = parts[1].replace("*", "").strip()
                    index_str = parts[2].replace("*", "").strip()
                    if priority_str.isdigit() and index_str.isdigit():
                        priority_map.append({
                            "priority": int(priority_str),
                            "index": int(index_str)
                        })

    priority_map.sort(key=lambda x: x["priority"])
    return priority_map
