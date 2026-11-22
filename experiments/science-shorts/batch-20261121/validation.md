# 科普試片驗收紀錄

Git HEAD：`2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`。本輪交付為未提交工作樹；保留進場前其他未提交內容。範圍為使用者授權的三支科普本機pilot，不代表完整SC-00/01產品化、M1完成或公開核准。

## 工程驗收

| 影片 | 最終MP4容器時長 | 影格 | 文稿分數A/B | 最終一次本機處理 |
| --- | --- | ---: | --- | ---: |
| ice | 48.10s | 1441 | 88/89 | 31.97s |
| sky | 46.10s | 1381 | 87/86 | 105.82s |
| space | 51.80s | 1552 | 89/87 | 121.04s |

處理時間以各片provenance記錄為準，含該次本機合成/字幕/渲染/初步解碼；冰重跑有重用音檔，不能與其他兩片直接比較。時間不含完整研究、修正、獨立審查及人工工時，不能當成總生產成本。

| 命令/檢查 | 結果 |
| --- | --- |
| `uv sync --locked`；`uv run --locked pytest` | 成功；61 passed。實際uv為artifacts/tooling/bin/uv.exe，UV_CACHE_DIR指定同磁碟artifacts/uv-cache |
| `video/`: `npm.cmd ci`；`npm.cmd run typecheck` | 成功；Node24.13.0對repo要求22.x有EBADENGINE警告 |
| `python -I experiments/science-shorts/batch-20261121/finalize-gate.py` | 來源機構去重、兩讀者分項重算、public words/visual等值、hash全部相符 |
| README渲染命令加`--reuse-audio` | 三集成功；45–60秒。前次sky44.73秒在影片前被拒，調結尾非語音停留後重審/重跑 |
| `artifacts/render-venv/Scripts/python.exe -X utf8 experiments/science-shorts/verify.py --mode all` | PASS；10個實際main負面案例+1正控制；12個MP4規格/完整解碼/音量、雙語字幕/內嵌字幕回讀，實際MP4逐cue抽格 |
| `artifacts/render-venv/Scripts/python.exe -I artifacts/science-shorts/batch-20261121/check-black-silence.py` | 三支繁中試看片無blackdetect片段；只有sky結尾43.88075–46.1秒的2.21925秒靜音，與加長非語音收尾一致，無中途長靜音 |
| 獨立事實/科學圖解審查與最終MP4抽格 | 九核心claim、29組英中cue與三片抽樣科學畫面無critical defect；保留首次BLOCK和修正 |

驗收原始argv、stdout/stderr、exit code與file hashes在 `artifacts/science-shorts/batch-20261121/qa.json` 和 `qa-evidence/commands/`。[詳細工程審查](engineering-review.md) · [媒體抽驗](reviews/final-video-review.md) · [成本/素材權利](rights-and-cost.md)

初次以預設C槽uv cache執行README命令因暫存跨磁碟WinError17失敗；改設同磁碟UV_CACHE_DIR後sync與61項測試成功。黑畫面/靜音補驗argv與結果另存black-silence-qa.json及各片log。完整影音主觀聽感仍待真人。

| 試看片 | SHA-256 |
| --- | --- |
| `ice-zh.mp4` | `9fc5e599b90a086a5fbc32d7647067a4442119bb0ed119c33a7c262afc15d94f` |
| `sky-zh.mp4` | `dc0c4d365f8305bda8dddb7aad85d63915a645813178093ca17e925a68bd288f` |
| `space-zh.mp4` | `60475a4f6126bee867b63c340b3550b6166040dac052890a571e92925bd695ea` |

最終ScienceScript SHA-256：`d0b7de7d7ac4c1aa9986840999721c83735fea615703b0ba3479648f00a73cf8`。Renderer：`432700a6bc30e8295ccaeda13c98599c66335b888a704df202e065853cedd1d8`。QA腳本：`72c345548adfe7523a94793d6dc6842a2cb69d145ce2e0f38ea6d451947080f0`。

未驗證：手機實際播放/字幕與喇叭聽感、真人五人首次理解度、獨立專業科學家認證、YouTube播放器字幕/上傳、跨平台重建、全新clone無資產重現。FFmpeg/ffprobe已綁定binary；Python環境、套件與Windows/DLL沿用本機信任，沒有整體信任鏈認證。原生AI讀者是提示隔離，沒有CLI沙箱認證。沒有修改src、Episode v1、SQLite、video或治理版本。

## 市場驗收

**PENDING**。真人樣本0；D7/D28、自然有效觀看、受眾重疊與回訪均N/A。未建立頻道、未上傳、未公開。AI分數與工程通過不代表市場成功。建議目前先不開第二頻道；若真人及持續產能驗證通過，一般科普定位傾向獨立。[頻道判斷與後續決策條件](channel-decision.md) · [主持包](viewer-test.md)
