# DECISIONS.md - 架構重大決策記錄 (Architecture Decision Records)

本文件採用 ADR (Architecture Decision Record) 格式，詳實記錄自 2026-06-02 本專案立項以來的重大架構與技術決策、權衡背景與結果。

---

## 目錄
- [ADR-001: 捨棄 Selenium，全面採用 Playwright Sync API](#adr-001-捨棄-selenium全面採用-playwright-sync-api)
- [ADR-002: 採用非無頭 (Headed) 原生 Chrome 實體](#adr-002-採用非無頭-headed-原生-chrome-實體)
- [ADR-003: 採用 Markdown 文件作為優先級排程的人機互動介面](#adr-003-採用-markdown-文件作為優先級排程的人機互動介面)
- [ADR-004: 人性化雙軌隨機微延遲 (Tiered Latency) 策略](#adr-004-人性化雙軌隨機微延遲-tiered-latency-策略)
- [ADR-005: 憑證防外洩與安全配置隔離方針](#adr-005-憑證防外洩與安全配置隔離方針)
- [ADR-006: 導入 src-layout 與 uv 套件管理體系](#adr-006-導入-src-layout-與-uv-套件管理體系)
- [ADR-007: 專案結構標準化審計與 02 指引對齊機制](#adr-007-專案結構標準化審計與-02-指引對齊機制)


---

### ADR-001: 捨棄 Selenium，全面採用 Playwright Sync API
- **狀態**：已採納 (Accepted)
- **日期**：2026-06-02
- **決策背景**：
  - 最初原型曾考量使用 Selenium WebDriver。但東華選課系統大量採用 ASP.NET PostBack 機制與原生 JavaScript `window.alert`。
  - Selenium 在處理突然彈出的 native alert 與非同步 AJAX 表格載入時，容易引發 `UnexpectedAlertPresentException` 或 `StaleElementReferenceException`，且需依賴外部 chromedriver 安裝維護。
- **決策內容**：
  - 全面遷移至 Microsoft Playwright，並採用 `sync_api`（同步 API）符合互動腳本設計。
  - 使用 `page.on("dialog", handle_dialog)` 建立全域彈窗監聽器。
- **結果與影響**：
  - 徹底免除 chromedriver 版本不一致困擾。
  - 原生 alert 攔截成功率達到 100%。

---

### ADR-002: 採用非無頭 (Headed) 原生 Chrome 實體
- **狀態**：已採納 (Accepted)
- **日期**：2026-06-02
- **決策背景**：
  - 選課關乎學分與畢業資格，使用者需要極高的掌控感，不可完全處於 Headless 黑箱狀態。
  - 學校伺服器對無頭 Chromium 可能具備基礎特徵識別。
- **決策內容**：
  - 使用 `browser = p.chromium.launch(headless=False, channel="chrome")`。
- **結果與影響**：
  - 使用者能親眼見證登入與頁面切換狀態。
  - 萬一遭遇驗證碼或緊急狀況，使用者隨時能無縫接手瀏覽器手動操作。

---

### ADR-003: 採用 Markdown 文件作為優先級排程的人機互動介面
- **狀態**：已採納 (Accepted)
- **日期**：2026-06-02
- **決策背景**：
  - 使用者希望在終端執行時自訂選課優先順序，但終端命令列互動（如輸入一長串代碼或陣列）容易打錯字且無法直觀檢視限修人數與餘額。
- **決策內容**：
  - 程式爬取預排課程後，動態寫入 `courses_info.md`，提供預設欄位「搶課順序」。
  - 使用者在 VS Code 或文字編輯器中修改數字並存檔。
  - 終端輸入 `2` 即直接解析該 Markdown 表格取得目標陣列。
- **結果與影響**：
  - 零學習成本，表格視覺化極佳。
  - 資料留底於本機，選課前可反覆推敲最佳志願序。

---

### ADR-004: 人性化雙軌隨機微延遲 (Tiered Latency) 策略
- **狀態**：已採納 (Accepted)
- **日期**：2026-06-03
- **決策背景**：
  - 延遲過長（> 0.5s）會失去搶課優勢；完全零延遲則可能引發封包並發被伺服器誤判為 DoS 攻擊或吞噬 PostBack。
- **決策內容**：
  - **階段 1 (Query Phase)**：150ms 延遲，求穩，確保表格與人數對話盒完全就緒。
  - **階段 2 (Rush Phase)**：20ms ~ 50ms 隨機微延遲，模擬電競選手極限手速特徵。
- **結果與影響**：
  - 搶課速度達到秒級加選，同時保持連線協議之穩定性。

---

### ADR-005: 憑證防外洩與安全配置隔離方針
- **狀態**：已採納 (Accepted)
- **日期**：2026-10-08
- **決策背景**：
  - 舊腳本直接以明文 `config.txt` 存放學號與密碼，且缺乏範本與 `.gitignore` 隔離保護，存在外洩風險。
- **決策內容**：
  - 建立 `.env.example`，將 `.env` 與 `config.txt` 納入 `.gitignore`。
  - 重構配置讀取器，優先讀取系統環境變數，向下相容讀取 `.env` 與舊版 `config.txt`。
  - 所有公開文檔與歷史對話備份中，對真實學號密碼執行正則表達式脫敏遮蔽。
- **結果與影響**：
  - 符合現代軟體工程安全治理規範。

---

### ADR-006: 導入 src-layout 與 uv 套件管理體系
- **狀態**：已採納 (Accepted)
- **日期**：2026-10-08
- **決策背景**：
  - 原專案為根目錄單檔 `auto_login.py`，缺乏模組化、單元測試與現代 Python 包標準。
- **決策內容**：
  - 建立標準 `src/ndhu_course_selector/`（含 `core/` 與 `tools/`），將瀏覽器驅動、身分認證、課表解析與搶課排程拆分模組。
  - 根目錄保留 `auto_login.py` 與 `main.py` 作為相容性進入點。
  - 採用 `uv` 鎖定 Python 3.11 及全部依賴，配置 `pyproject.toml` 與 `pytest`。
- **結果與影響**：
  - 專案架構清晰健全，具備良好的可測試性與可擴展性。

---

### ADR-007: 專案結構標準化審計與 02 指引對齊機制
- **狀態**：已採納 (Accepted)
- **日期**：2026-10-08
- **決策背景**：
  - 為確保專案結構與 Antigravity 規格標準長期保持一致，並符合《02_PROJECT_ALIGN_CHECK_GUIDE.md》的規範治理要求，需要建立可重複驗證的審計機制與工具鏈整合。
- **決策內容**：
  - 納入 `audit_project.py` 於專案根目錄，嚴格檢查 13 項核心檔案、7 項必備目錄與禁止重複/異名舊檔案。
  - 在 `Makefile` 整合 `make audit`，並在 `.github/workflows/ci.yml` CI 流水線中加入合規審計步驟。
  - 依指引步驟 1 與步驟 5 規範，實時歸檔對話歷程至 Milestone 007 (`conversations/`)，並以單一語意 Commit 落地。
- **結果與影響**：
  - 審計驗證可於本地與 CI 自動執行，杜絕文檔漂移或結構退化。

