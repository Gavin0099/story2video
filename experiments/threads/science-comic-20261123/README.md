# Threads 科普四格首篇

本次在 `@gavinlog0099` 試一篇繁中生活科普四格，主題為一般冰為什麼浮在液態水上。Owner 明確授權發布；範圍與原文見 [authorization.md](authorization.md)。

## 內容與產物

- 貼文：[caption.txt](caption.txt)，289 個 Unicode 字元，含兩份查核來源及 AI 圖像說明。
- 原始生圖提示：[image-prompt.txt](image-prompt.txt)。使用內建 image_gen，非付費 API CLI；工具未提供金額。
- 科學查核：[sources.md](sources.md)。
- 本機初稿：`artifacts/threads/science-comic-20261123/ice-comic-v1.png`，1122×1402，SHA-256 `fd46cc9b41f356cfd88e85e2f27eb24edf53d80fa3fdcc6b1f085928ed4080c1`。初稿第二格分子數量不一致，未通過發布檢查，已要求定向修正。
- 最終版：[ice-comic.png](ice-comic.png)，1122×1402，SHA-256 `2bdeed5559d632b601a1d541ede1b5e43e346e749e51fa1dcdf2991f66d7d0ce`。已保存可進版控副本，與 `artifacts/threads/science-comic-20261123/ice-comic-final.png` 相同。體積示意修正與 360 CSS px 手機寬度檢查見 [visual-qa.md](visual-qa.md)。
- 尚待完成：目標帳號登入、公開發布與線上讀回；目前未發布。

## 工程驗收

工作區基準 Git SHA：`9f2324b2180402a840edb5a5c3ef91e99d3a9e16`。沒有改動 `src/story2video/`、`video/`、Episode 契約或 SQLite。

2026-11-23 執行 README 所列 pytest；環境中 `uv` 不在 PATH，改用既有工具的絕對路徑。預設 C 槽快取曾因跨磁碟 temporary-file rename 失敗，改用同磁碟快取成功：

```powershell
& 'D:/story2video/artifacts/tooling/bin/uv.exe' --cache-dir './artifacts/tooling/whynest-uv-cache' run --locked pytest
git diff --check
```

結果：61 passed in 13.41s；`git diff --check` exit 0。未改動 video，未重裝 npm 或重跑 typecheck；本次不以引擎測試取代漫畫科學與版面檢查。

兩個 Browser Use 連線均無法使用：Primary 需要重新驗證，Browser Use 回覆 `insufficient_credits`。改檢查本機 Chrome；以已填入目標使用者名稱的登入資料送出後未建立可核對的 Threads session，Instagram 轉向後登入頁顯示另一個候選帳號 `reiko0099`。未使用該候選帳號發布，已請 Owner 在網站直接登入 `gavinlog0099`；沒有索取、匯出或記錄密碼／驗證碼。

之後目前分頁顯示「目前無法登入帳戶」，仍沒有可核對的目標帳號登入狀態。未反覆送出登入、未使用其他帳號、未點擊發布。逐篇狀態見 [publication.json](publication.json)。

## 市場驗收

尚未發布，沒有實測觸及、互動、追蹤或 YouTube 導流結果。成功製作或公開不等於市場驗收。

發布後可在實際滿 24／72 小時時讀取觀看、按讚、其他讀者回覆、轉發／引用、追蹤趨勢，並記錄製作與回覆耗時。不可用發布當下數字替代固定觀察窗；本篇為新帳號單篇探索，沒有對照組，不宣稱格式優劣或因果。
