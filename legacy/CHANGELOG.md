# CHANGELOG.md - 版本演進歷程

本專案遵循 [Semantic Versioning 2.0.0](https://semver.org/) 規範，記錄所有里程碑版本與功能變更。

---

## [Unreleased]
### 🛠️ 規範對齊與審計強化 (Project Alignment & Compliance)
- **合規審計**：引入 `audit_project.py`，完整涵蓋目錄結構、核心檔案與異名重複檢查。
- **工具鏈整合**：`Makefile` 新增 `make audit` 目標；`.github/workflows/ci.yml` CI 新增合規審計步驟。
- **決策與對話同步**：追加 ADR-007 架構決策記錄，歸檔 Milestone 007 對話溯源 (`raw/` 與 `summaries/`)。

---

## [1.0.0] - 2026-10-08

### 🚀 架構與規格重構 (Project Standardization)
- **架構升級**：全專案重構為現代標準 `src-layout`（`src/ndhu_course_selector/`）。
- **模組化分層**：
  - `core.browser`：負責真實 Chrome 實體管理與原生 Alert 監聽。
  - `core.auth`：負責帳號密碼登入與教學評量 DIV 彈窗自動解除。
  - `core.parser`：負責 ASP.NET 表格爬取、名額彈窗讀取與 `courses_info.md` 雙向同步。
  - `core.selector`：負責自訂優先序選課排程與電競級延遲微調。
  - `tools.config`：相容 `.env` 與舊版 `config.txt` 解析。
- **向後相容**：根目錄保留 `auto_login.py` 與 `main.py` 作為進入點包裝器。
- **自動化測試**：引入 `pytest`，撰寫配置讀取與 Markdown 課表解析單元測試（`tests/`）。
- **CI/CD**：新增 GitHub Actions 測試流水線（`.github/workflows/ci.yml`）。
- **治理規範**：完整建立 `AGENTS.md`、`WORKFLOW_GUIDE.md`、`DECISIONS.md`、`KNOWN_ISSUES.md`。
- **對話全量備份**：歷史 33 輪開發對話及重構對話全數備份至 `conversations/raw/` 並產生 6 份獨立 `conversations/summaries/`。

---

## [0.4.0] - 2026-06-03
### ⚡ 擬真人流延遲調校與速度極大化
- **雙軌延遲機制 (Tiered Latency)**：
  - 登入與查人數階段採用穩定延遲（150ms），確保 ASP.NET ViewState 穩定渲染。
  - 搶課衝刺階段採用極限微延遲（20ms~50ms），模擬電競選手反應手速。
- **PostBack 等待優化**：移除非必要之長休眠，只等待關鍵 DOM 節點渲染。

---

## [0.3.0] - 2026-06-02
### ✨ 自訂搶課志願序與乾跑演練 (Dry-run)
- **Markdown 課表同步**：自動生成 `courses_info.md`，提供直觀的 Markdown 表格讓使用者標註搶課順序（0, 1, 2...）。
- **互動選單**：
  - `Y`：依網頁預設順序點擊。
  - `2`：依使用者修改之 `courses_info.md` 順序搶課。
  - `N`：退出並安全關閉瀏覽器。
- **無按鈕容錯**：在非選課開放時段執行預演時，能安全偵測到按鈕不存在並跳過，不拋錯崩潰。
- **名額即時探查**：自動點擊課程代碼並攔截原生 Alert 訊息，即時提取「限修人數」、「已選人數」並計算「剩餘空位」。

---

## [0.2.0] - 2026-06-02
### 🔍 預排課程查詢與表格渲染修正
- **查詢預排**：登入後自動點選 `ContentPlaceHolder1_Button7` 載入預排清單。
- **表格列數修正**：修正 ASP.NET 資料列選擇器為 `tr:has(td)`，解決誤將整張表格判斷為單一列的計算錯誤。
- **安全退出**：解決使用者輸入 `N` 關閉瀏覽器時引發之 Playwright SyncBase 背景例外。

---

## [0.1.0] - 2026-06-02
### 🎉 專案誕生 (Initial Proof-of-Concept)
- **工具選型**：放棄 Selenium，改採 Playwright Sync API。
- **環境初始化**：使用 `uv` 建立虛擬環境與套件管理。
- **真實瀏覽器啟動**：透過 `channel="chrome"` 啟動獨立非無頭 Chrome 視窗。
- **登入自動化**：自動填寫東華大學選課系統學號密碼。
- **彈窗解除**：自動關閉教學意見評量（`evalModal`）彈窗。
