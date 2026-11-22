# 天空與太空｜科普視覺新版

Owner 驗看冰新版後同意另外兩題採用相同做法，並要求整理成 skill。保留原本經來源、AI 理解度審查的中英文文案與英文配音時間，改善場景、角色、分鏡與解說動畫；沒有重寫文案或把原讀者分數當作新影片分數。

原稿的 vector／programmatic-only 美術限制屬於初版圖解 pilot；Owner 後續明確要求並接受生成插畫分層，授權本次美術方式變更。「沿用原稿」指公開敘述、科學主張與配音時間，不是宣稱逐項沿用初版美術限制。科學機制仍用可核對程式圖解，未下載來源機構的圖片或音訊。

## 產物

根目錄 `artifacts/science-shorts/sky-space-visual-v2/`，每題子目錄為 `sky/`、`space/`：

- `{topic}-v2-zh.mp4`：完整片，英文旁白＋繁中燒錄字幕。天空約 46 秒，太空約 52 秒。
- `{topic}-v2-preview.mp4`：各 12 秒美術試看，不含完整解說。
- `en.srt`、`zh-Hant.srt`：可編輯獨立字幕；本輪不另做英文燒錄或可切換字幕版。
- `actual-mp4/`：實際成片抽格、科學動畫方向成對樣本及影音分析。
- `qa.json`、`provenance.json`：輸出 SHA、規格、解碼、音訊與輸入版本。

[分鏡與機制](visual-plan.md) · [素材與完整 prompts](image-prompts.json) · [驗收紀錄](validation.md)

天空使用內建 image_gen 產生藍天海岸，再以同圖編輯夕陽版保持人物與場景一致；太空使用透明太空人圖層，結合程式星空、空氣示意與頭盔剖面。三次生成共用於本批，工具未回報金額，不把訂閱、人工或運算當零成本。未呼叫計費媒體 API 或新增 TTS。

## 實作與審查

Pillow/numpy 分層動畫＋既有已驗證 FFmpeg，沿用冰新版的凍結字型／字幕 helper 並將其 SHA 納入新 inputs；不修改冰的 renderer、審查或影片。正式 `video/` Remotion 仍為骨架，這次未整合新 Episode、SQLite 或發布流程。

每題獨立 inputs 綁定來源、原文案／讀者結果／gate、音檔／時間、素材、prompt、視覺計畫及共用程式。最終編碼需要新的視覺回執與目前 renderer／inputs SHA 相符；沒有把舊 renderer 的通過挪用過來。圖解回執在 `{topic}-visual-review.json/md`，實際 MP4 回執在 `{topic}-final-video-review.json/md`。

## 重跑

需要本機已準備的 render venv（Pillow/numpy）、已驗證 FFmpeg 及現存素材、原始配音；不宣稱新 clone 缺少資產也能重建。

```powershell
& 'artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/sky-space-visual-v2/render.py --episode sky --mode preview
& 'artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/sky-space-visual-v2/render.py --episode sky --mode render
& 'artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/sky-space-visual-v2/render.py --episode sky --mode qa
```

太空改用 `--episode space`。`prepare.py` 僅凍結首次輸入，已有 manifest 時拒絕覆寫；修改素材或內容應另建版本並適當重審。

## Skill

版本副本在 `skills/science-shorts-visuals/`，可發現的本機副本在 `%USERPROFILE%/.codex/skills/science-shorts-visuals/`。主入口 `SKILL.md`，包含分鏡、素材、機制、獨立審查與實際 MP4 驗收；`references/story2video.md` 提供本專案的路徑與例子，`agents/openai.yaml` 提供呼叫介面。

結構驗證不等於行為通過；本輪另外安排隔離的交接草案 forward-test，結果與範圍見驗收紀錄。沒有把本機 pilot、AI 審查或此 skill 當成真人與市場驗證，沒有上傳、公開或建立頻道。
