# KNOWN_ISSUES.md - 已知問題與避坑避障指南

本文件記錄東華大學選課系統技術特徵、曾踩過的坑、現有機制與建議之因應處置措施。

---

## 1. ASP.NET PostBack 機制與 DOM 延遲競態 (Race Conditions)
- **現象**：
  - 點擊「查詢預排課程」或加選按鈕後，頁面並非一般 SPA 路由切換，而是 ASP.NET 典型的整頁 PostBack。
  - 若在點擊後立即尋找表格或按鈕，可能會抓到舊頁面的舊節點，或是此時表格僅渲染出 `<table>` 骨架而內部的 `<tr>` 與 `<td>` 尚未被 AJAX 填充。
- **曾踩過的坑**：
  - 歷史對話初期，終端曾誤判表格「只有 1 列」（誤判為單一表頭列），導致無法正確遍歷 14 門預排課程。
- **當前避障方案**：
  - 程式中使用 `table.locator('tr:has(td)').first.wait_for(state='visible', timeout=5000)`，確認至少包含實體 `td` 之資料列已渲染，並搭配 `page.wait_for_load_state('networkidle')`。

---

## 2. 教學意見評量 DIV 彈窗攔截 (Eval Modal)
- **現象**：
  - 登入進入選課主畫面時，若該學期有尚未填寫的教學評量，系統會跳出 jQuery UI 風格的對話框：
    `<div aria-describedby="evalModal">...</div>`
  - 此視窗若未點擊「取消」或關閉，會遮蔽底下的「查詢預排課程」按鈕，導致後續點擊逾時（Timeout）。
- **當前避障方案**：
  - 在登入成功進入主畫面後，程式主動探測 `div[aria-describedby='evalModal'] button:has-text('取消')`，若在 5 秒內出現則自動點擊予以關閉，若未出現則安靜跳過。

---

## 3. 非選課開放時段之加選按鈕消失
- **現象**：
  - 在非加退選開放時間（例如提前數天或前幾小時）執行系統時，預排課程表格的第一欄是空白的（加選按鈕 `Button` 尚未被伺服器產生）。
- **曾踩過的坑**：
  - 若直接尋找按鈕 locator 並進行點擊，Playwright 會因找不到元素而拋出 `TimeoutError` 崩潰退出。
- **當前避障方案**：
  - 在加選點擊迴圈中加入存在性防護檢測：
    ```python
    btn = row.locator("td:nth-child(1) input[type='submit']")
    if btn.count() == 0:
        print(f"⚠️ 編號 [{idx}] 沒有可點擊的加選按鈕，跳過。")
        continue
    ```
  - 此舉確保了系統具備離峰全流程預演（Dry-Run）的能力。

---

## 4. 終端機日誌列印 (Terminal I/O) 對反應時延之影響
- **評估議題**：
  - 在關鍵搶課迴圈中，終端列印 `print()` 是否會拖慢毫秒級反應速度？
- **實測與分析結論**：
  - 在 macOS / Linux 終端環境下，單行 `print()` 耗時通常小於 0.05 毫秒（Microseconds 級別），相較於網際網路往返時間（RTT 10~30ms）影響極微。
  - 然而，過度冗長或包含大量字串拼接的輸出仍應避免。當前設計在搶課階段僅印出關鍵動作，保證最高純粹執行效率。

---

## 5. Playwright 與 Chrome 背景進程關閉衝突
- **現象**：
  - 使用者在終端選擇 `N` 結束程式時，若直接呼叫 `browser.close()`，有時會伴隨 `SyncBase._sync.<locals>.<lambda>` 非同步回呼警告。
- **當前避障方案**：
  - 在關閉瀏覽器前，先解除對話盒事件監聽器，並將清理步驟包裹於 `try...except` 區塊中，確保終端無噪音乾淨退出。
