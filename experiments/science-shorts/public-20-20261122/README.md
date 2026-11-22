# WhyNest Lab｜20 支公開 Shorts

2026-11-22 Owner 明確授權將三支已完成且達門檻的科普試片轉公開，再新增 17 支達標成片至總數 20。新片圖解只用英文，採英文旁白並提供獨立英／繁中字幕。公開頻道 `UCJpx-XFeS91Vd26QokWAWOw`，首日觀察以各片實際公開時間為起點。

17 支新片均已製作完成。Studio 確認 10 支公開，上傳第 11 支時遇到每日上限。逐片分數、連結、滿 24 小時時間和待上傳 MP4 見 [發布紀錄](release-status.md)。

沿用科普評分規約。兩位獨立讀者各 85 分以上，另有事實、畫面與成片硬門檻。內容需按原始來源和實際影片驗收，出版授權由 Owner 本次明確給予。

| 影片 | Studio 確認公開（台灣） | 首個滿 24 小時（台灣） |
| --- | --- | --- |
| [冰](https://www.youtube.com/shorts/a-tHhhJhNG8) | 2026-11-22 00:42:19 | 2026-11-23 00:42:19 |
| [天空](https://www.youtube.com/shorts/EVWSVM3KBzA) | 2026-11-22 00:42:28 | 2026-11-23 00:42:28 |
| [太空](https://www.youtube.com/shorts/cezLqruPBzQ) | 2026-11-22 00:43:59 | 2026-11-23 00:43:59 |

上述時間為 Studio 確認值。這三支是原有試片，仍有繁中燒錄文字。新片將使用獨立字幕軌，因而能按觀看者偏好切換。既有上傳檔與線上連結保留。

首日從 YouTube Studio 進階模式的「影片發布後首 24 小時」讀取。記錄有效觀看、繼續觀看比例、平均觀看百分比、訂閱增量、總觀看和觀察時間。Studio 尚未提供的欄位填 N/A，保留讀取時間。後續可與 D7／D28 比較。[YouTube 進階模式](https://support.google.com/youtube/answer/9717005) · [Shorts 數據說明](https://support.google.com/youtube/answer/12220281)

新片沿用同一英語旁白與原定分鏡，採 35–60 秒的範圍。試片原有 45–60 秒限制仍是共用合成函式的預設值。成片使用 1080 × 1920、30 fps、H.264 和 AAC，解析度、時長、全檔解碼、黑畫面、靜音和響度均由 FFmpeg／FFprobe 驗收。審查收據綁定凍結稿、動畫快照、原生字幕和實際編碼檔。

### 驗收紀錄

- 工作區基準 Git SHA 為 `2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`。本輪內容與製作程式為工作區變更。
- `artifacts/tooling/bin/uv.exe --cache-dir ./artifacts/tooling/whynest-uv-cache run --locked pytest` 通過 61 項。`git diff --check` 通過。
- 使用與 MP4 不符的獨立審查收據測試 `release_package.py`，程式拒絕建立發布包。
- 片段的生圖提示、原圖與切圖位於 `artifacts/science-shorts/public-20-20261122/`。內建圖像生成工具未提供此次成本。
- 兩位 AI 讀者各自評分，科學審查抽看實際 MP4；獨立審查員未直接聆聽音訊。真人看懂與否、手機播放器字幕可讀性與首日市場成效待觀察。
- `record_publication.py` 從已核對的 Studio 可見性紀錄更新 `d1.csv`，保留各片的讀取時間與數據。
