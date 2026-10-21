# 已知問題 (Known Issues)

記錄「遇到什麼坑、根因是什麼、怎麼避開」：一個問題一個檔案。

- 新增：`python3 .agents/skills/adr-issue-tracker/scripts/tracker_cli.py --add-issue <slug> --title "標題" --status open`
- 格式：[`_TEMPLATE.md`](_TEMPLATE.md)；在相關程式碼註解加 `Refs: ISSUE-NNN`。
- 狀態：`open`（調查中）／`mitigated`（已規避）／`resolved`（已修復並有防回歸測試）。

> 命名規則：`_TEMPLATE.md` 是新增紀錄時要照著寫的範本；紀錄檔命名為 `NNN-<slug>.md`。整個專案只有根目錄一份 `README.md`。

## 總表

| ISSUE | 標題 | 狀態 | 發現日期 | 相關程式 |
|---|---|---|---|---|
| [ISSUE-001](001-aspnet-postback-race-condition.md) | ASP.NET PostBack 機制與 DOM 延遲競態 | resolved | 2026-06-02 | `src/ndhu_course_rush/services/parser.py` |
| [ISSUE-002](002-teaching-eval-modal-dismissal.md) | 教學意見評量 DIV 彈窗遮擋按鈕 | resolved | 2026-06-02 | `src/ndhu_course_rush/services/auth.py` |
| [ISSUE-003](003-missing-buttons-in-offpeak.md) | 非選課開放時段之加選按鈕消失 | resolved | 2026-06-02 | `src/ndhu_course_rush/services/selector.py` |
| [ISSUE-004](004-terminal-print-latency.md) | 終端機日誌列印對反應時延之影響 | resolved | 2026-06-03 | `src/ndhu_course_rush/services/` |
| [ISSUE-005](005-playwright-shutdown-cleanup.md) | Playwright 與 Chrome 背景進程關閉衝突 | resolved | 2026-06-03 | `src/ndhu_course_rush/services/browser.py` |
