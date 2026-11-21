# Story Quality AutoLoop 續跑

來源基準為 `306c472c7b494c1ab13c79bb9c0271ec987c6812`。每批至多四稿、每篇至多兩稿、至多十二場獨立試讀。每份正式結論都有對應帳本、凍結稿、隔離探針與逐場原始回覆。

**第一篇製作候選是 [04 v7〈停在姓氏前〉](qualified/04-v7.md)。** 三位讀者各給 91、91、93 分，全部認為題面支持必要核心，且無關鍵缺陷。第 9 批一通過即結束。

| 批次 | 評審協定 | 凍結稿 | 讀者場次 | 決定 |
|---|---|---:|---:|---|
| [第 1 批](run-01/final-report.json) | v1 | 4 | 12 | 名額用完 |
| [第 2 批](run-02/final-report.json) | v1 | 4 | 12 | 名額用完 |
| [第 3 批](run-03/final-report.json) | v1 | 4 | 12 | 名額用完 |
| [第 4 批](run-04/final-report.json) | v1 | 3 | 9 | 封存，轉入新稿與 v2 |
| [第 5 批](run-05/final-report.json) | v2 | 4 | 12 | 名額用完 |
| [第 6 批](run-06/final-report.json) | v2 | 4 | 12 | 名額用完 |
| [第 7 批](run-07/final-report.json) | v2 | 4 | 12 | 名額用完 |
| [第 8 批](run-08/final-report.json) | v2 | 4 | 12 | 名額用完 |
| [第 9 批](run-09/final-report.json) | v2 | 1 | 3 | 通過，等候開拍核准 |

## 評審規則

通過條件是同一凍結稿有三位有效正式隔離讀者，每人至少 90／100，且每人都認為題面支持全部必要核心、未發現關鍵缺陷，動機、因果及公平性各至少 3／5。

v2 說明哪些問題會使主要行動或核心答案無法成立，並讓容易猜中、驚喜有限等觀察反映在相應分數。必要核心在讀者收到題卡前鎖定。舊紀錄使用原量表與原提示重算。每份新測試均使用經過修訂的版本。

## 工程驗證

- `uv sync --locked` 完成，`uv run --locked pytest` 61 項通過。
- `uv run --locked python -m unittest discover -v -s .agents/skills/story-quality-autoloop/scripts` 10 項通過。獨立程式複查確認 v1 回放結果與基準版本一致。
- 九批判定全數重算，320 個探針和分段工作階段 ID 互不重複。第 9 批的凍結稿和候選頁逐段比對一致。
- `uv run --locked --group governance python governance/verify.py` 通過，框架 SHA 為 `b8a16828481e6b537c474d4e2e4be4d3e047e3e8`。
- `video/` 執行 `npm.cmd ci` 與 `npm.cmd run typecheck` 通過。Node 為 24.13.0，安裝時提示套件宣告的 Node 範圍為 22。

以下指令從 repo 根目錄重算第 9 批。

```powershell
uv run --locked python -X utf8 .agents/skills/story-quality-autoloop/scripts/autoloop.py verify experiments/shorts-story-review/autoloop/run-09
```

隔離試讀在 Windows 的本機 Codex 登入環境實測。真人試讀、英文旁白時長、字幕和市場數據待後續驗收。
