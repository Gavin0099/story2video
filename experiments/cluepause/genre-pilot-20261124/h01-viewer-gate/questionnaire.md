# H01 首看問卷與空白紀錄

**HUMAN_TEST_PENDING / EXPLORATORY ONLY**。遵守 [viewer-protocol.md](viewer-protocol.md)。以下「表單文字」可直接複製給觀眾；不顯示 host cut 或另一版本資訊。觀眾只見其匿名碼及中性播放碼。問卷在一次觀看結束後才出示，不能提前提示。

## 表單文字（繁體中文，可直接複製）

匿名代碼：＿＿＿＿

播放代碼：＿＿＿＿

請依剛才第一次觀看的感受回答。以下第 1–6 題各選 1–5 分，1 最低、5 最高（1＝完全沒有／非常低，2＝低，3＝普通，4＝高，5＝非常高）。若沒有看到相關內容、無法回答或不想回答，可留白並註明原因。沒有標準答案，請不要填姓名或聯絡資料。

1. 影片的前 3 秒，有多讓你想繼續看下去？（1–5）
2. 沒有看過劇本的情況下，你有多能理解影片發生了什麼事？（1–5）
3. 在揭曉之前，你有多想知道答案？（1–5）
4. 揭曉之後，你有多強烈的「原來如此」感？（1–5；若未看到揭曉請留白，註明「未看到」）
5. 你覺得影片整體看起來有多自然？（1–5）
6. 你有多願意繼續看這一類影片？（1–5）
7. 回想揭曉之前，你當時以為發生了什麼事？請依現在記得的想法回答；這是事後回憶，不是事前鎖定的預測。（開放回答）
8. 哪裡讓你不明白，或最想滑走？可描述畫面、台詞或大約時間；如果沒有，也可以寫沒有。（開放回答）

## 主持人計分及原始答案模板（不要顯示給觀眾）

六題完整才計「合計：＿＿ /30」；實際範圍 **6–30**。缺任一題記 `INCOMPLETE`，不補值、不換算 /100、不對應 90 分規則。問卷不是正式驗收，腳本 90 分不代表影片好看。Q4 未到揭露為 NA，不是低分。

以下只有空白欄位，沒有參與者；每個實際匿名碼複製一份。不要填聯絡或可辨識資訊。

填妥的分派與答案只存主持人私密位置；全部回覆鎖定前不可放進公開 repo。鎖定後依方案揭露分派檔與 seed，再發布去識別結果。

```text
anonymous_code:
allocation_slot:
playback_code:
host_cut:                   # STILL / MOTION，僅主持人
assigned_at_Asia_Taipei:    # 必須早於 started_at
started_at_Asia_Taipei:
prior_H01_exposure:         # no / yes / uncertain；播放前篩選
master_hash_checked:
caption_hash_checked:
device_player_caption_settings:
conditions_or_deviations:
last_playback_time_s:
reached_3s:
reached_saved_29_533333s:
completed_39s:
exit_or_technical_interruption:
neutral_retell_verbatim:    # 「請用自己的話說剛才發生什麼」；不糾正
Q1:
Q2:
Q3:
Q4:
Q5:
Q6:
total_out_of_30:            # 只有六題完整；否則 INCOMPLETE
missing_items_and_reasons:
Q7_recalled_before_reveal_verbatim:
Q8_confusion_or_swipe_verbatim:
other_spontaneous_comment_verbatim:
spontaneous_continuity_mention: # mentioned / not mentioned；不提示
mention_verbatim_and_viewer_recalled_time:
host_QA_ID_after_answers:   # C1..C4 / T1..T6 / other / none mentioned
protocol_validity_and_reason:
redaction_note:             # 如原話含個資，用 [已移除個資] 置換
```

## 空白逐人結果表

| commitment hash（分派檔 SHA-256） | commitment date（Asia/Taipei）／公開紀錄連結 | 回覆鎖定時間／答案快照 SHA-256 | reveal date（Asia/Taipei）／揭露連結 |
| --- | --- | --- | --- |
| | | | |

| 匿名碼 | slot | 播放碼 | host cut | 程序偏離／有效性 | 最後秒數／看完 | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | /30（6–30）或 INCOMPLETE | 缺值原因 | 自發提及問題／原話索引 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | | | | | | | |

## 空白逐題摘要（預先固定格式）

分派 N：STILL ＿＿，MOTION ＿＿；實際觀看 N：STILL ＿＿，MOTION ＿＿；符合程序 N：STILL ＿＿，MOTION ＿＿。提前退出、技術故障及排除原因另列原始紀錄，不刪掉低分或不喜歡的回答。

| cut | 題目 | 有效 N | 缺值 N | 1 分人數 | 2 分人數 | 3 分人數 | 4 分人數 | 5 分人數 | 中位數 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| STILL | Q1 | | | | | | | | |
| STILL | Q2 | | | | | | | | |
| STILL | Q3 | | | | | | | | |
| STILL | Q4 | | | | | | | | |
| STILL | Q5 | | | | | | | | |
| STILL | Q6 | | | | | | | | |
| MOTION | Q1 | | | | | | | | |
| MOTION | Q2 | | | | | | | | |
| MOTION | Q3 | | | | | | | | |
| MOTION | Q4 | | | | | | | | |
| MOTION | Q5 | | | | | | | | |
| MOTION | Q6 | | | | | | | | |

完整問卷總分的 N／中位數／原始分布：＿＿。回述的因果理解與誤解（匿名原話）：＿＿。自發連續性提及（每 cut N／匿名碼／原話，不提示）：＿＿。結論：＿＿（可為 **INCONCLUSIVE**，不可改成正式 PASS）。不做顯著性檢定；目前全部尚未收集，不是零。
