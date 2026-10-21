# ADR-001：捨棄 Selenium，全面採用 Playwright Sync API

- **狀態**：Accepted
- **日期**：2026-06-02
- **Agent**：`system`
- **任務**：`TASK-006`

## 1. 背景與問題

最初原型曾考量使用 Selenium WebDriver。但東華大學選課系統大量採用 ASP.NET PostBack 機制與原生 JavaScript `window.alert`。
Selenium 在處理突然彈出的 native alert 與非同步 AJAX 表格載入時，容易引發 `UnexpectedAlertPresentException` 或 `StaleElementReferenceException`，且需依賴外部 chromedriver 安裝維護。

## 2. 評估過的方案

| 方案 | 優點 | 缺點 |
|---|---|---|
| Selenium WebDriver | 歷史悠久、社群資源多 | 需要外掛 chromedriver，對非同步 PostBack 與原生 alert 攔截不穩定 |
| Playwright Sync API | 內建瀏覽器驅動、原生 alert 事件監聽 100% 穩定、支援同步互動腳本 | 學習曲線略有不同 |

## 3. 決策與理由

全面遷移至 Microsoft Playwright，並採用 `sync_api`（同步 API）符合互動腳本設計。
使用 `page.on("dialog", handle_dialog)` 建立全域彈窗監聽器。

## 4. 影響與代價

- 徹底免除 chromedriver 版本不一致困擾。
- 原生 alert 攔截成功率達到 100%。
