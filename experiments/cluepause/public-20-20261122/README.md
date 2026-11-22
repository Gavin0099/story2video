# CluePause 20 支公開核對

2026-11-22 台灣時間，Owner 指示「先改公開 然後看下一個10篇劇本」。公開範圍是上一輪交付的三支私人試看片。Studio 儲存後重新開啟影片詳情及 Shorts 清單，確認這三支與另外 17 支均顯示公開。[逐片機讀紀錄](release.json)

| 片號 | 影片 | 實際公開時間（台灣） | 首 24 小時截止（台灣） |
| --- | --- | --- | --- |
| V11 | [生日氣球](https://www.youtube.com/shorts/VyX6jxjfEDw) | 11/22 23:45:42 | 11/23 23:45:42 |
| V12 | [單車尾燈](https://www.youtube.com/shorts/mdAU5oD51uE) | 11/22 23:45:57 | 11/23 23:45:57 |
| V13 | [理髮師](https://www.youtube.com/shorts/bGBCSoRLP2g) | 11/22 23:46:11 | 11/23 23:46:11 |

工程驗收包含影片 ID、母片 SHA-256、英文與繁中可切換字幕，以及儲存後的可見性。市場驗收以影片公開後的實際觀察窗為準。

本機驗收以 Git 基底 9f2324b2180402a840edb5a5c3ef91e99d3a9e16 執行 uv run --locked pytest（61 項通過）、npm ci、npm run typecheck 與 git diff --check。npm 在 Node 24 發出專案版本警告，型別檢查通過。
