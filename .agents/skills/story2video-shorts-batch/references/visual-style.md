# 頻道視覺規格

## CluePause

海龜湯、日常詭異和都市怪談的成片使用電影感寫實或接近真人質感的劇照，像同一部短劇的相鄰鏡頭。使用自然膚質、日常服裝、有使用痕跡的空間和尺寸可信的實物。以場景內的窗光、燈具或走廊照明建立光向和明暗，暗處仍保留線索可讀性。平面向量、卡通、商業 AI 人像或自動畫出的草稿插圖只供內部構圖，勿當缺圖替代品或列入可交 Owner 的成片。

**跨集共用視覺。** 每片從既有批次素材紀錄選同一版 CluePause 頻道參考，再另選本集參考。頻道參考使用已確認權利與用途的本機劇照，可各放一張日光與低光樣本，記路徑、SHA-256、版本和 Owner 是否已確認。首次或換版尚未確認時標為暫定，先沿用本頁文字規格。頻道參考只比對光色、材質與對比，本集選角、服裝、地點及道具另定。跨題型維持自然肉色、低飽和背景、實景燈具或窗光、可辨暗部。以穩定的色彩與對比呈現戲劇氣氛，線索需要的顏色保持原意。

先挑一至兩張代表性的參考鏡頭，例如交代人物與場景關係的建立鏡，以及看得清關鍵道具狀態的近鏡。把選定畫面和角色外貌、服裝、場景位置、光向、道具尺寸與方向寫入既有分鏡及參照資料，後續鏡頭沿用。建立鏡可用全景或中廣角交代位置，角色與道具用自然視角的中景或近景，連續動作維持視線、方向和鏡頭軸。核對手部接觸、握姿、臉和視線。需要辨認的號碼與符號用經核對的道具圖層或實拍，確認字形、方向和位置前後一致。

把角色看到的證據與實際操作拍進正片。直式構圖保留主體、手部與道具的可讀位置，依實見的 Shorts 介面預留字幕與控制項區域。英／繁中試看片字幕跨集沿用同組字體和字重，以清楚的無襯線淺字為主，亮背景用低調深色描邊或底色維持對比。避免大塊色底、跳字或遮住證據，保留既有雙語字幕交付。

### 可重用生圖提示

將固定風格和每鏡欄位寫進既有 `shots.json` 的 `prompt`，並用 `references.json` 保存重複出現的人物、道具和場景。以 `python -B "<pipeline>/static_storyboard.py" prompts "<job>"` 匯出實際提示與雜湊。素材工具支援參照圖且參照圖已備妥時，匯出命令加 `--supports-images` 以準備本集參照，再附上頻道參照並標明兩者用途。使用文字提示時保留相同的光色與連戲描述。

> Vertical 9:16 cinematic live-action mystery or suspense drama still, grounded photoreal or realistic semi-photoreal. Follow the channel look reference for the muted background palette, practical lighting and readable shadows. Match this episode's reference casting, wardrobe, set geometry, prop scale and light direction. Natural skin and hands, believable objects. Camera: [shot size, natural lens perspective, axis and eyeline]. Action and visible evidence: [who sees what, contact, state change, final position]. Keep the essential subject and clue clear of the observed player and caption overlays. Preserve the exact scripted prop text or symbol from the episode reference. No vector look, cartoon, commercial portrait treatment, editorial captions, watermarks or decorative lettering.

### 素材與交付

單片、批次及返修優先走 [CluePause 既有寫實分鏡與渲染路徑](handoff.md)。製片者先在既有分鏡與素材紀錄寫下頻道、參考鏡頭及各鏡實際使用的素材檔、來源和版本。送進 render 前，對照 `shots.json` 的 sheet、cell 和 crop，以及實際使用的動態片段、插入鏡頭和替換素材，確認每鏡素材存在、可解碼，且套用裁切後符合該鏡的內容與風格。通用 renderer 的結構驗證與技術 QA 只驗其可執行範圍。歷史上會自動補本機插圖的探索腳本限內部重現或草稿。遇到缺圖、拒絕、草圖、風格不合或無法核對來源時，沿用 HOLD 與缺項紀錄。補齊符合規格的素材後用原有路徑重跑，成片核對以該版 MP4 為準。

優先用已有權利、合用的本機素材或自攝畫面。需要另行生成時按本次核准的素材用途、工具與預算執行。風格確認只適用於當下的素材與版本。S07 的一般內部探索授權也使用上述 Owner 交付規格。不同風格的試驗限內部研究，若 Owner 明確為某片及某版指定例外，依其指定用途交付並逐片記錄。

## WhyNest Lab

依科學主張選實拍、可編輯向量圖解、實驗示範、動畫或混合形式。讓時間、尺度、視角、控制條件和因果看得清楚，標示示意或實驗限制。沿用既有事實、圖解、字幕及手機看片檢查。
