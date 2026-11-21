# Story Quality AutoLoop 首次實跑

基準為 PR #5 的 `c096a2eeee45af162afaa6ed6c4b80d61a0e707b`。10〈刮痕〉已在啟動 Issue #6 前完成第五稿診斷，沿用原定停損。03、07 共做四稿、用十二個讀者名額，最後由門檻程式判定 `STOP_BUDGET`。**製作候選 0 篇。**

## 結果

| 稿件 | 可重算分數 | 判定依據 |
|---|---|---|
| [03 第三稿](run-01/03-v3.json) | 79，兩份格式不合 | 縫死五個扣眼與改成抱枕的必要關係不清楚。 |
| [07 第三稿](run-01/07-v3.json) | 74，兩份格式不合 | 媽媽讓新客人先買，卻能確保拿到最後一份。題卡沒有支持這個時機。 |
| [07 第四稿](run-01/07-v4.json) | 80、95、80 | 兩位只部分支持隊尾測聲音的動機。給 95 的讀者也指出題面缺乏遠處聽不清叫號的跡象。 |
| [03 第四稿](run-01/03-v4.json) | 82、80、80 | 三位都能推到暗房遮光，卻仍能把光點解釋為沿前襟漏出。白扣如何支持當下的選擇也仍有疑問。 |

03、07 的第三稿共有四份回覆把公平性標記放進了核心名稱，或把敘述放進支持程度欄位。原始回覆原樣保留、判為無效，並從第四稿起在輸出 Schema 約束欄位取值。10 的原生讀者當時共用工作區，三份 89 只用於停損診斷。[10 的原始試讀](../blind-tests/10-v5.md)

[程式產出的最終報告](run-01/final-report.json)可用[帳本](run-01/ledger.json)、四份凍結稿件及 `reader-01.json` 至 `reader-12.json` 重算。[四稿逐版文字差異](writer-diffs.md)

## 執行與驗證

- Writer 使用原生 Codex 子代理，每次交付兩段題面、揭曉與英文稿。主 Agent 在投遞前鎖定各稿核心與假設。讀者使用 Windows 上已登入 ChatGPT 的 Codex CLI 0.163.0，每場依序接收三段，共有 36 份 CLI 階段紀錄。正式 runtime 每批先做檔案讀取探針，保存四次拒絕及一次在正式投遞前被拒的設定試跑。每一段有唯一 CLI session ID，程式驗證實際工具事件、提示內容、稿件、量表及逐場紀錄 SHA-256。
- 前兩批執行中完成帳本格式的審查修訂，回補已確定的基準 SHA、執行參數、正式場次類別與紀錄雜湊。回覆、計分輸入與投遞沒有修整。最後兩批以完成修訂的程式執行。工程獨立複查未發現剩餘 P0 或 P1。
- 使用既有 ChatGPT 登入的正式稿件測試以外，本機不呼叫模型即可驗證。Windows 以外的 CLI 隔離、真人試讀、英文口播時長與字幕播放仍待後續驗收。市場驗收尚未開始。

```powershell
uv sync --locked
uv run --locked pytest
uv run --locked python -m unittest discover -v -s .agents/skills/story-quality-autoloop/scripts
uv run --locked python -X utf8 .agents/skills/story-quality-autoloop/scripts/autoloop.py verify experiments/shorts-story-review/autoloop/run-01
uv run --locked --group governance python governance/verify.py
git diff --check
```

61 項既有測試與 9 項 AutoLoop 測試通過。治理驗證使用 repo 固定的 `b8a16828481e6b537c474d4e2e4be4d3e047e3e8`。在 `video/` 執行 `npm.cmd ci` 和 `npm.cmd run typecheck` 通過，Node 24 提示專案要求 Node 22。
