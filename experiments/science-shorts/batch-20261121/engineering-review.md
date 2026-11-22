# 科普本機 pilot 工程驗收

驗收者 `/root/reader_a` 在兩階段文案評分已凍結後另接工程任務；本記錄不修改先前評分。工程範圍只新增獨立 `../verify.py` 與本記錄，輸出證據放 ignored `artifacts/science-shorts/batch-20261121/`；未更改 renderer、正式 Episode v1、SQLite、共享 memory、發布順序或治理框架。

Git HEAD：`2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`。新增工作樹檔案尚未提交；實際驗收程式及輸入 SHA-256 由 `artifacts/science-shorts/batch-20261121/qa.json` 記錄。

## 工程驗收：前置 gate 與十二支 MP4 機器檢查通過

獨立重算兩位讀者六項分數，核對每項上限、總分、85 分門檻、critical defects 與逐集 coverage；結果 ice 88/89、sky 87/86、space 89/87。核對原稿 parent hash、final script、renderer、來源卡、gate policy、review files 及科學圖解收據 hash。每項核心主張至少兩個成功讀取且不同 publisher 的來源；NASA 不同頁面統一只算一個機構。此程式只核對已存來源查證收據，不重新連網查證。

原稿至 final 的英中台詞、scene、claim_ids、visual、visual_constraints 均等值；純 timing 的 pause 差異另列記錄。sky 最後一句的 pause 由 0.8 增至 2.1 秒，沒有更改台詞或以加速語音壓縮內容。最終驗收應以更新後的腳本 SHA `d0b7de7d7ac4c1aa9986840999721c83735fea615703b0ba3479648f00a73cf8` 為準。

驗收呼叫實際 `render.main()`，只替換 `sys.argv` 與攔截副作用；每個負面案例複製獨立 temp batch，重綁被改動 review 的外層 hash，確保真正走到指定拒絕條件。十例均通過：stale script、gate 分數改寫、reader 分項改寫、空 episode gate、空 review_files、audit renderer hash 不符、critical visual defect、ffmpeg 大小錯誤、ffmpeg 同大小但 SHA 錯誤、ffprobe 同大小但 SHA 錯誤。每例 TTS、painter、Popen、subprocess.run、PATH lookup 均為零，測試輸出根目錄不存在。有效輸入正控制則通過實際 gate、兩個 binary 與模型檢查，到達輸出建立前的 painter 邊界，證明負面測試不是無條件擋住 main。

本次有一項驗收程式開發失敗已修正：首次採系統 C 槽 temp，D 槽固定工具無法跨磁碟建立 hard link（WinError 17）。temp 改用 ignored artifacts 的同磁碟臨時目錄後，完整重跑通過；沒有修改工具原檔。

| 命令 | 實際結果 |
|---|---|
| `artifacts/render-venv/Scripts/python.exe -X utf8 experiments/science-shorts/verify.py --mode preflight` | PASS；10 負面案例 + 1 正控制；`qa.json` media 為 NOT_RUN |
| `$env:UV_CACHE_DIR='D:/story2video/artifacts/uv-cache'; $env:UV_OFFLINE='true'; artifacts/tooling/bin/uv.exe run --locked pytest` | 61 passed in 6.64s；exit 0；離線執行，無下載 |
| `artifacts/render-venv/Scripts/python.exe -X utf8 experiments/science-shorts/verify.py --mode frames-only --episode ice` | 從 ice-zh.mp4 實際解碼 9 個 cue 中間格、首格、末格，輸出聯絡表及 frame hash；exit 0 |
| `artifacts/render-venv/Scripts/python.exe -X utf8 experiments/science-shorts/verify.py --mode media --episode ice` | ice 四種 profile 全部 PASS；其餘集數當次未驗；exit 0 |
| `artifacts/render-venv/Scripts/python.exe -X utf8 experiments/science-shorts/verify.py --mode media --episode sky` | sky 四種 profile 全部 PASS；其餘集數當次未驗；exit 0 |
| `artifacts/render-venv/Scripts/python.exe -X utf8 experiments/science-shorts/verify.py --mode frames-only --episode space` | space-zh.mp4 的 10 個 cue 中間格、首末格實際解碼並交付圖解審查；exit 0 |
| `artifacts/render-venv/Scripts/python.exe -X utf8 experiments/science-shorts/verify.py --mode all` | 最終凍結程式及輸入上重新執行 10 負面案例、1 正控制、3 episodes/12 MP4；全部 PASS；54 個媒體命令 exit 0 |

`video/`、`src/story2video/`、治理契約及框架版本未更改，因此本子任務未重跑 npm ci/typecheck 或治理框架驗收。未呼叫下載、上傳、付費或外部 API。

## 工具綁定

採既有 `experiments/episode-02-73h/render-manifest.json` 的 pinned size + SHA-256，驗收程式每次子程序呼叫前重驗，使用絕對 canonical binary 路徑與 argv 清單、`shell=False` 預設及 allowlisted SystemRoot/WINDIR/TEMP/TMP 環境，不使用 PATH fallback。

| Binary | 大小 | SHA-256 |
|---|---:|---|
| `artifacts/render-tools/verified/ffmpeg-9.1-essentials_build/bin/ffmpeg.exe` | 110590976 | `ed8f66cb877087a96f5bbb40a2944f0e764f2ad8870d5cb647360d912e62bc07` |
| `artifacts/render-tools/verified/ffmpeg-9.1-essentials_build/bin/ffprobe.exe` | 110374912 | `df0199f606faa88e9ad192732a7c3987acfb647663534c297772e17730611a08` |

使用 `external-executable-trust-audit` skill。就本次實測 FFmpeg/ffprobe 路徑，未發現 ambient executable trust root；這不是整個 Windows、DLL 搜尋、Python interpreter 或套件依賴的信任認證。實際 renderer 在 binary 綁定前會讀公開 gate 並 import 既有 helper；未宣稱其滿足所有高權限治理 launcher 的更嚴格 import 前排序。

## 成片 QA 設計與實際影格

`verify.py --mode all` 在三集完成後可一次驗收；`--mode media --episode ice` 僅驗指定集，明列其餘未驗。檢查全部四種 MP4 profile 的 1080×1920、30 fps、H.264/yuv420p、AAC/48 kHz、45–60 秒、timeline frame count、provenance hashes；對每支完整解碼並測量 encoded audio 的 integrated loudness 與 true peak。QA 門檻為 -18 至 -14 LUFS、true peak 不超過 -0.5 dBTP。

逐 cue 比對 frozen 英中台詞、timeline、SRT 文字/時界/無重疊、ASS 文字/時界，再由 selectable MP4 的兩條 mov_text 內嵌字幕回讀核對內容與毫秒時間。這證明文字軌一致，沒有假稱 OCR 已驗證燒錄字幕像素或真人聽覺同步。

影格以 pinned FFmpeg 直接解碼實際 MP4 的指定零起算 frame，Pillow 只拼合與縮小這些解碼 PNG，未呼叫 renderer 的繪圖函式製造 QA 預覽。每個 profile 提供 cue 中間格、0 秒首格及末格；sky 額外提供 sunset 同 cue 相隔 6 frames（0.2 秒）的 pulse 影格，本凍結批次取 frame1050/1056（35.0/35.2秒），避開動畫 phase 重置。聯絡表、單張圖、來源 MP4 SHA、frame/time/PNG SHA 及抽格命令保存於 `artifacts/science-shorts/batch-20261121/qa-evidence/`。

已提供的冰篇實際抽格：`qa-evidence/ice/ice-zh/actual-mp4-contact.png`、`cue-01.png` 至 `cue-09.png`、`first-frame.png`、`last-frame.png`、`frames.json`。最初來源 MP4 SHA 為 `9fc5e599b90a086a5fbc32d7647067a4442119bb0ed119c33a7c262afc15d94f`；若重製 bytes 改變，應以最終 QA 新收據為準。

完整成片 QA 已執行，`qa.json` 的 status、preflight_status、media_status 均為 PASS，包含三集各四種 profile（master、en、zh、selectable）。十二支皆通過 1080×1920/30fps/H.264/yuv420p/AAC/48kHz、完整影音 decode、長度與 frame count、provenance、SRT/ASS 內容與時間一致性。三支 selectable MP4 的 EN/ZH 內嵌字幕均實際回讀並通過。每支 MP4 均另量測 encoded audio，未借用旁白 WAV 的數值。

| 集數 | Video frames / 秒 | Container 秒 | 四種 profile 的 LUFS | True peak dBTP |
|---|---|---:|---:|---:|
| ice | 1441 / 48.033333 | 48.1 | -16.96 | -1.42 |
| sky | 1381 / 46.033333 | 46.1 | -16.99 | -1.30 |
| space | 1552 / 51.733333 | 51.8 | -17.13 | -1.41 |

最終驗收程式 SHA-256：`72c345548adfe7523a94793d6dc6842a2cb69d145ce2e0f38ea6d451947080f0`。最終 `artifacts/science-shorts/batch-20261121/qa.json` SHA-256：`54562c610b61fc6cf24b9554bc1fad7c9da0913e19cbb3476a567e482f156e3d`。驗收後已再次讀取程式 bytes 確認與 qa.verify_sha256 一致；之後只更新本工程記錄，未改驗收程式或 renderer。

54 個媒體命令的完整 argv、exit code、stdout/stderr 另存 `qa-evidence/commands/001.json` 至 `054.json`，每個 log 的 hash 在 qa.json。十二份實際 MP4 聯絡表位於 `qa-evidence/{ice,sky,space}/{MP4 stem}/actual-mp4-contact.png`，同目錄有完整 1080×1920 cue 中間格、首末格、sky pulse pair 與 `frames.json`。原始 renderer 自製的 storyboard-contact.png 不列為此處的實際 MP4 抽格證據。

本記錄僅核實機器檢查與實際影格來源。最終科學圖解審查由 `/root/fact_visual_audit` 另外記錄，不由本程式自行推導；抽格也不能證明連續播放、手機裁切或真人閱讀/聽感已通過。

## 市場與真人驗收

PENDING。AI 分數、來源審查、機器規格、抽格及工程測試均不代表五位首次真人的機制重述、手機可讀性、實際聽感或 D7/D28 市場證據。未授權也未執行上傳、公開、建立新頻道；本工程任務不改變這些界線。
