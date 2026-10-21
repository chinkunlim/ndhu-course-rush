# NDHU Course Rush (東華大學自動選課與預排檢視系統)

> 國立東華大學（NDHU）學生專屬自動化選課與預排檢視輔助系統。以 **Playwright** 驅動真實 Chrome 瀏覽器，具備自動登入、評量彈窗解除、預排課表抓取與人數分析、以及本機 `courses_info.md` 雙向同步排程搶課等完整功能。

---

## 🌟 核心特點

1. 🖥️ **真機可視化運作 (Headed Chrome)**：啟動本地真實 Chrome 瀏覽器，完整掌握每個動作，絕非黑箱操作。
2. 🛡️ **自動除障與彈窗處理**：登入時自動解除「教學意見評量」DIV 視窗，並智慧攔截並處理系統原生 JavaScript Alert 訊息。
3. 📊 **預排課程動態同步**：登入後自動查詢預排課程，動態爬取每門課的「限修人數」、「已選人數」，計算「剩餘空位」並匯出為好看的 Markdown 表格。
4. 📝 **Markdown 優先級志願序排程**：直接在 `courses_info.md` 最左側填寫志願序號碼（如 0, 1, 2...），系統將嚴格依據個人偏好依序加選。
5. ⚡ **擬真人流極速調校**：具備 20ms~50ms 微延遲模擬，既能享有電競級點擊手速，又不易觸發伺服器高頻阻擋。
6. 🎯 **離峰演練模式 (Dry-Run)**：非選課期間亦可安全執行完整預演，自動跳過未出現之加選按鈕，不拋錯崩潰。

---

## 📂 專案架構導覽

```text
ndhu-course-rush/
├── pyproject.toml               # 現代化專案依賴與工具設定 (uv 管理)
├── .env.example                 # 帳密配置範本 (複製為 .env)
├── README.md                    # 專案首頁指南
├── AGENTS.md                    # AI Agent 規範與協同指引
├── CHANGELOG.md                 # 完整版本歷程記錄
├── courses_info.md              # 預排課程清單與自訂順序檔案
├── main.py                      # 根目錄執行入口
│
├── src/ndhu_course_rush/        # 核心原始碼 (單向分層)
│   ├── config/                  # 設定層 (AppConfig, logging, legacy_config)
│   ├── domain/                  # 領域模型 (Course, CoursePriority)
│   ├── services/                # 業務邏輯 (auth, browser, parser, selector)
│   └── entrypoints/             # 進入點 (CLI, main)
│
├── docs/                        # 架構、規格、ADR 與已知問題庫
│   ├── adr/                     # 架構決策記錄 (ADR-001 ~ ADR-007)
│   ├── architecture/            # 系統架構圖與目錄樹
│   ├── known-issues/            # 已知問題與避坑指南 (ISSUE-001 ~ ISSUE-005)
│   ├── specs/                   # 功能規格 (SPEC-001)
│   └── standards/               # 工程規範與本專案專屬規則 (PROJECT_RULES.md)
│
├── scripts/                     # 專案腳本 (agentctl.py, auto_login.py)
└── tests/                       # 單元測試套件
```

---

## 🚀 快速上手 (Quick Start)

### 1. 必備環境
- 作業系統：macOS / Linux / Windows
- [uv](https://github.com/astral-sh/uv) (極速 Python 套件管理器)
- Google Chrome 瀏覽器

### 2. 安裝依賴與驅動
```bash
# 同步安裝專案虛擬環境與依賴
uv sync

# 安裝 Playwright 瀏覽器核心
uv run playwright install chromium
```

### 3. 設定帳號與密碼
複製環境變數範本並填入東華學生證號碼與密碼：
```bash
cp .env.example .env
```
編輯 `.env`：
```ini
NDHU_USERNAME=411383***
NDHU_PASSWORD=your_password_here
LOGIN_URL=https://sys.ndhu.edu.tw/aa/class/subjselect/course_sele.aspx
```

### 4. 執行程式
您可透過以下任一方式啟動：
```bash
# 方式 A：透過 CLI 工具
uv run ndhu-course-rush

# 方式 B：透過根目錄入口腳本
uv run python main.py

# 方式 C：僅查詢預排課表不搶課
uv run ndhu-course-rush --query-only
```

---

## 🎮 選課操作流程簡述

1. **自動登入**：程式啟動 Chrome 並自動登入東華選課系統。
2. **查詢預排**：自動爬取預排清單中各科目限額與空位，輸出 `courses_info.md`。
3. **設定志願序**：在 `courses_info.md` 最左側填寫志願序號（例如 0, 1, 2...）並存檔。
4. **搶課衝刺**：終端輸入 `2`，系統將以極速微延遲自動完成加選！

---

## 🧪 執行測試與品質檢查

```bash
# 執行所有單元測試
uv run python -m unittest discover -s tests -v

# 執行靜態程式碼審查與分層檢查
python3 scripts/agentctl.py check
```
