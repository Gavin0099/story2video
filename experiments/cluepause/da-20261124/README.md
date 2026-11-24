# CluePause D-a：時間間隔、反轉候選分類與資料缺口

本次授權限資料與分析，以 PR #19 head `a5be360edfbb2b012ae5e373d6a5c01315f1b8f6` 為基底，分支 `codex/cluepause-da-20261124`。輸入為 [首日與時間碼主表](../performance-p0-20261124/first-24h-and-timing.csv) 和 [其他時窗表](../performance-p0-20261124/other-windows.csv)，各 29 列（舊 20、新 9）。既有 CSV、假設和 README 結論維持原樣。本目錄沒有品質分數、門檻或發布判定，未操作已公開影片。

## 交付與定義

- [derive_clue_intervals.py](derive_clue_intervals.py)：只使用 Python 標準函式庫，預設讀主表並寫 [clue-to-reveal.csv](clue-to-reveal.csv)，可用 `--input`、`--output` 指定其他路徑，拒絕覆寫輸入。讀完並完成計算後才開啟輸出；非空但無法轉成數字的值會報錯，不冒充缺值。
- `clue_to_reveal_s = reveal_s - key_clue_s`：以原始十進位時間計算，四捨六入五成雙至小數 2 位；任一輸入空白則結果空白。保留輸入時間欄位的原始精度。`clue_before_paradox` 是嚴格小於比較，以 `true`／`false` 表示；線索或題面時間缺失時留白，與揭曉是否缺失分開計算。
- [twist-taxonomy.csv](twist-taxonomy.csv)：僅依主表 `anomaly`、`key_clue`、`reveal` 的文字分類，每列一個中文依據；不從標題、其他稿件或外部故事補情節。全部 `label_status=candidate`，`owner_confirmed` 全留白。`secondary_tags` 同用下表詞彙，以分號分隔多標籤，無適用標籤可留白。
- [rights-source.csv](rights-source.csv)：既有權利證據的盤點，來源欄不確定即留白；不因公開、故事分數或凍結稿雜湊而判定核准。
- [單元測試](../../../tests/unit/test_cluepause_da.py)：一般計算、精度、零值與空值、嚴格小於旗標、CSV 寫入與輸入保護，以及不使用 fixture 的真實主表中位數檢查。

候選詞彙的本次判讀口徑如下；類別可重疊，主標籤只是暫定的主要重新理解方式。

| 標籤 | 判讀口徑 |
| --- | --- |
| benevolent_misunderstanding | 表面不友善或破壞性的行為，揭曉可解作協助、照顧或承擔責任 |
| identity_reversal | 對人物身分或作者歸屬的理解改變 |
| context_reversal | 場所、對象、關係、規則或分工等情境改變原先理解 |
| object_function | 物件的用途或作用改變原先理解 |
| causal_reversal | 揭曉以線索重新解釋異常的原因；此候選用法不主張物理因果方向顛倒 |
| other | 以上皆不適用時使用，並在 rationale 解釋；本次未使用 |

## 假設（尚待驗證）

線索到揭曉的間隔可能影響觀眾形成有根據猜測的時間；間隔較短可能減少思考空間，也可能保持節奏。這些方向均待資料驗證，沒有最佳秒數或及格線。此延伸假設未改寫 PR #19 的三項既有假設。

候選反轉類型可作未來分組描述的欄位，但類別是否與同窗續看或留存有關仍未知。標籤不是品質分數，Owner 尚未確認，也沒有據此排名或選片。

## 觀察

29 列的線索和揭曉時間皆可計算。先逐片相減並保留 2 位，再取組內中位數並顯示 2 位：舊 20 支為 **12.16 秒**，新 9 支為 **8.97 秒**。這是相減結果的中位數，不能用「揭曉中位數減線索中位數」替代。新組較短只是這兩組時間安排的描述。

唯一 `clue_before_paradox=true` 是 26M-B〈尋人啟事〉：`16.00 < 22.90`，其間隔為 22.63 秒。主表已註明兩版共用尾段字幕，且線索早於貼回動作；旗標僅提示這個順序供診斷。

**反例：V12〈單車尾燈〉的舊組間隔最短，僅 6.36 秒，卻有最高 D1 views 1,048，平均觀看百分比 72.1%。因此間隔只能當作風險訊號，不能當作規則。** 這些數值均來自主表 D1，沒有換成累計觀看。

## 同窗 D1 缺口清單

以主表非空欄位計數，分母固定為 29；來源明確記錄的零值算有值，空白不算。以下數字為「有資料的列數」，0／29 不代表指標數值為零。其他時窗表只用來辨認不可混用的資料。

| 同窗 D1 指標 | 主表欄位 | 舊組有值／20 | 新組有值／9 | 合計有值／29 |
| --- | --- | ---: | ---: | ---: |
| Shorts feed shown | shorts_feed_shown_d1 | 0／20 | 0／9 | 0／29 |
| stayed to watch | stayed_to_watch_d1_pct | 0／20 | 0／9 | 0／29 |
| engaged views | engaged_views_d1 | 20／20 | 0／9 | 20／29 |
| avg % viewed | avg_viewed_d1_pct | 18／20 | 0／9 | 18／29 |
| per-second retention | retention_d1 | 0／20 | 0／9 | 0／29 |
| likes | likes_d1 | 20／20 | 0／9 | 20／29 |
| subscribers | 未收錄 D1 訂閱欄位 | 0／20 | 0／9 | 0／29 |

平均觀看百分比缺值的舊片為 12-v7、09-v6。18 個非空比例包含 Studio 記錄的零，不等於 18 個正數互動觀看樣本。`subscribers` 在兩份輸入中皆未收錄，不能從 views、likes 或其他欄位推算。

**Lifetime／其他時窗值不能替代 D1。** `other-windows.csv` 的 `lifetime_stayed_pct`、累計留存卡狀態、`export_*`（Studio 日期區間為 2026-10-26 至 2026-11-22）均不回填本表；縮圖曝光也不能代替 Shorts feed shown。逐秒曲線若標「發布至今」，不能算 D1 曲線。

新 9 支 D1 於 **2026-11-25 01:08–01:17 Asia/Taipei** 依各片公開時間陸續截止；主表秒級範圍為 `01:08:55+08:00` 至 `01:16:54+08:00`。補資料時須逐片記錄 **D1 cutoff time** 和 **Studio observed time**（含日期與時區），另保留 Studio 實際選取的報表時窗及來源。觀察時間可能晚於截止時間，兩者不可互代；若截止後仍未提供數值，維持空白並記原因。此輪只分析現有快照，沒有補查 Studio。

## 權利／來源盤點依據

已照指定指令讀取 PR #17 分支的規範：

```sh
git show origin/codex/cluepause-story-rights-gate:.agents/skills/story2video-shorts-batch/references/story-rights.md
```

`rights_status` 僅使用其原有詞彙：`approved`、`pending_permission`、`pending_verification`、`rejected`。本輪 29 列均為 `pending_verification`，沒有把發布核准推論為權利核准，也沒有已知必須取得特定許可的證據可支持改標 `pending_permission`。

已檢索本基底版控檔案中的權利狀態、審查與來源線索，並查看 [舊組發布紀錄](../public-20-20261122/release.json)、[新組發布紀錄](../retention-ten-public-20261124/publication.json)、[新組素材清單](../retention-ten-public-20261124/media-manifest.json) 和 [海報題卡來源說明](../../story-quality-lab/README.md)。新 9 支素材清單的描述宣告「原創虛構故事」，故 `source_type=original_declared`，意為已有原創宣告、仍待查證；這是來源描述，並非 PR #17 權利狀態詞彙。舊 20 支未找到足以逐片確認來源類型的紀錄，故該欄留白；26M-B 僅追到既有試片字幕，尚未追到原始來源。

新組雖有凍結稿雜湊和品質評分，尚缺可追溯的作者或製作來源、參考機制與具體情節相似性比對、審查人及本次用途審查。舊組也缺完整逐片權利鏈。各列 `rights_note` 留下已見紀錄及缺證。本輪未核對版控外的私有權利文件，狀態表示目前證據不足，不宣稱作品侵權或已取得許可。

## 尚不能證明／市場驗收

目前不能證明較短間隔、某反轉類型或新版開場帶來較好的市場表現；新 9 支尚缺同窗 D1，全部 29 支缺同窗動態分發與逐秒留存，且故事、發布時段等條件同時改變。也沒有真人首次觀看資料來驗證猜測時間、理解或情緒反應。候選標籤未經 Owner 確認，來源宣告未完成權利查證，不能據此推導品質或權利通過。市場驗收仍未完成。

## 工程驗收

Git 基底：`a5be360edfbb2b012ae5e373d6a5c01315f1b8f6`。使用既有 `D:\story2video\.venv\Scripts\python.exe`（Python 3.13.18）執行，未安裝或更動該環境。此 shell 預設無 `python`；bundle Python 3.12.14 沒有 pytest，因此改用符合專案 Python 版本的既有環境。測試第一次為 10 passed、1 error，原因是 pytest 預設暫存目錄無讀取權限；將本次程序的 `TEMP`／`TMP` 導向 repo 下忽略的 `artifacts/da-20261124-tmp` 後重跑。

從 repo root 執行：

```powershell
$env:PATH = 'D:\story2video\.venv\Scripts;' + $env:PATH
$env:PYTHONDONTWRITEBYTECODE = '1'
New-Item -ItemType Directory -Force artifacts/da-20261124-tmp | Out-Null
$env:TEMP = (Resolve-Path artifacts/da-20261124-tmp).Path
$env:TMP = $env:TEMP
python experiments/cluepause/da-20261124/derive_clue_intervals.py
python -m pytest tests/unit/test_cluepause_da.py -q -p no:cacheprovider
git diff --check
```

結果：腳本寫出 29 列；指定測試 11 passed；`git diff --check` 通過。另核對三份輸出 CSV 各 29 個唯一 code、與主表同順序同集合、候選與權利詞彙、空白 Owner 確認欄、缺口計數及 V12 反例；產生檔可重跑得到相同內容。以 `git diff --exit-code HEAD -- experiments/cluepause/performance-p0-20261124` 確認既有 PR #19 兩份 CSV 與 README 未變更。

未執行根 README 的全套 `uv sync --locked`、`uv run --locked pytest`、`npm ci`、`npm run typecheck`，也未跑治理驗證；本次變更限新增分析檔與獨立測試，沒有改 `src/story2video/`、`video/`、治理契約或框架版本。未重新驗證 Studio 數據、實際成片時間碼、權利文件或真人理解；工程測試通過不代表市場驗收。
