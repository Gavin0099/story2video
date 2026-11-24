# P01 — The Thread Under the Scale

| 欄位 | 草稿值 |
| --- | --- |
| series_code / series | puzzle / Solve It |
| revision | draft-1, 2026-11-24 |
| format / duration_target | 9:16 / 42 s（容許 35–45 s；未實測） |
| narration / subtitles | English / 繁體中文；下表 ZH 以 `／` 分行，不是旁白 |
| twist_type | object_function |
| rights_status | pending_verification |
| human_status / quality_gate | HUMAN_TEST_PENDING / 未評分、未通過 |

**Logline:** A buyer cuts one thread beneath a jeweler's scale; the gold stays in the pan, but its price drops with the needle.

**核心題目：** 金子一點沒動，剪斷一條線為何讓秤變輕？

**解答因果：** 賣家用穿過櫃檯的細線向下拉秤盤，讓機械秤多算重量。買家剪斷線，額外拉力消失。這是詐術揭露與物件功能反轉，沒有「看似惡意其實幫忙」的善意誤會。

## Beat sheet、雙語稿與分鏡

時間全為目標秒數。只唸 EN 欄；表內分鏡是未製作的指示，不是已有影像證據。

| 目標秒數／beat | English narration | 繁中字幕行 | 9:16 storyboard / visual spoiler risk |
| --- | --- | --- | --- |
| 0–3 / first visible anomaly（約 1 s） | She snipped. The gold got lighter. | 她剪了一下。／金子竟變輕了。 | 同框呈現完整秤盤、同一堆金料與大型機械指針突然下降；剪刀只在櫃檯下緣露出。**風險：**若首圖直接拍到賣家拉線，答案已洩漏；若金料被裁掉，則異常無法成立。 |
| 3–8 / question | Nothing left the tray. Why did the weight drop? | 秤盤上什麼都沒少。／重量為什麼下降？ | 固定構圖確認金料沒有換掉或滑出；不要加電子數字或魔法光。 |
| 8–14 / first clue | Before buying, she'd noticed a thread beneath the counter. | 購買前，她注意到／櫃檯下有條細線。 | 以清楚的「Earlier／稍早」標記回看。細線穿過櫃檯孔，至少可辨認，不把整條路徑亮出。**風險：**線太細會成為藏線索。 |
| 14–21 / key clue | The seller's fingers tightened. The needle rose, but the gold never moved. | 賣家手指收緊，指針就上升。／金子卻完全沒動。 | 櫃檯側面：手拉線與指針上升同次動作可讀，秤盤沒有新增物。**風險：**不可只靠旁白說動作，亦不加第二名同夥。 |
| 21–26 / think | There were no batteries. Watch what the thread was pulling. | 秤沒有電池。／看那條線拉著哪裡。 | 純機械彈簧秤的盤、掛臂與指針同框，重播此前已出現的拉線動作；給推理節拍。 |
| 26–37 / reveal | It ran through the counter and tugged the tray downward. He was selling the pull of his hand as extra gold. | 線穿過櫃檯，把秤盤往下拉。／他把手的拉力，也算成金子的重量。 | 首次完整呈現線固定於盤下，再接回開場剪線、指針回落的連續因果。**風險：**線若只接秤外殼，物理因果不成立；接點須在承重盤。 |
| 37–42 / payoff | She hadn't removed any gold. She'd removed his extra weight. | 她沒有拿走金子。／她拿掉的是他多加的「重量」。 | 保持同一堆金料，指針停在較低值；不加逮捕或其他新情節。 |

開場是剪線後的結果，8 秒回到稍早，26 秒才揭示整個機構；不得用不連續的金料或指針狀態混淆。42 秒含推理與讀圖時間，實際口述和字幕需日後驗時。

## 公平性、替代解釋與測試口徑

合理首猜可能是秤故障、金料掉落或被調整校準。固定金料與純機械秤排除前兩項的主要視覺歧義；手拉線與指針同步、盤下接點支持額外向下拉力。仍可質疑線是否碰到其他機件，日後分鏡須讓它只拉承重盤，不以隱藏遙控器或磁鐵補解。

主持人核心答對口徑：要說到「線向下拉秤盤、增加讀值，剪斷移除額外拉力」，只說「秤有問題」或「線有重量」不足。首看異常口徑：沒有拿走金料，指針卻下降。不得因作者覺得解釋合理就宣稱符合既有 90 分 gate。

## 創作與權利待辦

創作來源：本次由 Codex 依 Owner 的 genre brief 新寫；未使用第三方故事原文、經典題卡、網路故事或真實新聞。抽象機制是「測量結果受外加力影響」；具體場景、先結果後回看的順序、細線與機械秤線索及雙語表達為本稿設計。這是創作方式紀錄，不是已完成原創性查核的聲明。

`rights_status = pending_verification`。仍需：與 repo 全部既有分集（含 29 支的凍結稿）比對事件、順序、人物、線索與解答；以中英關鍵組合搜尋「jeweler scale thread pulling tray / 金店 細線 拉秤盤 剪線」等相關情節；由審查人記錄來源、相似元素與獨立表達，必要時重寫。不得把「搜不到」當作保證原創。未作外部搜尋，未借用找到的現成情節。

權利紀錄用語依 PR #17 參照文件：`approved / pending_permission / pending_verification / rejected`。參照讀取命令為 `git show origin/codex/cluepause-story-rights-gate:.agents/skills/story2video-shorts-batch/references/story-rights.md`。製作前須凍結本稿 SHA-256、補審查人／日期、用途與相似性證據；私人試看與公開／營利用途分開核對。本稿是虛構，未宣稱真實案件或 CCTV。
