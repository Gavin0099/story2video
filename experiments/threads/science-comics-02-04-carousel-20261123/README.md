# Threads 生活科普 02–04｜新版父女輪播

依 [Owner 授權](authorization.md)，2026-11-23 在 `@gavinwu05191023` 逐篇刪除 02 至 04 的舊文，隨後用新版爸爸與女孩補發同一主題。每篇四張 4:5 圖，每張兩格。時間採 Asia/Taipei。[逐篇結果與圖文雜湊](publication.json)

| 篇目 | 舊文刪除 | 新文送出 | 新貼文 |
| --- | --- | --- | --- |
| 02 天空為什麼是藍色？ | 17:12:18 | 17:13:34 | [Threads](https://threads.com/@gavinwu05191023/post/DgFCEKsE2Cw) |
| 03 太空人怎麼聊天？ | 17:14:35 | 17:14:41 | [Threads](https://threads.com/@gavinwu05191023/post/DgFCMYlk5iz) |
| 04 水怎麼爬上紙巾？ | 17:15:18 | 17:15:23 | [Threads](https://threads.com/@gavinwu05191023/post/DgFCRkAk0WA) |

## 素材與驗收

- [藍天分鏡與圖片](02-blue-sky/storyboard.md) · [太空通話分鏡與圖片](../space-radio-carousel-20261123-cast-v2/storyboard.md) · [紙巾分鏡與圖片](04-paper-towel/storyboard.md)。太空通話沿用上一輪預覽，藍天與紙巾沿用科普定稿的核心機制並重寫成八格。新畫面使用內建 imagegen 和新版插畫角色圖。
- 工程驗收基準 Git SHA 為 `8b449a6927e9b04de2e32c22fb2791336b52ff5a`。確認 12 張 1080 × 1350 PNG、四張順序、逐格繁中、圖解及桌面 Edge 的 360 CSS px 可讀性。藍天第 2 張的空氣分子圖示以雙原子重畫。發文前從 Threads 編輯器核對每篇四圖與逐字配文，刪除後舊網址均轉回帳號首頁，從三個新貼文網址讀回帳號、文案和各四張圖。
- 依 README 執行 `uv run --locked --offline pytest --tb=line`，61 項通過。另以 Git 檢查變更與逐檔雜湊。
- 未登入 HTTP 請求回 HTTP 200，回應中沒有足夠的作者、配文和圖片資料可獨立核對。未測真實手機、平台壓縮後畫質與真人理解度。市場驗收依新貼文各自的首 24 小時觀察，尚未量測。
