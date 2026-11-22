# WhyNest Lab 頻道分流交接

後續狀態：Owner 另授權原三支轉公開，三支已核對為公開。本文保留首次私人交付的紀錄。公開時間及後續 20 支試驗見 [20 支公開 Shorts](../public-20-20261122/README.md)。

2026-11-22 Owner 已採納分流、選定 WhyNest Lab｜一分鐘科普、Primary 瀏覽器，以及三支影片「私人」試看。這是建立新科普頻道與私人上傳的增量授權，不含公開／排程或修改原海龜湯內容。

Owner 後續已確認插畫版品牌 v2 並要求建台及上傳。已建立 [WhyNest Lab](https://www.youtube.com/@WhyNestLab)，ID `UCJpx-XFeS91Vd26QokWAWOw`，與 CluePause ID 不同。三支影片均已在 WhyNest Lab 的 Shorts 清單核對為私人，並以登入帳號自觀看連結確認可開始播放。頻道頁目前顯示 `WhyNest Lab`，繁中名稱可見於橫幅，雙語簡介已從公開頁讀回。

| 私人試片 | 觀看連結 |
| --- | --- |
| 冰為什麼浮在水上？ | [a-tHhhJhNG8](https://www.youtube.com/shorts/a-tHhhJhNG8) |
| 天空為什麼是藍色？ | [EVWSVM3KBzA](https://www.youtube.com/shorts/EVWSVM3KBzA) |
| 隔著真空，太空人怎麼通話？ | [cezLqruPBzQ](https://www.youtube.com/shorts/cezLqruPBzQ) |

- `approved-settings.json`：登錄已確認品牌、實際頻道及私人影片 ID。
- `delivery-preflight.json`：首次準備快照，含三支新版 MP4、QA 綁定 SHA、英文／繁中標題與說明、來源與字幕路徑。快照中的名稱／可見性為選擇前狀態，以 approved-settings 為最新 Owner 選擇；不覆寫已產生的交接快照。
- `prepare.py`：重算三支 MP4 SHA 與原 QA 一致，並核對字幕檔存在。已有交接快照時拒絕覆寫，避免丟失之後登錄的狀態。
- `brand_assets.py`：原創幾何問號標誌與雙語品牌版面，使用本機既有 Pillow／Windows 字型；沒有套用海龜湯品牌或第三方圖片。輸出為 ignored artifacts 下的 avatar、banner、brand-preview PNG。

品牌素材：[預覽](../../../artifacts/science-shorts/channel-split-20261122/brand-preview.png)。頭像 800×800；橫幅 2560×1440，主要內容位於中央 1546×423 範圍。實際 YouTube 裁切尚待上傳後確認。

## 插畫版品牌 v2

依 Owner 對色彩和圖像的回饋，改用印刷質感的冰塊、夕照與太空人插畫。靛藍、冰藍、夕照橘與暖白對應三支試片。圓形頭像採用同色系環形行星。先定構圖和主色，再分開生成畫面與排雙語文字。參考 [Anthropic canvas-design](https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md)、[OpenAI imagegen](https://github.com/openai/skills/blob/main/skills/.system/imagegen/SKILL.md) 與 [ImageSizeKit 裁切模板](https://github.com/atricfox/imagesizekit-youtube-banner-safe-area-template)。

新版存於 `artifacts/science-shorts/channel-split-20261122/brand-v2/`，包含 `preview.jpg`、`banner.jpg`、`avatar.png`、`mobile-crop.jpg` 和兩份原始插畫。執行 `artifacts/render-venv/Scripts/python.exe -X utf8 experiments/science-shorts/channel-split-20261122/brand_assets_v2.py` 可重新排版。`qa.json` 保存輸出尺寸、大小、SHA 及文字範圍。橫幅 2560×1440、1.54 MB，頭像 800×800、1.08 MB，文字位在中央 1544×422 裁切內。裁切以 [YouTube 官方尺寸](https://support.google.com/youtube/answer/10456525) 等比例換算並向內取整。已檢視全幅與手機裁切的本機預覽。實際 Studio 頁面及上傳後的顯示待確認。

本輪先以人工 Studio 與分開交接清單落實分流，尚未新增正式 CLI channel profile、Episode 欄位、資料庫或自動上傳功能。

## 操作順序

1. 先核對可管理 CluePause 的帳號與是否已有 WhyNest Lab。若上次操作狀態未知，讀回既有頻道／草稿後再繼續，避免重複建立。
2. 建立獨立科普頻道，核對 handle 可用性並保存實際 channel ID；上傳前確定與 CluePause ID 不同。
3. 設定新頻道名稱、頭像、橫幅、簡介，核對可讀性與實際保存結果。
4. 只把 ice、sky、space 的 v2 完整片上傳新科普頻道，均設私人，補上對應字幕與雙語資料。
5. 重新開啟每支影片確認實際 video ID、私人可見性、處理畫質、字幕與試播，再交付線上觀看連結。私人影片需使用擁有觀看權限的登入帳號。

## 驗證

- Git 基準 `2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`，保留進場前未提交內容；未 commit／push。
- `.venv/Scripts/python.exe -X utf8 experiments/science-shorts/channel-split-20261122/prepare.py`：PASS；冰 48.1 秒、天空 46.1 秒、太空 51.8 秒，三支 SHA 與既有 PASS QA 一致，雙語 SRT 存在。
- `artifacts/render-venv/Scripts/python.exe -X utf8 experiments/science-shorts/channel-split-20261122/brand_assets.py`：成功；已人工目視 brand-preview 的文字、構圖與顏色，尚無平台裁切驗證。
- Primary 唯一一次 read-only 瀏覽器啟動回覆 UNAUTHORIZED／requires reauthentication；沒有 run ID 或已登入的頻道觀察，沒有遠端變更。
- 未改 src/story2video、video、Episode／SQLite、治理契約或框架；未重跑核心／影片測試。上述檔案 hash 檢查不等同新的影音完整 QA。
- 工程交接部分完成；線上分流待連線恢復。市場驗收仍 PENDING，新增真人資料 0。

## 線上交付驗收

- Git 基準 `2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`。Primary 重連後再次回覆 UNAUTHORIZED。已改用本機已登入的 Chrome，以 Windows UI Automation 讀取 CluePause Studio 與頻道切換器，再建立新頻道。
- 完整雙語名稱第一次建立時回報錯誤，重新檢查頻道清單後，使用 `WhyNest Lab` 與 `@WhyNestLab` 建立成功。Studio 之後儲存插畫版頭像、橫幅及雙語簡介。公開頁查核仍顯示英文名稱 `WhyNest Lab`。
- `upload-start.ps1`、`upload-finish.ps1` 和 `localize.ps1` 及收據保存在 ignored artifacts 的 `science-shorts/channel-split-20261122/`。MP4 和 SRT 選檔均核對雜湊。Studio 清單三筆逐列顯示私人。各片字幕頁讀回繁中、英文手動字幕與繁中標題／說明已儲存。三個 Shorts 連結都在登入中的 Chrome 成功開始播放，未逐支完整觀看或做手機實機檢查。
- `Invoke-WebRequest` 查核公開頻道頁 `og:title`、`og:description` 和 `og:url`。本次未執行核心、影片或市場測試，未新增真人觀看證據。

使用 [YouTube Studio skill](%USERPROFILE%/.codex/skills/story2video-youtube-studio/SKILL.md) 及 [Browser Use 外掛](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt) 嘗試連線。線上操作由本機 Chrome 完成。
