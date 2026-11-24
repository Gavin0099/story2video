# Classic Puzzle Benchmark

CluePause 的選題參考。每張技法卡記錄一種觀眾可能忽略的前提、如何改變猜測，以及揭曉時如何用鏡頭或聲音證明因果。

## 先用七張卡做校準

[首批技法卡](classics.json)只保留抽象機制和可追溯的參考來源。線索順序及視覺建議是本專案的短片試驗方向。來源欄記錄找到的流傳版本或近似類型。七張卡均為待確認，僅供研究。查到最早來源、確切版本及確認適用權利後，才能另提經典特別企劃。

| 分析欄位 | 使用方式 |
| --- | --- |
| `paradox`、`hidden_assumption` | 確認第一眼看得見矛盾，記下觀眾會預設什麼。 |
| `clue_sequence`、`reveal_mechanism`、`reveal_proof` | 設計哪條可觀察的線索改變猜測，及揭曉用何種聲畫證明。 |
| `visual_spoiler_risk`、`shorts_suitability` | 檢查分鏡會不會提前露出解答，評估是否能在 Shorts 時間內公平揭曉。 |
| `source_and_rights` | 研究索引、目前能確認的版本線索和用途限制。作品查核使用單集 Story Rights Gate。 |

## 接到現有流程

1. 主力原創稿從一張技法卡抽取一種機制，Writer 另寫事件、人物關係、線索與解答因果。需要交叉比較時，以[原 20 支公開批次清單](../../cluepause/public-20-20261122/release.json)的影片 ID 對看片證據。每支先記一個主要反轉、開場異常、線索出場與揭曉證據，並保留時間碼和未核對欄位。
2. 如要翻拍經典，逐題查證特定版本是公共領域，或持有商業改作許可。兩種路線都在製片前為凍結稿完成 [Story Rights Gate](../../../.agents/skills/story2video-shorts-batch/references/story-rights.md)。
3. 依既有 AutoLoop 做三位獨立讀者盲評，三人都達 90 分且通過內容條件，才成為故事製作候選。成片依 [Shorts Viewer Gate](../shorts-viewer-gate.md) 檢驗，再按既有 Owner 授權發布。
4. 以同頻道、相近片長及同發布後時窗比較續看／滑走、互動觀看、平均觀看百分比和按讚。把真人首看與 Studio 數據各自對回影片版本。

研究外部專案時，可以參考它們的多輪問答方法、線索設計或頓悟測量。引用研究、轉用資料、使用程式與改編故事各自適用來源的權利條件。這個 Benchmark 以專案自行撰寫的技法卡開始。 [SPLAT](https://github.com/chenqi008/LateralThinking) · [writing-turtle-soup](https://github.com/906491213/writing-turtle-soup) · [The Appeal of Insight](https://github.com/mariusmercier/paper_insight_culture)

## 驗收紀錄

2026-11-24（台北時間）。驗收基底為 `3fbc2d2bb5f9e85b0d448fe873c0e2f18b60d04c`，檢查對象為本節所在提交的變更。

| 工程檢查 | 結果 |
| --- | --- |
| `uv sync --locked`、`uv run --locked pytest` | 依賴同步成功，61 項測試通過 |
| `npm ci`、`npm run typecheck`（`video/`，Node 22.16.0） | 安裝及型別檢查通過 |
| `uv run --locked python experiments/story-quality-lab/verify.py` | 既有題卡、揭曉稿、評分及本機連結結構通過 |
| `python -X utf8 <skill-creator>/scripts/quick_validate.py <skill-directory>` | Repo 與本機安裝的批次 skill 均通過 |
| `python -X utf8 -`（一次性資料及連結檢查）、`git diff --cached --check` | 七個唯一 ID 均為待確認且僅供研究，27 個相對連結可解析，兩份 skill 的權利參考文件相同，差異格式乾淨 |

本次驗收涵蓋編輯流程、資料與文件。逐題權利判定、原 20 支的逐片結構標註、真人首看及市場驗收尚未執行。
