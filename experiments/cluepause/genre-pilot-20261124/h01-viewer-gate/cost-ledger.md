# H01 製作成本帳

2026-11-24；**EXPLORATORY ONLY / HUMAN_TEST_PENDING**。本帳不宣稱貨幣成本、ROI 或正式驗收。當前基準 HEAD `e189e294a09120588006885ddbe40ac837928c34`；兩版凍結，這次只盤點、抽幀與寫文件，沒有追加製作。

## Integrator-collected measured data（原值照錄）

Measured from Codex rollout token_count events (total_token_usage at session end) and rollout first/last timestamps, 2026-11-24 (UTC). Codex jobs only.

| job | wall clock | input | cached input | output |
| --- | --- | --- | --- | --- |
| motion module v1 (5253512d) | 10:07:16-10:31:52 (24.6 min) | 2,931,687 | 2,852,608 | 46,678 |
| motion review 1 (REQUEST_CHANGES) | 10:35:00-10:39:20 (4.3 min) | 598,821 | 542,208 | 7,460 |
| motion fix (6270889a) | 10:39:42-10:55:51 (16.2 min) | 2,188,778 | 2,110,720 | 27,765 |
| motion review 2 (APPROVE) | 10:56:23-10:59:43 (3.3 min) | 407,413 | 363,520 | 6,100 |
| H01 A+B render, one job, A and B not separable (4784b93a) | 11:00:08-11:35:06 (35.0 min) | 6,771,505 | 6,583,040 | 65,452 |
| path scrub | 11:35:46-11:37:09 (1.4 min) | 243,502 | 206,592 | 2,078 |
| H01 A/B review (APPROVE partial) | 11:37:31-11:44:09 (6.6 min) | 1,520,089 | 1,417,472 | 11,324 |
| continuity record (e189e294) | 11:44:31-11:46:33 (2.0 min) | 379,819 | 331,392 | 2,985 |

Not measured: human intervention time (owner and integrator), A-only vs B-only split, ImageGen share of the weekly limit.

以上是使用者提供的 integrator-collected 資料，來源定義為 session 結尾累計用量及首末 rollout 時間；本次沒有重新讀取 rollout 來獨立稽核。cached input 是 input 的子集，不能再加一次當成額外 token。wall clock 包含工作等待／工具等時間，不等於模型運算時間或人時。這次 viewer-gate 文件工作的 token／時間不在該表中。

## Derived 算術（不是額外實測）

- Input：2,931,687 + 598,821 + 2,188,778 + 407,413 + 6,771,505 + 243,502 + 1,520,089 + 379,819 = **15,041,614**。
- Cached input：2,852,608 + 542,208 + 2,110,720 + 363,520 + 6,583,040 + 206,592 + 1,417,472 + 331,392 = **14,407,552**。
- 非 cached input：15,041,614 − 14,407,552 = **634,062**。
- Output：46,678 + 7,460 + 27,765 + 6,100 + 65,452 + 2,078 + 11,324 + 2,985 = **169,842**。
- Input + output：15,041,614 + 169,842 = **15,211,456**；不是計價金額，也不另加 cached input。
- 表列已四捨五入分鐘加總：24.6 + 4.3 + 16.2 + 3.3 + 35.0 + 1.4 + 6.6 + 2.0 = **93.4 min**。
- 用原始時間差另算：1,476 + 260 + 969 + 200 + 2,098 + 83 + 398 + 122 = **5,606 s = 93 min 26 s**。第一個開始到最後結束為 99 min 17 s；其間未計入各 job 的間隔合計 5 min 51 s。不要把間隔或整段跨度當成人工介入時間。

## 圖片、重試與修正

已提交來源：[h01-v2.1-imagegen.json](../h01-v2.1-imagegen.json) 及 [h01-v2.1-ab.md](../h01-v2.1-ab.md)。前者記錄 **4 requests = 2 initial + 2 correction**，輸出四張 2×2 contact sheets（不是四個獨立成片鏡頭）；後者記錄採用兩張修正版、保留兩張未採用初版。四個 request 的 prompt／來源檔名保留在原 JSON；沒有 API 失敗 request 的已記錄數字，不能把「未記錄」寫成確知零失敗。另重用 **7 個 demo 圖像資產，為這些資產新增 request = 0**。本次新增 image request = 0。

本機 `artifacts/genre-pilot-20261124/h01-v2.1/shared/attempt-ledger.json` 與既有 `A/`、`B/`、`shared/` 的 `commands.jsonl` 補充歷史製作證據：5 次 render CLI invocation＝1 次 staging 中止 + 4 次完成 pair build；最後只選一組 A/B。**71 次成功 production H.264 encode = 34 A cuts + 27 B cuts + 10 reusable raw motion passes**，另 1 AAC encode、8 master muxes。含被取代的工作，不是最終影片數，也不能按 encode 次數切分 token 或成本。抽幀、解碼 QA、framemd5、歷史測試及 synthetic fixture 不在 production encode 數內；這次抽幀也不混入原數字。

逐關鍵鏡頭修正如下，照原帳的定義計 source／visual／shot-encoding 修正；同一共用修正可分配到多鏡，不可把各列加總當成獨立 request 數。

| Key shot(s) | 已記錄 corrections | 原因／尚存限制 |
| --- | --- | --- |
| opening-handle | 0 | 重用 demo；不是從零製作成本為零。 |
| device-rules / device-consent / device-saved | 1 | 共用 native readout alpha 邊界修正。 |
| mother-cough | 2 | ImageGen sheet 連續性修正；JPEG range normalization。 |
| device-cough | 1 | JPEG range normalization。 |
| harder-handle | 0 | 重用 demo。 |
| flinch / hand-slipped | 2 | Sheet 連續性修正；JPEG range normalization；手落下仍是 pose cut。 |
| nia-reply | 2 | Sheet 修正；native screen perspective／progressive input；沒有 lip-sync claim。 |
| device-input（包含最後三個 cuts） | 2 | 共用 alpha；第一次完成 render 後 progressive-input 修正。 |
| latch-retract | 0 | 重用 demo。 |
| brace / foot / final-brace | 2 | Sheet 修正；JPEG range normalization；仍為照片局部變形。 |

兩次 correction 上限後停止，不能把 unresolved 動作當作已完成。新增 cut index 引起的不變畫面重編碼算 render，不隱藏為「免費」；chroma-header 修正為 stream-copy remux，沒有再作 shot encode。歷史 demo 的更早成本未包含在本次新修正數內。

保留的失敗路徑：缺 SciPy 中止音訊混音（後改 NumPy FFT、重用已快取旁白，未重合成）；opaque physical-readout 被 alpha 檢查拒絕；前兩次 QA 因 JPEG range／chroma location 使 select(n) 重置而中止，第三次通過；補充 edge QA 有不支援的 1-pixel scaler（失敗 FFmpeg returncode 4294967274）及把刻意黑門縫誤判的過嚴 assertion。這些失敗／重跑是成本背景，不是新的 ImageGen request。

## NOT MEASURED 與來源限制

| 項目 | 狀態／理由 |
| --- | --- |
| Human intervention time（Owner / integrator） | **NOT MEASURED**；不能由 job 間隔倒推。 |
| A-only vs B-only token／wall time split | **NOT MEASURED**；一個 job 同時製作 A+B，不能除二或依 encode 數攤分。 |
| ImageGen share of the weekly limit | **NOT MEASURED**；request 數不等於配額占比。 |
| 每條 FFmpeg render command 的耗時 | **NOT MEASURED**；七個 commands.jsonl 共 226 entries，只記 argv、environment_keys、returncode、stdout、stderr，沒有 start/end/elapsed。檔案 mtime 不作耗時證據；35.0 min 是整個 Codex A+B job。 |
| 貨幣費用、電力／GPU 時間、旁白及歷史資產完整成本 | **NOT MEASURED**；沒有可核對的帳單／費率／硬體使用資料，不產生估價。 |
| 共用 motion module 的未來攤提、穩定單片成本 | **NOT MEASURED**；本輪含模組開發與返工，不能當成每支片固定成本。 |

226 entries 算式：8 + 68 + 44 + 8 + 54 + 42 + 2 = 226。這是本次讀取現有 logs 的 entry 數，包含 probe／QA，不等於 226 次 render。已提交紀錄的歷史數字與本機 logs 的可得欄位分開呈現；artifact 不在 Git，紀錄摘要與 script 讓下一位可再盤點，不能聲稱缺欄位已測得。

## Owner 的製作層級假說與 ROI 問題

以下 **L1/L2/L3 是製作層級假說**，不是 repo 治理風險等級，也尚未證明各層價格／效益：

| Tier hypothesis | 使用情境假說 |
| --- | --- |
| L1 | Stills + camera move + voice，用於便宜的題材測試。 |
| L2 | Layered motion + partial character action，用於已有證據支持的題材。 |
| L3 | High-quality generative video，用於 flagship work。 |

這次可以保留「這一組探索實作花了哪些可量測的 Codex 用量、出了哪些重試」的基線，日後配合真人逐題結果，決定是否值得為這個故事安排下一個更受控的小測試。現在真人資料為空，沒有任何 ROI 結論。

這次不能估算 B 相對 A 的邊際成本或每一分喜好提升的成本；不能隔離 animation 效果（B 兩個關鍵動作未完成、連續性有 confound）；不能比較尚未製作的 L3、證明 tier 普遍性、外推廣告收入／訂閱／公開留存或長期產能。既有 90 分 rule 不變；不以腳本分數、/30 問卷或技術 encode PASS 取代好影片與市場證據。
