# 本地與環境部署指引 (DEPLOYMENT.md)

本文件說明如何在 macOS、Linux 或 Windows 開發環境中從零安裝與部署 NDHU Course Selector。

---

## 1. 系統需求
- **Python**: 3.11 或以上
- **uv**: 推薦使用 Astral `uv` 進行套件管理
- **Chrome**: 系統已安裝 Google Chrome 瀏覽器

---

## 2. 部署流程

### Step 1: 安裝 uv
若本機尚未安裝 `uv`：
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 2: 檢出專案與同步環境
```bash
git clone https://github.com/chinkunlim/PyTest.git
cd PyTest
uv sync
```

### Step 3: 安裝 Playwright 驅動
```bash
uv run playwright install chromium
```

### Step 4: 配置環境變數
```bash
cp .env.example .env
# 使用文字編輯器填寫 .env 中的 NDHU_USERNAME 與 NDHU_PASSWORD
```

### Step 5: 執行測試確認就緒
```bash
uv run pytest
```
看到測試皆為 PASSED 即表示環境部署完成！
