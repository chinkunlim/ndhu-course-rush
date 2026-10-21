# ISSUE-003：非選課開放時段之加選按鈕消失

- **狀態**：resolved
- **發現日期**：2026-06-02
- **Agent**：`system`
- **任務**：`TASK-006`

## 1. 現象

在非加退選開放時間（例如提前數天或前幾小時）執行系統進行演練時，表格第一欄為空白，按鈕尚未由伺服器產生。

- **錯誤訊息**：`playwright.sync_api.TimeoutError: Element not visible or missing`
- **重現步驟**：在選課時段外執行加選操作。
- **影響範圍**：加選迴圈。

## 2. 根本原因

伺服器端依時間動態決定是否渲染 `input[type='submit']` 或加選按鈕。

## 3. 修正或規避方式

在點擊加選按鈕前加入 `action_btn.wait_for(state="visible", timeout=500)` 與異常捕獲，不存在時記錄 warning 並安全略過，使離峰 Dry-Run 能順暢進行。

## 4. 防回歸

`src/ndhu_course_rush/services/selector.py` 中的 `_click_course_action`。
