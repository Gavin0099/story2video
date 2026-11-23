# Threads 科普四格首篇

首篇繁中生活科普四格已在 `@gavinwu05191023` 公開發布。瀏覽器於台灣時間 2026-11-23 15:04:16 送出，隨後在個人檔案與貼文頁讀回。Owner 另授權將同一帳號的 Threads 顯示名稱改為 `GavinWu`，於 15:06:08 儲存，重新載入後確認名稱與帳號代稱。見 [公開貼文](https://www.threads.com/@gavinwu05191023/post/DgEzRLWExjX)、[授權原文](authorization.md)與[逐篇紀錄](publication.json)。

## 內容與產物

- 貼文：[caption.txt](caption.txt)，289 個 Unicode 字元，含兩份查核來源及 AI 圖像說明。
- 原始生圖提示：[image-prompt.txt](image-prompt.txt)。使用內建 image_gen，非付費 API CLI；工具未提供金額。
- 科學查核：[sources.md](sources.md)。
- 本機初稿：`artifacts/threads/science-comic-20261123/ice-comic-v1.png`，1122×1402，SHA-256 `fd46cc9b41f356cfd88e85e2f27eb24edf53d80fa3fdcc6b1f085928ed4080c1`。初稿第二格分子數量不一致，未通過發布檢查，已要求定向修正。
- 風格原版：[ice-comic.png](ice-comic.png)，1122×1402，SHA-256 `2bdeed5559d632b601a1d541ede1b5e43e346e749e51fa1dcdf2991f66d7d0ce`。體積示意與 360 CSS px 手機寬度檢查見 [visual-qa.md](visual-qa.md)。
- 實際發布圖：[ice-comic-public.png](ice-comic-public.png)，SHA-256 `af565743725763c71088b4a7a761610e57b17d1de072ec05c05f525e071719e3`。用內建 image_gen 依[修圖提示](image-signature-edit-prompt.txt)移除右下角舊帳號字樣，逐格檢視繁中對白及科學圖解。

## 工程驗收

工作區基準 Git SHA：`9f2324b2180402a840edb5a5c3ef91e99d3a9e16`。沒有改動 `src/story2video/`、`video/`、Episode 契約或 SQLite。

2026-11-23 執行 README 所列 pytest；環境中 `uv` 不在 PATH，改用既有工具的絕對路徑。預設 C 槽快取曾因跨磁碟 temporary-file rename 失敗，改用同磁碟快取成功：

```powershell
& 'D:/story2video/artifacts/tooling/bin/uv.exe' --cache-dir './artifacts/tooling/whynest-uv-cache' run --locked pytest
git diff --check
```

結果：61 passed in 13.41s；`git diff --check` exit 0。未改動 video，未重裝 npm 或重跑 typecheck；本次不以引擎測試取代漫畫科學與版面檢查。

原帳號曾遇到登入阻礙，使用者後來已在本機 Chrome 登入新指定帳號。從 Threads 自身個人檔案入口、編輯個人檔案權限及編輯器帳號核對新身分。貼文送出前逐字讀回文案、核對兩個來源連結與上傳檔 SHA-256。Threads 自動產生的來源預覽卡會佔用影音欄位，因此清除卡片，保留文案中的可點選來源。

發布回合基準 Git SHA 為 `673fa146e3750b96f14824b67dd235f4b2d9c6d2`。以 Chrome UI Automation 核對貼文網址、署名、文案、附件與個人檔案「公開」狀態，另以未登入 Edge 取得可見貼文與圖片的預覽，Threads 同時顯示登入提示。改名後在重新載入的個人檔案確認 `GavinWu` 與 `@gavinwu05191023`。`Get-FileHash -Algorithm SHA256` 與 `git diff --check` 驗證證據檔。本回合變更限發布內容及證據，未另重跑引擎測試。

## 市場驗收

市場數據待量測。發布滿 24 小時為 2026-11-24 15:04:16，滿 72 小時為 2026-11-26 15:04:16，均為台灣時間。

發布後可在實際滿 24／72 小時時讀取觀看、按讚、其他讀者回覆、轉發／引用、追蹤趨勢，並記錄製作與回覆耗時。不可用發布當下數字替代固定觀察窗；本篇為新帳號單篇探索，沒有對照組，不宣稱格式優劣或因果。
