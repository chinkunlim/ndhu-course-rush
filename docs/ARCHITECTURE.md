# 系統架構與服務架構圖 (ARCHITECTURE.md)

本文件詳述 **NDHU Course Selector (東華大學自動選課與預排檢視系統)** 的系統架構設計、核心模組職責與循序互動流程。

---

## 1. 模組分層架構 (src-layout)

```text
src/ndhu_course_selector/
├── __init__.py           # 套件導出介面
├── cli.py                # 終端流程整合主控台
├── core/                 # 核心業務與瀏覽器交互
│   ├── auth.py           # ASP.NET 登入與 evalModal 對話框解除
│   ├── browser.py        # Playwright Chrome 實體與原生 Alert 監聽器
│   ├── parser.py         # grd_subjs 表格爬取、人數提取與 Markdown 雙向同步
│   └── selector.py       # 自訂志願序排程加選與電競擬真微延遲
└── tools/                # 底層輔助工具
    └── config.py         # .env / config.txt 憑證解析器
```

---

## 2. 系統互動循序圖 (Sequence Diagram)

```mermaid
sequenceDiagram
    autonumber
    actor User as 使用者 (Student)
    participant CLI as 終端介面 (cli.py)
    participant Core as 核心模組 (Browser/Auth/Parser)
    participant Page as Playwright Chrome (NDHU Web)
    participant MD as 本機檔案 (courses_info.md)

    User->>CLI: 啟動選課腳本 (uv run auto_login.py)
    CLI->>Core: 讀取設定檔 (.env / config.txt)
    Core->>Page: 啟動真實 Chrome 並導向選課頁面
    Core->>Page: 自動填入學號密碼並點擊登入
    Page-->>Core: 偵測到教學意見彈窗 (evalModal)
    Core->>Page: 自動點擊「取消」跳過彈窗
    Core->>Page: 點擊「查詢預排課程」
    Page-->>Core: 渲染 grd_subjs 課程表格
    loop 每門預排課程
        Core->>Page: 點擊代碼連結觸發 Alert
        Page-->>Core: 原生 Alert 回傳已選人數
        Core->>Core: 擷取數字並計算剩餘空位
    end
    Core->>MD: 輸出表格資料至 courses_info.md
    CLI->>User: 提示確認 (Y: 預設 / 2: 依 md / N: 退出)
    User->>MD: (可選) 編輯最左側欄位調整志願序
    User->>CLI: 輸入 "2"
    CLI->>MD: 解析自訂順序列表
    loop 依志願序排程
        CLI->>Page: 點擊加選按鈕 (若無則跳過)
        Page-->>CLI: 系統對話框 (handle_dialog 自動確認)
        CLI->>CLI: 擬真人流延遲 (20ms~50ms)
    end
    CLI->>User: 搶課結束，瀏覽器保持開啟
```

---

## 3. 關鍵設計原則 (Key Design Principles)
- **非同步事件轉化同步直覺**：Playwright Sync API 提供平順的命令列互動體驗，避免過度複雜的 Async Event Loop 爭用。
- **降級容錯 (Graceful Degradation)**：任何單一課程在提取人數或加選時失敗，均不中斷整體主流程。
- **外部人機互動界面**：將 Markdown 檔案作為 GUI 的輕量級替代方案，兼顧簡單、透明與版本可追溯性。
