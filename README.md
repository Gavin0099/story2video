# story2video

以 Python CLI、Episode JSON 和本機 SQLite 管理影片製作流程。M0 交付本機分集資料與狀態基礎。完整規格與各階段驗收見 [PLAN.md](PLAN.md)。

## 安裝與驗收

使用 Python 3.13、Node 22.16.0 和 uv 0.13.9。首次安裝從套件 registry 下載開發依賴。CLI 與測試可在安裝後離線執行，無需提供任何憑證。

```sh
uv sync --locked
uv run --locked pytest
cd video
npm ci
npm run typecheck
cd ..
```

Windows PowerShell 若阻擋 `npm.ps1`，使用 `npm.cmd` 執行相同指令。GitHub Actions 在 Windows 與 Ubuntu 跑上述檢查，並掃描 Git 歷史中的憑證。具備 Gitleaks v8.30.1 時可在本機重跑 `gitleaks git --redact --no-banner .`。

## 本機 CLI

```sh
uv run --locked s2v init
uv run --locked s2v validate --file tests/fixtures/episode.valid.json
uv run --locked s2v register --file tests/fixtures/episode.valid.json --actor local-reviewer
uv run --locked s2v status --id puzzle-0001 --revision 1
```

`validate` 檢查欄位結構及旁白 ID 是否唯一，成功時回傳內容 SHA-256。`register` 將分集索引為 `DRAFT`，同一版本的相同內容重跑只回傳既有紀錄。`status` 讀取索引，省略 ID 可列出所有分集。錯誤會以非零結束碼回報，例如下列測資缺少已授權來源的證明資訊。

```sh
uv run --locked s2v validate --file tests/fixtures/episode.invalid.json
```

資料庫路徑依序讀取全域參數 `--db`、環境變數 `S2V_DB_PATH`、`--config` 指定的 TOML 或目前目錄的 `story2video.toml`，最後用 `artifacts/story2video.sqlite3`。TOML 的相對路徑以該檔所在目錄為基準。CLI 直接讀取 shell 環境，`.env.example` 提供設定範例。

## 資料與權限邊界

- [Episode v1](src/story2video/schemas/episode.v1.schema.json) 隨 Python 套件分發。正式合約沿用 PLAN 範例並依 §5.2 加上必填 `script_revision`。M0 只驗證繁體中文 30–60 秒 Shorts 的 manifest。科普及科技教學枚舉保留給後續版本的流程。
- Episode JSON 保有內容真相。SQLite 儲存 manifest 絕對路徑、原始位元組 SHA-256、版本、狀態與事件。請保留每個已登錄版本的原始 JSON。修改內容後以另一份 JSON 登錄新 revision。
- SQLite schema 初始版本為 1。狀態與事件在同一筆交易寫入。可重試錯誤只能回到原失敗階段。QA 退件回到草稿重新驗證。流程圖保留獨立公開核准，並在進入私人上傳狀態前要求明確標記受眾。
- `video/` 提供可型別檢查的 Remotion 入口。內容審核、影片合成、API 成本、真實人工權限驗證與 YouTube 串接留待後續階段。

治理採用 AI Governance Framework 的 [外部契約模式](governance/README.md)，可手動使用指定的上游 commit 驗證契約。
