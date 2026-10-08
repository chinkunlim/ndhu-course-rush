# 提示詞範本與調教手冊 (PROMPT_TEMPLATES.md)

本文件整理與 AI Agent 協作開發、除錯或演練本專案時的最佳 Prompt 範本。

---

## 1. 離峰搶課演練與測試提示詞
```text
請啟動本專案的選課流程，執行乾跑演練 (Dry-Run)：
1. 確保讀取 .env 中的測試設定。
2. 檢查 courses_info.md 是否成功生成。
3. 模擬輸入 "2" 執行自訂順序點擊。
4. 回報各科目的加選按鈕檢測狀態。
```

---

## 2. 爬蟲解析與 ASP.NET 頁面除錯提示詞
```text
東華大學選課系統更新了頁面 DOM 結構，請協助檢查：
- 檢查 #ContentPlaceHolder1_grd_subjs 表格選擇器是否有效。
- 檢查代碼查詢人數時原生 Alert 視窗是否有變更為其他 Modal。
- 請在不破壞現有擬真人流延遲架構下提供修補建議。
```

---

## 3. CI/CD 與自動化發布檢查提示詞
```text
請執行專案健康檢查：
1. 執行 uv sync 與 uv run pytest。
2. 檢查有無未脫敏之敏感資訊洩漏於 Markdown 或 log 檔案中。
3. 驗證 Makefile 指令皆能正常運作。
```
