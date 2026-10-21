# 系統架構 (Architecture)

> 手動維護本檔的「系統概覽」；以下報告由工具自動產生，請勿手動修改。

| 文件 | 內容 | 產生方式 |
|---|---|---|
| [`PROJECT_TREE.md`](PROJECT_TREE.md) | 完整目錄樹 | `agentctl sync` / 每次 commit |
| `GRAPH_REPORT.md` | 模組依賴圖、分層檢查、函式大小 | 需要時 `agentctl graph`（不進 git） |
| `AGENT_AUDIT_REPORT.md` | 各 Agent 的 commit 與任務 | 需要時 `agentctl audit`（不進 git） |

## 系統概覽

**NDHU Course Rush** 是一套以 Microsoft Playwright 驅動原生 Chrome 瀏覽器的國立東華大學自動化選課與預排課程檢視系統。
系統透過單向分層架構，自動化處理憑證登入、教學評量彈窗解除、預排課表抓取、名額空位即時計算、`courses_info.md` 雙向同步以及自訂志願序極速加選。

```mermaid
sequenceDiagram
    autonumber
    actor User as 使用者
    participant CLI as Entrypoints (CLI / main.py)
    participant Auth as Services (auth.py)
    participant Browser as Services (browser.py)
    participant Parser as Services (parser.py)
    participant Selector as Services (selector.py)
    participant Portal as 東華選課系統 (ASP.NET)

    User->>CLI: 啟動選課程式 (uv run ndhu-course-rush)
    CLI->>Browser: 啟動 Chrome 並註冊原生 Alert 監聽器
    CLI->>Auth: 執行登入 (perform_login)
    Auth->>Portal: 提交學號與密碼
    Auth->>Portal: 檢查並關閉教學評量 DIV 彈窗 (evalModal)
    CLI->>Parser: 查詢預排課程 (query_and_parse_courses)
    Parser->>Portal: 點選「查詢預排課程」載入表格
    loop 每一門預排課程
        Parser->>Portal: 點選課程代碼觸發原生 Alert
        Portal-->>Parser: 回傳限修與已選人數
    end
    Parser-->>User: 輸出 courses_info.md Markdown 課表
    User->>User: 於 courses_info.md 排定「搶課順序」
    User->>CLI: 觸發加選 (輸入 2 依自訂順序)
    CLI->>Selector: 執行選課 (execute_course_selection)
    loop 依志願序加選
        Selector->>Portal: 點選加選按鈕 (搭配 20~50ms 人性化微延遲)
        Portal-->>Selector: 原生 Alert 確認加選結果
    end
    CLI-->>User: 完成搶課並保持瀏覽器就位供檢視
```

## 分層

見 `.agents/project.toml` 的 `[architecture] layers` 與 [`ARCHITECTURE_RULES.md`](../standards/ARCHITECTURE_RULES.md)。
- **entrypoints**: `cli.py` 與 `main.py`
- **adapters**: 外部整合
- **services**: `auth.py`, `browser.py`, `parser.py`, `selector.py`
- **domain**: `Course`, `CoursePriority`
- **config**: `AppConfig`, `settings.py`, `legacy_config.py`
