# Threads 生活科普 02–04

依 repo 的科普腳本改編成繁中四格，於 2026-11-23 在 Threads `@gavinwu05191023` 公開發布。保留各腳本的核心機制，重新寫對白和結尾。

| 漫畫 | 配文 | 腳本 |
| --- | --- | --- |
| [02 天空為什麼是藍色？](02-blue-sky.png) | [02 配文](02-caption.txt) | [藍天定稿](../../science-shorts/batch-20261121/scripts-final.md#天空為什麼是藍色) |
| [03 太空人怎麼聊天？](03-astronaut-radio.png) | [03 配文](03-caption.txt) | [太空通話定稿](../../science-shorts/batch-20261121/scripts-final.md#隔著真空太空人怎麼通話) |
| [04 水怎麼爬上紙巾？](04-paper-towel.png) | [04 配文](04-caption.txt) | [紙巾原稿](../../science-shorts/public-20-20261122/writer-b-17-20-r2.json#L330) |

藍天篇聚焦晴天，把夕陽段落留在原稿。太空篇聚焦頭盔內的聲音、跨越真空的無線電，以及另一端的收聽。紙巾篇保留水潤濕纖維、在相通小縫中上升及受重力限制的重點。

生圖採內建 imagegen，參考[已核准冰塊篇](../science-comic-20261123/ice-comic-public.png)的畫風、構圖和角色。工具未提供費用資訊。各篇配文附原始資料連結，逐字提示與漫畫同目錄。

## 驗收

- 基準 Git SHA 為 `42eeeabb76a60c4d83dd39e3d91b76c668514eae`。
- 工程範圍為靜態圖文。檢查項目為逐格文字、圖解、圖片規格、360 CSS px 瀏覽器預覽和配文字數。沒有應用程式或影片程式改動。
- 市場驗收待貼文各滿 24 小時後量測，發布時點見逐篇紀錄。真人試讀與平台圖片壓縮品質未驗證。

三張成圖都是 1122 × 1402 PNG。以 Edge 將三張圖各顯示為 360 CSS px 寬，實看[縮圖截圖](../../../artifacts/threads/science-comics-02-04-20261123/three-comics-360px.png)。標題、對白、圖解及箭頭可讀。藍天篇示意光散向不同方向，太空篇區分頭盔內的藍色聲波符號和外部的橘色無線電路徑，紙巾篇的濕痕持續連到杯水。太空篇末格經定向修正，耳機與聲波符號都在透明頭盔內，未改對白。瀏覽器檢查在桌面進行。

`git diff --check` 通過。三份配文分別為 216、256、310 個 UTF-16 字元，含換行及來源連結，均省略使用者指定的製作說明。依 README 執行 `uv run --locked --offline pytest --tb=line`，使用 repo 既有的本機快取與 Python，61 項通過。預設快取第一次遇到 Windows 跨磁碟寫入錯誤，改用同磁碟快取後通過。

## 公開發布

於 Chrome 核對指定帳號、編輯器完整配文與一張對應圖片後逐篇發布。每篇送出後讀回個人檔案與貼文網址，再檢查署名、配文與一張附件。個人檔案隱私顯示公開。另以未附登入憑證的 HTTP 請求讀取三個網址，皆收到 200，且回傳內容包含作者、配文開頭與圖片中繼資料。

| 篇目 | 台灣時間送出 | 公開貼文 |
| --- | --- | --- |
| 02 藍天 | 2026-11-23 16:13:04 | [Threads](https://threads.com/@gavinwu05191023/post/DgE7JINE6QJ) |
| 03 太空通話 | 2026-11-23 16:16:20 | [Threads](https://threads.com/@gavinwu05191023/post/DgE7g7rE5uB) |
| 04 紙巾 | 2026-11-23 16:17:40 | [Threads](https://threads.com/@gavinwu05191023/post/DgE7qx6Ew1w) |

[Owner 授權](authorization.md)及[逐篇發布與圖文雜湊](publication.json)。發布回合再次執行 `uv run --locked --offline pytest --tb=line`，61 項通過。
