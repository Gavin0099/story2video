# WhyNest Lab 生蛋動態樣片

WNL-021 的短版視覺試做。用原速實拍讓觀眾先看到手指停住生蛋、放開後再轉的現象。接著切入俯視示意，以外殼記號和內部液體的箭頭清楚呈現先後順序，最後回放真實畫面。英語旁白在本機生成，附英語與繁中兩條可選字幕。

## 畫面與來源

| 段落 | 畫面 | 科學重點 |
| --- | --- | --- |
| 實拍開場 | 同一顆生蛋在桌面上停止、接著恢復轉動 | 保留實際速度與接觸、放手的連續段落 |
| 剖視圖 | 同一個視野中，外殼記號停在原處，液體的箭頭持續轉動 | 外殼和液體可以有不同的轉動狀態。畫面標示為示意，延長停止段落供觀察 |
| 回放 | 先看外殼恢復轉動，再切回實拍中的放手瞬間 | 放手後，仍在轉的液體帶動外殼 |

實拍出自 Coyau 的《Spinning hardboiled and raw eggs 01》，在 Wikimedia Commons 公開。選用原片中生蛋段落，重新裁切成直式、節錄與回放、補上短標示、圖解、旁白和字幕。實拍片段維持原速，25 FPS 來源依輸出幀率轉成 30 FPS。此改作樣片依 CC BY-SA 3.0 授權。[原片與作者授權](https://commons.wikimedia.org/wiki/File:Spinning_hardboiled_and_raw_eggs_01.ogv) · [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)

短暫按停蛋殼時，生蛋內部的液體可繼續轉動。放手後，液體能使蛋殼重新轉動。示意圖放大了時序，省略蛋黃和蛋白的個別流動。[Exploratorium 實驗](https://annex.exploratorium.edu/cooking/eggs/activity-spin.html) · [Institute of Physics 實驗](https://spark.iop.org/spinning-eggs)

完整集數的雙蛋對照、英語稿及繁中字幕稿見文案庫。這支樣片採公開來源中可直接觀察的生蛋段落，動畫仍可用於後續自攝的雙蛋對照。[WNL-021 文案](../script-library/drafts-021-023.md#wnl-021)

## 本機重跑

將 Commons 公開的 1080p 轉碼存到 `artifacts/science-shorts/egg-motion-sample/coyau-source.webm`，來源 SHA-256 為 `c2ed2177faf36f77001c56ab6e38557ccd82be26b51e980bf61a5b77decdf8e9`。[Commons 1080p 影片](https://upload.wikimedia.org/wikipedia/commons/transcoded/3/31/Spinning_hardboiled_and_raw_eggs_01.ogv/Spinning_hardboiled_and_raw_eggs_01.ogv.1080p.vp9.webm)

```powershell
& ./artifacts/render-venv/Scripts/python.exe -I experiments/science-shorts/egg-motion-sample/render.py
```

輸出為 `wnl-021-motion-preview.mp4`，另附 `en.srt`、`zh-Hant.srt` 及 `render-evidence.json`。輸出都在同一個本機素材目錄。

## 資源實測與驗收

| 項目 | 本次實測 |
| --- | --- |
| 片長和檔案 | 13.60 秒，408 格，2,187,788 bytes |
| 規格 | 1080×1920，30 FPS，H.264、AAC、兩條可切換字幕 |
| 本機生成英語旁白與字幕 | 17.43 秒 |
| 分層合成與編碼 | 12.90 秒 |
| 本機整次執行 | 30.46 秒，含輸入雜湊核對與輸出 |
| 付費媒體 API | 0 次 |

上表只記錄這次短樣的機器時間。採公開原始素材，因此沒有新拍攝的計時資料。找素材、設計、檢查與返修的工時沒有完整計時，也沒有同題長版對照。

- Git 基準 `2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`。MP4 SHA-256 為 `53789550bbf49d83e284bb47804bb6fbb3ce9d81fb1c666f797a4965990af7e0`。
- 工程檢查以本機 `uv.exe --cache-dir ./artifacts/tooling/whynest-uv-cache sync --locked` 與 `run --locked pytest` 執行，61 項通過。`npm.cmd ci` 與 `npm.cmd run typecheck` 通過，本機 Node v24.13.0 高於 repo 固定範圍，npm 回報版本警告。`git diff --check` 通過。
- 以 `ffprobe -show_streams -show_format` 核對格式，以 `ffmpeg -xerror -map 0:v -map 0:a -f null NUL` 完整解碼。兩條字幕以 `ffmpeg -map 0:s:0`、`-map 0:s:1` 分別讀回，確認文字、斷行和時間相符。
- `blackdetect=d=0.15:pix_th=0.1` 與 `silencedetect=noise=-45dB:d=2` 未發現非預期黑場或長靜音。成片響度 -17.30 LUFS、true peak -1.43 dBTP。實際畫格檢查與 FFmpeg 紀錄存於樣片目錄。
- 獨立科學審查以同一支 MP4 的實際編碼畫格為準。約 1.0 秒可見手指接觸，1.4–2.0 秒可見放手後的姿態改變。5.4、6.4、8.9 秒的外殼標記固定，液體箭頭持續順時針移動。9.4 秒放手，9.6–10.4 秒外殼標記才恢復同向移動。抽查未發現關鍵科學錯誤。另用 FFmpeg/libass 渲染 6.4 秒英語與 10.4 秒繁中字幕，均未遮擋主要動作。其他播放器展示和主觀聆聽待驗證。
- 完整的雙蛋文案盲評、手機實機試看、真人理解與市場成效待驗證。
