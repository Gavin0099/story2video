# Issue #32 製片入口與依賴盤點

範圍為 2026-11-26 的 Git 資料、這台製片機及既有試作。表中的「載入」指 Codex 新程序能發現／讀取指令；「使用」另看對應作品紀錄。公開的市場觀察綁影片版本，無法歸因給某一工具。

| 能力 | 受版控的來源 | 開工前已安裝／能發現 | 使用或成片證據 | 建議接法 |
|---|---|---|---|---|
| 題材與故事生成 | [story-generation 固定版本](https://github.com/Gavin0099/story2video/blob/b4320b0810d912d095e9d4b9ecfc5b44e11465c8/.agents/skills/story-generation/SKILL.md) | 乾淨 pilot clone 可發現 repo Skill；原預設分支的乾淨 clone 缺這個入口。 | 有舊分支方法與稿；單看檔案無法證明它產生每支母片。 | 沿用由謎底逆推必要線索及首猜的方法，再做原創與用途檢查。 |
| 批次、Viewer Gate 與發布 | [批次 Skill](https://github.com/Gavin0099/story2video/pull/9) · [權利](https://github.com/Gavin0099/story2video/pull/17) · [Viewer Gate](https://github.com/Gavin0099/story2video/blob/82d55304cc00b385133341a8b9cb879f6791be52/skills/shorts-viewer-gate/SKILL.md) | 製片機的 user 安裝可發現；PR #9 工作樹另列同名 repo 版，換行正規化後內容仍有差別。 | 已有線索時間、開場抽查與既有發布操作紀錄；本次研究僅讀取頻道。 | 使用目前 checkout 明確路徑的批次入口，原有正式門檻與人工發布權限照舊。 |
| 分鏡與道具動作 | [靜態分鏡 Pipeline](https://github.com/Gavin0099/story2video/tree/3170e0bab567007c6c5fc1fccf97e10fb02c3af1/experiments/cluepause/static-ten-20261124/pipeline) · [動作原型](https://github.com/Gavin0099/story2video/pull/25) | 有可執行的工作樹檔案。既有 Codex 清單沒有名為 video-storyboard 的本機 Skill。 | PR #28 的十部靜態分鏡及 PR #26 的門閂／燈號時序量測。 | 讀原 shots、references、素材收據與工具鎖；外部同名 Skill 各自評估。 |
| 科普圖解 | [science-shorts-visuals](https://github.com/Gavin0099/story2video/blob/82d55304cc00b385133341a8b9cb879f6791be52/skills/science-shorts-visuals/SKILL.md) | 新 Codex 程序可發現 user 安裝；主工作樹與 user 主檔相同。 | 冰、天空、太空的分層影像、音軌與圖解驗收有記錄。 | 重用已有合成器；科學結論、畫面及資料來源綁定同版。 |
| ImageGen | 系統 imagegen 指令及專案的 [H01 素材收據](https://github.com/Gavin0099/story2video/blob/f21677f7a78d8e68fbb0c23fd12952640efda1fb/experiments/cluepause/genre-pilot-20261124/h01-v2.1-imagegen.json) | Codex 可發現系統指令。 | H01 有已生成圖版與提示紀錄。 | 可用於有權使用的情境與道具底圖，科學光路與定量面積交給可驗的原生圖層。 |
| Kokoro ONNX | [基準實作與 manifest](https://github.com/Gavin0099/story2video/tree/82d55304cc00b385133341a8b9cb879f6791be52/experiments/episode-02-73h) | 本機 render 環境可載入 kokoro-onnx 0.6.1；模型、voices 雜湊與 manifest 相符。 | 73H 實際旁白與時間軸。 | 用實際語句樣本長度排聲音與英繁字幕。 |
| FFmpeg、ffprobe | [工具鎖](https://github.com/Gavin0099/story2video/blob/3170e0bab567007c6c5fc1fccf97e10fb02c3af1/experiments/cluepause/static-ten-20261124/pipeline/tools.lock.json) | 兩個執行檔經 bytes 與 SHA-256 比對，ffprobe 能開啟既有母片。 | 73H 為 H.264/AAC、1080×1920、30 fps、45.6 秒。 | 現有影音輸出與 QA 共用這一組工具。 |
| Remotion | [M0 入口](../../video/src/Root.tsx) | 依賴可安裝及型別檢查，現有 Root 回傳 null。 | 未見以上母片使用該 Root 的證據。 | 留給具體動畫瓶頸；S12 仍為選擇性工作。 |

### 可重現的範圍

基底為預設分支 `codex/story2video-m0` 的 `44fccc8d6184d15561395c657d121e9aa3128a31`，盤點時它沒有上述 repo Skills。檢查了目前工作樹、PR #28、#31、#9、#7 的五個 cwd。新的 Codex app-server 0.163.0 使用 `initialize`、`initialized`、`skills/list`，按 cwd 指定 `forceReload:true`。五處均為零載入錯誤，分別取得 26、26、26、27、27 項。另從遠端各做一次未改動的 shallow clone；預設分支為 26 項，pilot 分支為 27 項，多出 repo scope 且 enabled 的 story-generation。

這些結果包含製片機的 user/system 安裝。新機仍需取得對應資產與執行環境；完整重建與某個模型實際自動選擇哪一份指令，不能從清單筆數判斷。Claude CLI 在此機器可找到，盤點時使用者層沒有對應的 Skills 目錄。僅憑名字不能判定 Claude 已消費此流程。

### 既有成果如何處理

- [#16](https://github.com/Gavin0099/story2video/pull/16) 的治理與 [#17](https://github.com/Gavin0099/story2video/pull/17) 的故事權利可獨立追溯；[#18](https://github.com/Gavin0099/story2video/issues/18) 為類型擴展議題。[#19](https://github.com/Gavin0099/story2video/pull/19) 為歷史市場基準，[#20](https://github.com/Gavin0099/story2video/pull/20) 是目前預設分支基底。
- [#21](https://github.com/Gavin0099/story2video/pull/21) 收錄線索間隔及權利盤點。[#22](https://github.com/Gavin0099/story2video/pull/22)、[#23](https://github.com/Gavin0099/story2video/pull/23)、[#24](https://github.com/Gavin0099/story2video/pull/24) 是不同時點的分型稿／試片，應依版本查核。
- [#25](https://github.com/Gavin0099/story2video/pull/25)、[#26](https://github.com/Gavin0099/story2video/pull/26)、[#28](https://github.com/Gavin0099/story2video/pull/28) 有動作、時序 QA 與靜態製片管線。[#27](https://github.com/Gavin0099/story2video/issues/27) 為選擇性的進階動作研究。
- [#29](https://github.com/Gavin0099/story2video/pull/29)、[#30](https://github.com/Gavin0099/story2video/pull/30)、[#31](https://github.com/Gavin0099/story2video/pull/31) 的凍結研究與市場欄位可查；評審研究 PAUSED。本批沿用適用方法，沒有合併這些疊接 PR。
