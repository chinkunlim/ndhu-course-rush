# 🤝 Agent 狀態看板與交接紀錄 (`LATEST.md`)

> **AI Agent 開工必讀**：進入對話時請先閱讀下方「即時狀態看板」，確認上一位 Agent 的完成進度、待接手任務 (`handed_off`) 與注意事項；詳細過程請看本機的 `.agents/conversations/`。

<!-- LIVE_STATE_START -->
## 📊 即時狀態看板 (Live Snapshot)

- **最後更新時間**: `2026-10-21 17:00 UTC`
- **最近操作 Agent**: `system`
- **目前 Git 分支**: `main`
- **最新 Git Commit**: `84b3357 chore(migrate): move existing project into legacy/, data excluded [agent:migrate_project]`

### 🎯 進行中 / 待接手任務 (Active & Handed-Off Tasks)

| 任務 | 狀態 | 目前/上一位 Agent | 建議接手 | 相關範圍 | 已完成 | 待辦與卡點 |
|---|---|---|---|---|---|---|
| **TASK-001**<br/>遷移批次 1：依賴與設定檔轉換（uv / pnpm / .env.example / Brewfile） | ⚪ `open` | `-` | `-` | `legacy`, `legacy` | - | - |
| **TASK-002**<br/>遷移批次 2：config 層（設定、環境變數讀取） | ⚪ `open` | `-` | `-` | `src/ndhu_course_rush/config/`, `legacy` | - | - |
| **TASK-003**<br/>遷移批次 3：services 層（業務流程） | ⚪ `open` | `-` | `-` | `src/ndhu_course_rush/services/`, `legacy` | - | - |
| **TASK-004**<br/>遷移批次 4：entrypoints 層（CLI、HTTP、排程入口） | ⚪ `open` | `-` | `-` | `src/ndhu_course_rush/entrypoints/`, `legacy` | - | - |
| **TASK-005**<br/>遷移批次 5：測試 | ⚪ `open` | `-` | `-` | `tests/`, `legacy` | - | - |
| **TASK-006**<br/>遷移批次 6：文件（README、規格、決策、已知問題） | ⚪ `open` | `-` | `-` | `docs/PROMPT_TEMPLATES.md`, `docs/adr/`, `docs/architecture/ARCHITECTURE.md`, `docs/known-issues/`, `docs/specs/`, `docs/standards/PROJECT_RULES.md`, `evals/EVALS.md`, `legacy` | - | - |
| **TASK-007**<br/>遷移批次 7：其他（資料、資源、需人工判斷） | ⚪ `open` | `-` | `-` | `docs/standards/PROJECT_RULES.md`, `legacy` | - | - |

<!-- LIVE_STATE_END -->

## 📜 交接與活動時間軸 (Handoff & Activity Timeline)

### [2026-10-21 17:00 UTC] 建立任務 `TASK-007`: 遷移批次 7：其他（資料、資源、需人工判斷） (by `system`)
- **狀態**: `open`
- **相關範圍**: `docs/standards/PROJECT_RULES.md, legacy`

### [2026-10-21 17:00 UTC] 建立任務 `TASK-006`: 遷移批次 6：文件（README、規格、決策、已知問題） (by `system`)
- **狀態**: `open`
- **相關範圍**: `docs/PROMPT_TEMPLATES.md, docs/adr/, docs/architecture/ARCHITECTURE.md, docs/known-issues/, docs/specs/, docs/standards/PROJECT_RULES.md, evals/EVALS.md, legacy`

### [2026-10-21 17:00 UTC] 建立任務 `TASK-005`: 遷移批次 5：測試 (by `system`)
- **狀態**: `open`
- **相關範圍**: `tests/, legacy`

### [2026-10-21 17:00 UTC] 建立任務 `TASK-004`: 遷移批次 4：entrypoints 層（CLI、HTTP、排程入口） (by `system`)
- **狀態**: `open`
- **相關範圍**: `src/ndhu_course_rush/entrypoints/, legacy`

### [2026-10-21 17:00 UTC] 建立任務 `TASK-003`: 遷移批次 3：services 層（業務流程） (by `system`)
- **狀態**: `open`
- **相關範圍**: `src/ndhu_course_rush/services/, legacy`

### [2026-10-21 17:00 UTC] 建立任務 `TASK-002`: 遷移批次 2：config 層（設定、環境變數讀取） (by `system`)
- **狀態**: `open`
- **相關範圍**: `src/ndhu_course_rush/config/, legacy`

### [2026-10-21 17:00 UTC] 建立任務 `TASK-001`: 遷移批次 1：依賴與設定檔轉換（uv / pnpm / .env.example / Brewfile） (by `system`)
- **狀態**: `open`
- **相關範圍**: `legacy, legacy`

### [2026-10-21 17:00 UTC] Initial Bootstrap (by `init_project`)
- **狀態**: 專案已初始化（框架 v3.3.0）。
- **下一步**: 檢視 `.agents/project.toml`，再用 `agentctl task create` 建立第一個任務。
