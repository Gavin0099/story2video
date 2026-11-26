---
name: story2video-shorts-batch
description: Plan and deliver a batch of original or rights-cleared classic CluePause Shorts, verify its YouTube publication count, and compare first-day viewing and likes. Use for adding films to a target count or following a batch through story rights, production, and performance. Also use for developing CluePause puzzles, uncanny mysteries, urban horror and WhyNest Lab science Shorts through a versioned editorial or production handoff.
---

# story2video Shorts 批次製作與成效

先讀 story2video 的 `AGENTS.md`、`PLAN.md`、最新批次交付與發布紀錄。以本次指定的頻道、作品及授權執行。續做前從同一批的證據和影片 ID 恢復。

若同時發現 repo 與個人同名 skill，Issue #32 使用目前 worktree 的 `.agents/skills/story2video-shorts-batch/SKILL.md`。記錄 Git SHA 與實際入口 SHA-256。選題、雙語編輯、開場、分鏡、Owner 看片或小批交接，從 [創作與製片交接](references/content-workflow.md) 開始。只核對數量或有獨立發布授權時，依下方原先對應的步驟。

開始各階段前，先讀取該階段引用的 skill。按名稱從專案或使用者已安裝的 skills 尋找。缺少所需 skill 或隔離評分程式時，先完成可獨立驗證的階段，記下待補項目和該階段狀態。

## 定義交付數量

- 從 YouTube Studio 的 Shorts 清單核對指定頻道和實際可見性。對上批次的作品代碼、成片版本與影片 ID。把已公開、已上傳待試看、已成片待上傳、尚未完成各自計數。排除重複上傳、A/B 測試及批次以外的草稿。總成片數由唯一作品相加，頻道公開數由 Studio 核對。使用者只說「做到 N 支」時，依對話確定累計或新增，並說明採用的口徑。
- 發布授權綁定使用者指到的作品。交付新作品時依既有私人試看流程，等使用者另行核准該批公開。最新要求只是核對數量時，讀取實際狀態並回報。

## 從題面到可播放成片

1. 委託 Writer subagent 構思原創稿。優先挑一眼可理解的反常動作、一個能改變解釋的前提，以及揭曉前在畫面或聲音能辨認的關鍵線索。情感誤解、逐步升級懸疑、純推理可當比較組。異常升級用場景或動作改變，情感則在解答後用可見的選擇收尾。可研究別片的節奏與公開成效，故事、人物及道具設計自行創作。若使用 Story Quality Lab 的 Classic Puzzle Benchmark，只把抽象機制交給原創稿 Writer。若是經典特別企劃，先查證特定來源版本的公共領域或商業改作授權。
2. 依 `story-quality-autoloop` 隔離三位新讀者分段盲評。每位至少 90 分、核心均有線索支持且無關鍵缺陷，才通過故事品質。製作批可使用多個編輯輪次，各自遵守 AutoLoop 的回合、讀者及單篇上限。每篇沿用原本的凍結稿、逐輪讀者紀錄與雜湊，達到單篇上限就換故事。作者自評單獨保留。當次只要求寫稿或評分時，交付候選稿。
3. 製片前完成 [Story Rights Gate](references/story-rights.md)，逐篇對應凍結稿 SHA-256。權利待授權、待確認或拒絕的題目限內部研究。使用者已要求製片時，將同時通過故事品質與權利查核的凍結稿移交製作。
4. 依 `shorts-viewer-gate` 製作。將一句鉤子對到開場鏡頭，讓證據和結果可以直接被看見或聽見。用實際英文配音排時間軸，保留思考節拍。依 PLAN 輸出 9:16、1080×1920、30 FPS、30–60 秒。交付英文旁白母片、英／繁中 SRT 及方便試看的繁中燒錄版或雙字幕 MP4。逐集核對變化前後的角色、重要道具、音效與字幕。保留素材、成本、版本雜湊、命令和驗收。
5. 文字分數、媒體 QA、真人單次首看、公開後觀看數據各有自己的證據。首看測試只給從未接觸同稿的觀眾對應 MP4，保留原話與版本。照已有門檻判斷，沒有足夠真人樣本就記待驗。

## 上傳與重新核對

上傳前比對成片和雙語稿的權利紀錄。稿件、來源素材或用途變更時，重審受影響的範圍。發布前確認署名及其他條件已履行。

依 `story2video-youtube-studio` 用已登入的 Chrome。每次變更前確認頻道及影片 ID，新片先私人。每支影片使用英文來源及繁中在地化標題、說明和兩條可切換字幕。保存影片 ID、成片雜湊、雙語與高畫質處理驗收、實際可見性及本次授權。套用明確公開授權後重新開啟影片詳情和頻道清單核對，記實際發布時間與時區。

Studio 顯示每日上傳上限時，記下原文、時間、待上傳代碼及現有 ID，停止本輪新增上傳。已產生 ID 的影片從既有紀錄補做可行欄位。無 ID 時回到正確頻道確認沒有草稿，記下依平台提示的重查時間。上傳額度到點後先用一支已驗收的成片試一次，成功再接續同批；仍達上限時照實保留待辦。分開給可看的 YouTube 連結和本機成片連結，公開數按當下 Studio 核對。

## 首日及後續成效

依 [首日觀察](references/first-day.md) 統一片齡紀錄。使用者要觀察一天時，算出每支實際公開後滿 24 小時的時間，在同一任務等到該時窗並擷取已可用的數據。報表處理中時標明具體欄位，保存已取得的數字、擷取時間和重查時間。
