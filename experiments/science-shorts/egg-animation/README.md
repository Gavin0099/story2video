# WhyNest Lab 生蛋題全原創動畫

WNL-021 採全原創動畫。開場在同一桌面上比較兩顆蛋，放手後只有生蛋的外殼標記恢復轉動。接著用相同角度和尺度比較兩種剖面，最後演示同一顆生蛋按得更久的第二次試驗。畫面標出動畫示意及放大的示意時間。

畫面中的蛋、手指、質感、指示線與標籤由本機程式繪製，旁白由本機 Kokoro 生成。原樣片的 Coyau 影片只有前一輪樣片使用紀錄，這支成片的合成輸入為原創繪圖、配音與字幕。科學參考只用文字主張。[雙語定稿與來源](script.json)

## 文案審查

兩位無歷史讀者先看開場，再看完整雙語稿與分鏡。v2 各得 94、95 分。科學審查要求說清按停與移開的先後、對齊第 4 段繁中說法，以及補列長按推論的來源。v3 由另外兩位無歷史讀者再次盲評。

| v3 分項 | 讀者 A | 讀者 B |
| --- | ---: | ---: |
| 開場 /15 | 14 | 14 |
| 清楚度 /25 | 24 | 24 |
| 因果複述 /25 | 24 | 25 |
| 圖解構想 /20 | 19 | 19 |
| 節奏 /10 | 9 | 9 |
| 語言 /5 | 4 | 4 |
| 總分 /100 | 94 | 95 |

兩人都能複述熟蛋內外一起停止、生蛋液體在短暫停殼時繼續轉，以及液體若已停下便無法帶動外殼。讀者建議保留放手後的一拍，並讓長按後靜止的結果停在可看清的位置。長按減速是有來源支持的定性推論，畫面的角速度、停留長度與液體箭頭都是教學示意。[Exploratorium 雙蛋試驗](https://annex.exploratorium.edu/cooking/eggs/activity-spin.html) · [NASA JPL 實驗](https://www.jpl.nasa.gov/edu/resources/lesson-plan/planetary-egg-wobble-and-newtons-first-law/) · [Illinois Physics Van](https://van.physics.illinois.edu/ask/listing/609)

## 本機產出

```powershell
& ./artifacts/render-venv/Scripts/python.exe -I experiments/science-shorts/egg-animation/render.py preview
& ./artifacts/render-venv/Scripts/python.exe -I experiments/science-shorts/egg-animation/render.py render
```

第一步建立配音、時間軸和預覽影格圖。第二步核對原稿、聲音、渲染程式和預覽的實際雜湊，以及兩位理解度評分與科學圖解審查，通過後才輸出。影片、英語與繁中 SRT、編碼檢查產物位於 `artifacts/science-shorts/egg-animation/`。[編碼前審查紀錄](preflight-review.json)

## 成片與工程驗收

| 項目 | 實際結果 |
| --- | --- |
| 成片 | `wnl-021-original-animation.mp4`，40.80 秒，4,891,946 bytes |
| 格式 | 1080×1920、30 FPS、1224 格、H.264/AAC，可選英語和繁中字幕 |
| 配音與字幕首次產出 | 57.77 秒 |
| 合成與編碼 | 74.34 秒，付費媒體 API 0 次 |
| 影音 | -17.08 LUFS，true peak -1.45 dBTP |

Git 基準為 `2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`。MP4 SHA-256 為 `5cc6937b572c3e43375aa629671c6c012afa328d5c8ecfa42313993ccf8d3e27`。

- 實際跑過無審查收據的 `render`，程式拒絕編碼且沒有產出 MP4。之後在可核對的獨立審查通過後執行正式編碼。
- `ffprobe -show_streams -show_format` 規格核對及 `ffmpeg -xerror -map 0:v -map 0:a -f null NUL` 完整影音解碼通過。兩條字幕以 `-map 0:s:0` 和 `-map 0:s:1` 抽出，逐段比對時間、文字與換行均相符。
- `blackdetect=d=0.15:pix_th=0.1` 與 `silencedetect=noise=-45dB:d=2` 沒有檢出不預期黑場或長靜音。從實際 MP4 抽取 16 格查看開場對照、短按剖面、放手及長按段落。
- 獨立審查另外從該 SHA 對應的 MP4 抽取 23 格。2.00 至 2.47 秒兩顆蛋的殼都停住，3.37 秒只有生蛋的記號改位。17.60 至 18.30 秒熟蛋內外同停，24.27 至 25.57 秒生蛋蛋殼停住、液體仍轉。27.43 至 28.87 秒放開後殼再轉，長按對照也呈現減速、停止到放手維持靜止。兩條內嵌字幕各有六段，時間與內容核對一致。抽樣未見關鍵科學錯誤。
- `uv sync --locked` 與 `uv run --locked pytest` 以本機 `artifacts/tooling/bin/uv.exe` 執行，61 項通過。`npm.cmd ci`、`npm.cmd run typecheck` 與 `git diff --check` 通過。使用本機 Node v24.13.0，npm 提示超出 repo 固定 Node 範圍。
- 主觀聆聽、手機上的實際播放器、真人理解和公開成效待驗證。

## 配色修訂

比較圖使用相同的開場和生蛋剖面影格，展示冰藍／深海藍、鼠尾草綠／森林綠、霧紫／莓果紫。冰藍版採用淺藍桌面、深藍剖面與暖色蛋殼。調色以已驗證的原創成片為輸入。英文旁白及英語、繁中字幕以相同封包與時間直接複製。

```powershell
& ./artifacts/render-venv/Scripts/python.exe -I experiments/science-shorts/egg-animation/palette.py preview
& ./artifacts/render-venv/Scripts/python.exe -I experiments/science-shorts/egg-animation/palette.py ice
```

輸出位於 `artifacts/science-shorts/egg-animation/palette-revision/`。三組靜態對照為 `palette-comparison.png`，冰藍完整影片為 `wnl-021-ice-palette.mp4`。成片 SHA-256 為 `bdeb41bfc80cf12b11cdd322cbfe3a0422586523b36125576f3a62c5e5619421`，對應的輸入、調色表與程式雜湊見同目錄的 `ice-evidence.json`。

- `ffprobe -show_packets -show_data_hash sha256` 核對音訊及兩軌字幕的封包與時間一致。影片為 40.80 秒、1080×1920、30 FPS、1224 格。
- `ffmpeg -xerror -map 0:v -map 0:a -f null NUL` 完整解碼通過。黑場與靜音偵測沒有回報異常，測得 -17.08 LUFS、-1.45 dBTP。抽看成片開場、熟蛋停轉、生蛋停殼、放手和長按結果。
- 獨立審查抽取冰藍成片第 60、549、728、767、866、1161 格，確認蛋殼定位點、液體箭頭、內部追蹤點與說明文字都可辨識。
- 沿用上述 Git 基準。使用本機 `uv.exe --cache-dir ./artifacts/tooling/whynest-uv-cache run --locked pytest`，61 項通過。此次驗收涵蓋本機成片，手機播放器、真人理解與市場成效待驗證。

## 改拍鏡頭與剖面

WNL-021 開場以同一張桌面比較兩顆蛋，約 2.62 秒放手，約 3.23 秒切近生蛋。約 13.70 秒與 21.47 秒從蛋殼淡入同位置、同角度的內部示意，方便對照外殼和內部是否一起轉。殼上定位點、液體箭頭和狀態提示分層繪製。長按段維持放大示意與獨立標記。

兩顆蛋、手指、桌面與光影均由程式繪製。使用深色桌面襯托蛋殼，綠色定位點連到生蛋內部的箭頭。鏡頭安排參考同題的直式示範及 Sky Blue 影片的尺度轉場。旁白時間、英文旁白與英／繁中可選字幕沿用已核准原片。[同題短片](https://www.youtube.com/watch?v=hFcBGDKfn8I&t=8s) · [日本機械學會](https://www.jsme-fed.org/experiment-e/2009_12/005.html) · [NASA／NOAA](https://www.youtube.com/watch?v=ehUIlhKhzDA&t=78s)

```powershell
& ./artifacts/render-venv/Scripts/python.exe -I experiments/science-shorts/egg-animation/camera.py preview
& ./artifacts/render-venv/Scripts/python.exe -I experiments/science-shorts/egg-animation/camera.py render
```

輸出位於 `artifacts/science-shorts/egg-animation/camera-revision/`。預覽包含 `preview.mp4` 與 `shot-contact.jpg`。正式編碼核對該次預覽、原片、時間軸、科學稿、共用程式及 FFmpeg 的雜湊，並要求同一組輸入的獨立畫面審查。

- [獨立製作前審查](camera-review.json) 核對 10 項檔案雜湊與預覽成片 24 格。未放置審查記錄時，`camera.py render` 按預期拒絕編碼。原稿的理解度評分沿用原先紀錄。
- 正式檔 `wnl-021-camera-revision.mp4` 為 40.80 秒、1080×1920、30 FPS，共 1224 格。編碼 110.31 秒，付費媒體呼叫 0 次。影片 SHA-256 為 `f53d502df7d9bce2f61e68d89cff441bd5980f9886a71abfd88d65f2e82dfe45`，收錄於 `render-evidence.json`。另備 `wnl-021-opening.mp4` 快速觀看開場。
- `ffprobe -show_streams -show_format` 核對格式，`-show_packets -show_data_hash sha256` 核對音訊及雙語字幕的內容與時間與原片一致。以 `ffmpeg -xerror -map 0:v -map 0:a -f null NUL` 完整解碼。黑場與靜音掃描通過，-17.08 LUFS、-1.45 dBTP。
- 獨立抽驗解碼正式檔 9 格，確認放手切近時的蛋殼姿態相符，標記清楚，停殼轉液、放手再轉與長按靜止均可辨。預覽以手機寬度抽看英文與繁中字幕和圖解標記。真實手機播放器的字級與介面、真人理解及市場成效待驗證。
- Git 基準為 `2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`。`uv sync --locked`、`uv run --locked pytest`（61 項）、`npm.cmd ci`、`npm.cmd run typecheck` 與 `git diff --check` 通過。實際 Node 24.13.0，npm 提示與指定 Node 22.x 不符。
