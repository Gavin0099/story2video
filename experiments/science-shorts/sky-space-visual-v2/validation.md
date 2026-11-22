# 天空／太空視覺新版與 skill 驗收｜2026-11-21

Owner 已驗看冰新版並續准另兩題以同方式製作，另要求 skill。本輪沿用公開文案、來源主張、原配音及時間，生成原創插畫層與可核對科學圖解。初版 programmatic-only 美術方式由後續 Owner 要求改為生成場景＋程式機制；沒有把來源圖形下載或把生成結構當科學證據。

Git HEAD：`2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`。工作區已有未提交變更，本輪未 commit／push；以下 source／input／影片 SHA 才是本次具體驗收內容，不宣稱 Git HEAD 已收錄新檔。

## 實際產物

根目錄：`artifacts/science-shorts/sky-space-visual-v2/`，每題在同名子目錄。

| 影片 | 容器長度 | 大小 bytes | SHA-256 |
|---|---:|---:|---|
| `sky/sky-v2-zh.mp4` | 46.100 秒 | 6,056,262 | `9adfd0223447378f8ac0f0bdc2c7256608ab86cfa976e6072e2c487d251af1ed` |
| `sky/sky-v2-preview.mp4` | 12.000 秒 | 1,509,136 | `4b56064dc0831478704a2dab104af7e93581ef1771abd78bed5830dc80f2552b` |
| `space/space-v2-zh.mp4` | 51.800 秒 | 5,045,731 | `fbf7b55750137cbf33e22318fba93ff101ab86be4854a38bdee8f7c134ce8a0f` |
| `space/space-v2-preview.mp4` | 12.000 秒 | 1,104,573 | `6e531005176cdb72b12f76d4beb3a3e6963c7b973d21c2be559e3c6d4aaddae3` |

四片皆 1080×1920、30 FPS、H.264/yuv420p、AAC。天空完整視訊 1381 格（46.033 秒）、太空 1552 格（51.733 秒），容器含編碼後音訊尾端。完整影片為英文旁白＋繁中燒錄；另有兩語 SRT，未另作英文燒錄或可切換字幕版。短版只作美術試看，不作完整科學解釋。

## 版本與新獨立審查

- 新 renderer：`f74cf527f05dd0bb80c31433cb654f6d6f482e88d5c71600bc21b0647fc692b4`。
- 天空 inputs：14 個檔案，SHA `abdebf4f4f9e5ebfd10cd6e4a406ba1b55003b779ced9176eb5145503c85432c`。
- 太空 inputs：13 個檔案，SHA `33210b286522a69ddbc69cd8978872c9ed75fdab69dfaa679d1daac34cb7569d`。
- inputs 包含來源、原稿／讀者結果／gate、原始 audio／timeline、素材、prompt、visual plan，以及冰版共用 helper 的 SHA；沒有更改冰的凍結程式或舊影片。
- 新圖解獨立審查：天空／太空皆 PASS、critical defects 0。回執分別 `sky-visual-review.json/md`、`space-visual-review.json/md`。
- 製作前曾修正天空人物裁切與結尾卡片位置，首次 `e531…` 回執隨程式變更而過期。未用舊回執編碼；原 reviewer 獨立比對四處座標變更及新預覽後重新出具目前 SHA 的審查，revision_history 保留首次回執與重審範圍。
- 最終製作前回執 SHA：天空 `8e32fd856c6c7e56eae10ceefd2dbed0760c7885d37f19e46b66ef6a51d3ba2d`；太空 `2628011c75adce7aacbd9532f70b7a87707cc52d821495cdf89a1dedcde0b16b`。
- 實際 MP4 的獨立科學畫面抽驗：兩題皆 PASS、critical 0。另存 `sky-final-video-review.json/md`、`space-final-video-review.json/md`；四個 MP4 的大小／SHA 與 QA 一致，完整版視閱天空16張、太空19張PNG，並獨立以驗證過的 FFmpeg 重抽天空3＋太空6張機制關鍵格，與既有實際抽格的SHA完全一致。前置review及renderer未改。
- 最終科學抽驗回執 SHA：天空 `3d4229976881659dab8c3d9d2bc2ea504dc00967806b605588fe6ee4e8887f82`；太空 `8366c5c06a4904f002eed9959ee1de424bf2c6ffb1a1e41790cdb1c92f6cedee`。短preview僅 hash／機器QA核對，未另行整段視閱。這些為畫面取樣，沒有宣稱完整影音聽看或專家／真人驗收。

## 工程結果

- `prepare.py` 首次凍結 14／13 個檔案；現存 manifest 會拒絕覆寫。
- 兩題新 review 不存在時，實際 render CLI 均 exit 1 且無影片產出；證據各題 `preflight-rejected.json/.txt`。
- 最終新回執通過且 renderer／inputs SHA 相符後，兩題 render CLI 均 exit 0；天空編碼及短版 68.84 秒，太空 57.73 秒，兩程序平行。這不是總製作時間。
- 兩題 qa CLI 均 exit 0。四片規格、完整音視訊解碼、caption 字寬≤850px／高度≤250px、黑畫面檢查（至少0.15秒、像素閾值0.08）通過。
- 音訊：天空完整 -16.9 LUFS／-1.4dBFS true peak，短版 -17.1／-1.4；太空完整 -17.1／-1.4，短版 -17.0／-1.3。QA 依 -19～-13 LUFS、true peak≤0dBFS 驗證，未見削波。
- 靜音檢查閾值 -45dB、至少2秒。僅天空完整片在43.869875秒開始末段靜音，對應原始 speech_end 43.933秒及約2.1秒非語音停留；按原時序明確允許。其餘三片無此長段靜音。
- 每題從實際MP4抽十鏡中點、首末格與機制時間對：天空1040／1046／1070格，太空380／386、1040／1046、1190／1196格；不是只看編碼前PNG。
- README 指令：uv sync 成功；pytest **61 passed in 4.97s**；video/ 的 npm ci／typecheck 成功、0 vulnerabilities。Node v24.13.0 超出指定 >=22.16.0 <23，npm 有 EBADENGINE，不宣稱指定版本驗收。
- 正式 src/story2video、video/、Episode v1、SQLite 與治理契約未修改；Pillow／FFmpeg 原型未宣稱已整合 Remotion。

實際重跑命令，從 repo root 執行（render 需該題新 review）：

```powershell
& 'artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/sky-space-visual-v2/prepare.py
& 'artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/sky-space-visual-v2/render.py --episode sky --mode preview
& 'artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/sky-space-visual-v2/render.py --episode space --mode preview
# 審查尚未存在時，上述兩題的 --mode render 為預期 exit 1，並保存失敗證據。
# 最終回執通過後，下列均 exit 0。
& 'artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/sky-space-visual-v2/render.py --episode sky --mode render
& 'artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/sky-space-visual-v2/render.py --episode space --mode render
& 'artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/sky-space-visual-v2/render.py --episode sky --mode qa
& 'artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/sky-space-visual-v2/render.py --episode space --mode qa
$env:UV_CACHE_DIR='D:/story2video/artifacts/uv-cache'
& 'artifacts/tooling/bin/uv.exe' sync --locked
& 'artifacts/tooling/bin/uv.exe' run --locked pytest
cd video
npm.cmd ci
npm.cmd run typecheck
```

## Skill 交付與行為驗證

- 可發現的本機版本：`%USERPROFILE%/.codex/skills/science-shorts-visuals/`；repo 副本 `skills/science-shorts-visuals/`。包含 `SKILL.md`、`references/story2video.md`、`agents/openai.yaml`，沒有增加不必要的執行器或另一套製片引擎。
- 使用 skill-creator 的 initializer；quick_validate 在兩份副本均通過。原 repo Python 無 PyYAML，改用 uv 的隔離環境搭配 `pyyaml==6.0.2` 執行驗證，未修改專案 lock 或依賴。
- 首次隔離 forward-test 已完成：另一個有原 batch 經驗的 agent 讀 skill 與原始 sky 稿／來源／時間表，實際產出十鏡交接、素材需求、驗收安排、輸入 binding 與一致性驗證；未讀新 renderer／review，未生圖、編碼或外部變更。結果在 `artifacts/science-shorts/sky-space-visual-v2/skill-forward-test/`。
- 依實際使用問題補充：先核對 visual／rights 與後續 Owner 授權、按所求階段交付、speech_end／end-exclusive／hold、最小交接例子、declared與measured hash、歷史範例與可用入口的區別、QA參數與例外記錄。兩份副本修訂後格式再次通過。
- 修訂後針對性行為確認已完成：`delta-handoff.md`、`post-revision-check.md/json` 依更新skill更正交接：辨別本輪Owner已授權生成插畫、保留科學與rights約束、仍按planning-only交付。六項原疑義已具體澄清，本次規劃任務無剩餘阻塞；hash及cue9時界核對通過。首次測試與舊skill SHA保留，不將首次測試冒充新版end-to-end證明。
- 最終 SKILL.md SHA：`03c8756167365a1bce37b460cd39f1303758c83d8336dc9cb28873fc86643264`；reference SHA `aa572951f5839e618ac5a1a073de31e267d9e3139eaa404e75afdc593e30548a`；UI metadata SHA `4c5d930a8f67f4d8403ef6975185ec92dc412ddc30073f88cce763b38795f966`。三個檔案的本機／repo副本逐檔hash相符，證據 `skill-copy-check.json`。行為驗證限於有repo經驗的AI之規劃交接與修訂確認，不是新題目端到端、陌生使用者或真人試用。

驗證命令：

```powershell
& 'artifacts/tooling/bin/uv.exe' run --no-project --with pyyaml==6.0.2 python -X utf8 %USERPROFILE%/.codex/skills/.system/skill-creator/scripts/quick_validate.py %USERPROFILE%/.codex/skills/science-shorts-visuals
& 'artifacts/tooling/bin/uv.exe' run --no-project --with pyyaml==6.0.2 python -X utf8 %USERPROFILE%/.codex/skills/.system/skill-creator/scripts/quick_validate.py D:/story2video/skills/science-shorts-visuals
```

## 成本與未驗證範圍

三次內建 image_gen（藍天新圖、同圖夕陽編輯、透明太空人），實際素材及 prompts 見 image-prompts.json。工具未回報金額；訂閱、人力、獨立審查與運算成本未定價，不稱零成本。未呼叫計費媒體 API 或新增 TTS。

真人與市場驗收 PENDING，新增真人樣本0。未完成手機實機完整試看、完整影音人工聽看、專家背書、全新題目／陌生使用者 skill 實測、公開市場與完整人工成本、新 clone 跨平台重建。未上傳、公開、建立頻道或寫入 GitHub。
