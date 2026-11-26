# 從選題到 Owner 看片

從[目前 checkout 的批次 Skill](../../.agents/skills/story2video-shorts-batch/SKILL.md)選頻道和作品。製片者負責選題、改稿、找素材、分鏡、合成與檢查。Owner 收到可播放的版本，只需指出哪裡不好看，可附時間碼。調整同一支片最多兩輪。公開決定綁定片名、版本、頻道與實際操作。[Issue #32](https://github.com/Gavin0099/story2video/issues/32)

| Slice | 本次交付與可核對範圍 |
| --- | --- |
| S00、S07 能力與版本 | [可重用工具及分支](capabilities.md)涵蓋製片機、乾淨 checkout 和成片紀錄。新 Codex 程序在本工作樹能找到 repo 版批次 Skill。其他分支要先取得該版本。Claude 的自動載入及新機重建仍待實測。 |
| S01 現有影片 | [60 支公開 Shorts](public-shorts.csv)，CluePause 40 支、WhyNest Lab 20 支。這份快照可按影片 ID、發布時間、擷取時間及來源驗證；後續的可見性與觀看數可能變動。 |
| S02 外部方法 | [16 個固定版本候選](external-methods.md)記錄授權、適用範圍、成本與採用取捨。[9 支公開對標](peer-sources.md)記錄格式、對照組、取樣方式和片齡差異。 |
| S03、S04、S05 創作 | [四種題型](../../.agents/skills/story2video-shorts-batch/references/editorial.md)提供編輯前後、開頭選擇、雙語示例及線索與揭曉的銜接。範例的估時在取得同版配音後換成實測時碼。 |
| S06、S08 成片與修正 | [逐片交接](../../.agents/skills/story2video-shorts-batch/references/content-workflow.md)把稿件、可見證據、聲軌、字幕、播放檢查、修正意見連回同一版本。先做 Owner 可看的本機輸出，正式品質與權利要求依原流程查核。 |
| S09、S10 批次與市場 | [製片與數據交接](../../.agents/skills/story2video-shorts-batch/references/handoff.md)供各片在獨立目錄並行。每日上限 10 支，初始分配為 CluePause 6 支與 WhyNest Lab 4 支。七天試行須累積實際合格數、失敗、人工時間與成本才可判斷產能。 |
| S11、S12 營運與進階動畫 | 完整閉環待取得新版本的 Owner 決策及公開後資料。進階動畫保留於 [#27](https://github.com/Gavin0099/story2video/issues/27)，有具體鏡頭瓶頸再做小範圍比較。 |

## 如何重查公開快照

2026-11-26（Asia/Taipei）逐一讀取兩個頻道公開 Shorts 清單的影片 ID，以各列的 watch 頁重新核對 `channelId`、標題、影片長度、累計觀看和平台發布時間。匯出只包含公開頁欄位。以 `video_id` 核對一支實際上架的剪輯，同一故事的不同剪輯分別保留。花瓶與濕鞋兩題已有公開版本，安排新片時需納入排重。[花瓶](https://www.youtube.com/watch?v=DyJQGUIlH0E) · [濕鞋](https://www.youtube.com/watch?v=tdpt2le3S68)

不同片齡的公開累計數不能用來判定哪個開頭較有效。比較內容時，在 Owner 的本機資料以頻道和相同片齡選片，對照實際剪輯與可取得的流量來源、續看、平均觀看與互動。空白欄保留缺值，時窗未到期的列待補。最新 Studio 明細由 Owner 在本機保存。
