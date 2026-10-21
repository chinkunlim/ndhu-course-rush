# 專案遷移計畫 (MIGRATION)

> 舊專案的檔案目前在 `legacy/`（原封不動）。依下方批次逐一搬到新結構，**每一批都要符合新專案的所有規範**，全部完成後刪除 `legacy/`。

## 1. 來源

- **舊專案位置**：`/Users/limchinkun/Desktop/projects/Old/PyTest`
- **舊專案遠端**：`-`
- **遷移時的最後 commit**：`6caf1d2`
- **git 歷史**：已保留（新 repo 由舊 repo clone；舊檔案以 `git mv` 移到 `legacy/`，`git log --follow` 可追溯）
- **模式**：開發模式：Flask 必須全部改寫成 FastAPI（對照表：[`FLASK_TO_FASTAPI.md`](../../.agents/skills/legacy-migration/FLASK_TO_FASTAPI.md)）（舊專案未使用 Flask）
- **建立時間**：2026-10-21 17:00 UTC
- **檔案數**：62

## 2. 完成標準

### 每一批

每一批都必須做到（做到才可 `agentctl task done`）：

1. **兩個 commit：先搬、再整理**（保證 `git log --follow` 與 blame 追得到舊歷史）：
   - 第一個 commit 只用 `git mv legacy/舊路徑 新路徑` 搬移，內容一個字都不改：`agentctl commit --bump none -m "refactor(migration): move <檔名> from legacy"`。pre-commit 只對「從 legacy/ 原樣搬入」的檔案暫時放行註解、大小、分層與 print 問題（秘密與禁用套件仍會擋）。
   - 下一個 commit 必須把這批檔案全部整理到符合規範（第 2 點），否則任何 commit 與 `agentctl check` 都過不了，所以一批只搬少量檔案。
2. 依新規範修改：
   - **註解**：檔案開頭用途說明；每個函數/類別的說明、每個參數（`Args:` / `@param`）與回傳值（[`CODING_PRINCIPLES.md`](../standards/CODING_PRINCIPLES.md) §0）。
   - **型別**：Python 參數與回傳值都有型別，`uv run mypy` 通過（strict）。
   - **分層**：放到正確的層；環境變數只在 `config` 層讀取，其他層改收 `AppConfig` 參數（[`ARCHITECTURE_RULES.md`](../standards/ARCHITECTURE_RULES.md)）。
   - **函式大小**：符合 `[quality]` 門檻。
   - **Log**：除了 entrypoints，`print` 一律改成模組 logger；關鍵步驟、外部呼叫與例外都要記 log（[`CODING_PRINCIPLES.md`](../standards/CODING_PRINCIPLES.md) §0.4）。
   - **秘密**：金鑰移到 `.env`，`.env.example` 只留變數名稱。
   - **依賴**：只用 `uv add` / `pnpm add`（[`ENVIRONMENT_AND_DEPENDENCIES.md`](../standards/ENVIRONMENT_AND_DEPENDENCIES.md)）。
   - **本機服務**：綁 `127.0.0.1`，網址不用 `localhost`。
   - **測試**：搬移的程式要有測試（沿用舊測試或補寫，[`TESTING_AND_QUALITY.md`](../standards/TESTING_AND_QUALITY.md)）。
3. `python3 scripts/agentctl.py check` 與專案測試全部通過。
4. 下方「檔案清單」把這批的 ☐ 改成 ☑；過程中的重要決策寫 ADR、發現的舊 bug 寫 known-issue。
5. `python3 scripts/agentctl.py commit --agent <名字> --task TASK-NNN`，再 `agentctl task done TASK-NNN --summary ...`。

### 整個遷移

全部完成才算遷移成功（`python3 scripts/agentctl.py migration --verify` 會逐項檢查）：

- [ ] `legacy/` 已刪除（所有檔案都搬到新結構或確認不需要）。
- [ ] 舊資料已依 §4.5 複製到 `DATA_DIR`，程式透過 config 讀取路徑，專案資料夾內沒有資料檔。
- [ ] 沒有 `requirements.txt`、`package-lock.json`、`yarn.lock`、`Pipfile`：依賴只在 `pyproject.toml` + `uv.lock`、`package.json` + `pnpm-lock.yaml`。
- [ ] `python3 scripts/agentctl.py check` 全部通過（註解、分層、秘密、lint、mypy strict、目錄樹）。
- [ ] 專案測試全部通過。
- [ ] 所有遷移任務卡都是 `done`。
- [ ] 模板的範例程式（`greeting` 相關的 services / domain / cli / api / 資料表 `greetings` 與其 Alembic revision、測試）已刪除或換成真正的程式。
- [ ] `README.md` 改寫為這個專案的說明；`docs/architecture/ARCHITECTURE.md` 有系統概覽；主要功能在 `docs/specs/` 有規格。
- [ ] 舊專案已知的問題記在 `docs/known-issues/`；遷移中的重要決策記在 `docs/adr/`。
- [ ] `.env.example` 列出所有需要的變數（只有名稱）。
- [ ] 最後執行 `agentctl closeout`（本機對話紀錄＋交接看板記下遷移完成）。

## 3. 批次

| 順序 | 任務 | 內容 | 檔案數 |
|---|---|---|---|
| 1 | `TASK-001` | 依賴與設定檔轉換（uv / pnpm / .env.example / Brewfile） | 4 |
| 2 | `TASK-002` | config 層（設定、環境變數讀取） | 1 |
| 3 | `TASK-003` | services 層（業務流程） | 9 |
| 4 | `TASK-004` | entrypoints 層（CLI、HTTP、排程入口） | 2 |
| 5 | `TASK-005` | 測試 | 3 |
| 6 | `TASK-006` | 文件（README、規格、決策、已知問題） | 36 |
| 7 | `TASK-007` | 其他（資料、資源、需人工判斷） | 7 |

## 4. 依賴轉換

舊專案有 pyproject.toml / setup.py / Pipfile：把其中的依賴逐一用 uv add 加入，再比對版本：

```bash
uv tree
```

舊 `.env.example` 的變數（加到新 `.env.example`，只寫名稱）：`NDHU_USERNAME`、`NDHU_PASSWORD`、`LOGIN_URL`、`RUSH_DELAY`、`QUERY_DELAY`

## 4.5 資料搬到 DATA_DIR（資料不進新專案）

- 舊專案沒有偵測到資料檔。

## 5. 風險

- 未發現機密檔或大型檔案。

## 6. 檔案清單

| 狀態 | 舊檔案 | 建議位置 | 批次 |
|---|---|---|---|
| ☐ | `legacy/.env.example` | `pyproject.toml / package.json / .env.example（轉換後刪除舊檔）` | deps |
| ☐ | `legacy/.gitignore` | `pyproject.toml / package.json / .env.example（轉換後刪除舊檔）` | deps |
| ☐ | `legacy/.python-version` | `pyproject.toml / package.json / .env.example（轉換後刪除舊檔）` | deps |
| ☐ | `legacy/pyproject.toml` | `pyproject.toml / package.json / .env.example（轉換後刪除舊檔）` | deps |
| ☐ | `legacy/src/ndhu_course_selector/tools/config.py` | `src/ndhu_course_rush/config/` | config |
| ☐ | `legacy/audit_project.py` | `src/ndhu_course_rush/services/` | services |
| ☐ | `legacy/auto_login.py` | `src/ndhu_course_rush/services/` | services |
| ☐ | `legacy/src/ndhu_course_selector/__init__.py` | `src/ndhu_course_rush/services/` | services |
| ☐ | `legacy/src/ndhu_course_selector/core/__init__.py` | `src/ndhu_course_rush/services/` | services |
| ☐ | `legacy/src/ndhu_course_selector/core/auth.py` | `src/ndhu_course_rush/services/` | services |
| ☐ | `legacy/src/ndhu_course_selector/core/browser.py` | `src/ndhu_course_rush/services/` | services |
| ☐ | `legacy/src/ndhu_course_selector/core/parser.py` | `src/ndhu_course_rush/services/` | services |
| ☐ | `legacy/src/ndhu_course_selector/core/selector.py` | `src/ndhu_course_rush/services/` | services |
| ☐ | `legacy/src/ndhu_course_selector/tools/__init__.py` | `src/ndhu_course_rush/services/` | services |
| ☐ | `legacy/main.py` | `src/ndhu_course_rush/entrypoints/` | entrypoints |
| ☐ | `legacy/src/ndhu_course_selector/cli.py` | `src/ndhu_course_rush/entrypoints/` | entrypoints |
| ☐ | `legacy/tests/__init__.py` | `tests/` | tests |
| ☐ | `legacy/tests/test_config.py` | `tests/` | tests |
| ☐ | `legacy/tests/test_parser.py` | `tests/` | tests |
| ☐ | `legacy/.github/CONTRIBUTING.md` | `docs/standards/PROJECT_RULES.md（只留本專案特有的規則；通用規則已在 AGENTS.md / standards）` | docs |
| ☐ | `legacy/.github/SECURITY.md` | `README.md 的安全說明，或 docs/standards/PROJECT_RULES.md` | docs |
| ☐ | `legacy/AGENTS.md` | `docs/standards/PROJECT_RULES.md（只留本專案特有的規則；通用規則已在 AGENTS.md / standards）` | docs |
| ☐ | `legacy/CHANGELOG.md` | `CHANGELOG.md（舊版本紀錄貼在 0.1.0 下方，保留原日期）` | docs |
| ☐ | `legacy/DECISIONS.md` | `docs/adr/（每個決策拆成一個 NNN-*.md，用 adr-issue-tracker）` | docs |
| ☐ | `legacy/KNOWN_ISSUES.md` | `docs/known-issues/（每個問題一個 NNN-*.md）` | docs |
| ☐ | `legacy/README.md` | `README.md（改寫成新專案的說明）` | docs |
| ☐ | `legacy/WORKFLOW_GUIDE.md` | `docs/standards/PROJECT_RULES.md（只留本專案特有的規則；通用規則已在 AGENTS.md / standards）` | docs |
| ☐ | `legacy/conversations/completed/001_playwright_and_login.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/completed/002_dialog_and_course_query.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/completed/003_markdown_table_and_seat_count.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/completed/004_selection_strategy_and_dryrun.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/completed/005_delay_tuning_and_human_speed.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/completed/006_project_standardization.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/completed/007_project_alignment_check.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/raw/001_playwright_and_login.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/raw/002_dialog_and_course_query.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/raw/003_markdown_table_and_seat_count.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/raw/004_selection_strategy_and_dryrun.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/raw/005_delay_tuning_and_human_speed.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/raw/006_project_standardization.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/raw/007_project_alignment_check.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/summaries/001_playwright_and_login_summary.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/summaries/002_dialog_and_course_query_summary.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/summaries/003_markdown_table_and_seat_count_summary.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/summaries/004_selection_strategy_and_dryrun_summary.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/summaries/005_delay_tuning_and_human_speed_summary.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/summaries/006_project_standardization_summary.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/conversations/summaries/007_project_alignment_check_summary.md` | `決策 → docs/adr/、錯誤根因 → docs/known-issues/；原檔移到 .agents/conversations/（只存本機，不進 git）` | docs |
| ☐ | `legacy/courses_info.md` | `README.md / docs/specs/ / docs/architecture/ARCHITECTURE.md` | docs |
| ☐ | `legacy/docs/ARCHITECTURE.md` | `docs/architecture/ARCHITECTURE.md` | docs |
| ☐ | `legacy/docs/CONTEXT.md` | `docs/specs/ 或 docs/adr/ 或 docs/known-issues/` | docs |
| ☐ | `legacy/docs/DEPLOYMENT.md` | `docs/specs/ 或 docs/adr/ 或 docs/known-issues/` | docs |
| ☐ | `legacy/docs/PROMPT_TEMPLATES.md` | `docs/PROMPT_TEMPLATES.md` | docs |
| ☐ | `legacy/docs/TOOLS.md` | `docs/specs/ 或 docs/adr/ 或 docs/known-issues/` | docs |
| ☐ | `legacy/evals/README.md` | `evals/EVALS.md（全專案只有根目錄一份 README）` | docs |
| ☐ | `legacy/.cursorrules` | `docs/standards/PROJECT_RULES.md（只留本專案特有的規則；各工具入口檔由 agentctl sync 產生）` | other |
| ☐ | `legacy/.github/workflows/ci.yml` | `比對模板產生的 .github/workflows/ci.yml，只併入本專案特有的步驟` | other |
| ☐ | `legacy/.vscode/launch.json` | `比對模板產生的 .vscode/，只保留本專案特有的 launch / settings` | other |
| ☐ | `legacy/.vscode/settings.json` | `比對模板產生的 .vscode/，只保留本專案特有的 launch / settings` | other |
| ☐ | `legacy/LICENSE` | `LICENSE（保留原授權）` | other |
| ☐ | `legacy/Makefile` | `改用 agentctl / uv run / pnpm 指令，寫進 README；仍需要的腳本放 scripts/` | other |
| ☐ | `legacy/uv.lock` | `依用途判斷（資料 → DATA_DIR，靜態資源 → web/ 或 src/<pkg>/）` | other |
