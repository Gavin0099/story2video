# 冰為什麼浮在水上？｜畫面新版試片

Owner 在三支科普 pilot 後回饋「說明清楚、圖片不生動」，並同意先做一個主題。這次選冰，保留原本經來源核對及兩位 AI 讀者給 88／89 分的中英文文案、英文配音與時間，新增場景插畫、獨立透明冰塊層、入水與浮動、微觀放大、粒子排列與體積比較。這不是新的文案盲測分數。

素材使用本機 imagegen skill 的內建 image_gen 模式，共兩次生成；完整 prompt 見 [image-prompts.json](image-prompts.json)。素材已複製至專案 `artifacts/science-shorts/ice-visual-v2/assets/`，不依賴使用者的 Codex 快取。金額沒有由工具回報，不能把訂閱成本或製作人力當成零成本；未呼叫計費媒體 API，沒有新增 TTS 呼叫。

本次以隔離的 Pillow 分層合成器與既有 FFmpeg 完成可觀看樣片，未改動正式 Remotion 骨架、Episode 合約、SQLite 或發布流程。分鏡與素材可用作後續 Remotion 實作的參考，但不宣稱已完成正式引擎整合。原版 renderer、gate 及影片維持原版本。

## 產物

根目錄：`D:/story2video/artifacts/science-shorts/ice-visual-v2/`

- `ice-v2-zh.mp4`：約 48 秒完整試片（1441 格，視訊 48.033 秒、MP4 容器 48.100 秒），英文旁白、繁中燒錄字幕。
- `ice-v2-preview.mp4`：11.6 秒開場與放大段落，方便先看美術與動態。
- `en.srt`、`zh-Hant.srt`：獨立可編輯字幕。此次成片為繁中燒錄；沒有宣稱另做英文版或可切換字幕版。
- `actual-mp4/contact.png`：從實際成片取樣的九鏡聯絡表；`preview/` 是製作前畫格。
- `provenance.json`、`qa.json`：輸入與輸出 SHA、規格、解碼與影音分析。

## 科學與製作關卡

先把原稿、來源、讀者結果、既有 gate、原始配音及時間、兩個新素材凍結在 `inputs.json`。每次預覽／編碼前檢查檔案長度與 SHA，逐句核對配音時間表的公開文字與原稿一致。FFmpeg／ffprobe 沿用 Episode02 的指定絕對路徑、長度與 SHA 綁定，在每次啟動前重驗並使用 allowlist 子程序環境。

編碼另需 `visual-review.json` 通過且對應目前 renderer 與 inputs 的 SHA；新畫面不沿用舊 renderer 的圖解通過紀錄。排列示意清楚標成非實際晶體模型、不依比例；液態與冰的比較都保留 12 個相同尺寸符號，代表相同數量的水分子。這是科普動畫示意，沒有進行水體或晶體的物理模擬。

## 重跑

沿用現有 render venv 的 Pillow／numpy 與已驗證 FFmpeg；新 clone 需要另行準備素材及既有配音，不宣稱缺少資產即可重建。

```powershell
& 'D:/story2video/artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/ice-visual-v2/render.py --mode preview
& 'D:/story2video/artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/ice-visual-v2/render.py --mode render
& 'D:/story2video/artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/ice-visual-v2/render.py --mode qa
```

`prepare.py` 僅用於首次凍結 inputs，已有 manifest 時會拒絕覆寫。改素材或原稿應另建版本，修改 renderer 則需重新審查；不應為了重跑而更新既有審查 SHA。

實際結果、命令與未驗範圍在 [validation.md](validation.md)。影片供本機試看，沒有上傳、公開或建立頻道；真人理解、美術接受度、留存與成本可持續性仍待驗證。
