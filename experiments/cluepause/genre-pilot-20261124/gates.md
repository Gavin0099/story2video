# Genre gates — draft, no results

所有故事：**HUMAN_TEST_PENDING**。目前只有文字；無獨立讀者分數、真人回覆、成片驗收或市場數據。新 genre 的準則及負例全部為 **PENDING（未核准）**，是供 Owner 審議的草案，不能用作者自評換成 PASS。

## 共通前提

權利狀態須依 PR #17 的 `approved / pending_permission / pending_verification / rejected` 分開記錄。本輪三稿都是 `pending_verification`；原創性外部查核尚未做。製作候選要同時完成權利及適用品質 gate。畫面不得藏掉必需線索、提前暴雷或把 fiction 包裝成真新聞／CCTV。人類測試、公開需求、工程驗收各自記錄；任何 PASS 都不是公開授權。

`twist_type` 使用：`benevolent_misunderstanding / identity_reversal / context_reversal / object_function / causal_reversal / other`。它是描述，不是評分。本輪 puzzle 採 object_function，明確避開 benevolent_misunderstanding。

## puzzle — reference existing gate, unchanged

- [既有 skill](../../../skills/shorts-viewer-gate/SKILL.md) 與 [專案題型工作流](../../../skills/shorts-viewer-gate/references/story2video.md)：三位獨立讀者**每位至少 90**，核心因果須有線索支持。不是三人平均達 90；本次沒有重訂或執行此門檻。
- [既有五人完整首看流程](../../story-quality-lab/shorts-viewer-gate.md)：同版五位有效首看，至少四位說對核心答案，至少三位明確覺得反轉有趣並說出理解改變；少於五人保持待驗。原文件不修改。
- 本輪兩測試的 3–5 人探索是新增診斷，不取代既有門檻，不把 A 的三秒曝光加進 B 的完整理解人數，也不把 4/5 按比例改成 2/3。puzzle 若尚缺既有完整首看證據，不宣告已通過；補驗安排見 protocol。

Viewer questions（完整不中斷播放後，先開放問題，再追問）：

1. 這支在問什麼？你認為為什麼會發生？
2. 哪個畫面、聲音或動作支持你的解釋？哪裡跟不上？
3. 你原先如何想，揭曉改變了什麼？這個改變有趣、普通、無感，為什麼？

本稿主持人答對口徑在 [puzzle.md](puzzle.md)。未取得符合門檻的獨立評閱，不可自寫 90 分；這次不啟動評閱／製作流程。

## uncanny_mystery — every criterion PENDING

| 狀態 | 草擬準則 | 負例（也是待核定的失敗判準） |
| --- | --- | --- |
| PENDING | 0–3 s 可自行辨認日常場景中的反常，而非只讀到作者宣稱很怪 | 黑畫面寫「你絕對想不到」，卻沒可見事件 |
| PENDING | 觀眾能形成至少一個使用已給資訊的合理猜測，不需猜中唯一答案 | 唯一可行猜法依賴從未提過的雙胞胎／機關 |
| PENDING | 揭曉前有可辨認的具體線索，逐條支持物理／人為因果 | 只在最後一秒首次說出牆後有一台設備 |
| PENDING | 揭曉重解開場及至少一項反覆模式；重要限制一致 | 說「都是夢」；鞋明明全濕，卻用只沾鞋底的水解釋 |
| PENDING | 結尾完成此篇承諾，讓先前的恐懼變成可理解的發現 | 漏水已解決，又加鬼手否定所有證據；答案留給下一集 |

Viewer questions（先收原話，不公布主持人答案）：

1. 你看到什麼不尋常？你一開始怎麼猜？有沒有形成一個你覺得合理的猜測？為什麼？
2. 哪個線索讓你保留或改變猜測？不記得也可照實說。
3. 揭曉後，你會怎麼解釋剛才的異常？哪些細節被重新解釋，哪些還不通？
4. 哪裡想繼續看、想停看？會想看另一篇這類故事嗎？為什麼？

PENDING 候選決策方式：只有預先核定的準則都具可追溯證據、無未解因果矛盾時，才可提名「值得公開測試」。保留每人的合理猜測與完整解釋，不以猜中率單獨當成功率。樣本缺漏或意見分歧可判 INCONCLUSIVE；不在看到答案後增設數字門檻。

## urban_horror — every criterion PENDING

| 狀態 | 草擬準則 | 負例（也是待核定的失敗判準） |
| --- | --- | --- |
| PENDING | 0–3 s 有可讀的異常或威脅，不安不只依靠音量或黑暗 | 突然尖叫，但不知道角色面對什麼 |
| PENDING | 主衝突與角色目標清楚，後續每段增加壓力或改變選擇 | 連列五條怪規則，卻不知角色要做什麼 |
| PENDING | 世界規則先建立，高潮遵守；心理反應可理解 | 明說不獲邀不能入內，最後卻無理由瞬移進房 |
| PENDING | 結尾回到同一衝突，產生後果或理解變化；不要求唯一可猜答案 | 最後突然說「兇手是某人」，前面毫無關係；只丟下一集連結 |
| PENDING | 虛構、心理、不血腥；可有未解存在，但不能靠假紀實取信 | 「真實監視器流出」；用傷口或真實受害者代替故事 |
| PENDING | 續看意願可由觀眾原話說明原因，與「嚇到」分開 | 只因有人受驚就宣稱有市場需求 |

Viewer questions（完整觀看後）：

1. **什麼時候開始感到不安？**記得哪個畫面／聲音？若沒有，直接說沒有。
2. **你知道主角的主要衝突是什麼嗎？**她要避免什麼？哪個規則影響了她？
3. **結尾有兌現前面的期待嗎？**什麼有用、什麼牽強或沒交代？
4. **你會看另一篇這類故事嗎？**為什麼？

PENDING 候選決策方式：先核定敘事與規則一致性，再依原話判斷衝突／兌現是否可讀。不設解謎正確率，不因看出結尾或提出另一個逃法就自動扣分。若觀眾只記住驚嚇、無法理解衝突，列修稿問題；若資料不夠或分歧，INCONCLUSIVE。所有條件仍未核准，無 PASS。

## 記錄與授權邊界

每條準則留 `criterion | status | frozen_revision/hash | evidence/respondent | raw_answer | interpretation | missing | reviewer/date`。目前 evidence 均為 NOT_COLLECTED。品質觀察只能指向這篇及這個版本，不可推成 genre 勝負。私人試看通過只容許提出公開測試建議，不能證明需求；公開需求另看 README 規劃的 D1/D7 資料，公開動作逐片另需 Owner 明確授權。
