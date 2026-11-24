# CluePause genre pilot — staged exploration

日期：2026-11-24（Asia/Taipei）。狀態：**PLANNING + SCRIPTS ONLY / HUMAN_TEST_PENDING**。

本目錄依 Owner 本次提供的 Issue #18 修訂摘要規劃，沒有讀取或改寫線上 issue。起點為 PR #19 head `a5be360edfbb2b012ae5e373d6a5c01315f1b8f6`，分支 `codex/cluepause-genre-pilot-20261124`。本次不 commit。

## 要回答的決策

**CluePause 應該是純海龜湯頻道，還是更廣的、由好奇心驅動的懸疑短故事頻道？**

這是與 puzzle 基線工作並行的小規模探索，不取代基線。Owner 優先順序為 `uncanny_mystery`，其次 `urban_horror`；puzzle 是對照題型。三個 series code 是研究標籤，不是 Episode v1 合約變更。

| series code | 對外系列工作名 | Round 1 草稿 |
| --- | --- | --- |
| puzzle | Solve It | [The Thread Under the Scale](puzzle.md) |
| uncanny_mystery | Something's Wrong / 日常詭異事件 | [The Shoes That Stayed Wet](uncanny_mystery.md) |
| urban_horror | After Dark / 都市怪談 | [The Last Two Words](urban_horror.md) |

目前授權僅限本目錄的計畫、文字腳本、分鏡註記與測試設計。沒有渲染、TTS、圖片／影片生成、付費 API、YouTube 操作或發布。下述各輪都是**未執行的條件式計畫**；製作、招募／私人試看、私人上傳等未獲本次執行授權。私人試看可使用日後另行授權的本機成片，不要求上傳 YouTube。

## 分階段計畫

### Round 0 — 目前文字交付

先審 uncanny_mystery，再審 urban_horror，puzzle 維持既有流程。每篇為原創候選，`rights_status = pending_verification`，均未取得權利 gate、品質 gate 或真人 gate 的 PASS。完成原創性比對、權利紀錄、腳本審核及所需 Owner 授權，才可製作。35–45 秒是文字估時，非實測片長。

### Round 1 — 三支私人 pilot

只規劃 **3 支：每類 1 支**。同為 9:16、英文旁白、繁中字幕，35–45 秒。每支招募 **3–5 位從未接觸該故事任何版本的真人**，優先採每支 5 人，依 [first-view-protocol.md](first-view-protocol.md) 分成不同人的 Test A 與 Test B。五人配置為 A 兩人、B 三人；不讓看過 A 的人充當 B 的首次觀看者。三至四人的縮小配置只能作診斷，資料不足可直接記 INCONCLUSIVE。

私人測試只回答「這個故事是否清楚、有足夠吸引力，值得再做公開測試」。它不能證明題材需求、推薦流量、訂閱轉換、跨故事穩定性或另一個頻道的可行性。一類一支也無法區分故事本身與 genre 的效果。

依 [gates.md](gates.md) 逐支記錄修稿需求與判定。uncanny_mystery / urban_horror 的新標準全為 PENDING，須先核定才可據以宣告通過。puzzle 三位讀者各至少 90 的 gate 不變；本輪小樣本不能冒稱通過既有五人完整首看門檻。若要依既有門檻判定，需另行安排未曝光的完整首看樣本（見 protocol），未滿即保持待驗。**任何未通過或證據不足的 pilot 都不自動升級公開。**

### Round 2 — 僅於通過後考慮六支公開探索

只有三支各自完成適用 gate，且 Owner 另行明確核准下一階段，才考慮 **每類 2 支，共 6 支公開探索**。可由每類通過的 pilot 作第一支，再各寫一篇不同故事；不是自動再做六支或十二支。三篇第二故事尚未撰寫，也須各自審核、權利查核及授權。若有一類未通過，先停止升級；不以其他類補數。

預先固定以下相對日與時段；D0 實際日期須由 Owner 核准後才填。以下為提案，沒有建立排程。

| 相對日 | 預定時間（Asia/Taipei） | 類別／樣本 |
| --- | --- | --- |
| D0 | 20:00 | uncanny_mystery 1 |
| D1 | 20:00 | puzzle 1 |
| D2 | 20:00 | urban_horror 1 |
| D3 | 20:00 | uncanny_mystery 2 |
| D4 | 20:00 | puzzle 2 |
| D5 | 20:00 | urban_horror 2 |

跨日、交錯類型、預先固定時間，是為了讓結果較容易解讀並減少臨時挑時段；**不是 YouTube 規則，也不保證推薦**。星期、順序、流量來源與題目差異仍會干擾；這不是因果實驗。若時程須變動，保留原計畫、理由與實際公開時間，勿事後改寫預註冊安排。

**每個公開步驟都需要另一次明確 Owner 授權**，對應該片最終版本、metadata、video ID、可見性與時間；本計畫、私人 PASS、品質分數或前一支的授權均不包含下一支。不能以批次計畫自動公開或排程。依 AGENTS.md，真正執行對外動作時，其 Owner 授權與逐片結果須在動作當天（Asia/Taipei）commit 並 push；若未另獲允許完成該落版控義務，不執行對外動作。本次「不 commit」與「不做 YouTube 操作」一起遵守。

## 假設、觀察與推論邊界

| 假設（尚未證明） | 預定觀察 | 不能由此宣稱 |
| --- | --- | --- |
| uncanny_mystery 能用異常＋公平線索吸引觀看 | A 能自行描述異常；B 有合理首猜，揭曉重解異常 | 私人喜歡代表市場有需求 |
| urban_horror 能以不安與敘事兌現吸引觀看 | B 能說出衝突、不安起點、結尾感受及續看意願 | 沒猜中唯一答案代表失敗；害怕就等於訂閱 |
| 非善意誤會的 puzzle 可提供更有差異的對照 | 既有 puzzle gate；B 重述證據與因果 | 單篇表現代表 29 支基線的所有反轉類型 |
| broader suspense 值得留在同一頻道探索 | 六支同窗 D1/D7 的個片結果、方向是否重複 | 六支可證明 genre 因果、長期需求或需要第二頻道 |

「29 支既有公開片以 benevolent_misunderstanding 為主」是本次 Owner 提供的背景，本輪未獨立查核其數量或分布。puzzle 草稿刻意改用 `object_function`。

## 預定公開觀察：D1 / D7

每支依**實際公開時刻**算 D1 累積 0–24 小時與 D7 累積 0–168 小時，不能拿某片首日與另一片第七天相比。所有影片分開列兩個窗；D7 包含 D1，兩者不是獨立樣本。只比較同窗數字，並保留時區、抓取時間、報表可提供的實際時間範圍及流量來源。若 Studio 無法給精確同窗，記缺項／範圍差異，不以日曆日值假裝 24 小時值。

| 每片每窗必填 | 記錄方式 |
| --- | --- |
| stayed-to-watch | 原始百分比；可得時附對應分子／分母與 Shorts 動態曝光背景。缺分母明記未提供 |
| engaged views | 該片該窗原始計數，非全頻道同期總數 |
| avg % viewed | 原始百分比及實際片長，保留報表標籤；重播可能影響數字，不擅自截為 100% |
| subscribers | 該片該窗帶來的訂閱數；可得則分 gained / lost / net，缺值不寫 0；不可拿頻道總增量當單片歸因 |
| 條件與缺項 | 實際公開時間、版本、流量來源／曝光、延遲、報表缺項、授權紀錄索引 |

空白紀錄列：`story_id | genre | video_id | revision/hash | public_at | D1/D7 | actual_window | extracted_at | stayed_to_watch + denominator_if_available | engaged_views | avg_percent_viewed | subscribers_gained/lost/net | traffic_context | missing | observation`。目前全部 **NOT_COLLECTED**，不是零。

報每支原始值，必要時附每類兩支的範圍，不只報百分比增幅或綜合分數。曝光極少、兩支方向不一致、字幕／片長差異、來源混雜或缺值時可判 **INCONCLUSIVE**。不預設成功數字，不靠一支爆量宣布轉型；公開資料最多支持下一個小測試的假設，最終定位由 Owner 決定。

## 明確延後

- 12-video batch；本輪不生產 12 支。
- 第二頻道、擴產、自動公開或排程。
- 任何對既有 puzzle 90 分 gate 的修改。
- 正式引擎／Episode v1／CLI／SQLite 變更與一般 M1 擴建。

## 驗收紀錄

工程／文件驗收與市場驗收分開記錄。此處不是 Episode manifest，不登錄正式 pipeline。2026-11-24 的檢查基準為 HEAD `a5be360edfbb2b012ae5e373d6a5c01315f1b8f6`；六份文件仍為未提交內容，該 SHA 不包含這些新檔。市場驗收為 **HUMAN_TEST_PENDING / PUBLIC_DATA_PENDING**。

| 工程／文件命令（PowerShell） | 實際結果及限制 |
| --- | --- |
| `git branch --show-current` / `git rev-parse HEAD` | 指定分支與上述完整 SHA 相符；未 commit |
| `uv sync --locked` | 無法執行：PATH 找不到 uv；未完成 Python 依賴驗收 |
| `uv run --locked pytest` | 無法執行：PATH 找不到 uv；沒有測試通過的主張 |
| 在 `video/` 執行 `npm.cmd ci` | exit 1：使用者 npm-cache 讀取 EPERM；另有 Node 24.13.0 不符專案 Node 22 範圍的警告。未重建成功 |
| 在 `video/` 執行 `npm.cmd run typecheck` | exit 1：找不到 tsc；未完成型別驗收 |
| `git diff --check` / `git diff --name-only` | exit 0、無既有 tracked 檔變更；前者不涵蓋新 untracked 檔，不能拿來宣稱新文件檢查通過 |
| `git status --short` | 只有本目錄為 untracked；未改 src、video、治理契約或既有 gate |
| 下方 PowerShell here-string 經 `node` 的本機靜態檢查 | 另檢查新文件：6 個 Markdown、相對連結、待驗標示、七段連續時間與繁中欄位；檢查方式及最終結果如下 |

文字估時結果：puzzle 77 個英文詞、42 s（含停頓平均 110.0 詞／分）；uncanny_mystery 85 詞、43 s（118.6）；urban_horror 78 詞、44 s（106.4）。這是詞數與目標秒數的算術，不是語音、閱讀速度或成片驗收。

從 repo 根目錄可重跑文件檢查（不產生媒體、不呼叫服務）：

```powershell
@'
const fs = require('fs'), path = require('path');
const root = path.resolve('experiments/cluepause/genre-pilot-20261124');
const files = fs.readdirSync(root).filter(n => n.endsWith('.md'));
let errors = [];
for (const name of files) {
  const body = fs.readFileSync(path.join(root, name), 'utf8');
  if (!body.includes('HUMAN_TEST_PENDING')) errors.push(name + ': human status');
  const prose = body.replace(/\x60{3}[\s\S]*?\x60{3}/g, '');
  for (const m of prose.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
    if (!/^(https?:|#)/.test(m[1]) &&
        !fs.existsSync(path.resolve(root, m[1].split('#')[0]))) errors.push(name + ': link ' + m[1]);
  }
  if (body.split(/\r?\n/).some(line => /[ \t]+$/.test(line))) errors.push(name + ': trailing whitespace');
  if (!['puzzle.md', 'uncanny_mystery.md', 'urban_horror.md'].includes(name)) continue;
  const rows = body.split(/\r?\n/).filter(line => /^\| \d+[\u2013-]\d+/.test(line));
  let end = 0, words = 0;
  for (const row of rows) {
    const c = row.split('|'), m = c[1].match(/^\s*(\d+)[\u2013-](\d+)/);
    if (+m[1] !== end || +m[2] <= end) errors.push(name + ': timeline');
    end = +m[2];
    if (!/[\u3400-\u9fff]/.test(c[3])) errors.push(name + ': ZH line');
    words += (c[2].match(/[A-Za-z]+(?:['\u2019][A-Za-z]+)*/g) || []).length;
  }
  if (rows.length !== 7 || end < 35 || end > 45) errors.push(name + ': beats/duration');
  if (!body.includes('pending_verification')) errors.push(name + ': rights');
  console.log(name + ': ' + rows.length + ' beats, ' + end + 's, ' + words + ' words');
}
console.log(files.length + ' Markdown files; findings: ' + errors.length);
errors.forEach(e => console.log(e));
process.exitCode = errors.length ? 1 : 0;
'@ | node
```

上段原樣重跑結果為 exit 0：`6 Markdown files; findings: 0`；三稿各 7 beats，秒數／詞數依序為 42/77、43/85、44/78。這項檢查只核對結構與連結，沒有自動判斷故事品質、原創性或字幕可讀性。由於只新增文件，未執行狀態機、SQLite 回滾、正式 Episode 合約、媒體或上傳操作驗證；不宣稱引擎驗收完成。未變更治理契約或框架版本，未執行框架更新或完整治理驗收。

未驗證：真人理解與偏好、外部原創性相似查核、獨立品質分數、實際旁白／字幕長度、手機畫面與聲音、任何 D1/D7 或需求結果。權利尚未 approved，無製作或公開授權。
