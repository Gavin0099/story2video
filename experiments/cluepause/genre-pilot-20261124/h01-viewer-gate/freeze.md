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

## r1 — Owner 授權的聆聽燈局部修訂（無損 MASTER）

2026-11-24（Asia/Taipei），基準 HEAD `695d7db4aaee1790a71ceff6e26afa124519be41`，分支 `codex/cluepause-h01-viewer-gate-20261124`。本節為新增修訂，前文原始凍結紀錄與原片保持原樣。範圍只有兩版對講機燈號；共用 [light-timeline.md](light-timeline.md)／[light-timeline.json](light-timeline.json)，JSON SHA-256 `26908ecda19f1d1586ebc5f3ece37a149da7a20243a8fe154d2c1023e2006cdc`。沒有 ImageGen、TTS 或外部服務呼叫。

以下兩支保留原檔名、原 bytes，明確定義為 **r1 MASTER（無損母檔）**，不供手機觀眾測試播放。本節逐格 zero-diff 結論只適用於母檔。手機測試專用的 r1 DELIVERY 與其雜湊、大小、編碼及驗證另見本頁末節。

| cut | r1 MASTER MP4（repo-relative） | MASTER SHA-256 |
| --- | --- | --- |
| A r1 / STILL | `artifacts/genre-pilot-20261124/h01-v2.1-r1/A/h01-v2.1-r1.mp4` | `b98be2d207c2f42115d09f09eb45e28c87112474e5d85b09feedcb62a6ebb9b8` |
| B r1 / MOTION | `artifacts/genre-pilot-20261124/h01-v2.1-r1/B/h01-v2.1-r1.mp4` | `bf0c1c211a914351a00ad8b36780bedb64b958923c6d93cbb0b95433a9c5739a` |

原 A SHA-256 仍為 `fbe60ff93d13cd8f8fac105b7c0da78445aca2fab3ef76d5891f7ab7d3402412`；原 B 仍為 `2d636b0304c4e3744b32e424a40ee940bf59f4136f96f0f10ea4b25b369f11fd`，修訂前後均核對。兩版 r1 皆為 39 s、1,170 格、1080×1920、30/1 fps、PTS=n/30、yuv420p、TV range、SAR 1:1；使用無損 H.264，profile 為 **High 4:4:4 Predictive**（實際像素格式仍為 yuv420p）。這讓燈區外原生 Y/U/V 樣本可精確保留，但檔案較大，手機硬體解碼／播放器相容性未實測。TV range／SAR 以兩次 stream-copy bitstream metadata remux 恢復；沒有再編碼音訊或改變像素。

兩版音軌直接複製原片，AAC packet SHA-256 仍為 `97f9ad93d95fd719526e6f7a739f9b4b825bbab520a4998d05fb0a38461b1d66`。相鄰字幕名為 `h01-v2.1-r1.en.srt`、`h01-v2.1-r1.zh-Hant.srt`，兩版各一組；英文 SHA-256 仍為 `c36c869765801e49088a75346d2bdc91b2b4b32d0b51e1d65ab3a15c5833ff2a`，繁中仍為 `ab0a17dc4884f6ab2b1533b855d35059d09e6a85626626c4fac7e555ca792707`。字幕 bytes、聲音、開閂時序與完整拒絕句五格都保留。

從 repo 根目錄重跑；render 拒絕覆寫既有 r1 目錄，須先保留現有證據或在新的隔離 checkout 執行，不刪原片：

```powershell
python -B experiments/cluepause/genre-pilot-20261124/h01-viewer-gate/revise_light.py render
python -B experiments/cluepause/genre-pilot-20261124/h01-viewer-gate/revise_light.py verify
python -B experiments/cluepause/genre-pilot-20261124/h01-viewer-gate/temporal_qa.py --r1
git diff --check
```

| 本輪檢查 | 結果／範圍 |
| --- | --- |
| `revise_light.py render` | 最終版 exit 0；既有燈罩素材、`hybrid_motion.stage` glow 與 smoothstep fade，逐鏡追蹤原 zoom／B flinch；輸出至全新 r1 目錄。 |
| `revise_light.py verify`（最終 metadata 後） | exit 0；兩版各 1,170 格全片原生 Y/U/V 樣本比對。各 658 個燈可見格均常亮，預期合成 mismatch 0；燈區外 changed samples **0**。其餘各 512 格整格 byte-identical；17–30 秒每格同樣涵蓋。 |
| `temporal_qa.py --r1` | exit 0；兩版各 1,170 格、39 個逐秒序列頁、全部 PTS、每語言 20 字幕 cues、15 voice events 與 5 個指定咳嗽／尾詞事件對位 PASS。最終片 hash 前後不變。 |
| `git diff --check`、個人路徑 grep、AST／空白檢查 | exit 0；8 個 changed/new 原始檔含 untracked：個人路徑 0、行尾空白 0、Python AST／JSON PASS；artifacts 全檔路徑掃描結果另見下段。 |
| README 的 pytest/npm 全套 | 未重跑；未改 src、video、依賴、Episode、SQLite 或治理。只驗證本輪媒體與 QA 腳本，不把完整引擎回歸列為 PASS。 |

可重建證據在新 r1 根目錄：`light-measurements.json`，各 cut 的 `qa/frame-checks.csv`、`qa/light-crops/`、`qa/light-sequence.png`，以及 `temporal-qa/` 的全片影格／序列頁／音訊與字幕量測。純色初版與中止的檢查保留說明於 [cost-ledger.md](cost-ledger.md)，不計為最終測試成片。

最終 Python byte grep 掃描本輪寫入的 **4,258 個 artifacts 檔案**（包含 r1、未採用 draft 與燈位 survey；二進位採分塊並跨界保留尾段，另涵蓋 NUL 分隔文字），個人絕對路徑 **0 findings**。8 個 changed/new 原始檔另掃包含 untracked。兩份量測 JSON 的最終 MP4 雜湊相符；每版密集 `[f510,f900)` 共 390 格，其中 315 格燈可見，逐格外區差分全為 0。

工程驗收：燈號與非燈區差分 PASS；整片仍為 continuity FAIL / action PARTIAL，其他已知問題沒有修復或降級。市場驗收：**NOT_TESTED / HUMAN_TEST_PENDING**；[viewer-protocol.md](viewer-protocol.md) 已指定 r1。未驗證：真人 1× 同步視聽、手機播放器／無損 profile 相容性、字幕可讀性、首次理解與市場表現；31–39 秒鏡外的燈不可視驗。沒有 commit、push、上傳、YouTube、memory 編輯或唯讀來源工作區寫入。

## r1 DELIVERY — 手機測試交付凍結

2026-11-24（Asia/Taipei）；基準 HEAD `695d7db4aaee1790a71ceff6e26afa124519be41`，分支 `codex/cluepause-h01-viewer-gate-20261124`，本次修改未提交。Owner 授權保留無損 r1 MASTER，另外製作與原始交付設定相同的手機測試檔。原 MASTER 沒有重新命名或覆寫；下表以角色明確區分。**viewer test 只播放 DELIVERY**，不要播放約 233–250 MB 的 MASTER。

以下路徑共用前綴 `artifacts/genre-pilot-20261124/h01-v2.1-r1/`；大小為實際 bytes，MB 使用十進位。

| cut / 角色 | 前綴下檔案 | bytes / MB | SHA-256 |
| --- | --- | --- | --- |
| A MASTER | `A/h01-v2.1-r1.mp4` | 232,870,061 / 232.870061 | `b98be2d207c2f42115d09f09eb45e28c87112474e5d85b09feedcb62a6ebb9b8` |
| B MASTER | `B/h01-v2.1-r1.mp4` | 250,181,314 / 250.181314 | `bf0c1c211a914351a00ad8b36780bedb64b958923c6d93cbb0b95433a9c5739a` |
| A DELIVERY / STILL | `A/h01-v2.1-r1-delivery.mp4` | 16,489,753 / 16.489753 | `256918124d0c2eb9eb1f1d2c8adc60ff70b5e6807a5e6f502c4c47378caaa6e7` |
| B DELIVERY / MOTION | `B/h01-v2.1-r1-delivery.mp4` | 16,946,384 / 16.946384 | `5fe085536b3d5d8ec61914a296e9e289db0b4ead346c0c5268eddbe5571543a0` |

編碼依據：原始 `h01-v2.1/{A,B}/commands.jsonl` 的最後一組命令是 concat 加 audio stream copy；真正的 encoder options 位於各版 `cuts/commands.jsonl`。全部編碼紀錄一致為 `-c:v libx264 -preset medium -crf 18 -threads 1 -pix_fmt yuv420p -r 30 -map_metadata -1 -movflags +faststart`。使用原有鎖定並核對 SHA-256 的 FFmpeg／ffprobe。同原流程將 **26 個鏡頭分別編碼再串接**，不以全片單一 encoder 改變短鏡頭 GOP。最終 mux 使用 `-c copy`、`-movflags +faststart`，以及原紀錄相同的 `h264_metadata=video_full_range_flag=0:colour_primaries=2:transfer_characteristics=2:matrix_coefficients=2:chroma_sample_loc_type=0`。

兩版 DELIVERY 的 ffprobe 均為 **H.264 High、Level 4.0（數值 40）、yuv420p、TV range、SAR 1:1、1080×1920、30/1 fps、39.000000 s、1,170 格**，與原始交付相同。High 4:4:4 Predictive 只屬於無損 MASTER。逐格 PTS=n/30；26 個 keyframe 的實際 frame index 全部與各自原片相同。從原片與 DELIVERY 各段 SEI 讀出的完整 x264 options 集合完全相同，包括 `keyint=250 keyint_min=25 scenecut=40 open_gop=0 bframes=3 ref=3 rc_lookahead=40 rc=crf crf=18.0`；沒有另設固定 bitrate。直接解析 MP4 box 確認兩版 `moov` 都在 `mdat` 前。

| cut | 原始交付 bytes | DELIVERY bytes | 大小差 | 原 video bit/s | DELIVERY video bit/s |
| --- | --- | --- | --- | --- | --- |
| A | 16,470,212 | 16,489,753 | +0.1186% | 3,177,164 | 3,181,173 |
| B | 16,973,434 | 16,946,384 | −0.1594% | 3,280,389 | 3,274,841 |

音訊從各自凍結原片直接 `-c copy`，不是重編 AAC：AAC-LC、48 kHz、stereo、192,046 bit/s，packet SHA-256 仍為 `97f9ad93d95fd719526e6f7a739f9b4b825bbab520a4998d05fb0a38461b1d66`。每版新增同名相鄰外掛字幕 `h01-v2.1-r1-delivery.en.srt`（1,302 bytes）及 `h01-v2.1-r1-delivery.zh-Hant.srt`（1,408 bytes），英／繁中 SHA-256 分別仍為 `c36c869765801e49088a75346d2bdc91b2b4b32d0b51e1d65ab3a15c5833ff2a`、`ab0a17dc4884f6ab2b1533b855d35059d09e6a85626626c4fac7e555ca792707`。原 MASTER、原交付及腳本雜湊前後不變。

燈號與 outside 量測方法、容差及初次失敗紀錄見 [temporal-qa.md](temporal-qa.md) 的 DELIVERY 節。結果如下；min／mean 是各版全部 1,170 格的最小值／算術平均，PSNR 單位為 dB。

| DELIVERY | 可見燈 / 鏡外格 | 最終燈號失敗 | outside SSIM min / mean | outside PSNR min / mean |
| --- | --- | --- | --- | --- |
| A | 658 / 512 | 0 | 0.991071 / 0.994804 | 47.819 / 51.198 |
| B | 658 / 512 | 0 | 0.991019 / 0.994744 | 47.827 / 51.148 |

從 repo 根目錄重跑下列命令；`encode` 拒絕覆寫既有交付／鏡頭目錄，需使用保留原媒體的新隔離工作區才能重製。`verify` 只解碼及寫入 QA 數據，不修改影片，也不重建光暈 PNG。

```powershell
python -B experiments/cluepause/genre-pilot-20261124/h01-viewer-gate/delivery_encode.py encode
python -B experiments/cluepause/genre-pilot-20261124/h01-viewer-gate/delivery_encode.py verify
git diff --check
```

工程驗收：`encode` exit 0；最終腳本 `verify` exit 0，兩版 profile／像素格式／SEI options／實際 keyframes／PTS／faststart／音軌 hash／字幕 hash／大小及逐格燈號、outside 量測通過。測量資料在 `artifacts/genre-pilot-20261124/h01-v2.1-r1/delivery-qa/measurements.json`，每 cut 有原片與交付 ffprobe、`light-frames.csv`、`outside-frames.csv`、`excluded-regions.json`、各矩形逐格 SSIM／PSNR logs 及相對路徑命令紀錄；編碼命令在各 cut 的 `delivery-commands.jsonl`。腳本與本節保留在 experiments，沒有用 ignored artifacts 作為唯一文字紀錄。

最終靜態檢查：本輪新增／修改的四個來源檔 Python AST（適用者）、行尾空白、個人絕對路徑與文件相對連結 PASS；新增 delivery artifacts 含 52 個分鏡編碼共 365 個檔案，逐 byte 分塊／跨塊掃描個人路徑 0 findings。兩版 `light-frames.csv`／`outside-frames.csv` 各 1,170 列且 frame index 完整連續，量測 JSON 的 hash／大小與本頁一致；`git diff --check` exit 0。既有 Git 全域 ignore 讀取權限警告仍存在，不影響本次 repo 內檔案驗證；沒有修改全域設定。

未改 `src/story2video/`、`video/`、Episode、SQLite、依賴或治理；README 的 `uv sync --locked`、`uv run --locked pytest`、`npm ci`／`npm run typecheck` 本輪未重跑，完整引擎回歸未驗證。未測實體手機解碼、手機字幕呈現、真人 1× 同步視聽或首次理解；High／Level 4.0 與原片一致不等於已測每款手機。整片 continuity FAIL / action PARTIAL 的其餘結論維持。市場驗收：**NOT_TESTED / HUMAN_TEST_PENDING**。沒有 commit、push、上傳、memory 編輯、AI 圖像生成或個人路徑寫入。
