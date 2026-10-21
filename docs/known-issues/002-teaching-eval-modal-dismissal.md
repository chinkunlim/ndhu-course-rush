# ISSUE-002：教學意見評量 DIV 彈窗遮擋按鈕

- **狀態**：resolved
- **發現日期**：2026-06-02
- **Agent**：`system`
- **任務**：`TASK-006`

## 1. 現象

登入進入選課主畫面時，若該學期有尚未填寫的教學評量，系統會跳出 jQuery UI 對話框遮蔽底下的按鈕，導致後續點擊逾時（TimeoutError）。

- **錯誤訊息**：`playwright.sync_api.TimeoutError: Timeout 5000ms exceeded while waiting for locator`
- **重現步驟**：有未填寫教學意見之帳號登入系統。
- **影響範圍**：登入後至點擊查詢按鈕階段。

## 2. 根本原因

系統彈窗覆蓋主頁面圖層（z-index 較高），使底層元素不可被點擊。

## 3. 修正或規避方式

在登入成功後，主動探測 `div[aria-describedby='evalModal'] button:has-text('取消')`，若在 5 秒內出現則自動點擊關閉，未出現則安靜略過。

## 4. 防回歸

`src/ndhu_course_rush/services/auth.py` 中的 `_dismiss_survey_modal` 函式。
