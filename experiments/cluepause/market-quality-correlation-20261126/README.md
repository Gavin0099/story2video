# AI 盲評分數 × 市場成效 對照（2026-11-26）

本目錄只讀取既有紀錄，沒有連線 YouTube、沒有呼叫付費 API、沒有製作或修改影片、沒有新增或變更任何品質 gate。無法取得的數據一律標為缺漏，不以累積觀看數替代首日數據。

交付前經過一次獨立 subagent review，其指出的問題已修正，修正項列於 [§九](#九review-指出並已修正的問題)。

## 交付物

| 檔案 | 內容 |
| --- | --- |
| [score-index.csv](score-index.csv) | 160 筆盲評紀錄，含 story SHA-256、讀者人數與 clear 旗標、評分規約版本、來源 commit 與證據檔雜湊 |
| [score-granularity.txt](score-granularity.txt) | **為什麼 92.9% 的合格影片剛好 91 分**，由 383 筆逐維度評分推導 |
| [market-schema.json](market-schema.json) | 市場欄位的統一契約：來源、時間窗、型別與衍生規則 |
| [reader-reliability-experiment.md](reader-reliability-experiment.md) · [reliability-sample.csv](reliability-sample.csv) | AI 評審穩定性實驗設計與選稿（**未執行**） |
| [quality-vs-market.csv](quality-vs-market.csv) | 29 支影片的盲評、版本核對、分鏡時間軸與各時間窗市場數據 |
| [correlations.txt](correlations.txt) | 相關係數，附 n、兩側缺值、相異值數、離群值與去除離群值後的敏感度 |
| [data-gaps.csv](data-gaps.csv) | 97 列缺漏，**由程式產生**，不手工維護 |
| [build_index.py](build_index.py) · [build_table.py](build_table.py) · [build_gaps.py](build_gaps.py) · [analyze_rubric.py](analyze_rubric.py) · [select_reliability_sample.py](select_reliability_sample.py) | 可重跑的蒐集、join、缺口盤點、量尺分析與選稿 |
| [test_pipeline.py](test_pipeline.py) | 43 項測試 |

```powershell
cd D:\story2video\experiments\cluepause\market-quality-correlation-20261126
python -I build_index.py
python -I build_table.py
python build_gaps.py
python -I analyze_rubric.py
python -I select_reliability_sample.py
python -m unittest test_pipeline -v
```

`build_index.py` 與 `build_table.py` 的輸出可逐位元重現；`build_gaps.py` 的輸出含「跑的當下」時間，窗口狀態會隨日期改變。`test_pipeline.py` 的整合測試在缺少本機 `artifacts/` 或 `D:\s2v-gp` 時會 skip，所以「43 項通過」只在兩者俱在時才有意義。

### 內容主鍵

版本 id（`04-v7`、`62-v1`）**不是**唯一識別。本分析以

```
story_sha256 = sha256( first | second | reveal | english )
```

為主鍵，並保留 story id、artifact family、video id、評分規約版本與來源 commit。

### 範圍

表中 29 支是 `media-map.json` 的內容，**不是頻道公開影片的全集**：另有 P02／U02／H02／H03／H04 於 11/25 轉公開，目前沒有任何數據，只出現在 `data-gaps.csv`。下文所有「29 支」都指這 29 支。

---

## 一、修正：04-v7 的盲評紀錄確實存在

你指出的 PR #7 證據成立，先前版本標為 `NOT_TESTED` 是錯的。

| 查核項目 | 結果 |
| --- | --- |
| commit | `063cc51d1d81f33ff3c7801a4af481740ef33778`（分支 `codex/story-quality-autoloop`，PR #7，未合併） |
| 路徑 | `experiments/shorts-story-review/autoloop/run-09/final-report.json` |
| 讀者分數 | 91 / 91 / 93 |
| cores | `重錄是為了去除哥哥提前搶進的聲音` → supported |
| status | `READY_FOR_HUMAN_PRODUCTION_DECISION`，`qualified: ["04-v7"]` |
| 凍結稿 SHA-256 | `6e3e945a06f251cccb44b43a8500bbfe6115831c347bd223681a51db10fbd6a3` |
| 母片所用文字 | `artifacts/04-v7-pilot/approved-story.json`，同一 SHA-256，四欄逐字相同 |
| 判定 | `GATE_PASS` / `TEXT_MATCHES_MASTER_SOURCE` |

**錯誤原因**：先前只掃本機 `artifacts/`，證據卻在未合併分支的 `experiments/shorts-story-review/autoloop/`。現在 `build_index.py` 掃全部 28 條遠端分支加本機，記錄每筆的 source kind／分支／commit，並有一項測試鎖住這個 hash。

重掃得到 **160 筆評分紀錄（git 32、local 128）**，全部可算出內容主鍵。已知限制：git 掃描只比對檔名 `final-report.json`，若日後有其他檔名的評分證據會被略過。

### `TEXT_MATCHES_MASTER_SOURCE` 核對到什麼程度

它確認「被評分的文字」等於「母片所依據的 artifact 內 `story.json`」。它**沒有**重新核對上傳影片的旁白內容；影片與該 artifact 的連結來自 `media-map.json` 的 `asset` 與母片 sha256。

### 連帶發現：同一份文字從來沒有被重複評過

160 筆紀錄對應 **160 個相異 story SHA-256**，所以**這套制度的跑次間再現性從未被測過**。先前看似「同稿不同分」的四個案例（`61-v1`、`61-v2`、`62-v1`、`65-v1`）其實是不同故事共用版本 id：

| 版本 id | script-batch-001 的故事 | market-twelve 的故事 |
| --- | --- | --- |
| 62-v1 | 阿姨站在畢業典禮最後一個空車位（= R04） | 我媽把背包剪開了 |
| 61-v2 | 評審走到沙堡前（= R10 本機試片） | 跟進巷子的紅燈 |

用 id join 的話 R04 會被配到 `95,87,87`，而不是真正的 `91,91,95`。

## 二、修正：我先前說「異常越早越好是唯一穩健訊號」，撤回

依你的第 5 點，零互動觀看的平均觀看比例不能當有效樣本。`correlations.txt` 現在把留存分三層輸出，讓每一次排除的影響**可稽核**而不是用講的：

| 留存欄位 | n | 第一個可見異常秒數 Pearson | Spearman |
| --- | ---: | ---: | ---: |
| raw（含 0 互動的假 0%） | 16 | −0.415 | −0.410 |
| valid（0 互動視為缺值） | 8 | **+0.389** | **+0.405** |
| valid 再去掉重播破百 | 7 | +0.654 | +0.668 |

排除假零之後方向就反轉。**這不表示異常越晚越好，而表示這個資料集定不出方向。**

> 先前版本在這裡引用的是「−0.481／−0.409，n=18」。那組數字來自一個已被取代的中間計算，無法從本目錄任何檔案重現，已改為上表可稽核的 raw 基準（−0.415／−0.410，n=16）。

### n=8 不只是「脆弱」，是結構性退化

這 8 列的實際構成：

- `anomaly_s` **只有 3 個相異值**（0 出現六次、1.5、2.5）→ 那個 ±0.40 由兩個點決定。
- `ai_min` **只有 2 個相異值**（91 七次、95 一次）→ 它的 Spearman −0.577 由單一點（05-v6）決定。
- 其中三列的留存值建立在 **1–2 次互動觀看**上（V06 1 次 → 16.2%、V10 1 次 → 106.6%、05-v6 2 次 → 15.3%）。

`correlations.txt` 每一行現在都印出 `distinct_x`，相異值 ≤3 會自動標註；留存區塊也印出最小的互動觀看分母。

### 先前漏掉的一條係數

同一個 n=8 區塊裡最強的是 **`AI 最低分 ~ D1 平均觀看比例：Pearson −0.545、Spearman −0.577`**（去掉重播後 −0.578／−0.612）。先前版本引用了同區塊較弱的片長、線索、揭曉三條當「脆弱」的例子，卻沒引這條，讀起來像是迴避了一個負向的分數–留存關係。

它確實是負的，但 `distinct_x=2`：整條線由 05-v6 一個點撐住，而 05-v6 的 15.3% 又只有 2 次互動觀看。**它不構成「分數越高留存越差」的證據**，和其他 n=8 的數字一樣不可採信。

### 唯一不受假零影響的是 D1 觀看（真實計數）

| 預測變數 ~ D1 觀看 | n | Pearson | Spearman |
| --- | ---: | ---: | ---: |
| 第一個可見異常秒數 | **18** | −0.163 | −0.414 |
| AI 最低分 | 19 | −0.121 | +0.105 |
| 揭曉秒數 | 19 | −0.270 | +0.062 |

異常那一行是 n=18 不是 19：V07 的 `first_visible_anomaly_s` 在來源 CSV 是空的（原始註記寫明 0／1.5／3 秒抽幀無法確認開場位移）。

D1 觀看的離群值是 04-v7、V09、V12、V13。`correlations.txt` 另外輸出一個**去除這四支後**的區塊：異常秒數的 Spearman 變成 −0.630（n=14），AI 最低分變成 +0.352。方向沒翻轉但數值變動很大，所以這條只能當待驗假設。

## 二之二、為什麼 92.9% 的合格影片剛好是 91 分

由 383 筆逐維度評分推導，完整輸出在 [score-granularity.txt](score-granularity.txt)。答案是**量尺結構**加上**停止條件**，不是評審寬鬆或串通。

### 分數是離散的，而且實際只用到幾個階

```
total = 4·suspense + 5·reframe + 4·motivation + 3·causality + 2·fairness + 2·visuals
```

383 筆評分的實際用值：

| 維度 | 權重 | 給 5 分 | 給 4 分 |
| --- | ---: | ---: | ---: |
| visuals | 10% | 99.0% | 1.0% |
| causality | 15% | 91.4% | 7.8% |
| fairness | 10% | 66.8% | 21.1% |
| motivation | 20% | 43.1% | 55.9% |
| suspense | 20% | 26.4% | 72.6% |
| **reframe** | **25%** | **5.5%** | **84.6%** |

**權重最大的 `reframe` 幾乎永遠是 4 分。** 它一落 4，總分天花板就被壓到 95。

### 門檻 90 掉在階與階之間的空隙裡

固定最常見的 `reframe=4、causality=5、fairness=5、visuals=5`，只剩 suspense 與 motivation 可動，各值 4 分：

| suspense / motivation | 總分 |
| --- | ---: |
| 4 / 4 | **87** |
| 4 / 5 或 5 / 4 | **91** |
| 5 / 5 | **95** |

**這條階梯上沒有 88、89、90。** 門檻訂在 90，但 90 不在階上，所以實質門檻是 91，而 **91 是能通過的最低一階**。

實際分佈完全吻合：383 筆裡 **87 分 96 次、91 分 113 次**，兩座峰剛好夾著門檻；**90 分只出現 2 次**。所有維度不低於 3 分且總分恰為 90 的組合有 18 種，其中 15 種需要 `reframe=5`（只佔 5.5%），其餘需要某處給 3 分 — 90 分在理論上可達，實務上幾乎不可能。

### 停止條件把質量堆在最低那一階

`autoloop.py`：

```python
PASS_SCORE, FINAL_READERS = 90, 3
passed = (len(valid) == FINAL_READERS
          and all(row["score"] >= PASS_SCORE and row["clear"] for row in valid))
```

加上「已合格的故事不得再修」（`this story already qualified`）與 `RUN_LIMIT = 4`：**改稿改到第一次通過就停**，而第一個通過的階就是 91。

### 這代表什麼

你的兩個懷疑都成立，但成因是設計而非評審行為：**分數確實集中，自動修稿確實在剛好通過時停止**，而兩者相乘的結果就是 92.9% 落在 91。

更值得注意的是衍生的問題：**在通過區間裡，這個「100 分制」只有約三階可用（91／95／96+）**。91 分與 87 分的差距是「某一個維度差一格」。這個數字承載的資訊遠少於它的刻度看起來的樣子，而權重最高的 `reframe` 因為幾乎不變，實際上不提供任何區辨力。

這是量尺的性質，不是市場發現。**同一份稿換一批評審是否還得到相近分數，仍然未知** — 160 筆紀錄對應 160 份相異文字，沒有任何一份被評過兩次。設計與選稿見 [reader-reliability-experiment.md](reader-reliability-experiment.md)。

## 三、90 分 gate：具備篩選能力，但現有資料無法驗證市場預測能力

29 支中 28 支有可追溯評分、全部 `TEXT_MATCHES_MASTER_SOURCE`、全部使用 `story-quality-autoloop/v2`（整個 index 則是混合的：145 筆 v2、15 筆 v1）。這 28 支的最低讀者分數：

| ai_min | 支數 |
| ---: | ---: |
| 91 | 26 |
| 92 | 1 |
| 95 | 1 |

**區間寬度 4 分，應變數變異三個數量級。** gate 是公開前的過濾器，低於 90 的劇本從未被拍成影片公開，所以任何對 ai_min 的係數都是在這 4 分帶內算出來的，無法支持也無法否定它的市場預測力。這與「gate 沒有用」是兩件事 — 160 筆紀錄中 131 筆是 `NEEDS_RETHINK`，它確實篩掉了大量稿件。**篩選能力與預測能力要分開驗證。**

剩下 1 支 26M-B 標 `VERSION_UNVERIFIED`：找不到可核對的凍結文字，且該系譜走六維編輯評分（加權 82／100），與三讀者制不是同一量尺。它不被當成通過，也不被當成未達標，且不進入任何相關係數。

## 四、04-v7 的 201% 要怎麼讀

| 指標 | 時間窗 | 數值 | 量的是什麼 |
| --- | --- | ---: | --- |
| stayed-to-watch | lifetime | 11.1% | 動態刷到後選擇繼續看的比例 → 開場／動態層 |
| 平均觀看比例 | 進階匯出（2026-10-26 至 11-22） | 201.39% | 留下的人看了多久，含重播 → 敘事層 |
| 平均觀看比例 | **D1** | 61.8% | 同上，但只看首日 |

逐秒曲線（`9rt4gNnVGTw-retention-curve.png`，發布至今，平均 1:46／201%）由約 300% 起跌，第 10 秒附近降到約 215%，之後近乎水平。**曲線形狀是人眼讀 PNG 得到的，無法從文字資料核對。**

依你的提醒，**201% 不等於每位留下的觀眾都看了兩遍** — 它是平均值，可能由少數高重播觀眾或部分片段的反覆重播拉高。

V08（208.95%）、V10（106.63%）同樣破百。

> **立場更正**：先前版本寫「這些值不能與未破百的值放在同一欄比較」。那是錯的 — **重播是真實觀看行為，破百是有效數據，應留在主要分析中**。`quality-vs-market.csv` 以 `d1_repeat_play` 標記它們，`correlations.txt` 的主要留存區塊**包含**它們；「去掉破百」只作為敏感度對照輸出，不是認定它們無效。

## 五、兩條留存曲線（n=2，列為假設不列為結論）

| 影片 | 片長 | lifetime 平均觀看比例 | D1 平均觀看比例 | 曲線 | 關鍵線索／揭曉 |
| --- | ---: | ---: | ---: | --- | --- |
| 04-v7 刪除試鏡 | 52.2s | 201% | 61.8% | 前 10 秒 ~300% → ~215%，之後水平 | 21.0s／35.6s |
| V09 生日視訊 | 38.4s | 57% | 59.7% | 持續跌到第 19 秒 ~45%，之後水平 | 17.2s／30.3s |

兩支的流失都集中在關鍵線索之前，抵達中段的觀眾幾乎都看到結尾。支持「線索時機影響留存」這個假設，但 n=2，且這兩支本來就是因為被演算法分發才有足夠觀看數產生曲線，樣本有選擇性偏誤。

## 六、分發集中的程度

old cohort 20 支 D1 總觀看 **2,355**，其中 04-v7、V12、V13 三支合計 2,173，佔 **92.3%**。（n=19 的分析集不含 26M-B，總數 2,320、佔比 93.7%，兩個分母不同。）

其餘 17 支裡有 **14 支 D1 觀看 ≤ 7**；剩下三支是 V09（94）、26M-B（35）、V11（35）。

觀看數 0–7 的影片之間比高下沒有意義，差異幾乎全來自演算法有沒有送流量。**任何「哪一類比較好」的結論，在拿到更多被分發的樣本之前都不成立**，包含 11/25 公開的五支。

## 七、資料缺口

`data-gaps.csv` 由 `build_gaps.py` 從來源推導，共 97 列：

| 狀態 | 列數 | 意義 |
| --- | ---: | --- |
| `CLOSED_NOT_COLLECTED` | 32 | 窗口已關閉但沒有數據 → **現在就能補** |
| `PENDING_WINDOW` | 38 | 窗口尚未關閉 |
| `UNKNOWN_PUBLISH_TIME` | 22 | 只有日期沒有時刻，窗口邊界算不出來 |
| 其他 | 5 | 版本、規約、從未抓取的欄位 |

重點項目：

- **R01–R09 的 D1**：窗口 11/25 01:08–01:16 已關閉，九列仍全空。
- **old cohort 的 D3**：11/24 就已關閉，**先前的手工版本整批漏列**。
- **P02／U02／H02／H03／H04**：`upload-metadata.json` 只有 `observed_visibility_date: 2026-11-25`，沒有時刻，三個窗口全部 `UNKNOWN_PUBLISH_TIME`。
- **WhyNest Lab 十支的 D1**：11/23 到期，`d1.csv` 十列 `data_status=waiting`。
- **`shorts_feed_shown` / `stayed_to_watch_d1_pct`**：欄位存在但 20 支全空，從未抓取。
- **逐秒留存曲線**：全頻道只有 2 支。

## 八、下一輪實驗設計（依你的優先順序）

公開 82–87 分影片的方案**降為第 5 順位候選**，本輪不執行。

驗證分三層：**Reliability**（評審自己穩不穩）→ **Human Validity**（評分合不合真人感受）→ **Market Validity**（品質能不能轉換成留存與收益）。三層目前都未完整驗證，且後一層的結論在前一層成立前沒有意義。

| 順位 | 實驗 | 層級 | 驗證目標 | 前置條件 |
| ---: | --- | --- | --- | --- |
| 0 | **AI 評審穩定性複評** | Reliability | 同稿換評審是否得到相近分數與相同 gate 判定 | 選稿已完成；需你決定 runtime 並授權 |
| 1 | 不同 AI 分數區間的真人盲測 | Human Validity | 評分能否反映真人的理解與娛樂感受 | 無，現在就能做 |
| 2 | 相同故事、不同開場 | Market | 開場是否影響續看意願 | 需要開始抓 `stayed_to_watch` |
| 3 | 相同故事、不同線索時間 | Market | 線索時機是否影響留存 | 需要逐秒留存，等於需要足夠分發量 |
| 4 | 不同故事類型 | Market | 海龜湯 vs 都市怪談 | 目前 3:1:1 且同日公開，樣本不足 |
| 5 | 不同評分區間的公開影片 | Market | gate 的市場預測能力 | 承擔公開品質風險，需 Owner 另行授權 |

**實驗 1 現在就能選稿**：`score-index.csv` 的單一讀者分數涵蓋 72–100，`reader_min` 在 82–87 的紀錄有 **94 筆**，高分帶（≥91 且 cores supported）也充足。真人盲測只讀文字，不製作影片，是目前成本最低、且不需要任何新授權的驗證。

**主要觀察指標**：觀看數是分發的函數，平均觀看比例與逐秒留存較接近內容本身。建議以平均觀看比例為主、觀看數為次，破百單獨標示，並補抓 `shorts_feed_shown` 與 `stayed_to_watch`。

| 你的四維 | 對應欄位 | 現況 |
| --- | --- | --- |
| 故事邏輯 | 三位讀者盲評、cores supported | 已有，但對公開影片無變異 |
| 開場吸引力 | `stayed_to_watch_pct`、`shorts_feed_shown` | 欄位存在，**從未填過** |
| 敘事吸引力 | `avg_pct_viewed`、逐秒留存 | 部分有，曲線僅 2 支 |
| 觀看滿意度 | `likes`、分享、訂閱轉換 | 僅有讚 |

## 九、Review 指出並已修正的問題

| # | 問題 | 處置 |
| ---: | --- | --- |
| 1 | `data-gaps.csv` 仍寫著 04-v7 查無評分紀錄，與 §一 的修正矛盾（手工維護、未同步） | 改由 `build_gaps.py` 從來源產生，並加測試禁止它與 join 結果矛盾 |
| 2 | 「舊 −0.481／−0.409，n=18」無法從交付物重現 | 改為可稽核的 raw 基準 −0.415／−0.410（n=16），並在輸出中保留 raw／valid／去重播三層 |
| 3 | §四 聲明破百不可同欄比較，n=8 區塊卻含 V10 的 106.6% | 新增 `d1_repeat_play` 欄與「去掉破百」敏感度區塊 |
| 4 | n=8 的相異值結構與 1–2 次互動分母未揭露 | 每行加印 `distinct_x`，≤3 自動標註；留存區塊加印最小互動分母 |
| 5 | 離群值只點名不排除，且無敏感度 | 新增去除離群值後的對照區塊；四分位數改為線性內插 |
| 6 | README 寫 n=19，異常那行其實 n=18 | 已更正並說明 V07 缺值原因 |
| 7 | 「其餘 14 支」把 17 支寫成全部 | 已更正 |
| 8 | §五「平均觀看比例」未標時間窗（實為 lifetime） | 表格加上時間窗欄 |
| 9 | 漏引 n=8 區塊最強的 `ai_min ~ 留存` −0.545／−0.577 | 已補上並說明為何仍不可採信 |
| 10 | `d3_status`／`d7_status` 是寫死常數，且 old cohort 的 D3 其實 11/24 就關閉 | 改為從發布時間推導，old cohort D3 已進缺口清單 |
| 11 | `missing=` 只數應變數缺值，造成 `n=18 missing=0` 自相矛盾 | 改為分開輸出 `missing_x` 與 `missing_y` |
| 12 | `TEXT_MATCHES_PUBLISHED` 名稱宣稱超過實際核對 | 更名 `TEXT_MATCHES_MASTER_SOURCE` 並說明核對範圍 |
| 13 | `gate_state` 把 cores 未記錄當成未達標 | 新增 `CORES_NOT_RECORDED` |
| 14 | 「29 支公開影片」讀起來像全集 | 加註範圍，並說明 11/25 的五支不在表內 |
| 15 | 92.3% 的分母未說明 | 已標明 old cohort 20 支，並附 n=19 分析集的 93.7% |
| 16 | 測試在缺檔時 skip，「全過」可能什麼都沒測 | 已於執行說明中寫明 |

### Owner 第二輪 review 指出並已修正（2026-11-26）

| # | 問題 | 處置 |
| ---: | --- | --- |
| 17 | `gate_state()` 只看最低分與 cores，沒檢查讀者是否滿三位，也沒檢查每位讀者的 `clear` | 改為逐字對應 `autoloop.py` 的契約：`len(valid)==3 and all(score>=90 and clear)` 加上 cores supported。索引新增 `readers_clear`／`all_readers_clear` 欄 |
| 18 | 128／160 筆評分證據只存在本機 `artifacts/`，他人無法驗證 | 索引每列新增 `evidence_sha256`（該 `final-report.json` 的檔案雜湊），連同 `story_sha256`、來源 kind／分支／commit／路徑一併落版 |
| 19 | 來源讀取失敗時程式回傳空集合，會被誤讀為沒有缺漏 | `build_gaps.py` 改為產生 `SOURCE_UNAVAILABLE` 列並附失敗原因 |
| 20 | D3／D7 沒有資料匯入介面，每加一個欄位就要改分析程式 | 新增 [market-schema.json](market-schema.json)，`build_table.py` 由 schema 產生市場欄位；新增欄位只需改 schema |
| 21 | 破百的平均觀看比例被當成無效值排除 | **立場更正**：破百是有效數據，保留在主要分析，排除只作敏感度對照（見 §四） |

其中 #17 目前**不改變這 28 支的判定**（寬鬆檢查與完整契約的通過集合都是 29 筆），但漏洞是真的：索引裡有 3 筆只有 1–2 位讀者、66 筆存在未標 clear 的讀者，日後擴充資料就會分類錯誤。

Review 另確認：pearson／spearman／ranked 三個函式的實作正確（獨立重算 10 組皆吻合至小數三位）；輸出可逐位元重現；三個 `.py` 無任何網路呼叫；`D:\s2v-gp` 除本目錄外無任何變更（`git diff` 對基底分支為空）。

## 十、Market Feedback Loop 的整合構想（本輪不實作）

每一環都存在，但彼此以人工搬運相連。把它接成迴圈需要的是**識別與契約**，不是新模型。

1. **內容主鍵**（本輪完成一半）：story SHA-256 貫穿劇本 → 母片 → video id → 市場數據。沒有它任何自動回饋都會配錯，R04 就是現成例子。
2. **市場數據落地為結構化紀錄**：固定 schema，每個時間窗一列，每格都有 `status`（collected / pending_window / closed_not_collected / unknown_publish_time），讓缺漏本身也是資料 — `data-gaps.csv` 已是這個形狀的雛形。
3. **Analyzer 只產出假設，不改規則**：依你的指示 AI 不自動調整 gate。輸出應是「可驗證假設清單」，每條附依據欄位、有效樣本數、相異值結構、競爭解釋與建議的驗證設計。`correlations.txt` 是這種輸出的雛形。
4. **Experiment Planner 排發布設計**：需要的是時段、長度、類型的平衡，而不是更多影片。以 92.3% 觀看集中在三支的現實，每多發一支未經設計的影片，對學習的邊際貢獻接近零。
5. **最後才把規則寫進 Skill**：等某條假設在真人盲測與市場數據上都站得住，再寫進 `shorts-viewer-gate`。在那之前規則留在實驗紀錄裡。

## 十一、本輪沒有做的事

- 沒有連線 YouTube、沒有讀取即時觀看數、沒有登入 Studio。
- 沒有修改 P01／U01／H01，沒有製作新影片，沒有改動任何已公開影片。
- 沒有新增或調整品質 gate，沒有改寫 `gates.md`、`AGENTS.md` 或任何 skill。
- 沒有呼叫付費 API。
- 沒有合併任何分支。
