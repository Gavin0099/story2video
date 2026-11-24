# v3 讀稿批次：九位隔離 AI 讀者盲讀結果（2026-11-24）

**驗證層級**：Story Quality Gate（劇本層）。本輪讀的是描述畫面與聲音的文字材料，不是實際影片；不是分鏡審查，也不是 Shorts Viewer Gate。真人首看：`HUMAN_TEST_PENDING`。本輪版本的分鏡、媒體／成片與市場驗收均未完成。

## 受測版本

- 劇本及讀者材料凍結於 `7015cbc6a13955b7b57b5b6975a79e6543d2a1cc`：P01 為 [puzzle-v3.md](../puzzle-v3.md)，U01 為 [uncanny_mystery-v3.md](../uncanny_mystery-v3.md)，**H01 為 [urban_horror-v2.1.md](../urban_horror-v2.1.md)**。`readers-v3` 是批次名稱，不表示 H01 已改成 v3。
- 受測材料為本目錄 `<series>/part1-setup.md`、`part2-reveal.md`；執行工具為 [readers/run_blind_readers.sh](../readers/run_blind_readers.sh)，已提交於 `ec45e80afda757df6047f4118acb26f696c174a9`。本次核對上述三稿及六份 packet 從凍結 SHA 到該 HEAD 無差異。
- 原稿開頭「尚未做新版讀者測試」是凍結當時的狀態；本報告補記其後已完成的讀稿，不改寫受測稿。v1／v2 分數、影音 QA 與 P01 v1 私人上傳（`YX8NJR966As`）不移轉到本輪。
- 本報告與 raw 匯入檔仍未提交；上列 HEAD 不包含本次新增證據。Owner 本次要求不 commit。

## 讀者流程與證據邊界

- 每篇三位讀者 A、B、C，共九位，使用 repo 工具在 repo 外的各自新資料夾執行。依工具流程，每位以獨立 Codex CLI session 先讀 setup，寫 `guess.md`，工具記錄 `guess.sha256` 及 `session-id.txt`，才放入 reveal，再續接同一 session 寫 `review.md`。工具會檢查原先記憶中的 guess 雜湊、manifest 及續接 session 一致；任一失敗會回傳非零。
- 工具預設模型／推理為 `gpt-6.1-sol`／high。Owner 提供九場已完成的執行事實；本次只整理既有結果，未重跑讀者，也未讀取或匯入 logs。四種 raw 檔本身沒有模型／推理參數或完整執行軌跡，不能單靠它們獨立證明實際參數、歷史揭曉時序或讀者未越界。隔離是資料夾與提示隔離，沒有 OS 層讀取屏障。
- 海龜湯與日常詭異：揭曉前問主猜與信心、替代解、改變理解的線索、關字幕理解與續看；揭曉後問解釋是否完整、新增必要設定、關鍵因果缺陷、反轉感受、兌現與 0–100 總分。都市怪談改問威脅、規則、預期、不安及緊張感；**沒有要求單一答案或信心百分比**，不補造數值。
- 評分面向沿用工具提示；不是已有逐項權重的 90 分量表。下表使用讀者明示的 overall，沒有重算各面向平均，也沒有由整合者改分。
- 本次僅匯入每位的 `guess.md`、`review.md`、`guess.sha256`、`session-id.txt`，共 36 檔；不匯入來源的 part1／part2 副本或 logs。匯入前掃描無個人路徑，逐位元複製後核對來源與目的 SHA-256 相同；九份現存 guess 均符合其 lock manifest，九個 session UUID 互異。
- `guess.sha256` 記錄原始位元組；本次未改換行。repo 的 `.gitattributes` 指定 LF，日後入 Git 若發生正規化，應保留原始 lock 並交代位元組差異，不可重寫 lock 冒充讀者當時產物。

## 結果

下表數字及判語取自各人的原始回覆；長句以忠實摘要表示，英文引號保留原判語。每位連結到揭曉後回覆，同資料夾的 `guess.md` 是揭曉前證據。關鍵缺陷欄保留讀者分歧，不把「沒有因果洞」等同「沒有任何關鍵缺陷」。

| 劇本 | 讀者 | 揭曉前主猜／預期（信心） | 續看 | 揭曉新增必要設定 | 關鍵缺陷 | 反轉感受 | 兌現 | 分數 |
|---|---|---|---|---|---|---|---|---|
| P01 海龜湯 v3 | [A](raw/puzzle/A/review.md) | 老闆用腳拉連到秤盤的線，抬高讀數（65%） | 4/5 | Yes：鞋尖線圈、砝碼由架子支撐且吊環空著；視為預先暗示過的確認 | none；另指出懸念弱、揭曉確認主猜，未升為 critical | “Ordinary, with a satisfying visual confirmation.” | 4/5 | 81 |
| | [B](raw/puzzle/B/review.md) | 老闆用腳向下拉線加重讀數（65%） | 4/5 | Yes：鞋與線的連接、排除砝碼供力的支撐；合理確認細節 | none | “Ordinary for me.” | 4/5 | 80 |
| | [C](raw/puzzle/C/review.md) | 老闆用腳拉線、增加秤盤向下力（65%） | 4/5 | Yes：鞋尖線圈、架子及空吊環；合理鋪陳的揭曉 | none | “Ordinary, with a satisfying visual explanation.” | 4/5 | 84 |
| U01 日常詭異 v3 | [A](raw/uncanny_mystery/A/review.md) | 澆水系統的管線或櫃內接頭漏水（70%） | 4/5 | No necessary new setup；既有接頭的裂縫與運轉示範是新資訊，六點時刻非必要 | “None in the causal chain.”；同節另列 “Early-answer weakness”，稱為 suspense defect，非 logic hole | “Ordinary.” | 4/5 | 77 |
| | [B](raw/uncanny_mystery/B/review.md) | 澆水管漏水，可能是櫃內淡色有紋接頭（70%） | 4/5 | No new prerequisite equipment or route；裂縫是公平揭曉細節 | “Early answer exposure / heavy signposting”；“Critical logic holes or impossible actions: none.” | “Ordinary.” | 4/5 | 72 |
| | [C](raw/uncanny_mystery/C/review.md) | 澆水系統在櫃內管線或接頭漏水（65%） | 4/5 | None；裂縫是既有設備的故障，精確時刻非必要 | none；另列明顯預示與未解釋的外部水痕，未升為 critical | “Ordinary.” | 4/5 | 78 |
| H01 都市怪談 v2.1 | [A](raw/urban_horror/A/review.md) | 預期 “Don’t come in” 被截成 “come in”（未問／未提供百分比） | 4/5 | No necessary new rule；新增播放／重播行為非開門所必需 | critical 節列答案過度預示、致命回話缺乏立即誘因；“No confirmed rule break or unearned ending.” | “ordinary, with a solid audiovisual payoff” | 3/5 | 80 |
| | [B](raw/urban_horror/B/review.md) | 同樣預期否定邀請被截成 “come in”（未問／未提供百分比） | 4/5 | None；播放／重播非必要新條件 | “The central reveal is heavily telegraphed.”；無確定規則矛盾，另有動機弱點 | “ordinary, but earned” | 3/5 | 78 |
| | [C](raw/urban_horror/C/review.md) | 同樣預期 “Don’t come in” 的截字陷阱（未問／未提供百分比） | 4/5 | No necessary new rule；播放／重播不是開鎖所需的新規則 | none；預測性是弱點，但不把清楚規則本身列為 critical spoiler | “ordinary, with effective execution” | 3/5 | 79 |

## 判定

- **P01 海龜湯：未通過**既有 Story Quality Gate（三位各 ≥90，且關鍵缺陷 0）。本輪 A／B／C 為 **81／80／84**，三位 critical 均為 none，但三位都未達 90；零關鍵缺陷不能抵銷分數不足，也不能用平均或相對 v2 的進步代替門檻。
- **U01 日常詭異：探索性審查完成，77／72／78；正式 Gate 仍 `PENDING`。** B 在 critical 節明列答案外露；A 認為無因果洞但有懸念缺陷，C 列 none。三位都說沒有必要的新設備／路徑設定；這不代表正式標準已核定或通過。
- **H01 都市怪談：探索性審查完成，80／78／79；正式 Gate 仍 `PENDING`。** A、B 在 critical 節提出問題，C 列 none；三位均未發現已證明的規則破壞。不能延用 v2「三位無關鍵缺陷」，也不能套用 puzzle 的 90 分門檻宣布恐怖類型失敗。
- 三篇皆維持 `HUMAN_TEST_PENDING`。本輪沒有任何製作、上傳、公開或市場驗收通過的判定；[gates.md](../gates.md) 的新 genre 草擬準則未因此獲核准。權利查核亦不在本輪完成範圍。

## v2 → v3 批次比較

v2 基準為 [results-v2.md](../readers-v2/results-v2.md) 及其 raw（劇本凍結 `933f5427fe43a3f726a94a6625b08aba8587a808`）。以下 A／B／C 是各輪本地標籤，**不是同一讀者追蹤配對**；列序差值只供描述，不能當作受控的修稿效果。H01 的新版實際為 v2.1。

| 劇本 | 分數（A／B／C；範圍） | 揭曉前信心／預期 | 關鍵缺陷比較 | 支持的判讀 |
|---|---|---|---|---|
| P01 v2 → v3 | 75／67／71（67–75）→ 81／80／84（80–84） | 原先「用線向下拉秤」92／88／92% → 精確腳拉機制 65／65／65%；仍全為主猜，砝碼替代解各 30% | v2 三位均列揭曉前答案外露 → v3 三位均 none，仍描述廣義拉力原理早已明顯 | 分數較高、明示信心較低；主猜粒度已改，不能把信心差當成精確可比的改善幅度。仍無有趣反轉或 ≥90 證據 |
| U01 v2 → v3 | 66／72／70（66–72）→ 77／72／78（72–78） | 定時澆水軟管漏水 90／85／88% → 櫃內管／接頭漏水 70／70／65%；仍全為主猜，花盆溢水替代解 25／25／30% | v2 三位列答案外露 → v3 B 明列；A 保留 early-answer weakness，C 為 none；不能統一計成零缺陷 | 新版說明水如何流到鞋底及櫃底滴出，三位都接受既有接頭故障為合理揭曉；反轉仍普通，外部舊水痕未交代 |
| H01 v2 → v2.1 | 83／80／80（80–83）→ 80／78／79（78–80） | 兩輪三位均預測到確切的否定邀請截字陷阱；兩輪皆未問／未提供信心百分比 | v2 三位 none → 新版 A 列過度預示及回話誘因弱、B 列過度預示、C none；無已證明規則矛盾 | 續看由三位 5/5 → 三位 4/5；兌現由 4／4／3 → 3／3／3。這輪未顯示刪改讓讀者更投入，不能推成 genre 趨勢 |

補充：P01 的新增必要細節由 v2 的秤盤綁點改為本輪的鞋尖線圈與砝碼支撐；三位均接受為已鋪陳的確認，不能因 critical 為 none 而改寫成「無新設定」。U01 v2 三位將接頭裂縫列為新增必要設定，本輪三位把已露出的接頭之故障視為揭曉細節，並非必要新設備／路徑；這是讀者判語的變化，不表示揭曉前已看見裂縫。

## 仍存在的共同缺陷

1. **仍是確認主猜，多於推翻原理解。** P01 三位主猜腳拉、U01 三位主猜內部漏水、H01 三位預測精確字詞陷阱。P01／U01 信心下降，但六位仍稱 ordinary；H01 也都是 ordinary 的兌現。不能把更有猶豫直接當成反轉成功。
2. **線索支持因果，同時收窄懸念。** P01 的剪線降讀數和可見秤盤綁點，先交代了外加拉力，只剩由誰供力；U01 的內部接頭反覆露出，再加水源及 timer，仍直接指向答案；H01 的「最後兩字＋邀請開門」已提供完整陷阱。讀者對何時升為 critical 有分歧，不能替他們抹平。
3. **替代解的排除與揭曉細節仍要分開檢查。** P01 的砝碼替代解由最後才看到的架子與空吊環排除；讀者接受公平，但不覺得理解被大幅翻轉。U01 的乾紙排除了當次花盆溢水，卻未說明原來的白水線及櫃背乾痕；三位都提及，不能寫成所有線索均已解釋。
4. **H01 的壓力發展仍有平台。** 三位都指出規則解說令動作放慢、結尾 35–39 秒的抵門／重播沒有新發展；A、B 另質疑已知母親在屋內且懂得閉嘴的 Nia，為何恰好說出那句話。這不是已證明的門移動或超自然規則矛盾。

## 類型解釋（假設，未驗證）

- 觀察：新版 P01／U01 的主猜信心較 v2 低、分數範圍較高；H01 兩輪都被猜中陷阱，本輪續看、兌現及分數較低。
- **假設**：物理懸疑加入可成立的替代路徑，可能保留「等待驗證」的興趣，卻還不足以帶來有趣的理解改變。都市怪談可能需要角色選擇與壓力逐步改變，單靠猜中的語言陷阱仍不足。這些都是下一輪可測的編輯假設，不是本輪證明的因果，也不是 genre 勝負。
- 限制：每類只有一篇、每版三位 AI；模型參數未由這四檔獨立確認，沒有真人、隨機分派或同版重複測試。分數及 critical 分類含主觀差異，跨類提示亦不同，不能據此推論真人留存、需求、頻道定位或市場表現。

## 下一輪修改方向（候選，尚未執行）

- P01：優先檢查「剪線＋秤盤連接」是否已把真正問題縮小成找拉力來源。考慮讓最初合理的解讀在揭曉時確實改變，而不只把砝碼換成腳；仍須保留可追溯的因果線索，不能靠遮掉必要資訊增加難度。
- U01：減少對同一接頭的重複強調，保留可辨認水路；讓乾紙實驗改變觀眾理解，而非只驗證已占優勢的答案。交代或移除外部舊水痕，避免裝飾性誤導未收束。
- H01：補強角色失言的立即情境與心理誘因，檢查規則是否必須連續講九秒；釐清 “LATCH: SAVED CONSENT” 是規則還是狀態。讓最後抵門階段增加後果或選擇，而非只延長重播。可預測性是否妨礙恐怖效果仍需按敘事與真人反應檢查，不另設猜中即失敗規則。
- 若獲後續改稿授權，另凍結版本，再用新隔離讀者重評；不沿用分數、不降低 P01 門檻、不事後替 U01／H01 創建數字門檻。本次沒有改稿或啟動新讀者。

## 工程／文件驗收與未驗證範圍

驗收基準：分支 `codex/cluepause-genre-pilot-v3-20261124`，HEAD `ec45e80afda757df6047f4118acb26f696c174a9`；本次新增檔案未提交。工程檢查與劇本判定分開，工程成功不會使 Story Quality Gate 通過。

| 命令／檢查 | 結果與限制 |
|---|---|
| `git branch --show-current`、`git rev-parse HEAD` | 指定分支及上述 HEAD 相符；未 commit |
| `git diff 7015cbc6 HEAD --`，後接三份受測稿及 `readers-v3` 路徑 | 無差異；只證明凍結稿與本次 HEAD 一致，不代替執行歷史 |
| PowerShell 匯入：逐檔 `Copy-Item`、來源／目的 `Get-FileHash -Algorithm SHA256`、比對 lock 與 session | PASS：36 檔位元組相同，9 份 guess 符合原 lock，9 個唯一 UUID；未匯入 packet 副本或 logs |
| `uv sync --locked`、`uv run --locked pytest` | 無法執行：PATH 找不到 uv；未宣稱 Python 工程驗收通過 |
| `video/`：`npm.cmd ci --cache ..\artifacts\npm-cache` | exit 1：下載 TypeScript 套件遭 `EACCES`；Node 24.13.0 另超出專案 Node 22 範圍。未完成依賴重建，未改套件契約 |
| `video/`：`npm.cmd run typecheck` | exit 1：找不到 `tsc`；未完成型別驗收 |
| 本報告下方 PowerShell 靜態核對 | PASS：36 raw、9 hashes、9 unique sessions、無個人路徑、報告連結／空白核對通過；不自動判斷故事品質 |
| `git diff --check`、`git status --short` | diff exit 0；狀態為本輪 raw／報告新增與必要的兩份 memory 審查紀錄更新。diff 不涵蓋 untracked 內容，另以靜態核對補足；未 commit |

可在 repo 根目錄重跑本輪匯入後的文件／raw 核對（不需來源個人路徑）：

```powershell
$ErrorActionPreference = 'Stop'
$root = Join-Path (Get-Location) 'experiments/cluepause/genre-pilot-20261124/readers-v3'
$raw = Join-Path $root 'raw'
$names = @('guess.md', 'review.md', 'guess.sha256', 'session-id.txt')
$ids = @()
$count = 0
foreach ($s in @('puzzle', 'uncanny_mystery', 'urban_horror')) {
  foreach ($r in @('A', 'B', 'C')) {
    $dir = Join-Path $raw "$s\$r"
    if ((Get-ChildItem -LiteralPath $dir -File).Count -ne 4) { throw 'Unexpected files' }
    foreach ($name in $names) {
      $file = Join-Path $dir $name
      if ((Get-Item -LiteralPath $file).Length -eq 0) { throw 'Empty raw file' }
      $body = [IO.File]::ReadAllText($file)
      if ($body -match '(?i)([A-Z]:[\\/]|/(?:Users|home|mnt/[a-z])/)') { throw 'Personal path' }
      $count++
    }
    $hash = (Get-FileHash -LiteralPath (Join-Path $dir 'guess.md') -Algorithm SHA256).Hash.ToLowerInvariant()
    $lock = [IO.File]::ReadAllText((Join-Path $dir 'guess.sha256')).Trim()
    if ($lock -cne "$hash  guess.md") { throw "Guess mismatch: $s/$r" }
    $sid = [IO.File]::ReadAllText((Join-Path $dir 'session-id.txt')).Trim()
    if ($sid -notmatch '^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$') { throw 'Invalid UUID' }
    $ids += $sid
  }
}
if ($count -ne 36 -or (Get-ChildItem -LiteralPath $raw -File -Recurse).Count -ne 36) { throw 'Raw count' }
if (($ids | Sort-Object -Unique).Count -ne 9) { throw 'Duplicate sessions' }
$report = [IO.File]::ReadAllText((Join-Path $root 'results-v3.md'))
$prose = [regex]::Replace($report, '(?s)```.*?```', '')
foreach ($m in [regex]::Matches($prose, '\[[^\]]+\]\(([^)]+)\)')) {
  if (!(Test-Path -LiteralPath (Join-Path $root $m.Groups[1].Value))) { throw 'Broken report link' }
}
if ($report -match '(?m)[ \t]+\r?$') { throw 'Report trailing whitespace' }
'PASS: 36 raw files; 9 hashes; 9 unique sessions; no personal paths; report links/whitespace'
```

**市場／真人驗收**：`HUMAN_TEST_PENDING / PUBLIC_DATA_PENDING`；未收集，不記為零或 PASS。未驗證實際鏡頭能否呈現必要細節、手機字幕、音效／旁白、成片理解、原創性外部查核、真人興趣及 D1／D7。未改動正式引擎、Episode v1、SQLite、治理契約或框架版本；未做媒體生成、上傳或發布，也未宣稱完成完整工程或治理驗收。
