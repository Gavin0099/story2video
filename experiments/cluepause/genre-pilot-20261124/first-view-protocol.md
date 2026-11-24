# Private first-view protocol — HUMAN_TEST_PENDING

這是一份未執行的私人首看設計，可與 S3 共用「三秒停止」及「完整不中斷」兩測試的概念。此處 Test A/B 指**不同觀察任務**，不是剪輯版本 A/B 或兩個實驗處理；不聲稱已核對某份 S3 執行紀錄。本次沒有成片、招募、播放或真人資料。

## 樣本與分派：每片合計 3–5 位

每片以 **5 位**為優先：Test A 兩位、Test B 三位；若只能招募三至四位，事前選定 A 一位、B 兩至三位，合計仍為 3–5 位，僅作更弱的診斷。不能看完再挑五位。A 與 B 對同一故事必須是**不同真人**；看過腳本、任何剪輯、題卡、透露答案的群聊或 A 片段者，都不能計入同一故事 B 的首看。

可同一人看其他全新故事，但須平衡順序並記錄跨片曝光；為減少 genre 順序影響，優先各片不同人。每人隨機分派 A 或 B 並保留分派順序，以匿名代碼保留原話，勿把帳號或聯絡資料放入 repo。不得要求招募者看本目錄含解答文件。

這個配置不提供五位完整觀看者。既有 puzzle 90 分規則不變；若依既有五人完整首看規則判定，B 少於五人就**保持待驗**。未來在另行核准的補驗安排下，可以同一凍結版本為 B 補足兩位全新觀眾；A 人員不可補入。保留原三位 B（含主動退出者）而非換掉不利回答，累計首五位有效 B 依原門檻判定。補驗會使該片總招募超出本輪 3–5 人，須明記為後續補驗，不能假裝屬於本輪樣本。若改版，重新使用未曝光觀眾，不混用版本。

## 播放前固定條件

未來取得製作與私人試看授權後，先凍結各片 revision、腳本及實際 MP4 SHA-256、時長、字幕版及測試日期；本次不能以文字目標時間充作實片時間碼。主持人先寫下該片異常辨認、核心因果／衝突與各線索的判讀口徑，參見三篇稿及 [gates.md](gates.md)。新 genre 的判準須在收樣本前核定，不能看結果再調。

以中性代碼交付，例如 41K、73H、26M；觀看者不先知道 genre、片名、假設、作者希望的解答或評分。三片同樣手機直式、英文旁白＋已開啟繁中字幕、相同音量／耳機條件；記裝置、語言理解背景與實際設定。fiction 標示保留，不做假新聞盲測。可隨時停看，無須給作者面子；不承諾測試者會看完。

主持人中性開場：「請像平常看短片一樣看。你可以隨時停止，之後我會問你看見什麼。沒有必須喜歡或猜中的答案。」A 組另說「這次會在三秒停止」。不預告異常位置。

## Test A — 3 s stop

1. 從實際成片 0:00 播至 0:03.000 後停止；不展示後續縮圖、進度預覽、檔名答案或解答題卡。不把暫停造成的未完播算主動滑走。
2. 先問「剛才有什麼不尋常？」逐字記錄；再問「你接下來想知道什麼？」及「你會想繼續看嗎，為什麼？」不問帶答案的「你有看到指針下降嗎」。
3. 記是否主動描述預定異常、其他觀察、不記得／未答、繼續意願及理由。A 無法量測自然三秒留存，也不能得知揭曉是否公平。只有兩人時報 0/2、1/2 或 2/2，不單報百分比。
4. 收完前不提示或重播；若之後應本人要求看完整片，可另記為已曝光的編輯回饋，永不升格同故事 B。

## Test B — full uninterrupted viewing

1. 換未看過 A 或故事的人，從頭正常播放一次。主持人不暫停、不問中段猜測、不倒帶、不解說；可由觀眾主動退出。
2. 先記行為：是否自願退出、退出／最後觀看秒數、是否自行重播、是否到達預先標定的 first clue / key clue / reveal。不能把播放到結尾當作已理解；缺精確記錄時填未量測。
3. 播完或退出後，先問「這支在講什麼？你怎麼理解剛才發生的事？」與「哪裡想繼續看、哪裡想停看？」收完原話，再依 gates 的 genre 問題追問。不能要求「先猜對再看結尾」。
4. puzzle 問核心因果、證據、理解改變及反轉趣味；uncanny_mystery 問回想的合理首猜、揭曉如何重解異常；urban_horror 問不安起點、主要衝突、結尾兌現、是否會看另一篇。B 的首猜是**事後回想**，不得當作揭曉前鎖定的預測。
5. 先保存原話、未答與不確定，再由主持人依凍結口徑編碼。若之後提供提示或答案，另記提示後理解，不改寫初次原答。

## 有效樣本與缺漏

自願退出屬有效負向／中性觀察，不排除。播放器故障、字幕未照設定顯示、先前曝光、主持人提示、誤派任務或非首看重播等場次全部留存，明記技術／程序排除理由；排除人不計理解分母，可用新觀眾按事前規則補足。A 的預定暫停不算故障。若首看後自行重播，保留首輪行為，重播後新增理解另欄，不能替換首輪理解。

報有效 N、已答 N、退出 N、排除 N 及原因；理解同時報「符合口徑／已作答」與「符合口徑／有效 B」。只用 A 的分母報異常辨認，不混 A/B。拒答不是猜錯，保留缺漏；有效退出或拒答不能拿新觀眾替換到數字好看。小樣本保留 INCONCLUSIVE，不做顯著性或市場需求推論。

## 每片複製的空白首看表

以下三張表全部未填，破折號代表待填，不代表零、否定或通過。每位受試者複製一張「個人原始紀錄」。完整原話保存於日後同目錄的匿名原始紀錄，不只摘選正面語句；本次不虛構回答。

| 片別 sheet | P01 / puzzle | U01 / uncanny_mystery | H01 / urban_horror |
| --- | --- | --- | --- |
| 中性播放代碼 | 待隨機分配 | 待隨機分配 | 待隨機分配 |
| revision / script hash / MP4 hash | — / — / 未製作 | — / — / 未製作 | — / — / 未製作 |
| actual duration / anomaly / key clue / reveal | 全部待實片核對 | 全部待實片核對 | 全部待實片核對 |
| 事前 A/B 配置 | 2 / 3（提案） | 2 / 3（提案） | 2 / 3（提案） |
| A 異常辨認口徑（主持人） | 金料沒少，秤指針下降 | 鎖住的鞋櫃滴水／鞋底又濕 | 對講機自行要求最後兩字 |
| B 因果／衝突口徑（主持人） | 線下拉盤多算重量，剪斷移除拉力 | 定時澆水管裂口使盤積水，非夜間穿鞋 | 想拒絕入侵，截句保存 COME IN 造成解鎖；不是唯一猜法考題 |
| A valid / B valid / exclusions | 未收集 | 未收集 | 未收集 |
| raw answers location | 待私人測試後建立 | 待私人測試後建立 | 待私人測試後建立 |
| 人類狀態 / 判定 | HUMAN_TEST_PENDING / 待驗 | HUMAN_TEST_PENDING / gate PENDING | HUMAN_TEST_PENDING / gate PENDING |

### 個人原始紀錄（每片、每人各一份）

| 欄位 | 原始值／逐字原話 |
| --- | --- |
| story ID / neutral code / revision / hashes | — |
| anonymous viewer ID / date + timezone / allocation order | — |
| Test A or B / prior exposure screening / other clips and order | — |
| device / audio / subtitle / language familiarity | — |
| started / ended / voluntary exit time / reached beats | — |
| playback fault / prompts / replay / validity + exclusion reason | — |
| A：什麼不尋常？接著想知道什麼？願否繼續及理由 | — |
| B：開放重述與理解、想繼續／停看處 | — |
| B puzzle：因果、證據、理解改變、趣味及理由 | — |
| B uncanny：回想首猜及依據、揭曉如何重解異常、未解處 | — |
| B horror：不安起點、主衝突、結尾兌現、續看意願及理由 | — |
| unanswered / uncertain / later prompted feedback（分開保留） | — |
| moderator coding / quoted basis / reviewer + date | — |

### 每片彙整（與原話分開）

`frozen version | recruited | valid A | A anomaly n/N + missing | valid B | answered B | voluntary exits + seconds | excluded + reasons | B cause/conflict n/answered and n/valid | payoff raw responses | watch-another raw responses | disagreements | missing evidence | decision + owner/reviewer/date`

判定可為待驗、需修稿、INCONCLUSIVE，或在適用規則核定且證據齊全後「值得申請公開測試」。私人通過並不是市場需求證明或公開授權。即使全部私人 PASS，每個公開步驟仍須另獲明確 Owner 授權。
