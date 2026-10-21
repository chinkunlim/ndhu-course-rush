# 對話摘要：006 - 專案工程化重構與規格標準化

## 📌 階段概述
本階段響應使用者的 `/goal`, `/plan`, `/grill-me` 指令，對累積至今的歷史對話進行全景深度解讀，並將專案從單檔自動化腳本升級為符合現代 Python 工程最高標準的軟體專案。

## 🎯 使用者核心訴求
1. **對話全量備份與摘要**：
   - 解讀所有歷程，建立 `conversations/raw/` 與 `conversations/summaries/`。
2. **治理文檔體系**：
   - 從最早對話起建構：`AGENTS.md`、`CHANGELOG.md`、`README.md`、`WORKFLOW_GUIDE.md`、`DECISIONS.md (ADR)`、`KNOWN_ISSUES.md`。
3. **標準專案架構（src-layout）**：
   - 升級 `pyproject.toml`、`.gitignore`、`.env.example`、`Makefile`、`LICENSE`、`.vscode/`、`.github/`、`docs/`、`tests/`、`evals/`。
   - 保留原 `auto_login.py` 與 `main.py` 向後相容進入點。
4. **機敏資訊保護**：
   - 歷史對話與文檔中全面進行帳號、學號與憑證脫敏。

## 🛠️ 關鍵技術決策與架構變更
1. **模組化分層架構（src/ndhu_course_selector/）**：
   - `core/browser.py`：管理 Playwright Chrome 實例。
   - `core/auth.py`：負責登入與評量彈窗解除。
   - `core/parser.py`：負責表格爬取、人數提取與 Markdown 雙向同步。
   - `core/selector.py`：負責優先級策略選課迴圈與延遲控制。
   - `tools/config.py`：相容 `.env` 與舊版 `config.txt` 讀取。
2. **自動化測試體系**：
   - 導入 `pytest`，撰寫針對配置解析與 Markdown 課表解析的單元測試。
3. **CI/CD 自動化與 GitHub 治理**：
   - 建立 GitHub Actions CI 流水線、安全漏洞通報（SECURITY.md）與貢獻指南（CONTRIBUTING.md）。

## ⚠️ 踩坑、阻礙與解決方案
- **問題**：重構目錄時若刪除或移動根目錄的 `auto_login.py`，會破壞使用者的原有執行習慣。
- **解法**：在根目錄保留 `auto_login.py` 作為 Thin Wrapper，直接轉發調用 `ndhu_course_selector.cli`，兼顧架構整潔與無痛相容。

## 📊 產出產物與成果
- 完整的 6 篇 raw 對話紀錄與 6 篇對應 summary。
- 根目錄 6 大規範核心 Markdown 檔案。
- 標準 `src-layout` 原始碼模組與測試套件。
