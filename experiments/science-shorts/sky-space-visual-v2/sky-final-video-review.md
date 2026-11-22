# 天空 v2 實際成片科學抽驗

**PASS — 抽樣科學畫面通過，critical defects：0。** 與本題前置 visual-review 的判斷一致，未見編碼新增科學問題。

審查者 `/root/fact_visual_audit`；模型 `inherited native agent (API未提供精確版本)`。Git `2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`。此為獨立 AI 抽驗，沒有聲稱完整連續影音觀看、真人或領域專家驗收。

| 實際檔案 | 實測 SHA256 | 影片／容器秒數 |
| --- | --- | --- |
| sky-v2-zh.mp4 | `9adfd0223447378f8ac0f0bdc2c7256608ab86cfa976e6072e2c487d251af1ed` | 46.033333 / 46.1 |
| sky-v2-preview.mp4 | `4b56064dc0831478704a2dab104af7e93581ef1771abd78bed5830dc80f2552b` | 12 / 12 |

兩檔的 SHA 與大小都與 qa.json 相符。Renderer `f74cf527f05dd0bb80c31433cb654f6d6f482e88d5c71600bc21b0647fc692b4`；provenance 綁定前置回執 `8e32fd856c6c7e56eae10ceefd2dbed0760c7885d37f19e46b66ef6a51d3ba2d`，renderer／inputs／原配音的實測雜湊也符合。既有機器 QA：PASS；1080×1920、30fps、H.264/AAC。完整片43.869875秒開始的長靜音屬既有結尾 hold。 這些完整 decode／音訊分析為既有 QA 證據，本審查沒有重跑全片工程分析。

- **same-medium-observer — PASS**：Actual shot08 and ten-cue contact: short and long paths remain in the same atmospheric shell to the same observer, matching new visual plan.

- **relative-scattering — PASS**：Actual shot05: blue/red comparison each has five incident traces, blue four redirected versus red one; explicit schematic/nonquantitative qualifier remains. No blue-to-red conversion.

- **scattered-light-to-eye — PASS**：Actual shot06: blue paths enter eye symbol from sky, distinct from direct solar path; subtitle remains consistent with original claim.

- **outward-pulses — PASS**：Actual frames1040→1046: all three blue markers move up/outward on the blue arrows (approximately y −25,−29.5,−34px as predicted by frozen formula). Frame1070 is a later repeated pulse phase, not a reversed path. Red direct line remains forward and red.

- **cue-alignment — PASS**：Contact spans all ten cue midpoints; sampled scientific labels, note and Traditional Chinese subtitles remain aligned. No encoding-introduced critical change observed.

實際 MP4 聯絡表涵蓋十個 cue 中點，另開原尺寸：frame-1040.png、frame-1046.png、frame-1070.png、shot-05.png、shot-06.png、shot-08.png。3 張關鍵時間格由審查者使用驗證過 SHA／大小的 FFmpeg 絕對路徑重新從完整 MP4 解碼，PNG SHA 與所提供抽格逐一完全相同。檔案留在 `actual-mp4/independent-audit/`；同名 JSON 留每張抽樣 PNG 的 SHA、來源 MP4 SHA、零起算名義影格與時間、查看方式，以及完整命令模式。

範圍限制：12秒短預覽只核對檔案綁定及 QA，沒有另抽短片畫面；這不是完整解說或留存率證據。字幕與圖解是抽樣核對，不是逐幀保證。示意尺度與波速不代表量測物理。未評真人理解、手機閱讀、美術吸引力或市場接受度；未重做來源研究、文案評分。原 renderer、前置 review、assets、ice、原 gate/audit 均未改。

本次採用 [science-shorts-visuals](%USERPROFILE%/.codex/skills/science-shorts-visuals/SKILL.md) 的 encoded-video audit 流程；沒有發布或傳送外部訊息。

