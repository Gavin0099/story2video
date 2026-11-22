# Episode 02 · 73H〈窗裡的求救燈〉

英文旁白使用 73H 的矮牆、手電筒和對街店面反光作為線索。猜題之後揭曉船長怎麼看見訊號，最後由姊姊說「先接他」。[題卡](../story-quality-lab/readers/73H.md) · [謎底](../story-quality-lab/reveals.md#73h)

## 成片與字幕

45.57 秒成片在本機 `artifacts/73h-episode02/`，來源腳本為 [story.json](story.json)。影片規格為 1080 × 1920、30 fps、H.264／AAC。[驗收紀錄](validation.md)

| 檔名 | 用途 |
|---|---|
| `73H-master.mp4` | 準備上傳的乾淨母片 |
| `73H.en.srt` | English（US）可切換字幕 |
| `73H.zh-Hant.srt` | 中文（繁體）可切換字幕 |
| `73H-selectable.mp4` | 本機可切換版。支援 MP4 字幕軌的播放器可選英語、繁中或關閉。 |
| `73H-bilingual.mp4` | 本機校閱版，畫面同時顯示英文及繁中字幕 |

影片獲得上傳授權後，在同一支母片的 YouTube Studio 字幕頁分別上傳兩個 UTF-8 SRT，指定 English（United States）與中文（繁體）。在播放器的 CC 選單逐一驗證。公開另依專案的人工授權關卡。[YouTube 字幕說明](https://support.google.com/youtube/answer/2734796)

## 重跑

1. 準備獨立的 Python 3.12 環境，安裝 `kokoro-onnx==0.6.1`、`onnxruntime==1.26.0`、`numpy==2.5.5`。旁白使用本機 Kokoro `am_michael`，無外部語音請求。
2. 準備 Windows Gyan FFmpeg 9.1 Essentials。驗收使用 7z 安裝包，SHA-256 為 `835b9a733445ba7a56a37a26cf7bde84e2f3ce7da2a8ec984276bb2abb1b922c`。[Gyan 9.1 釋出頁](https://github.com/GyanD/codexffmpeg/releases/tag/9.1)
3. 建立此集專用的工作目錄，複製原始 `storyboard.png`。在其 `models/` 放入 `kokoro-v1.0.int8.onnx` 和 `voices-v1.0.bin`。[Kokoro 模型釋出頁](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0)
4. 從 repo 執行下方命令。以實際安裝位置替換兩個執行檔路徑，並以專用目錄隔開各次重跑。雙語校閱版採 Windows Segoe UI 與 Microsoft JhengHei。

```powershell
& 'D:\story2video\artifacts\render-venv\Scripts\python.exe' -I experiments/episode-02-73h/render.py `
  --work 'D:\story2video\artifacts\73h-episode02' `
  --ffmpeg 'D:\story2video\artifacts\render-tools\verified\ffmpeg-9.1-essentials_build\bin\ffmpeg.exe' `
  --manifest experiments/episode-02-73h/render-manifest.json
```

[render-manifest.json](render-manifest.json) 記錄實際使用的執行檔、模型與插畫的大小及 SHA-256。原始插畫使用內建 ImageGen 生成。提示內容是 3 欄 2 列、六格直式分鏡，台灣淹水巷道、同一對姊弟和橘色搜救艇，依序呈現拉回矮牆後、船駛過、調整手電筒方向、玻璃閃光、船繞過牆及救生員接住弟弟。儲存原始插畫可重用相同畫面。
