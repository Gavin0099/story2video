# H01 製作成本帳

2026-11-24；**EXPLORATORY ONLY / HUMAN_TEST_PENDING**。本帳不宣稱貨幣成本、ROI 或正式驗收。原始盤點基準 HEAD `e189e294a09120588006885ddbe40ac837928c34`；兩版凍結，原始盤點只抽幀與寫文件。後續 r1 無損 MASTER 與 DELIVERY 製作另記於下方。

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

以上是使用者提供的 integrator-collected 資料，來源定義為 session 結尾累計用量及首末 rollout 時間；本次沒有重新讀取 rollout 來獨立稽核。cached input 是 input 的子集，不能再加一次當成額外 token。wall clock 包含工作等待／工具等時間，不等於模型運算時間或人時。viewer-gate 文件工作及後續修訂的實測另列於下方本輪表格。

## Derived 算術（不是額外實測）

以下只加總上表原先八個 jobs，不包含下方 viewer-gate 與 r1 jobs。

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

## 本輪 integrator-collected measured data（原值照錄）

Measured from Codex rollout token_count events (total_token_usage at session end) and rollout first/last timestamps, 2026-11-24 (UTC wall clock). Integrator-collected Codex jobs only；以下六列由使用者提供，原值照錄，本次未獨立重讀 rollout 稽核。

| job | wall clock | input | cached input | output |
| --- | --- | --- | --- | --- |
| viewer-gate package (freeze, temporal QA, protocol, ledger, asset spec) | 13:31:30-13:54:59 (23.5 min) | 4,537,656 | 4,227,712 | 39,236 |
| viewer-gate review (REQUEST_CHANGES: public blinding key) | 13:55:34-14:00:42 (5.1 min) | 795,666 | 722,432 | 9,196 |
| blinding-key fix | 14:01:11-14:08:14 (7.0 min) | 687,452 | 646,272 | 15,855 |
| r1 light fix, lossless masters | 14:10:24-14:34:49 (24.4 min) | 5,856,798 | 5,751,168 | 40,304 |
| r1 delivery encodes | 14:35:25-14:49:01 (13.6 min) | 1,665,846 | 1,600,384 | 25,589 |
| r1 light review (APPROVE) | 14:49:35-14:56:40 (7.1 min) | 1,539,487 | 1,436,288 | 10,231 |

Human intervention time（Owner / integrator）仍為 **NOT MEASURED**。cached input 是 input 的子集，不另加；UTC wall clock 包含工具與等待時間，不代表人時。

### Derived — 一次燈號修訂與原始 A+B render 比較

一次燈號修訂、沒有新增圖片生成，包含無損 MASTER 與其後 DELIVERY 的成本代理量約等於原始 A+B render：

- Input：5,856,798 + 1,665,846 = **7,522,644**；cached input：5,751,168 + 1,600,384 = **7,351,552**（已包含在 input）。
- Output：40,304 + 25,589 = **65,893**；input + output：7,522,644 + 65,893 = **7,588,537**。
- 原始 A+B render 的 input + output：6,771,505 + 65,452 = **6,836,957**；7,588,537 / 6,836,957 = **約 1.11 倍**（約多 11.0%）。
- 表列四捨五入 wall clock：24.4 + 13.6 = **38.0 min**，原始 A+B 為 **35.0 min**；38.0 / 35.0 = **約 1.09 倍**。這是兩個 job 耗時相加，不含 job 間隔。

以上為 **derived 算術**，比較兩邊的製作 jobs；不含各自 review、viewer-gate 文件包或 blinding-key 修正，不能視為完整輪次成本、貨幣價格或人工工時。

## 2026-11-24 — H01 v2.1-r1 聆聽燈修訂 job

Owner 範圍：只修正兩版共用燈號；不生成圖片、不改聲音／字幕／其他影像，不做外部動作。基準 Git HEAD `695d7db4aaee1790a71ceff6e26afa124519be41`；本輪未提交。腳本、成片與驗證識別見 [freeze.md](freeze.md) 的 r1 節。

| 本輪項目 | 數值／狀態 |
| --- | --- |
| Codex tokens / UTC job 起訖與 wall clock | integrator-collected 實測見上表的 lossless masters、delivery encodes 與 light review 三列；製作兩個 jobs 的 token 加總見 Derived。 |
| 人工介入時間、貨幣費用 | **NOT MEASURED**；不以檔案時間或工具等待推算。 |
| ImageGen / TTS / paid AI request | 0；全部沿用既有素材及音軌。 |
| 本機完整影片 encode | 4 次成功＝2 次未採用純色燈 draft + 2 次最終燈罩紋理 r1；不是 4 部測試影片。 |
| 最終 metadata stream-copy remux | 2 次成功；恢復原片 TV range 與 1:1 SAR 標記，不新增影像／音訊 encode。可重跑 renderer 已帶相同 bitstream metadata 設定。 |
| 無損 MASTER | A r1、B r1 共 2 支 lossless masters；H.264 無損影像 encode，AAC packet stream copy，各 2 個原字幕 sidecars 的 byte copy。 |
| 後續 DELIVERY job | **52 次 shot encodes（26 A + 26 B）及 2 次 final muxes**；產出 2 支供手機播放的 H.264 High / L4.0、CRF 18 DELIVERY，AAC stream copy。無損 MASTER 保留；真人測試使用 DELIVERY，規格及驗證見 [freeze.md](freeze.md) 的 r1 DELIVERY 節；實體手機播放尚未驗證。 |
| A-only / B-only tokens 或成本拆分 | **NOT MEASURED**；共用同一 job，不平均分攤。 |
| 上傳／公開／YouTube 操作 | 0。 |

未採用 draft 保留於 gitignored `artifacts/genre-pilot-20261124/h01-light-draft-01/`，不能供真人測試。該版逐格差分已通過，但視覺檢查發現特寫燈罩被純色覆蓋；改重用既有燈罩紋理後重新編碼兩版。這是確定性本機修訂，沒有新增 ImageGen request。最終版第一次 verify 因舊純色驗證條件 `Cb < 135` 在 A f21 中止；實測該燈芯 Y/Cb/Cr 為 177/137/38，仍為亮青綠色。改用明定的亮度／色度範圍並保留整格預期合成 equality，再重跑全部驗證；不是隱藏渲染失敗或新增圖片。最終結果見時序 QA 與 freeze；QA 抽幀不計入 encode 數。
