# ISSUE-005：Playwright 與 Chrome 背景進程關閉衝突

- **狀態**：resolved
- **發現日期**：2026-06-03
- **Agent**：`system`
- **任務**：`TASK-006`

## 1. 現象

使用者在終端結束程式時，若直接關閉瀏覽器，有時會伴隨 `SyncBase._sync.<locals>.<lambda>` 非同步回呼警告。

- **錯誤訊息**：`Exception ignored in: <function SyncBase.__del__>`
- **重現步驟**：監聽器未解除時強制退出。
- **影響範圍**：瀏覽器資源回收。

## 2. 根本原因

事件監聽器尚未從 page 實體解除綁定時，底層連線已被強制切斷。

## 3. 修正或規避方式

在關閉瀏覽器前，先解除對話盒事件監聽器（`remove_listener`），並將清理步驟包裹於 `try...except` 區塊中，確保終端無噪音乾淨退出。

## 4. 防回歸

`src/ndhu_course_rush/services/browser.py` 中的 `create_browser_session` context manager 包含清理邏輯。
