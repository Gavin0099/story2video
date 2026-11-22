# story2video — AI 自動化影片製作與 YouTube 市場驗證計畫

> 版本：v1.0（2026-11-20）
>
> **最後更新**: 2026-11-20
>
> **Owner**: Gavin0099
>
> **Freshness**: Phase (30d)
>
> 專案目前範圍為 M0（S2V-001～002）。本機驗收指令見 [README.md](README.md)。
>
> 開發治理採用固定版本的 AI Governance Framework submodule，為開發治理用途的依賴例外。
>
> 核心策略：**先證明可以做出值得觀看的原創影片，再自動化擴產；先驗證市場，再追求被動收入。**

---

## 0. Executive Decision／核心決策

### 2026-11-22 WhyNest Lab 公開首日驗證

Owner 明確授權 WhyNest Lab 原三支科普 Shorts 轉為公開，再補十七支達標影片，總數二十。新片沿用兩位獨立理解度評閱各至少 85，以及事實、圖解與成片驗收。逐支達標才上傳與公開。依 Owner 隨後的語言回饋，圖解文字採英文，提供可切換的英文與繁中字幕。原三支維持原始檔與影片 ID。統計按實際公開時間分別看首 24 小時，記錄於 `experiments/science-shorts/public-20-20261122/`。此增量授權限 WhyNest Lab 公開試驗，既有正式引擎里程碑依原計畫辦理。

### 2026-11-22 科普頻道分流與私人試看授權

Owner 採納獨立科普品牌／頻道並要求執行分流及線上試看，確認「WhyNest Lab｜一分鐘科普」、插畫品牌 v2 與三支影片私人可見性。授權包括同帳號下獨立科普頻道、品牌設定及冰／天空／太空三支 v2 完整片的人工 Studio 私人上傳。Primary 重連後工具仍回報需驗證，改用已核對 CluePause 管理權的本機 Chrome。WhyNest Lab 已建立，三支均已從其 Studio Shorts 清單核對為私人。交接資料見 `experiments/science-shorts/channel-split-20261122/`。正式引擎與 M0/M1 範圍維持原合約，公開仍須另有授權，市場驗收待真人及公開後數據。

### 2026-11-21 科普本機試片授權

Owner 本次指示「按照完成的 flow 先寫出文案，給 sub-agent review，分數到後產出影片，評估是否另開頻道」，授權提前進行 Issue #8 的三支獨立科普本機試片。範圍為來源優先研究、雙語稿、獨立事實/圖解審查及理解度評分、通過後本機配音與動畫成片；證據位於 `experiments/science-shorts/batch-20261121/`。這是 M4 前置時序的單次隔離 pilot 例外，正式 M0/M1、Episode v1、SQLite 與發布順序維持原合約。一般 M1 擴建、完整 SC-00/01 產品化、付費媒體呼叫、私人上傳、公開發布及建立頻道均不在本次授權內。科普採 Issue #8 的 85 分理解度候選門檻，另有雙來源事實與科學圖解硬門檻；AI 分數不代表真人理解或市場驗收。

Owner 隨後回饋試片圖片不生動，並同意先做一個主題的畫面新版。此增量範圍為冰題目的本機視覺樣片：沿用既有文案、配音與時間，使用內建 image_gen 產生兩個插畫素材，新增分層運鏡及圖解動態，另做科學畫面審查與影音驗收；紀錄位於 `experiments/science-shorts/ice-visual-v2/`。不擴大為正式引擎產品化、另兩題重製或發布授權。

Owner 驗看冰新版後續准天空與太空兩題以同方式製作，並要求可重用 skill。本輪沿用兩題既有文案／配音／時間，產生同場景藍天與夕陽及透明太空人素材，新畫面另經獨立科學審查再本機編碼；實作與驗收位於 `experiments/science-shorts/sky-space-visual-v2/`。新增 `skills/science-shorts-visuals/` 並提供本機可發現副本；此增量授權不含上傳、公開、建立頻道、付費媒體 API 或正式引擎整合。

| 決策項目 | 本階段決定 |
|---|---|
| Repository | `story2video`（單一 Repo） |
| 首發市場 | 英文為主、繁中在地化。海龜湯由 CluePause 經營，WhyNest Lab 執行科普 Shorts 公開試驗 |
| 第一個內容垂直 | **原創海龜湯／日常懸疑推理**（並非轉貼既有謎題） |
| 首發影片格式 | **9:16、1080×1920、30 FPS、30–60 秒、H.264/AAC MP4** |
| 第二內容垂直 | 科普、歷史與世界奇聞（含證據查核） |
| 第三內容垂直 | AI／科技教學（需實際操作或可重現演示，禁止假裝實測） |
| 工作流程 | Python CLI + JSON Schema + SQLite + 本機檔案系統 |
| 影片產生 | Remotion（React／TypeScript）＋ FFmpeg/ffprobe |
| LLM／TTS／圖片 | 可替換 Provider Adapter；憑證一律使用環境變數 |
| YouTube | YouTube Data API v3（OAuth 2.0），第一階段只上傳私人影片 |
| 品質治理 | 腳本品質與授權檢查、機器影音 QA、**人工發布 Gate** |
| 市場實驗 | 先做 **12 部海龜湯 Shorts**，再決定是否擴充 |
| 明確不做 | 多 Agent、n8n 必需依賴、雲端分散式排程、多平台同發、全 AI 影片、全自動公開發布、多 Repo 維護 |

### 0.1 兩個相互獨立的成功標準

- **工程驗收：** 同一份已核准故事／設定可重現出正確影片；失敗能重試、追蹤與恢復；無需手工剪輯即可輸出；任意錯誤不會誤發布。
- **商業驗收：** 有來自非親友的持續觀看與回訪，觀看表現與生產成本合理，經過數據驗證後才考慮增加產量。

**非目標：** 產量、上傳數量或單一爆紅影片不等於成功；本專案不承諾 YouTube 演算法推薦或營利資格。

---

## 1. 市場假設與驗證邏輯

### 1.1 為何首選海龜湯

1. 強化「3 秒內問題 → 線索 → 思考 → 解答」的敘事鉤子，適合 30–60 秒的短影音。
2. 可以使用原創圖片、文字動效、少量鏡頭運動與配音，無需高價全程 AI 影片。
3. 分鏡與剪輯高度可參數化，適合重現性測試。
4. 但真正的海龜湯依賴互動詢問；單向 Shorts 必須重新設計，**不能只把問答唸出來**。

### 1.2 需要被挑戰的假設

| 假設 | 反證方式 |
|---|---|
| 「懸疑故事有完播率」 | 觀察前 3 秒滑走、有效觀看、平均觀看百分比與留存曲線；不只看 views |
| 「自動產生謎題可長期擴產」 | 讓測試者盲評 12 集的合理性、原創性與重複程度 |
| 「Shorts 可以帶來廣告被動收入」 | 將營利資格、實際 RPM 與觀看需求分開估算，先假定廣告收入為零 |
| 「影片容易製作，因此值得做」 | 記錄每部總成本（API、重試、審稿、剪輯修補、上傳與維護） |
| 「同一引擎可處理科普與 AI 教學」 | 第二階段證明核心 pipeline 不變，只替換內容 validator 與模板 |

### 1.3 第一批內容定位

- 語言：英文旁白與主要中繼資料，提供獨立可切換的英文、繁中字幕及繁中標題與說明。每個故事使用同一支影片。
- 系列：日常懸疑、情感反轉、邏輯推理；避免血腥、獵奇、針對兒童的恐嚇題材。
- 每支必須給完整且合理的答案；避免純粹誘導觀眾去別支影片找答案。
- 專案名稱 `story2video` 是**生成引擎**，頻道品牌名稱另行驗證，不必與 Repo 同名。

---

## 2. 產品需求（PRD）

### P0：海龜湯 Shorts 生成閉環

1. **Input：** 輸入主題、風格、時長目標或單篇人工編寫謎題。
2. **Script：** LLM 輸出符合 JSON Schema 的故事資料（含題目、線索、解答、分鏡、逐句台詞、建議時間）。
3. **Editorial Validation：** 結構、時長、答案邏輯、重複故事、敏感內容、授權來源檢查；不通過即停止。
4. **Audio：** 使用明確允許商用的 TTS Provider 產生旁白，記錄供應商、voice、輸出長度與成本。
5. **Visual：** 首版先以圖像＋文字動畫＋少量背景動效為主；可手動匯入圖片以取代 AI 生圖。
6. **Timeline：** 根據實際 TTS 時長排字幕；不能僅依文字字數猜時間。
7. **Render：** Remotion 組合 9:16 MP4；FFmpeg 用於轉碼、混音、檢查。
8. **QA：** 檔案規格、黑畫面／靜音、字幕越界、音訊削波、最後答案畫面存在性與逐集人工試看。
9. **Approval：** 人工確認後建立不可任意覆寫的批准紀錄。
10. **Publish：** 經 OAuth 上傳到 YouTube **private**；再次核對 metadata 後才能由人觸發公開／排程。
11. **Analytics：** 依 episode_id 與 video_id 關聯成效資料；比較同齡影片的固定觀察窗。

### P1：市場驗證後再擴充

- 科普／歷史腳本模板與「至少兩個獨立可追溯來源」的證據檢查。
- 5–10 分鐘橫式長影片模板，區分 Shorts 與長影片的內容節奏。
- 台詞／字幕／封面 A/B 候選版，保留實驗編號；避免短時間重複公開近似影片。
- 簡單本機 Review UI（只有 CLI 不夠用時才增加）。
- 半自動每週內容批次、排程、失敗通知。

### P2：暫不承諾

- 端到端無人值守公開發布。
- n8n/多 Agent、跨頻道與跨平台自動搬運。
- 真實感 AI 全動態影片、付費雲端 GPU、向量資料庫、微服務。
- 自動抓取、重配網路上的既有海龜湯或未授權影視素材。

---

## 3. 系統架構

```text
                            ┌────────────────────┐
人工主題／原創題目 ───────────▶│ CLI: draft           │
                            └─────────┬──────────┘
                                      │
                                      ▼
                            ┌────────────────────┐
                            │ LLM Adapter        │
                            │ Script JSON v1     │
                            └─────────┬──────────┘
                                      │
                                      ▼
                            ┌────────────────────┐
                            │ Content Gate       │◀─ 重複檢測、來源授權、邏輯／事實檢查
                            └─────────┬──────────┘
                                      │ PASS
                                      ▼
                            ┌────────────────────┐
                            │ TTS + Image Adapter│
                            │ asset manifest     │
                            └─────────┬──────────┘
                                      │
                                      ▼
                            ┌────────────────────┐
                            │ Remotion Renderer  │
                            │ + FFmpeg / ffprobe │
                            └─────────┬──────────┘
                                      │
                                      ▼
                            ┌────────────────────┐
                            │ Automated Media QA │
                            │ + Human Approval   │
                            └─────────┬──────────┘
                                      │ APPROVED
                                      ▼
                            ┌────────────────────┐
                            │ YouTube Private    │
                            │ Upload + Publish   │◀─ 人工 publish 明確授權
                            └─────────┬──────────┘
                                      │
                                      ▼
                            ┌────────────────────┐
                            │ Analytics Import   │
                            │ Cost / KPI Report  │
                            └────────────────────┘
```

### 3.1 原則

- **Single source of truth：** episode JSON 是內容真相來源；SQLite 是狀態與索引；`artifacts/` 是生成輸出。不得讓三者各自演化出不一致的 metadata。
- **Stage 隔離：** LLM、TTS、圖片、渲染與 YouTube Adapter 有明確輸入輸出；Provider 可替換。
- **重現性：** 鎖定腳本版本、prompt 版本、模型名稱、所有回應、輸入 hash、音檔與圖片 hash、render config、Git SHA。LLM 輸出不假定可重跑得到一樣結果。
- **Fail closed：** 未通過內容／QA／批准檢查的 episode 絕不可上傳或公開。
- **Idempotency：** 同一 episode、同一版本與同一操作不產生多份重複 YouTube 影片；重試前先檢查已存在的 video_id。
- **最小權限：** OAuth token 與 API key 只放環境／安全憑證儲存，不進 Git 與 log；上傳 OAuth scope 儘量最小。
- **可停止：** 每個 Stage 可暫停、獨立重試、人工修稿後從適當 Stage 恢復。

### 3.2 狀態機

```text
DRAFT
  └─ VALIDATING
      ├─ REJECTED  (可修稿回 DRAFT)
      └─ VALIDATED
          └─ ASSET_GENERATING
              ├─ FAILED_RETRYABLE
              └─ ASSET_READY
                  └─ RENDERING
                      ├─ FAILED_RETRYABLE
                      └─ RENDERED
                          └─ QA_RUNNING
                              ├─ QA_FAILED (須修正並重新驗證)
                              └─ QA_PASSED
                                  └─ AWAITING_APPROVAL
                                      ├─ REJECTED
                                      └─ APPROVED
                                          └─ UPLOADING_PRIVATE
                                              ├─ FAILED_RETRYABLE
                                              └─ UPLOADED_PRIVATE
                                                  └─ PUBLISH_APPROVED
                                                      └─ PUBLISHED
                                                          └─ ANALYZED
```

任一狀態變更留下 `actor`、`timestamp`、`input_hash`、`result`、`reason` 與關聯資產。**`APPROVED` 不代表自動允許 `PUBLISHED`；公開需第二道明確授權。**

---

## 4. Repository 結構（建議）

```text
story2video/
├── README.md
├── PLAN.md
├── pyproject.toml
├── uv.lock                     # 依實際套件管理工具產生
├── .env.example
├── .gitignore
├── configs/
│   ├── puzzle-short.yaml
│   ├── content-policy.yaml
│   └── providers.example.yaml
├── schemas/
│   ├── episode.v1.schema.json
│   └── publishing.v1.schema.json
├── src/story2video/
│   ├── cli.py
│   ├── domain/
│   │   ├── episode.py
│   │   ├── states.py
│   │   └── validators.py
│   ├── app/
│   │   ├── orchestrator.py
│   │   ├── store.py             # SQLite & artifact index
│   │   └── events.py
│   ├── providers/
│   │   ├── llm.py
│   │   ├── tts.py
│   │   └── image.py
│   ├── workflows/
│   │   ├── puzzle.py
│   │   └── science.py           # P1，先不實作
│   ├── services/
│   │   ├── script.py
│   │   ├── assets.py
│   │   ├── render.py
│   │   ├── media_qa.py
│   │   ├── publishing.py
│   │   └── analytics.py
│   └── adapters/
│       ├── remotion.py
│       └── youtube.py
├── video/
│   ├── package.json
│   ├── package-lock.json        # 依實際套件管理工具產生
│   └── src/
│       ├── Root.tsx
│       ├── compositions/PuzzleShort.tsx
│       └── components/
│           ├── Hook.tsx
│           ├── Clue.tsx
│           ├── Countdown.tsx
│           ├── Reveal.tsx
│           └── Captions.tsx
├── content/
│   ├── originals/              # 已確認權利的原創腳本／測資
│   └── episodes/               # episode manifests；不放憑證
├── artifacts/                   # gitignored：大檔、render、cache、logs
├── tests/
│   ├── fixtures/
│   ├── unit/
│   ├── integration/
│   └── golden/
└── docs/
    ├── decisions/
    ├── content-guidelines.md
    ├── editorial-checklist.md
    ├── security-and-licensing.md
    └── operations.md
```

除非有實際需求，不要拆成三個以上 Repo 或額外部署服務。

---

## 5. Episode Schema 與輸入輸出契約

### 5.1 參考 JSON（正式實作應制定 JSON Schema 並做嚴格驗證）

```json
{
  "schema_version": "1.0",
  "episode_id": "puzzle-0001",
  "script_revision": 1,
  "content_type": "puzzle",
  "language": "zh-TW",
  "target_audience": "general",
  "format": "shorts-9x16",
  "duration_target_sec": 45,
  "title": "她每天搭公車卻不用付錢？",
  "hook": "她每天搭同一班公車，卻從未付過車資。",
  "question": "她沒有逃票，也沒有違規，為什麼？",
  "answer": "她就是那班公車的司機。",
  "clues": ["她每天都在同一個時間上車", "她從不坐在乘客座位"],
  "narration": [
    {"id": "line-01", "text": "她每天搭同一班公車，卻從不買票。", "scene": "hook"},
    {"id": "line-02", "text": "她沒有逃票，也沒有特權。", "scene": "clue"},
    {"id": "line-03", "text": "答案是：她就是公車司機。", "scene": "reveal"}
  ],
  "visual_style": "cinematic-illustrated",
  "source": {"origin": "original", "source_refs": [], "license_reviewed": true},
  "ai_disclosure_review": {"required": false, "reviewed_by": null},
  "youtube": {"made_for_kids": null, "privacy_status": "private"},
  "review": {"logic": "pending", "editorial": "pending"}
}
```

此 JSON **僅為範例，不是已驗證可投入使用的題目**：例如「每天搭同一班公車」與「自己是司機」的語意仍需要編輯檢查，不能視為邏輯審核通過。

### 5.2 必填規則

- `episode_id` + `schema_version` + script revision 決定不可混淆的內容版本。
- `content_type` 僅允許 `puzzle`／`science`／`tech_tutorial` 等顯式枚舉。
- `source.origin` 可為 `original` 或經審核的 `licensed`，不可留空。
- YouTube 受眾設定必須在發布前經人工判定，`made_for_kids=null` 時禁止上傳。
- AI 真實感內容應披露與否由人工／規則共同判定，不能只以「用了 AI」概括。
- 每個資產記錄路徑、SHA-256、提供者、授權資訊、輸入成本及使用限制。
- 將宣告的 `duration_target_sec` 視為目標；實際長度由音檔與 render timeline 決定，必須驗證輸出。

### 5.3 CLI 合約（最初從本機 CLI 完成，不先建 UI）

```bash
s2v init
s2v draft --type puzzle --topic "日常推理" --id puzzle-0001
s2v validate --id puzzle-0001
s2v assets --id puzzle-0001
s2v render --id puzzle-0001
s2v qa --id puzzle-0001
s2v approve --id puzzle-0001 --reviewer human
s2v upload --id puzzle-0001 --privacy private
s2v authorize-publish --id puzzle-0001 --reviewer human
s2v publish --id puzzle-0001
s2v analytics sync --id puzzle-0001
s2v status --id puzzle-0001
s2v cost --id puzzle-0001
```

正式命令以實作為準。前四個步驟能在未設定 YouTube 的環境下完成；`upload`、`publish` 只能在明確配置 OAuth 後執行。**預設 `dry-run` 或 `private`，禁止隱式 public。**

---

## 6. 海龜湯影片模板規格

### 6.1 節奏與分鏡（45 秒示意，可按語音長度動態調整）

| 區段 | 參考秒數 | 目標 |
|---|---:|---|
| Hook | 0–3 | 直接提出反常現象，不要開場 Logo |
| Setup | 3–12 | 補充核心背景，避免冗長 |
| Clues | 12–25 | 提供能支持真實答案的線索 |
| Think | 25–32 | 留足短暫思考時間，倒數不是強制固定秒數 |
| Reveal | 32–42 | 完整答案與邏輯說明 |
| Close | 42–45 | 簡短收尾，不用欺騙性 CTA |

### 6.2 視覺設計

- 1080×1920、30 FPS；色彩風格與字體一開始只做 **1 套**，避免過早建立多樣模板。
- 中文字幕為主，建立可調字體大小、行數、字數上限、背景對比與安全區。
- 上下和右側預留 Shorts UI 可能覆蓋的區域；人工以手機預覽驗證，不能只靠座標推算。
- 圖片可先使用自建授權素材＋簡單平移縮放；暫不需逐秒呼叫 AI 影片模型。
- 真正的「反轉」必須由腳本提供；動效不可替代故事內容品質。

### 6.3 聲音設計

- 先選 1 種自然、有商用許可的 TTS 聲音，保持頻道辨識度。
- 依 TTS 語句時間資訊產生字幕，必要時依實際音訊做 forced alignment。
- 音效／背景音樂必須有明確授權與出處；不使用未授權流行歌曲。
- 檢查峰值、音樂與旁白比例、頭尾切斷、長段靜音、時間軸對齊。

---

## 7. 品質 Gate 與測試計畫

### Gate G0 — 需求／Repo 就緒

- [ ] Git Repo、README、PLAN、忽略檔案、環境樣板、基本 CI 就緒。
- [ ] `uv run pytest`（或明確宣告的測試命令）可成功執行。
- [ ] Node 與 Python 依賴鎖定；本機 Windows/Linux 至少一個主要平台可重建。
- [ ] `.env`、OAuth token、credential、渲染大檔不進 Git。

### Gate G1 — 原創腳本合格

- [ ] JSON Schema 合法，所有必填欄位齊全。
- [ ] 題目、線索與答案沒有明顯矛盾，並由人工確認不只是硬拗或任意設定。
- [ ] 同一批故事相似度與重複題材被提示，人工決定是否淘汰。
- [ ] 能證明來源是原創或已取得授權；不抓未授權題庫重新包裝。
- [ ] 安全審核避免真實人物誹謗、未經同意使用外貌／聲音、血腥或不當兒童內容。

### Gate G2 — 影片產生與媒體檢查

- [ ] 可從 `fixture episode` 無需人工剪輯生成可播放 MP4。
- [ ] `ffprobe` 檢查解析度、FPS、codec、音訊通道與時長。
- [ ] 首尾影格、抽樣畫面、字幕可視區與畫面完整性檢查。
- [ ] 旁白無截斷，答案畫面與答案語音都在輸出中。
- [ ] 同一份已鎖定 script/assets/renderer，重跑產生內容相同的影格和時間軸（容器 metadata 或編碼結果可能不保證 bitwise identical）。
- [ ] 模擬 API timeout、無回應、超額、壞音訊，確認停止且不會產出假成功檔。

### Gate G3 — 發布安全與回復

- [ ] `APPROVED` 前禁止上傳；`PUBLISH_APPROVED` 前禁止 public。
- [ ] 上傳時**顯式指定** `privacyStatus=private`，不可依賴 API 預設。
- [ ] `madeForKids` 受眾設定與合成內容披露由人工審查後明確填寫。
- [ ] 上傳中斷後重試不會造成重複影片；先查詢與落盤 video_id／上傳狀態。
- [ ] OAuth 失效、quota 限制、帳號限制與部分成功都有可恢復路徑。
- [ ] 未經人類確認，CI、排程或 CLI 不會自動執行 `publish`。

### Gate G4 — 商業實驗閉環

- [ ] 至少 12 部海龜湯影片完成品質檢查並按計畫發布。
- [ ] 每集保留成本、製作時間、API 重試、品質退件原因與分析 ID。
- [ ] 匯入 YouTube Analytics 可得指標，記錄 7 天與 28 天固定觀察窗。
- [ ] 確認觀看是否主要來自自然推薦，而非自己／親友重複觀看。
- [ ] 有書面 Go／Pivot／Stop 決策，而不是僅因產能可擴就擴。

---

## 8. YouTube 政策與授權風險

1. **大量重複內容：** YouTube 2025-07-15 將原「repetitious content」用語更新為「inauthentic content」，特別澄清大量製作或重複內容的營利限制。技術上使用 AI 本身不是禁止理由，內容仍需原創且有實質差異。
2. **AI 合成內容：** 寫文案、一般動畫不必然要求合成內容標記；真實感地製造現實人物、事件或地點影像等情況須依當時規範申報。API 支援 `status.containsSyntheticMedia`。
3. **兒童受眾：** 是否 Made for Kids 依實際目標受眾判定；不因「沒有成人內容」就預設是兒童內容，也不可為增加營利而故意錯誤標記。
4. **改編權：** 不批次搬運網路既有海龜湯題庫、論壇留言、影視片段；原創故事／清楚授權素材優先。
5. **商用授權：** LLM、TTS、AI 生圖、字體、音效、背景音樂、素材網站與 Remotion 都需個別檢查條款，留下版本與權利資訊。
6. **YouTube 上傳：** 官方在 2026-11-02 更新 API 行為，未經稽核專案的上傳不再一律強制 private，且部分情況未指定 privacyStatus 可能成為 public。**因此應在程式內強制 private，不靠平台預設。**
7. **API 限額：** YouTube Data API 目前有 `videos.insert` 獨立上傳配額 bucket，預設 100 次／日（可能變動）；此數字不是單一使用者的保證，實作需動態處理配額錯誤。
8. **Remotion 授權：** 官方現行方案允許個人及符合資格的小團隊免費商用／自動化；若成為較大規模公司或作為產品提供服務，必須重新核對授權。

**上線前人工檢查清單：** 來源權利 ✓／謎題合理 ✓／字幕與音效 ✓／影片重複程度 ✓／受眾設定 ✓／合成媒體披露 ✓／標題是否誤導 ✓／頻道政策 ✓。

---

## 9. 分階段實作 Backlog（可直接轉成 GitHub Issues）

> 每個 Issue 先依賴前置驗收，避免同時開過多分支。所有「完成」均要求留下可重現測試證據。

| Issue | 優先 | 範圍／交付物 | 依賴 | 完成定義 |
|---|---|---|---|---|
| S2V-001 | P0 | Repo 基礎、README、PLAN、測試／CI、設定檔 | 無 | 本機與 CI 跑通最小測試 |
| S2V-002 | P0 | Episode v1 JSON Schema 與狀態機 | 001 | 合法／非法 fixture 測試通過 |
| S2V-003 | P0 | Puzzle Script Adapter（先 mock，再接一個 LLM） | 002 | 生成、版本化、錯誤回報可重現 |
| S2V-004 | P0 | Puzzle Logic/Originality Gate | 003 | 不合理、重複、無權利資訊阻擋 |
| S2V-005 | P0 | TTS Adapter + 音訊／字幕時間軸 | 002 | 音訊與字幕可同步且可離線 mock |
| S2V-006 | P0 | 圖片素材／授權 Manifest | 002 | 來源及 hash 可查，缺失不繼續 |
| S2V-007 | P0 | Remotion PuzzleShort 模板 | 005,006 | 可輸出 1080×1920、30–60 秒 MP4 |
| S2V-008 | P0 | 媒體 QA 與人工批准紀錄 | 007 | 不合格不可 approve，hash 綁定 |
| S2V-009 | P0 | E2E 本機閉環與重試／重跑 | 003–008 | fixture 從 draft 到 QA_PASSED |
| S2V-010 | P0 | YouTube 私人上傳與二段授權 | 008,009 | 私人上傳、避免重複、禁止誤公開 |
| S2V-011 | P0 | 分集成本、執行時間、錯誤統計 | 009 | 每一集可出成本／失敗原因報告 |
| S2V-012 | P0 | 12 集市場實驗與觀察模板 | 010,011 | 7/28 天 KPI、Go/Pivot/Stop 書面報告 |
| S2V-013 | P1 | YouTube Analytics 同步 | 010 | 能以 video_id 匯入合法可得指標 |
| S2V-014 | P1 | 科普研究與來源查核 Gate | 012 | 主張到來源映射、查證失敗拒絕渲染 |
| S2V-015 | P1 | 16:9 5–10 分鐘科普模板 | 014 | 一篇可產長影片並通過媒體 QA |
| S2V-016 | P1 | 批次排程、通知、Review UI | 012 | 在有效需求與內容產能成立後才做 |
| S2V-017 | P2 | AI 工具教學專用螢幕錄影流程 | 012 | 具有實測證據、無假畫面／假結果 |

### 執行關卡

- **M0：Repo Bootstrap：** S2V-001～002。交付架構可跑、Schema 可驗證；不連外、不收費。
- **M1：First Local Video：** S2V-003～009。交付**一支本機合格的原創海龜湯 Shorts**；不觸碰 YouTube。
- **M2：Private Upload：** S2V-010～011。交付 YouTube 私人影片、權限防線、成本收據。
- **M3：Market Experiment：** S2V-012，視需要加入 013。交付 12 支影片與觀察結果，決定 Go/Pivot/Stop。
- **M4：Science Extension：** 只有 M3 證實有價值時才做 S2V-014～015；不是第一版必要條件。
- **M5：Scale：** 只有品質、需求、收益／成本都成立才加 S2V-016～017。

### 依賴先後（避免一次開太多工作）

```text
001 → 002 → 003 → 004
         ├→ 005 ─┐
         └→ 006 ─┴→ 007 → 008 → 009 → 010 → 012 → 014 → 015
                                     └→ 011 ─────┘
                                                └→ 016（需求證實後）
```

---

## 10. 市場實驗設計（避免自我感覺良好）

### 10.1 首批 12 支影片

- 都是原創題目，採固定規格與相同畫面品質。
- 類型分布：4 支日常懸疑、4 支情感反轉、4 支邏輯推理。固定旁白語言、字幕、品牌風格與影片規格，便於比較內容。
- 每支檢查謎題邏輯、揭曉前的劇透、字幕和影音。上述項目有實質錯誤才以內容問題退件，發布依既有授權關卡。
- 依可持續頻率發布；不短時間密集丟出 12 支相似影片。
- 每支正式發布後按第 7 天與第 28 天的等長觀察窗比較。第 1～3 支驗證製作流程，第 4～8 支比較初步觀看反應，第 9～12 支檢討市場與成本。第 13～20 支只在首輪有待驗證的問題時追加。
- 每集製作與發布後的觀察值記在 [首輪 Shorts 紀錄](experiments/shorts-series/README.md)。

### 10.2 衡量指標

**影片品質／內容：**
- 內容審核退件率、合理性盲評、重複題目率、字幕／配音錯誤率。

**市場：**
- 以 Shorts 動態曝光、選擇觀看比例、有效觀看、平均觀看百分比與留存曲線為主，另記留言、訂閱和回訪。
- 由 YouTube Studio 記錄可取得的指標。回訪觀眾若只提供頻道層級，在同期頻道紀錄中填寫。公開播放次數可作背景資訊。
- 觀察單一題材跨 12 集是否穩定；排除親友測試流量與付費推廣對比較的干擾。

**經濟性：**
- `cost_per_approved_video` = （所有呼叫費用 + 重試與報廢成本 + 外部渲染成本）／合格影片數。
- `labor_minutes_per_approved_video`：人工審稿、修正、審批時間。
- `effective_cost`：若要評估真正「被動收入」，再計入人工時間之機會成本。
- 營利後再記錄 `revenue_per_1000_views`；尚未加入 YPP 時不得以假設 RPM 認列營收。

### 10.3 Go / Pivot / Stop 決策規則

以下是**專案內部初始討論門檻**，不是 YouTube 官方保證或市場統計。實驗完成後按實際分布修正，保留原先預註冊假設。

- **GO（繼續）：** 品質與法遵 Gate 全通過；製作費用在預算內；有多支影片取得自然流量與合理留存，而非只有一部爆紅；人工投入可接受。
- **PIVOT（換方向）：** 技術流程穩定但自然流量／留存薄弱；優先測試不同劇情設計或科普題材，不立刻改寫架構。
- **STOP／PAUSE（停止擴產）：** 內容品質需大量人工修補、侵權／政策風險不易控制、長期成本大於觀察到的潛在價值，或連續多次實驗無法改善。

**證據不足：** Shorts 動態曝光不足、集中在少數影片，或 D28 尚未到期時，市場結論維持待定。先記錄缺少的證據，追加影片時寫明要驗證的假設。

---

## 11. 成本上限與收益模型

### 11.1 第一階段預算（供規劃使用，非報價）

| 項目 | 第一批 12 支的內部預算上限（USD） | 備註 |
|---|---:|---|
| LLM 文字 | 10 | 控制回合數，記錄 tokens 與重試 |
| TTS | 15 | 依服務商商用授權與使用量調整 |
| AI 圖片與素材 | 30 | 首版盡量用可重用授權素材 |
| 預留重試費用 | 15 | API 失敗、重渲染、替換模型 |
| **合計實驗支出上限** | **70** | 不含電費、人工、既有設備、訂閱費、稅金 |

- `S2V_MAX_TOTAL_SPEND_USD=70` 作為實驗監督條件，若 Provider 無法提供即時金額，應以預估成本及請求數限制並保留誤差，不能保證硬性即時封頂。
- `S2V_MAX_EST_COST_PER_EPISODE_USD=3` 作為單支自動化預算警戒；人工核准才可超額。
- 不為了追求低成本而使用授權不明的 TTS／音樂／影像素材。
- 第一階段不購買付費影片模型的長片套餐；先用靜態圖片與簡單動效確認需求。

### 11.2 收益觀念

- YouTube 完整廣告分潤門檻之一：**1,000 訂閱者 + 過去 90 天 1,000 萬次有效 Shorts 觀看**；另一條為 **1,000 訂閱者 + 過去 12 個月 4,000 小時有效公開長片觀看時數**，並且必須通過平台審核。
- 未通過 YPP 時，將 **YouTube 廣告收入設為 0**。
- 如需情境模擬，用 `收益 = 有效計費基礎對應的實際平台收益`，不要把 Shorts views 當成已售廣告曝光或保證可分潤。
- 長期獲利應計入：AI API、影片素材、人工審核、平台與稅費、設備折舊、維運。
- 不以「全自動」等同「被動收入」；維持內容品質與政策符合仍需要人工負責。

---

## 12. 主要風險與緩解

| 風險 | 早期警訊 | 應對 |
|---|---|---|
| YouTube 判斷大量重複／不真實內容 | 不同影片同框架換字、腳本高度相似 | 原創性 Gate、內容差異化、人工審稿，降低機械量產 |
| 海龜湯答案不合理 | 多個同樣合理答案、線索與答案矛盾 | 用反例測試＋人工盲評，退件優先於硬修 |
| 書面來源侵權／音訊權利不明 | 抓取外部題目、素材沒有權利記錄 | 原創優先；每個資產保存來源與商用授權 |
| Shorts 觀看很高但無法營利 | 只有播放量，缺乏訂閱／有效觀看 | 依官方資格與真實 RPM 評估；嘗試長影片而非盲目擴產 |
| API 額度與價格突然變動 | 429、失敗重試暴增、每支成本上升 | Adapter、重試上限、用量記錄、人工熔斷開關 |
| 影片誤公開 | `privacyStatus` 遺漏、重試時狀態錯誤 | 上傳明確 private、雙 Gate、publish 需明確命令 |
| 重複上傳／資料失聯 | Upload timeout 後再次 insert | durable upload journal、video_id 回寫、人工協調未知狀態 |
| 工程過度設計拖延驗證 | 先做三 Repo、複雜 UI、Agent orchestration | 以單一 CLI/SQLite/Remotion 完成 M1，後續按需求升級 |
| 科普 AI 幻覺與假實測 | 無來源的知識論斷、AI 生成假的工具畫面 | 對照權威來源，科技教學須實際執行並保存證據 |

---

## 13. 第一個開發迭代：交給 Codex 的工作指令

**目標只做 S2V-001～S2V-002，不要跳到 YouTube 上傳，也不需要任何外部 API 憑證。**

> 以 `story2video` 為單一 Repo，依 `PLAN.md` 建立 Python CLI 與 Remotion 預留目錄的最小骨架。先實作 Episode v1 JSON Schema、明確狀態機、SQLite 儲存介面、合法／非法 fixtures，以及本機與 CI 測試。不要加 n8n、雲端 DB、全功能 UI、多 Agent 或 YouTube 上傳；不要嘗試外連生成影片。建立 `README.md` 記錄一鍵安裝與測試方式；附上實際執行的測試命令、結果、Git SHA，以及尚未完成的項目。僅完成計畫中的 S2V-001／002，下一階段需再次授權。

### 初始 PR 應交付

- [ ] 合法範例、無效例子與 state transition unit tests。
- [ ] SQLite schema migration 或有版本的初始化機制。
- [ ] 初始 `s2v status`、`s2v init` 有最小可用性。
- [ ] 在 Linux／Windows 其中一個主要環境跑通測試。
- [ ] Secret 掃描基本檢查及 `.gitignore` 完備。
- [ ] 清楚註明哪些 Phase 尚未實作、哪些外部 API 尚未驗證。

---

## 14. 參考資料（2026-11-20 查核）

**可借鑑的開源專案**

- [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) — 參考腳本／TTS／素材／字幕／影片／上傳端到端流程，不直接假定內容品質可用。
- [Remotion](https://github.com/remotion-dev/remotion) — React/TypeScript 參數化影片模板。[官方授權說明](https://www.remotion.dev/docs/license/faq)。
- [FFmpeg](https://ffmpeg.org/) — 編碼與媒體檢查。

**YouTube 官方文件**

- [YouTube Partner Program 門檻](https://support.google.com/youtube/answer/72851)
- [YouTube 2025 年不真實／大量重複內容釐清](https://support.google.com/youtube/blog/356734251/response-to-creator-questions-about-ypp-policies-july-2025)
- [AI 合成內容揭露要求](https://support.google.com/youtube/answer/14328491)
- [YouTube Data API videos.insert](https://developers.google.com/youtube/data/reference/rest/v3/videos/insert?hl=zh-TW)
- [YouTube Data API 修訂紀錄](https://developers.google.com/youtube/data/revision_history?hl=zh-TW)
- [YouTube Data API 配額](https://developers.google.com/youtube/data/determine_quota_cost)
- [YouTube Analytics 指標](https://developers.google.com/youtube/analytics/metrics)

---

## 15. 最後的 Stop Rule

**M1 只求一支真正合格的本機影片；M2 只求安全上傳；M3 只求 12 支可比較的真實觀眾資料。** 不因為影片生成流程看起來完整，就提前建立大規模排程與自動公開系統。技術上能量產與市場上值得量產，必須由兩個不同的證據鏈證明。
