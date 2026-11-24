# H01 v2.1 凍結紀錄

日期：2026-11-24（Asia/Taipei）。**EXPLORATORY ONLY / HUMAN_TEST_PENDING**。Owner 凍結兩版；本次沒有重新生成圖片、重渲染影片或追加修正。只讀既有成片、解碼 QA 影格與撰寫紀錄，沒有 commit、push、上傳或 YouTube 操作。

本次工作分支：`codex/cluepause-h01-viewer-gate-20261124`；檢查基準 HEAD：`e189e294a09120588006885ddbe40ac837928c34`（PR #25 head）。這個 SHA 不包含本次未提交文件。

| 來源 | Git SHA / SHA-256 |
| --- | --- |
| A+B 製作實作 commit | `4784b93a6d53509e91343c1135df438a21b2309a` |
| 製作起點／motion fix | `6270889a9de8cfb056c7009b69ffa01f7e02e474` |
| 腳本來源 commit | `fe2ce6abd4c3ec1d8537850557077a1abd7c930e` |
| shared/urban_horror-v2.1.md SHA-256 | `83df72c03352d74ceb6977bcc665f0d6a715e37fae0ad10b81f6e1e8720c7bce` |

媒體本身在 gitignored `artifacts/`，不是上述 commit 內的 blob；以以下實測雜湊綁定。歷史製作來源見 [h01-v2.1-ab.md](../h01-v2.1-ab.md)。

| cut（僅主持人使用） | repo-relative MP4 | SHA-256 |
| --- | --- | --- |
| STILL（原 A） | `artifacts/genre-pilot-20261124/h01-v2.1/A/h01-v2.1.mp4` | `fbe60ff93d13cd8f8fac105b7c0da78445aca2fab3ef76d5891f7ab7d3402412` |
| MOTION（原 B） | `artifacts/genre-pilot-20261124/h01-v2.1/B/h01-v2.1.mp4` | `2d636b0304c4e3744b32e424a40ee940bf59f4136f96f0f10ea4b25b369f11fd` |

兩版各為 **39.000000 s、1,170 frames、1080 × 1920、30/1 fps**；H.264、yuv420p。實際逐格 PTS 為 `n/30`，`n=0..1169`。音軌各一條：AAC、48,000 Hz、stereo 2 channels、39.000000 s、ffprobe bitrate 192,046 bit/s；另有一條 video stream，沒有 muxed subtitle stream。

字幕為相鄰外掛 SRT，沒有把旁白字幕燒入 MP4（片頭標題不等於旁白字幕）。以下四個檔案各 20 cues；相同語言兩版雜湊一致。

| repo-relative caption file | SHA-256 |
| --- | --- |
| `artifacts/genre-pilot-20261124/h01-v2.1/A/h01-v2.1.en.srt` | `c36c869765801e49088a75346d2bdc91b2b4b32d0b51e1d65ab3a15c5833ff2a` |
| `artifacts/genre-pilot-20261124/h01-v2.1/A/h01-v2.1.zh-Hant.srt` | `ab0a17dc4884f6ab2b1533b855d35059d09e6a85626626c4fac7e555ca792707` |
| `artifacts/genre-pilot-20261124/h01-v2.1/B/h01-v2.1.en.srt` | `c36c869765801e49088a75346d2bdc91b2b4b32d0b51e1d65ab3a15c5833ff2a` |
| `artifacts/genre-pilot-20261124/h01-v2.1/B/h01-v2.1.zh-Hant.srt` | `ab0a17dc4884f6ab2b1533b855d35059d09e6a85626626c4fac7e555ca792707` |

兩版 compressed audio packet SHA-256 均為 `97f9ad93d95fd719526e6f7a739f9b4b825bbab520a4998d05fb0a38461b1d66`。歷史 common `shared/mix.wav` SHA-256：`d1fe9f6dd57641ab143951d22286303b51e7fb941711e94770f18edee8177422`。相同音訊不代表聲音品質或真人理解已通過。

重跑：從 repo 根目錄執行 `python -B experiments/cluepause/genre-pilot-20261124/h01-viewer-gate/temporal_qa.py`。使用既有 [tools.lock.json](../motion/tools.lock.json) 的 FFmpeg / ffprobe，執行前核對 bytes 與 SHA-256；工具來源工作區保持唯讀。本次兩版 MP4 在 QA 前後 SHA-256 一致。量測輸出在 `artifacts/genre-pilot-20261124/h01-viewer-gate/measurements.json`。

工程驗收：媒體識別、全片解碼、逐格時序、字幕結構及指定音訊事件對位 PASS；故事道具／角色連續性 FAIL，關鍵動作 fidelity PARTIAL，詳見 [temporal-qa.md](temporal-qa.md)。市場驗收：**NOT_TESTED / HUMAN_TEST_PENDING**。既有 90 分規則沒有降低；腳本 90 分不代表影片好看，也不代表本片正式驗收或可公開。

## 本次驗證紀錄

| 命令／檢查 | 實際結果與範圍 |
| --- | --- |
| `git branch --show-current`、`git rev-parse HEAD` | 分支與本頁基準 SHA 相符；本次文件尚未提交。 |
| `python -B experiments/cluepause/genre-pilot-20261124/h01-viewer-gate/temporal_qa.py` | 最終版 exit 0；兩版各 1,170 格、39 頁、20 字幕 cues／語言、15 voice events 與 5 個指定咳嗽／尾詞事件對位 PASS，凍結 hash 不變。 |
| 舊版分派 dry-run | 舊版將操作 seed、播放碼對照及分派放在公開來源中，已作廢並移除，不能作為正式測試排程。新版私密分派與承諾後揭露程序見 [viewer-protocol.md](viewer-protocol.md)；修正驗證見下方。 |
| Python stdin 靜態掃描本目錄全部檔案及 parent README | 個人絕對路徑 0、trailing whitespace 0、Python AST PASS、相對文件連結存在；另核對 library 15 個 source path/hash 全部相符。初版連結掃描誤讀舊 README code fence 內的 regex，排除 code fence 後重跑為 0 findings，沒有改寫舊段落。 |
| Python stdin 對本目錄、QA artifacts 及 parent README 全檔逐 byte 路徑掃描 | 2,541 個檔案（含抽幀圖片及 JSON）個人絕對路徑 0 findings。 |
| `git diff --check` | exit 0。另直接掃描新增 untracked 檔案的 trailing whitespace，避免把 tracked diff 檢查誤稱涵蓋新檔。 |
| README 的 `uv sync --locked`、`uv run --locked pytest`、`video/` 的 `npm ci`／`npm run typecheck` | 本次未重跑：交付範圍為紀錄／QA 腳本；沒有 src、video、依賴、狀態機、SQLite 或治理改動，不把歷史驗收當成本次 PASS。完整引擎／影片工具專案回歸未驗證。 |

未驗證：真人 1× 同步視聽、主觀流暢度／聽感、手機字幕閱讀、首次理解／偏好、任何市場或公開數據。沒有外部 originality／rights 新查核、發布授權或正式接受判定。沒有 commit、push、YouTube 動作、memory 編輯或唯讀來源工作區寫入。

## 公開 repo 分派洩漏修正驗證

2026-11-24（Asia/Taipei）；基準 HEAD 仍為 `e189e294a09120588006885ddbe40ac837928c34`，修正尚未提交。公開來源中的操作 seed、固定播放碼 key、舊分派 CSV 及其雜湊已移除，舊排程作廢。正式排程必須使用主持人新建的私密高熵 seed；目前沒有正式分派、承諾發布、招募或真人測試。啟動欄及結果表的正式承諾欄保持空白。

| 命令／檢查 | 實際結果與範圍 |
| --- | --- |
| `python -B experiments/cluepause/genre-pilot-20261124/h01-viewer-gate/assign_viewers.py --n 10 --seed throwaway-review-only-not-for-viewing --output artifacts/genre-pilot-20261124/h01-viewer-gate-private/throwaway-review.json` | exit 0；只印 SHA-256 承諾。以 `Get-FileHash` 核對原始 bytes 相符，私密 JSON 含 seed、N、code key 與 10 個空 slot；這是拋棄式測試 seed，禁止用於真人排程。 |
| `git check-ignore -v -- artifacts/genre-pilot-20261124/h01-viewer-gate-private/throwaway-review.json`；生成前後 `git status --short --untracked-files=all` 比較 | exit 0；套用 `.gitignore:8:/artifacts/`，前後 status 完全相同，沒有新增可提交的生成檔。Git 另警告無法讀取全域 ignore；repo 本身規則已直接驗證。測試檔已刪除。 |
| Python stdin CLI／分派驗證 harness（`python -B -`） | exit 0；N=8..12 可重現且組間差 ≤1、slot 唯一、碼與 cut 對應一致。seed argument 與 private file 得到相同 bytes；不同 seed 更新中性碼；stdout 精確等於承諾。缺省／空 seed、兩種 seed 同用、公開輸出路徑、repo 內公開 seed 檔、缺失 seed 檔均被拒絕；覆寫被拒絕且原 bytes 不變。所有拋棄式 JSON 與 seed 檔已清除。初次 PowerShell harness 遇預期的拒絕 stderr 而中止，finally 已清理；改由 Python harness 擷取 stderr 後完成上述驗證。 |
| `git ls-files --cached --others --exclude-standard -z` 列檔後以 Python regex 掃描 | 356 個非忽略文字檔：舊播放碼、舊操作 seed 用法及舊承諾雜湊 0 findings；包含 tracked 與 untracked。未修改 memory。 |
| Python regex／AST／連結掃描本目錄及 parent README；`git diff --check` | 9 個檔案：個人絕對路徑及 trailing whitespace 0 findings，Python 語法及相對文件連結通過；diff check exit 0。另掃未追蹤檔案，補足 tracked diff 的範圍。 |

工程驗收：本輪私密分派、承諾雜湊與上述拒絕路徑 PASS；既有媒體 QA 結論不變，沒有重跑解碼、生成圖片或重繪影片。未改 src、video、依賴、Episode、SQLite 或治理契約，README 的 pytest/npm 全套本輪未重跑。市場驗收：**NOT_TESTED / HUMAN_TEST_PENDING**；沒有真人資料、正式承諾發布或揭露操作。沒有 commit、push 或 memory 編輯。
