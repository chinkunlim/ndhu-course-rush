# ADR-005：憑證防外洩與安全配置隔離方針

- **狀態**：Accepted
- **日期**：2026-10-08
- **Agent**：`system`
- **任務**：`TASK-006`

## 1. 背景與問題

舊腳本直接以明文 `config.txt` 存放學號與密碼，且缺乏範本與 `.gitignore` 隔離保護，存在外洩風險。

## 2. 評估過的方案

| 方案 | 優點 | 缺點 |
|---|---|---|
| 明文 config.txt | 容易編寫 | 極易意外 commit 至公開 Git 倉庫 |
| .env + 環境變數隔離 | 符合 12-Factor App，受到 gitignore 保護，支援 CI 注入 | 需要載入 dotenv 工具 |

## 3. 決策與理由

建立 `.env.example`，將 `.env` 與 `config.txt` 納入 `.gitignore`。
配置讀取器優先讀取系統環境變數，向下相容讀取 `.env` 與舊版 `config.txt`。

## 4. 影響與代價

- 符合現代軟體工程安全治理規範。
- 學號與密碼不進版控。
