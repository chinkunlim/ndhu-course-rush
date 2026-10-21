# ISSUE-001：ASP.NET PostBack 機制與 DOM 延遲競態

- **狀態**：resolved
- **發現日期**：2026-06-02
- **Agent**：`system`
- **任務**：`TASK-006`

## 1. 現象

點擊「查詢預排課程」或加選按鈕後，頁面並非一般 SPA 路由切換，而是 ASP.NET 典型的整頁 PostBack。
若在點擊後立即尋找表格或按鈕，可能會抓到舊頁面的舊節點，或是此時表格僅渲染出 `<table>` 骨架而內部的 `<tr>` 與 `<td>` 尚未被 AJAX 填充，誤判表格只有 1 列。

- **錯誤訊息**：`IndexError` 或僅抓取到表頭導致預排課程清單為空。
- **重現步驟**：在網路延遲較高時點擊查詢按鈕並立即遍歷 rows。
- **影響範圍**：預排課程表格解析。

## 2. 根本原因

ASP.NET PostBack 機制非同步替換 DOM 內容，DOM 骨架出現與資料填充存在時間差。

## 3. 修正或規避方式

使用 `table.locator('tr:has(td)').first.wait_for(state='visible', timeout=5000)`，確認至少包含實體 `td` 之資料列已渲染，並搭配 `page.wait_for_load_state('networkidle')`。

## 4. 防回歸

`src/ndhu_course_rush/services/parser.py` 中的 `query_and_parse_courses` 包含資料列等待邏輯。
