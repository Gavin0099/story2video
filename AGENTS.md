# story2video 工作指引

先讀 [PLAN.md](PLAN.md) 並以使用者本次授權確認工作範圍。M0 只涵蓋 S2V-001 和 S2V-002。M1 需另行授權，公開發布日後也須另有人工授權。

驗收時執行 [README.md](README.md) 的指令，留下 Git SHA、命令、結果及未驗證範圍。分別記錄工程驗收與市場驗收。憑證使用環境變數或安全儲存，勿放入 Git 或測試資料。

治理入口為 [AGENTS.base.md](AGENTS.base.md) 與 [contract.yaml](contract.yaml)。開發治理使用固定版本的框架 submodule。安裝 hooks 和重跑驗收的方式見 [governance/README.md](governance/README.md)。

## AI Governance Update Intent Rule

- 檢查框架版本時只讀取狀態。明確要求更新框架時，依 `governance/AI_GOVERNANCE_UPDATE_PROTOCOL.md` 使用 F-7，並回報實際導入狀態表。

## Repo-Specific Risk Levels
<!-- governance:key=risk_levels -->

- 高風險涵蓋影片公開授權、憑證與 `src/story2video/app/store.py` 的既有資料遷移。此類改動需保留失敗路徑與可重跑的驗證證據。
- Episode 欄位或 CLI 行為變更需核對既有分集的相容性。文字與測試資料的修訂按實際影響判定。

## Must-Test Paths
<!-- governance:key=must_test_paths -->

- 改動 `src/story2video/` 時執行 `uv run --locked pytest`。狀態機或 SQLite 改動需驗證交易回滾及批准邊界。
- 改動 `video/` 時在該目錄執行 `npm ci` 與 `npm run typecheck`。改動治理契約或框架版本時執行 `uv run --locked python governance/verify.py`。

## L1 → L2 Escalation Triggers
<!-- governance:key=escalation_triggers -->

- 變更 Episode v1 合約、SQLite schema 或公開核准順序時，驗證既有資料、失敗回復和未授權路徑。

## Repo-Specific Forbidden Behaviors
<!-- governance:key=forbidden_behaviors -->

- 測試使用本機 fixture，禁止在 M0 呼叫付費 AI 或 YouTube 上傳 API。
- 勿將真實憑證或測試帳號資料放進 `tests/fixtures/`、Git、日誌或 `memory/`。
