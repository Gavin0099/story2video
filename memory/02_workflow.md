# Tech Stack

## Repo Facts

- 2026-11-22 科普分流已落實。`@WhyNestLab` 的實際 channel ID 是 `UCJpx-XFeS91Vd26QokWAWOw`，人工 Studio 上傳前比對此 ID。科普三片已私人存放，見 `experiments/science-shorts/channel-split-20261122/approved-settings.json`。目前共用 repo 及既有製片能力，正式 CLI／Episode 未整合雙頻道。

- 2026-11-22 Owner 已採納科普獨立頻道並選定 WhyNest Lab｜一分鐘科普、Primary 連線、三支 v2 私人試看。兩品牌共用 repo／製片能力，分開目標頻道、品牌、審稿與交接資料；本輪先人工 Studio，不改正式 CLI／Episode／SQLite。原海龜湯 CluePause 的歷史 channel ID 為 `UCG_nXXBzgg54w2zhkZ33Row`，需重新讀回驗證；新科普 channel ID 保持 null，未確認不得上傳。Primary 首次啟動要求重新驗證，尚無線上變更。見 `experiments/science-shorts/channel-split-20261122/approved-settings.json`。

- 2026-11-21 天空／太空視覺新版：新增同場景藍天與夕陽、透明太空人，沿用冰版凍結的字型／字幕函式並將helper納入各題新inputs（14／13檔）。每題另綁新renderer／inputs的獨立科學回執才encode，再審查實際MP4方向與局部振動。`skills/science-shorts-visuals/`為repo副本，本機可發現副本在Codex skills；流程涵蓋來源→文案→分鏡→素材→機制→新審查→成片QA與stage scope。Owner後續美術授權取代初版vector-only限制，科學／rights與原旁白時序仍保留。這是隔離Pillow／FFmpeg原型，未改正式Remotion／Episode／SQLite／發布合約。

- 2026-11-21 冰題目視覺新版：Owner 授權先做一個主題的畫面實驗；用內建 image_gen 產生玻璃杯場景及透明冰塊，Pillow 分層合成場景／微觀放大／粒子排列與密度動態，沿用既有英文旁白及繁中字幕，FFmpeg 本機編碼。`ice-visual-v2/inputs.json` 凍結 11 個輸入，新獨立視覺回執另綁 renderer／inputs SHA 才允許 encode，並抽驗實際 MP4；舊 gate 和影片不改。這是隔離視覺原型，正式 Remotion、Episode v1／SQLite 與發布架構未變；後續採用何種正式製片方案仍待 Owner 試看。

- 2026-11-21科普隔離pilot：使用者授權先文案、sub-agent review達標再本機影片，形成PLAN的單次M4前置例外；以Issue #8的85分理解度候選門檻及獨立Fact/Visual硬門檻運作。實驗共用既有Kokoro/模型、Episode02執行檔binding/字幕時間helper與FFmpeg；新加Pillow科學圖解composition及獨立驗收。正式Remotion入口仍為骨架，未實作共用Episode v2、改動v1/SQLite或宣告完整SC-00/01產品化。資料/版本證據在 `experiments/science-shorts/batch-20261121/`，影片在ignored artifacts；頻道建議先不開，真人及持續產能驗證後再決定一般科普獨立定位。

- Python 3.13 runs the `s2v` CLI. Episode v1 JSON is the source of content and SQLite stores revision, hash, state, and audit events.
- Node 22 checks the TypeScript and Remotion scaffold under `video/`.
- GitHub Actions runs Python and TypeScript checks. The pinned AI Governance Framework submodule supports development hooks and governance checks.
- M0 uses local fixtures. Rendering and YouTube publishing belong to later milestones in `PLAN.md`.
