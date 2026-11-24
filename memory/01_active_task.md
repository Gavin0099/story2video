# Active Task

## Current Status

- 2026-11-22：治理在實際開發目錄重新安裝並驗收（base `2d63c2d`）。11-21 重新 clone 後 submodule 未初始化、`.git/hooks/` 無 hook；已初始化 `b8a16828` 並裝回 pre-commit／pre-push。hook_install_validator、governance_drift_checker、external_repo_smoke、`governance/verify.py` 均 exit 0；post_task smoke 於拋棄式 worktree 執行 ok=True。commit `93acd55` 時 pre-commit 實際執行，輸出 memory workflow advisory（`warning_codes=missing_canonical_memory`，僅提示、未阻擋）。11-20 記錄的 PASS 證據檔位於不進版控的 `artifacts/`，新 clone 中已不存在。

- 2026-11-22：WNL-021 生蛋動畫新版已輸出 40.8 秒本機片及開場片段。獨立預覽及正式檔畫面抽驗通過。見[成片紀錄](../experiments/science-shorts/egg-animation/README.md#改拍鏡頭與剖面)。

- 2026-11-22：Owner 選定滿版微距構圖。已將同一物件的鏡頭連續性、實拍或生圖素材選擇、英文圖解及手機字幕檢查寫入 `science-shorts-visuals`，專案與本機版同步。

- 2026-11-22：依 Owner 對科普配圖的回饋，以第 20 支紙巾題目製作舊開場和滿版微距構圖對照。檔案見 `artifacts/science-shorts/visual-direction-20261122/comparison.jpg`。

- 2026-11-22：Owner 授權 WhyNest Lab 三支試片改公開並擴至 20 支。原三支已公開，17 支新稿均達兩位讀者各 85 分門檻。新片使用英文圖解與旁白、英／繁中獨立字幕。公開進度和首日時間見 `experiments/science-shorts/public-20-20261122/d1.csv`，製作紀錄見同目錄 README。

- 2026-11-22：WhyNest Lab `@WhyNestLab` 已建台，插畫版頭像、橫幅與雙語簡介已存。三支試片上傳為私人，雙語字幕與繁中資料已核對，三個觀看連結均在登入帳號成功開始播放。公開名稱目前為英文 WhyNest Lab。見 `experiments/science-shorts/channel-split-20261122/README.md`。

- 2026-11-22：依 Owner 回饋完成 WhyNest Lab 插畫品牌 v2，輸出全幅、頭像與手機裁切預覽。已查官方重連步驟及設計 skill／安全區 repo。線上分流仍待可用登入連線。見 `experiments/science-shorts/channel-split-20261122/README.md`。

- 2026-11-22：Owner 已准 WhyNest Lab 獨立科普頻道、Primary 連線及三支 v2 私人試看；品牌與雙語上傳交接備妥，三片 SHA 核對既有 QA PASS。Primary 回報需重新驗證，已請 Owner 重連；尚未建立／上傳。見 `experiments/science-shorts/channel-split-20261122/README.md`。

- 2026-11-22：完成科普／海龜湯分流評估，建議獨立品牌與頻道、同 Google 帳號管理、共用引擎；見 `experiments/science-shorts/channel-separation-plan.md`。屬待 Owner 採納建議，真人與市場待驗；未建立頻道或發布。

- 2026-11-21：Owner 驗看冰新版後續准天空／太空及skill；兩題新版完整片46.1／51.8秒、各12秒preview已交付，獨立新科學圖解與實際MP4抽驗均PASS、critical0，四片QA及pytest61通過。`science-shorts-visuals` 本機／repo副本格式與hash一致、隔離planning forward-test及修訂確認完成；真人／市場待驗。見 `experiments/science-shorts/sky-space-visual-v2/validation.md`；未上傳／公開／開頻道。

- 2026-11-21：Owner 同意先做冰題目畫面新版；已交付 48.1 秒完整片與 11.6 秒開場，兩個內建生圖素材、分層動畫及原旁白。新科學畫面審查／實際 MP4 抽驗均 PASS、0 critical，影音 QA 與核心 pytest 61 項通過；真人美術接受度與市場待驗。見 `experiments/science-shorts/ice-visual-v2/validation.md`；未上傳或建立頻道。

- 2026-11-21：Owner 回饋科普圖片不生動；已完成三片抽樣與繪圖實作的視覺診斷及官方 repo/skill 比較。建議先做插畫分層與科學動畫的短段比較，尚未採納實作、生成素材或重製；見 `experiments/science-shorts/visual-direction-review.md`。

- 2026-11-21：Owner授權科普三支本機pilot；已完成雙來源文案、獨立事實/圖解審查與兩位分段理解讀者（冰88/89、天空87/86、太空89/87），成片48.1/46.1/51.8秒。12 MP4機器QA與三片科學畫面抽驗通過；真人/市場待驗，未建立頻道或上傳。見 `experiments/science-shorts/batch-20261121/validation.md` 與 `memory/04_review_log.md`。

- Adopted governance baseline.
- 2026-11-21：Story Quality Lab 已備妥無問答主持包，並完成 26M A、B 成片畫面及字幕對照。影片問換號動機，題卡問來電者身分。兩道內容關卡仍 PENDING，新增真人資料 0。見 `memory/04_review_log.md` 及 `experiments/story-quality-lab/validation-2026-11-21.md`。
- 2026-11-21：Episode 02 73H 本機成片 45.57 秒，備妥英文及繁中 SRT、可切換字幕的校閱片及上傳母片。完整解碼、字幕回讀與畫面抽驗通過。待上傳與公開授權。見 `experiments/episode-02-73h/validation.md`。
- 2026-11-21：[PR #5](https://github.com/Gavin0099/story2video/pull/5) 首輪獨立評分最高 84／100，0 篇達開拍門檻。每篇該版獨立評分須達 90／100（含）。修訂稿 `0fa371a` 待重評。
- 2026-11-21：PR #5 更新至 `c096a2e`。10〈刮痕〉第四稿在首次分段 AI 試讀得 86、89／100，兩位讀者都只部分從題面推到動機。開拍名額仍為 0。

## Next Steps

- Update this file when task state changes.
- Episode 03、07 第二輪編輯複審各 86／100。兩篇仍待改寫與首次分段盲評。10 的兩版原始試讀回覆保存在 PR #5。
- 按 `experiments/shorts-series/README.md` 紀錄首輪 12 支的製作資料，正式發布後填 D7／D28。

- CluePause P0 覆核 29 支時間碼與舊 20 支首日基準，新 9 支首日數據另補。 <!-- memory_record_projection:active-task-summary:3fc2594cf61118b385f099e7d332f05d657d65e5e05625b70a4ec8be87f715df -->
