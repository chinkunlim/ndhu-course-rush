# 對話摘要：001 - Playwright 核心選型與學號密碼登入實作

## 📌 階段概述
本階段記錄了 NDHU（國立東華大學）自動選課輔助程式的最初誕生過程。從最初的使用者提問、自動化工具選型，到成功登入系統並繞過教學評量彈窗。

## 🎯 使用者核心訴求
1. **目標系統**：東華大學選課系統 (`https://sys.ndhu.edu.tw/aa/class/subjselect/course_sele.aspx`)。
2. **自動登入**：自動填入學號（`ContentPlaceHolder1_ed_StudNo`）與密碼（`ContentPlaceHolder1_ed_pass`），並點擊登入按鈕。
3. **套件與環境治理**：明確要求使用 `uv` 進行 Python 依賴安裝與環境鎖定。
4. **瀏覽器可視化**：禁止使用 Headless 無頭模式，要求彈出獨立真實的 Chrome 瀏覽器視窗，方便即時觀察。
5. **持久化保留**：登入完成後不可立即關閉瀏覽器，需保持在登入後的工作階段。

## 🛠️ 關鍵技術決策與架構變更
1. **捨棄 Selenium，擁抱 Playwright**：
   - 使用者最初曾提供 Selenium 舊程式碼，但在評估了現代非同步網頁交互、彈窗監聽與 Chrome 原生通道支援後，決定統一使用 Playwright Sync API。
2. **鎖定 Chrome Channel**：
   - 採用 `browser = p.chromium.launch(headless=False, channel="chrome")`，啟動本地系統已安裝的真實 Chrome，避免 Chromium 驅動特徵被伺服器阻擋。
3. **教學意見評量 DIV 彈窗處理**：
   - 登入後系統經常彈出 `div[aria-describedby='evalModal']` 評量問卷提示。透過定時 5 秒 wait_for 監聽器，發現出現時自動按下「取消」按鈕進行跳過。
4. **去除不必要的爬取與自動登出**：
   - 移除原先自動抓取 HTML 並登出的多餘步驟，確保會話停留在選課主畫面上。

## ⚠️ 踩坑、阻礙與解決方案
- **問題**：ASP.NET 頁面載入可能非同步，直接尋找元素會拋出元素未渲染錯誤。
- **解法**：導入 `page.wait_for_load_state('networkidle')`，等待所有網路封包通訊完畢再進行後續動作。

## 📊 產出產物與成果
- 建立初始 `pyproject.toml`（引入 `playwright`）。
- 建立 `config.txt` 儲存帳號與密碼（後續升級為 `.env` 機制）。
- 產出 `auto_login.py` 初始登入函式。
