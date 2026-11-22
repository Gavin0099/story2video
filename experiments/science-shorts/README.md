# 一分鐘科普本機試片

本輪依 [Issue #8](https://github.com/Gavin0099/story2video/issues/8) 的科普內容方法，製作冰、天空與太空通訊三支獨立pilot。Owner 2026-11-21 授權文案→sub-agent審查→達標後本機影片→頻道建議；沒有上傳或建立頻道。正式 M0 CLI、Episode v1、SQLite 與 video/Remotion骨架未整合科普功能。

## 文案與審查

- [WhyNest Lab 文案庫](script-library/README.md)整理已凍結的候選稿、下一批雙語文案和審查流程。公開狀態及成效沿用原發布紀錄。

- [最終中英文完整文案](batch-20261121/scripts-final.md)：含實際片長、分數與已核對來源。[Writer原稿與完整分鏡](batch-20261121/scripts-v1.md)保留作版本證據；最終修來源metadata及天空結尾非語音停留，公開旁白/字幕/分鏡不變。
- [最終腳本](batch-20261121/scripts-final.json)・[來源卡](batch-20261121/source-cards.json)・[預先固定門檻](batch-20261121/gate-policy.json)
- [獨立事實/科學圖解審查](batch-20261121/reviews/audit.md)：九個核心claim、兩獨立機構/claim；保留兩項視覺BLOCK與修正證據。
- [讀者A](batch-20261121/reviews/reader-a-v1.json)・[讀者B](batch-20261121/reviews/reader-b-v1.json)：先只給hook，再提供完整公開文案和精簡圖解計畫；不提供來源/答案表/分數門檻。這是無歷史native agent提示隔離，沒有宣稱CLI沙箱驗證，並非真人。
- [製作前Gate](batch-20261121/editorial-gate.json)：固定85分理解度候選門檻外，事實/圖解critical defect必須為零。分項重算，不以分數證明科學真實。

| 題目 | 讀者A | 讀者B | 文字稿修改輪數 |
| --- | --- | --- | --- |
| 冰為什麼浮在水上？ | 88 | 89 | 0 |
| 天空為什麼是藍色？ | 87 | 86 | 0 |
| 隔著真空，太空人怎麼通話？ | 89 | 87 | 0 |

兩位讀者都能重述機制，仍提醒冰稿略重複、天空觀看方向容易混淆、英文carrier有輕微歧義；原文非critical瑕疵保留在讀者記錄。獨立查核排除了無法重開的NASA Cosmicopia來源，換成可訪問的NASA EM頁；[來源與時序調整器](batch-20261121/finalize-sources.py)保留parent SHA並核對所有公開文字/分鏡等值。天空第一次實測44.73秒被45秒下限擋下，最後非語音停留由0.8延至2.1秒，增加39格，保留[失敗紀錄](batch-20261121/render-attempts.json)與[timing-only審查](batch-20261121/reviews/timing-only-review.json)。沒有改語速或為取得高分降低量表。

## 產物

Owner 回饋畫面不生動後，另有 [冰題目的視覺新版](ice-visual-v2/README.md)：同旁白、同時間，加入內建生圖素材與分層運鏡，另做新科學畫面審查。原批次不被覆寫。做法比較見 [視覺評估](visual-direction-review.md)。

Owner 驗看冰新版後，續作 [天空／太空視覺新版](sky-space-visual-v2/README.md)，並將流程整理為 `skills/science-shorts-visuals/`；本機 skill 副本與 repo 版本一併驗證。三題仍保留各自原稿與獨立新畫面審查，不涉及上傳或建立頻道。

影片與大檔位於 `D:/story2video/artifacts/science-shorts/batch-20261121/<ice|sky|space>/`：`<id>-zh.mp4` 為繁中燒錄試看片，`<id>-en.mp4` 為英文燒錄版，`<id>-selectable.mp4` 有可切換中英字幕，`master.mp4`為無字幕母片，另有`en.srt`及`zh-Hant.srt`。英語旁白一致，字幕不混燒；兩種profile不能當成兩個獨立題材樣本。

每集保留實際TTS生成的timeline.json、narration.wav、provenance.json與ffprobe資料。圖解為Pillow程式化動畫，FFmpeg沿用既有本機編碼器；正式Remotion仍只有預留入口，未宣稱本輪完成ScienceShort產品整合。沒有AI圖片輪播或下載別人的科學插圖。`provenance.models`沿用Episode02完整輸入binding，當中的storyboard.png為未使用的舊binding；實際本輪僅讀取兩個模型檔，畫面由render.py產生。

[完整驗收紀錄與影片SHA-256](batch-20261121/validation.md) · [工程驗收細節](batch-20261121/engineering-review.md) · [實際MP4科學圖解抽驗](batch-20261121/reviews/final-video-review.md)

## 重跑

需本機現存Python 3.12 render venv：kokoro-onnx 0.6.1、onnxruntime 1.26.0、numpy 2.5.5，本次加裝Pillow 12.0.0。Windows安裝Segoe UI/Microsoft JhengHei；兩個Kokoro模型與FFmpeg由[Episode02 manifest](../episode-02-73h/render-manifest.json)驗證大小及SHA-256。[權利與成本](batch-20261121/rights-and-cost.md)

```powershell
python -I experiments/science-shorts/batch-20261121/finalize-gate.py
& 'D:/story2video/artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/render.py `
  --batch experiments/science-shorts/batch-20261121 `
  --output artifacts/science-shorts/batch-20261121 `
  --tools artifacts/render-tools/verified/ffmpeg-9.1-essentials_build/bin `
  --models artifacts/73h-episode02/models
```

可加 `--episode ice` 單集重跑及 `--reuse-audio` 重用同腳本且hash相符的本機音檔。改旁白或圖解需新審查，舊Gate會拒絕。渲染入口沒有YouTube或頻道寫入功能。重跑依賴本工作樹既有Episode02 helper及模型，不宣稱全新clone無資產即可離線成片。

README工程命令照repo執行；本機uv位於 `artifacts/tooling/bin/uv.exe`，需設 `UV_CACHE_DIR=D:/story2video/artifacts/uv-cache`避免Windows跨磁碟暫存錯誤。執行 `uv sync --locked`、`uv run --locked pytest`，在video/執行`npm.cmd ci`、`npm.cmd run typecheck`。

```powershell
& 'D:/story2video/artifacts/render-venv/Scripts/python.exe' -X utf8 experiments/science-shorts/verify.py --mode all
python -I experiments/science-shorts/batch-20261121/write-delivery.py
```

`verify.py`重算來源/分數/凍結版本、執行10個實際render.main負面案例與1正控制，再驗全部12個MP4、字幕回讀、音量及從實際MP4抽格。其輸出為ignored `artifacts/science-shorts/batch-20261121/qa.json`；成片抽樣科學審查須另有獨立agent回執，不能只靠規格檢查通過。

## 人類與市場驗證

[真人試看主持包](batch-20261121/viewer-test.md)・[空白記錄表](batch-20261121/viewer-record.csv)・[頻道決策](batch-20261121/channel-decision.md)

先不建立第二頻道。定位上傾向將一般科普獨立經營，但目前沒有真人理解度、實際觀眾重疊、完整人工成本及D7/D28公開成效。五名真人與另行授權的公開試驗尚未完成，不能宣告產品或市場通過。完整SC-00/01資料契約、九題選題生成器、正式CLI整合與上架管線不在本次pilot交付範圍。
