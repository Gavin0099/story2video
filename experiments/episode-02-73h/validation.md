# Episode 02 驗收紀錄

日期為 2026-11-21。基準 Git SHA 為 `2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`（`codex/story-quality-lab`）。使用工作樹中的 73H 腳本與轉檔器，保留工作樹修改。

## 工程驗收

| 命令／操作 | 結果 |
|---|---|
| [README](README.md) 的 `python.exe -I experiments/episode-02-73h/render.py` 命令 | 產出 45.57 秒影片、1,367 格及雙語字幕。最終一次 58.2 秒，初版 57.2 秒；較早一次合成因低於 45 秒而中止，未計秒。此時間不含分鏡生成、下載、人工校閱與檔案檢查。 |
| 以普通文字檔替代 `--ffmpeg` 執行相同渲染入口 | 長度與 SHA-256 驗證在媒體輸出前拒絕。真實二進位檔經發行包驗證，FFmpeg 子程序使用絕對路徑與受限環境。驗證範圍為本機渲染入口與直接啟動的 FFmpeg，Python 環境與系統 DLL 使用本機既有信任。 |
| `ffprobe -v error -of json -show_entries stream:format=duration`，各 MP4 | H.264 1080×1920、30 fps、1,367 格、AAC，影音時長一致。母片與雙語燒錄版各兩軌，切換版另有 English 及 Traditional Chinese 兩條 `mov_text`。 |
| `ffmpeg -v error -xerror -i <mp4> -map 0:v -map 0:a -f null NUL`，各 MP4 | 三支完整解碼，無錯誤。 |
| `ffmpeg -i 73H-selectable.mp4 -map 0:s:0 check-en.srt -map 0:s:1 check-zh.srt` | 拆出的每語 12 段字幕與各自的 SRT 逐字與時間碼一致。 |
| `ffmpeg -i 73H-master.mp4 -vn -af loudnorm=print_format=json -f null NUL` | 整體響度 −16.95 LUFS，最高真峰值 −1.40 dBTP。 |
| `ffmpeg -vf select=…,scale=324:576,tile=4x3` 抽取每句字幕中間畫格，對照 73H 題卡與謎底 | 英繁可讀，未見裁切。揭曉含矮牆遮擋與玻璃反光，結尾保留「先接他」。 |
| `uv sync --locked`；`uv run --locked pytest` | 安裝成功，61 項測試通過。 |
| 在 `video/` 執行 `npm.cmd ci` 與 `npm.cmd run typecheck` | 成功。Node 24.13.0 顯示版本警告，repo 宣告 Node 22.16 至 23 以下。 |
| `uv run --locked python experiments/story-quality-lab/verify.py`；`git diff --check` | 結構檢查與 diff 空白檢查通過。 |

未驗證手機喇叭口播聽感、YouTube 播放器的字幕選單，以及未讀題者的推理體驗。本機測試使用獨立實驗腳本。

| 檔案 | SHA-256 |
|---|---|
| `73H-master.mp4` | `43e748fb7a3ec12706f7c5b9b26a2b559b243f20952dce9864c063ca01a5bdbe` |
| `73H-selectable.mp4` | `3f57848edd2a094f19bccb021d9a37fc86dcce058c07b3286b21f95d7f759e1f` |
| `73H-bilingual.mp4` | `41012bfdfdc7778603b5abe2176b3df555957ae0bd84c014a8fb99ff805a57c5` |
| `73H.en.srt` | `f924eb345a1089b6f8309e374fafb560cca34b93a2db8719047672e1e2295019` |
| `73H.zh-Hant.srt` | `b98654925105441942e28ba41313a259bade06ba03ab4d2ada54833ca209922a` |

## 市場驗收

73H 待上傳與發布授權。第 7 天、第 28 天的觀察窗自正式發布起算。外部直接支出及人工時間尚無完整紀錄。[首輪 Shorts 紀錄](../shorts-series/README.md)
