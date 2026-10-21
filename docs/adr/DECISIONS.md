# 架構決策 (Architecture Decision Records)

記錄「為什麼這樣設計」：每個重要的架構取捨一個檔案，之後的人（或 Agent）不用再猜。

- 新增：`python3 .agents/skills/adr-issue-tracker/scripts/tracker_cli.py --add-adr <slug> --title "標題" --agent <名字>`
- 格式：[`_TEMPLATE.md`](_TEMPLATE.md)；在相關程式碼註解加 `Refs: ADR-NNN`。
- 決策被推翻時不要刪檔，把狀態改成 `Superseded by ADR-NNN`。

> 命名規則：`_TEMPLATE.md` 是新增紀錄時要照著寫的範本；紀錄檔命名為 `NNN-<slug>.md`。整個專案只有根目錄一份 `README.md`。

## 總表

| ADR | 標題 | 狀態 | 日期 | 相關程式 |
|---|---|---|---|---|
| [ADR-001](001-playwright-sync.md) | 捨棄 Selenium，全面採用 Playwright Sync API | Accepted | 2026-06-02 | `src/ndhu_course_rush/services/browser.py` |
| [ADR-002](002-headed-chrome.md) | 採用非無頭 (Headed) 原生 Chrome 實體 | Accepted | 2026-06-02 | `src/ndhu_course_rush/services/browser.py` |
| [ADR-003](003-markdown-priority-interface.md) | 採用 Markdown 文件作為優先級排程的人機互動介面 | Accepted | 2026-06-02 | `src/ndhu_course_rush/services/parser.py` |
| [ADR-004](004-tiered-latency.md) | 人性化雙軌隨機微延遲 (Tiered Latency) 策略 | Accepted | 2026-06-03 | `src/ndhu_course_rush/services/selector.py` |
| [ADR-005](005-credential-isolation.md) | 憑證防外洩與安全配置隔離方針 | Accepted | 2026-10-08 | `src/ndhu_course_rush/config/settings.py` |
| [ADR-006](006-modern-layout-and-uv.md) | 導入現代分層架構與 uv 套件管理體系 | Accepted | 2026-10-08 | `pyproject.toml` |
| [ADR-007](007-project-alignment.md) | 專案結構標準化審計與規範對齊機制 | Accepted | 2026-10-08 | `scripts/agentctl.py` |
