# 冰題目視覺新版驗收｜2026-11-21

Owner 要求先做一個主題，驗證插畫分層與科學動畫做法。本機交付，不涉及上傳、公開、建立頻道或正式引擎整合。

Git 基準：`2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`；本輪新增檔案仍未提交，保留進場前已有修改。以下 SHA 與本機凍結 inputs 表示實際驗收內容，不能將 HEAD 當成已收錄這些檔案的 commit。

## 結果與產物

| 產物 | 容器長度 | 畫面 | SHA-256 |
|---|---:|---|---|
| `ice-v2-zh.mp4` | 48.100 秒 | 1080×1920、30 FPS、1441 格、H.264/yuv420p、AAC | `6a257fb0855af005f1d912199cb897ceb4325efe23f6106868ebd2310fe28260` |
| `ice-v2-preview.mp4` | 11.600 秒 | 同規格、348 格 | `37c59f5fc80054234c928d93ac82124b4df8f9fde503ffbf440e7f93e667c540` |

影片位於 `artifacts/science-shorts/ice-visual-v2/`。完整片 6,183,374 bytes，短版 2,299,443 bytes；短版涵蓋開場與微觀放大，不含完整科學解釋，完整理解應看全片。

新 renderer SHA：`aad0052d5f0f486ee3cc6a05e80982e9a0c1dbedee7caa7710b38da549ad1438`。

Inputs SHA：`41a98e1cf1b6fd1eb8a9fc2dd5c0f95e48dc6203ccc7f5610186cc4bd5b170d3`。

原始配音 SHA：`0c8a69645c622b40bc36218ce77f5ce20da0a1454533c27981c1e15957cd3286`。逐句公開文案、claim_ids 與既有時間表相符；沒有把新版視覺審查當作新的文案盲測。原 AI 讀者的 88／89 分只屬於原稿。

## 工程驗收

1. 首次 preview 發現冰塊完全在水面上方時，浸水色層的矩形範圍為負。已在獨立審查前修正為只有與水面相交才套色；重跑所有預覽與入水關鍵格通過。失敗時未編碼，舊版產物未變更。
2. 新 visual review 不存在時，實際執行 `render.py --mode render` 回傳 exit 1，且 MP4 不存在；證據為 `preflight-rejected.json/.txt`。新審查通過、renderer 與 inputs SHA 相符後，才開始編碼。
3. `--mode render` exit 0，1441 格成功，編碼及短版生成共 87.11 秒；這不是總製作時間。旁白重用原檔，新圖像為兩次內建 image_gen 生成，未呼叫計費媒體 API；工具沒有回報貨幣成本，訂閱、審稿與人工仍未定價。
4. `--mode qa` exit 0：兩片規格、完整影音解碼、黑畫面（0.15 秒以上）、低於 -45dB 且至少 2 秒的靜音檢查通過；沒有宣稱逐格藝術品質或完整音訊聽驗。
5. 音量分析：完整片 -16.9 LUFS，短版 -17.0 LUFS；兩片 true peak 均 -1.4dBFS，無超過 0dBFS 的削波。完整片末段約 0.8 秒為原時間表的預期停留。
6. 中英文字幕以實際字型測量：字寬不超過 850px、段落高度不超過 250px。實際影片只有繁中燒錄字幕，另附中英文 SRT；沒有製作可切換字幕版。
7. 從實際 MP4 抽取九個段落中點、開場 0/0.5/1/1.5/2 秒與最後視訊格，存入 `actual-mp4/`。來源圖像、編碼後畫格及 QA 檔分別保存。

完整命令（由 repo 根目錄執行）：

```powershell
& 'D:/story2video/artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/ice-visual-v2/prepare.py
& 'D:/story2video/artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/ice-visual-v2/render.py --mode preview
# 此時審查尚未存在，預期 exit 1，且無影片輸出。
& 'D:/story2video/artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/ice-visual-v2/render.py --mode render
# 獨立 visual review 通過後，以下兩步 exit 0。
& 'D:/story2video/artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/ice-visual-v2/render.py --mode render
& 'D:/story2video/artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/ice-visual-v2/render.py --mode qa
$env:UV_CACHE_DIR='D:/story2video/artifacts/uv-cache'
& 'D:/story2video/artifacts/tooling/bin/uv.exe' sync --locked
& 'D:/story2video/artifacts/tooling/bin/uv.exe' run --locked pytest
cd video
npm.cmd ci
npm.cmd run typecheck
```

README 檢查：uv sync 成功；pytest **61 passed in 7.49s**；npm ci／typecheck 成功（0 vulnerabilities）。本機 Node v24.13.0 超出指定 >=22.16.0 <23，npm 有 EBADENGINE；沒有宣稱指定 Node 版本驗收。這些是既有核心的回歸檢查，新的試片由上述獨立影音 QA 驗證；未改 src/story2video、video/、SQLite、Episode v1 或治理契約。

## 科學畫面審查

- [製作前獨立審查](visual-review.md)：PASS，critical defects 0。另一個 AI agent 核對全部 11 個凍結檔的大小／SHA、九鏡原尺寸預覽與入水關鍵格。新審查綁定目前 renderer 與 inputs，沒有挪用舊 renderer 的通過結果。
- 核對重點：液態／冰皆 12 個同尺寸分子符號；同質量、較大體積、較低密度的因果；浸水與浮起示意；明示非晶體模型、不依比例。
- [實際 MP4 科學畫面抽樣](final-video-review.md)：PASS，critical defects 0。獨立 agent 檢視完整版九鏡聯絡表、八張原尺寸畫格及開場 0.5／1／1.5 秒，確認等量分子、浮冰、密度因果與示意標示；兩支 MP4 的大小及 SHA 與 QA 紀錄一致。短版僅核對 SHA 與機器 QA，沒有另做整段視閱。
- 最終回執 JSON SHA：`59f4fe519f11535ea87449567dede9f9dbdfcd193fdeb616e12603d4149885cc`；抽樣不代表完整影音聽看、逐格科學審查或專家／真人驗收。

## 真人與市場驗收

PENDING，新增真人樣本 0。分層素材與較多鏡頭能否提升美術接受度或留存尚無實驗；沒有因此決定開新頻道。

未驗證：手機實機完整觀看、完整影音人工聽看、專家背書、公開市場反應、完整人工成本、新 clone 跨平台重建與正式 Remotion 移植。水體與粒子為科普示意，沒有物理模擬。
