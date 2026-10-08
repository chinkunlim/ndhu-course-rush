# 貢獻指南 (Contributing Guide)

感謝您對 NDHU Course Selector 專案的關注與貢獻！

## 開發流程
1. Fork 本專案並建立您的功能分支 (`git checkout -b feature/awesome-feature`)。
2. 使用 `uv sync` 設定虛擬環境。
3. 確保所有改動皆通過單元測試：
   ```bash
   uv run pytest
   ```
4. 提交您的變更，並確保 Commit 訊息清晰簡潔。
5. 推送分支並發起 Pull Request。

## 程式碼規範
- 遵循 PEP 8 命名規範與型別標註 (Type Hints)。
- 嚴格禁止提交任何含個人帳密或金鑰的檔案至 PR 中。
- 新增模組時，請一併撰寫對應的單元測試。
