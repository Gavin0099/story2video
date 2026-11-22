# 太空 v2 實際成片科學抽驗

**PASS — 抽樣科學畫面通過，critical defects：0。** 與本題前置 visual-review 的判斷一致，未見編碼新增科學問題。

審查者 `/root/fact_visual_audit`；模型 `inherited native agent (API未提供精確版本)`。Git `2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`。此為獨立 AI 抽驗，沒有聲稱完整連續影音觀看、真人或領域專家驗收。

| 實際檔案 | 實測 SHA256 | 影片／容器秒數 |
| --- | --- | --- |
| space-v2-zh.mp4 | `fbf7b55750137cbf33e22318fba93ff101ab86be4854a38bdee8f7c134ce8a0f` | 51.733333 / 51.8 |
| space-v2-preview.mp4 | `6e531005176cdb72b12f76d4beb3a3e6963c7b973d21c2be559e3c6d4aaddae3` | 12 / 12 |

兩檔的 SHA 與大小都與 qa.json 相符。Renderer `f74cf527f05dd0bb80c31433cb654f6d6f482e88d5c71600bc21b0647fc692b4`；provenance 綁定前置回執 `2628011c75adce7aacbd9532f70b7a87707cc52d821495cdf89a1dedcde0b16b`，renderer／inputs／原配音的實測雜湊也符合。既有機器 QA：PASS；1080×1920、30fps、H.264/AAC。QA 未報告超過兩秒的靜音。 這些完整 decode／音訊分析為既有 QA 證據，本審查沒有重跑全片工程分析。

- **independent-air-vacuum — PASS**：Actual shot04 and contact: AIR panel has30 orange particle symbols, ideal-vacuum panel none. The air mechanism is independent of the two astronauts' vacuum gap; distant star dots remain distinct and labeled.

- **local-oscillation — PASS**：Actual frames380/386: same30 symbols remain near own positions; orange emphasis guide advances right independently. Frozen formula limits each displacement to±8px, no mass flow across the gap. Regular rows/guide are schematic, not literal molecular trajectories or a calibrated pressure front.

- **electromagnetic-gap — PASS**：Actual frames1040/1046: cyan wave and forward signal connect radios across the vacuum, with no orange medium; marker/phase advance right.

- **receiver-sound — PASS**：Actual frames1190/1196 plus shot09: labeled receiver→speaker→20 local air-particle symbols→ear, confined to closed internal-helmet cutaway. Local air shifts near its own positions, no air in exterior vacuum. Ear cue remains audible-sound explanation.

- **cue-alignment — PASS**：Contact spans all ten cue midpoints; mechanism labels, schematic note and Traditional Chinese subtitles remain aligned. No new critical problem observed after encoding.

實際 MP4 聯絡表涵蓋十個 cue 中點，另開原尺寸：frame-0380.png、frame-0386.png、frame-1040.png、frame-1046.png、frame-1190.png、frame-1196.png、shot-04.png、shot-09.png。6 張關鍵時間格由審查者使用驗證過 SHA／大小的 FFmpeg 絕對路徑重新從完整 MP4 解碼，PNG SHA 與所提供抽格逐一完全相同。檔案留在 `actual-mp4/independent-audit/`；同名 JSON 留每張抽樣 PNG 的 SHA、來源 MP4 SHA、零起算名義影格與時間、查看方式，以及完整命令模式。

範圍限制：12秒短預覽只核對檔案綁定及 QA，沒有另抽短片畫面；這不是完整解說或留存率證據。字幕與圖解是抽樣核對，不是逐幀保證。示意尺度與波速不代表量測物理。未評真人理解、手機閱讀、美術吸引力或市場接受度；未重做來源研究、文案評分。原 renderer、前置 review、assets、ice、原 gate/audit 均未改。

本次採用 [science-shorts-visuals](%USERPROFILE%/.codex/skills/science-shorts-visuals/SKILL.md) 的 encoded-video audit 流程；沒有發布或傳送外部訊息。

