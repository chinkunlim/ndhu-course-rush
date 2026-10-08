# NDHU Course Selector (東華大學自動選課與預排檢視系統)

[![CI](https://github.com/chinkunlim/PyTest/actions/workflows/ci.yml/badge.svg)](https://github.com/chinkunlim/PyTest/actions)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Package Manager](https://img.shields.io/badge/managed%20by-uv-orange.svg)](https://github.com/astral-sh/uv)
[![Browser Engine](https://img.shields.io/badge/engine-Playwright-green.svg)](https://playwright.dev/)

**NDHU Course Selector** 是一套專為國立東華大學（NDHU）學生設計的自動化選課輔助系統。本專案以 **Playwright** 驅動真實 Chrome 瀏覽器，具備自動登入、彈窗自動解除、預排課程人數分析、以及本機 `courses_info.md` 雙向同步排程搶課等強大功能。

---

## 🌟 核心特點

1. 🖥️ **真機可視化運作 (Headed Chrome)**：啟動本地真實 Chrome 瀏覽器，完整掌握每個動作，絕非黑箱操作。
2. 🛡️ **自動除障與彈窗處理**：登入時自動解除「教學意見評量」DIV 視窗，並智慧攔截並處理系統原生 JavaScript Alert 訊息。
3. 📊 **預排課程動態同步**：登入後自動查詢預排課程，動態爬取每門課的「限修人數」、「已選人數」，計算「剩餘空位」並匯出為好看的 Markdown 表格。
4. 📝 **Markdown 優先級志願序排程**：直接在 `courses_info.md` 最左側填寫志願序號碼（如 0, 1, 2...），系統將嚴格依據您的個人偏好依序加選。
5. ⚡ **擬真人流極速調校**：具備 20ms~50ms 微延遲模擬，既能享有電競級點擊手速，又不易觸發伺服器高頻阻擋。
6. 🎯 **離峰演練模式 (Dry-Run)**：非選課期間亦可安全執行完整預演，自動跳過未出現之加選按鈕，不拋錯崩潰。

---

## 📂 專案架構導覽

```text
PyTest/
├── pyproject.toml               # 現代化專案依賴與工具設定
├── .python-version              # 鎖定 Python 3.11 Runtime
├── Makefile                     # 一鍵操作指令 (dev, test, run, sync)
├── .env.example                 # 帳密配置範本 (請複製為 .env)
│
├── README.md                    # 專案首頁指南
├── AGENTS.md                    # AI Agent 角色定義與協作協定
├── WORKFLOW_GUIDE.md            # 選課 SOP 與實戰操作指南
├── CHANGELOG.md                 # 完整版本歷程記錄
├── DECISIONS.md                 # 重大架構決策 (ADR)
├── KNOWN_ISSUES.md              # 踩坑與已知問題指南
│
├── courses_info.md              # 預排課程清單與自訂順序檔案
├── auto_login.py                # 根目錄向後相容啟動腳本
├── main.py                      # 模組進入點
│
├── src/ndhu_course_selector/    # 標準 src-layout 模組
│   ├── core/                    # 瀏覽器驅動、登入驗證、課表解析與搶課核心
│   └── tools/                   # 配置讀取與輔助工具
│
├── docs/                        # 深度系統架構與部署文檔
├── tests/                       # pytest 單元測試
└── conversations/               # 歷史開發對話 raw 與 summaries 溯源
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

# 安裝 Playwright Chromium / Chrome 支援
uv run playwright install chromium
```

### 3. 設定帳號與密碼
複製環境變數範本並填入您的東華學生證號碼與密碼：
```bash
cp .env.example .env
```
編輯 `.env`：
```ini
NDHU_USERNAME=411383***
NDHU_PASSWORD=your_password_here
LOGIN_URL=https://sys.ndhu.edu.tw/aa/class/subjselect/course_sele.aspx
```
*(系統亦向下相容原有的 `config.txt` 檔案格式)*

### 4. 執行程式
您可透過以下任一方式啟動：
```bash
# 方式 A：使用 Makefile
make run

# 方式 B：透過相容腳本執行
uv run auto_login.py

# 方式 C：透過標準模組執行
uv run python -m ndhu_course_selector
```

---

## 🎮 選課操作流程簡述

1. **自動登入**：程式啟動 Chrome 並自動登入東華選課系統。
2. **生成預排課表**：自動查詢預排課程並統計人數，即時更新 `courses_info.md`。
3. **終端機暫停提示**：
   - 輸入 `Y`：依據網頁原始清單全自動加選。
   - 輸入 `2`：**（推薦）** 讀取您在 `courses_info.md` 中自行標註的志願序加選。
   - 輸入 `N`：退出並安全關閉瀏覽器。

詳細實戰守則與緊急應變請參閱 [WORKFLOW_GUIDE.md](file:///Users/limchinkun/Desktop/PyTest/WORKFLOW_GUIDE.md)。

---

## 🧪 執行自動化測試

本專案具備離線單元測試，驗證課表解析與配置讀取相容性：
```bash
make test
# 或
uv run pytest
```

---

## 📄 授權條款 (License)
本專案採用 [MIT License](file:///Users/limchinkun/Desktop/PyTest/LICENSE) 授權。
