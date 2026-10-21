# Changelog

All notable changes to **ndhu-course-rush** are documented here
(format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versions: [SemVer](https://semver.org/)).

## [Unreleased]

### Changed
- refactor(config): integrate course rush settings and legacy loader (by `@Antigravity`)
- refactor(services): modernize course automation services and domain models (by `@Antigravity`)
- refactor(entrypoints): integrate course rush CLI and root runner (by `@Antigravity`)

### Documentation
- docs(migration): migrate architecture, ADRs, known issues, specs, and README (by `@Antigravity`)

### Testing
- test(migration): standardize test suite for config, parser, and CLI (by `@Antigravity`)

### Chore
- chore(migration): convert dependencies and config templates (by `@Antigravity`)

## [0.1.0] - 2026-10-22
### Added
- Initial project scaffold (framework v3.3.0).

---

## [1.0.0] - 2026-10-08
### 🚀 架構與規格重構 (Project Standardization)
- **架構升級**：全專案重構為標準結構與套件管理。
- **模組化分層**：瀏覽器驅動、身分認證、課表解析與搶課核心拆分。
- **向後相容**：根目錄保留進入點腳本包裝。
- **自動化測試**：單元測試與 CI 流水線建立。

## [0.4.0] - 2026-06-03
### ⚡ 擬真人流延遲調校與速度極大化
- **雙軌延遲機制**：查詢階段穩定延遲（150ms），搶課衝刺階段極限微延遲（20ms~50ms）。

## [0.3.0] - 2026-06-02
### ✨ 自訂搶課志願序與乾跑演練 (Dry-run)
- **Markdown 課表同步**：自動生成 `courses_info.md`，提供直觀 Markdown 表格標註搶課順序。
- **名額即時探查**：自動點擊課程代碼並攔截原生 Alert 訊息，即時提取剩餘空位。

## [0.2.0] - 2026-06-02
### 🔍 預排課程查詢與表格渲染修正
- **查詢預排**：登入後自動點選查詢預排清單。
- **表格列數修正**：修正 ASP.NET 資料列選擇器為 `tr:has(td)`。

## [0.1.0-legacy] - 2026-06-02
### 🎉 專案誕生 (Initial Proof-of-Concept)
- **工具選型**：採用 Playwright Sync API。
- **真實瀏覽器啟動**：透過原生 Chrome 視窗運作。
- **登入自動化**：自動填寫帳號密碼並關閉評量彈窗。
