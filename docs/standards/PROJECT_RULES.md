# 本專案專屬規則 (PROJECT_RULES)

> 規則分兩層：`docs/standards/` 的其他文件是**所有專案通用**的規範（由專案模板提供，`agentctl update` 會更新）；
> 本檔是**只適用這個專案**的規則，由這個專案自己維護，模板更新時不會被覆蓋。每次開工都要讀。

## 1. 領域知識與術語

- **東華選課系統**：網址為 `https://sys.ndhu.edu.tw/aa/class/subjselect/course_sele.aspx`，微軟 ASP.NET WebForms 典型架構，高度依賴 `__doPostBack`。
- **預排課程 (Pre-scheduled Courses)**：學生在選課開放前於系統預排的目標課程清單。
- **志願序 (Priority Order)**：使用者在 `courses_info.md` 最左側自訂填寫的搶課優先級順序（數字越小越優先，如 0, 1, 2...）。
- **Dry-Run (離峰演練)**：在非加退選開放時間執行系統，確認登入、表格查詢與排序邏輯正常，安全略過不存在的加選按鈕。
- **雙軌微延遲 (Tiered Latency)**：查詢階段使用穩定延遲（150ms），加選衝刺階段使用隨機微延遲（20ms~50ms），模擬真人電競手速。

## 2. 本專案特有的規則

1. **真實 Chrome 優先**：預設使用 `channel="chrome"` 啟動原生 Chrome 瀏覽器，確保使用者可親眼見證操作；Playwright 同步 API 進行 dialog 監聽。
2. **安全與憑證隔離**：
   - 學號與密碼一律放置於 `.env`，嚴禁寫死於程式碼或 commit 至版控。
   - 歷史紀錄與公開文件一律遮蔽真實學號與密碼。
3. **選課 SOP 作戰時程**：
   - 開放前 1 天：執行 `uv sync`、跑單元測試並執行 Dry-Run 演練。
   - 開放前 15 分鐘：執行程式查詢最新名額並在 `courses_info.md` 標註志願序存檔。
   - 開放前 2 分鐘：陣位就緒，終端鍵入 `2` 等候倒數。
   - 開放瞬間 (00 秒)：按下 Enter 執行極速加選。

## 3. 和通用規範不同的例外（要寫理由）

- 無特殊例外。所有 Python 模組嚴格遵循單向分層（`entrypoints ➔ adapters ➔ services ➔ domain ➔ config`）與 mypy strict 檢查。

## 4. 禁止事項

- 嚴禁在 `services` 或 `adapters` 層呼叫 `print()`；終端輸出僅限 `entrypoints`。
- 嚴禁略過或寫死憑證資訊。
- 嚴禁未經使用者同意執行 `git push`。
