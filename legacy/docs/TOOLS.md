# 自訂工具庫規範與介面定義 (TOOLS.md)

本文件定義 `ndhu_course_selector` 工具庫中的各項公共函式、型別定義與呼叫規範。

---

## 1. 配置管理模組 (`ndhu_course_selector.tools.config`)

### `load_config(config_file: str = "config.txt", env_file: str = ".env") -> Dict[str, str]`
- **功能**：載入系統運作所需之帳號、密碼與系統網址。
- **優先順序**：
  1. 作業系統環境變數 (`NDHU_USERNAME`, `NDHU_PASSWORD`, `LOGIN_URL`)
  2. `.env` 檔案
  3. `config.txt` 檔案
- **回傳值**：包含 `USERNAME`, `PASSWORD`, `LOGIN_URL`, `RUSH_DELAY`, `QUERY_DELAY` 等鍵值之字典。

---

## 2. 課表解析與 Markdown 介面 (`ndhu_course_selector.core.parser`)

### `query_and_parse_courses(page: Page, alert_msg_box: Dict[str, Any], md_filename: str) -> List[Dict[str, Any]]`
- **功能**：在選課系統主畫面點擊查詢預排課程按鈕，依序點擊課程代碼並透過原生 Alert 擷取各科目前已選人數與剩餘空位。
- **輸出副作用**：自動將解析結果格式化寫入指定的 Markdown 檔案（預設 `courses_info.md`）。

### `parse_markdown_priorities(filepath: str) -> List[Dict[str, int]]`
- **功能**：讀取並解析 Markdown 課表中的「搶課順序」欄位。
- **輸入範例**：`| 0 | **0** | CP__30000 | ...`
- **回傳範例**：`[{"priority": 0, "index": 0}, {"priority": 1, "index": 1}]`（自動按 priority 升序排序）。

---

## 3. 瀏覽器驅動模組 (`ndhu_course_selector.core.browser`)

### `create_browser_session(headless: bool = False) -> Generator[Tuple[Page, Dict[str, str], Browser], None, None]`
- **功能**：使用 Context Manager 封裝 Playwright Chrome 實體，自動註冊 Native Alert 對話框監聽器，並確保在工作階段結束或異常時乾淨釋放資源。
