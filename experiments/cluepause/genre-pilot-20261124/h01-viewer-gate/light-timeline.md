# H01 v2.1-r1 共用燈號時間表

Owner 本輪只授權燈號修正。A 與 B 都讀 [light-timeline.json](light-timeline.json)，沒有各自的狀態表或時間偏移。以下為該設定的閱讀版；區間皆為左閉右開、30 fps、零起算影格。腳本來源為 `codex/cluepause-genre-pilot-v3-20261124` 的 `urban_horror-v2.1.md`，來源 commit `fe2ce6abd4c3ec1d8537850557077a1abd7c930e`，原始 bytes SHA-256 `83df72c03352d74ceb6977bcc665f0d6a715e37fae0ad10b81f6e1e8720c7bce`，與凍結 shared 腳本相同。

腳本 7–12 秒明定 steady listening light；16–20 秒要求兩次 live sound indicator pulse；26–28 秒再次明定 steady listening light；28–31 秒要求先 INPUT、後 SAVED。其他等待窗的持續亮燈是從「等待第一次回覆且未關機」推導的連續狀態，不是假稱腳本逐秒規定亮度或色碼。`standby` 在此指裝置正在聆聽但尚未收到第一次回覆，`listening` 指正在收取 Nia 的回覆；兩者都常亮綠燈。`saved` 沿用既有綠燈與 SAVED 螢幕，沒有新增顏色規則或提前揭露。腳本沒有要求熄燈；不在畫面內不能判為 off。

| 秒數 [start,end) | 影格 [start,end) | 狀態（兩版共用） | 燈號／理由 |
| --- | --- | --- | --- |
| 無 | 無 | off | 沒有腳本支持的熄燈時段；鏡外只記 unobservable。 |
| 0–18 | 0–540 | standby | 常亮；可見鏡頭保持等待第一次回覆。 |
| 18–18.2 | 540–546 | standby + cough 1 | 常亮燈芯，光暈增亮；不關閉聆聽。 |
| 18.2–18.3 | 546–549 | standby | 回到常亮。 |
| 18.3–18.5 | 549–555 | standby + cough 2 | 同第一個脈衝；兩次均保留原成片的量化時間窗。 |
| 18.5–28 | 555–840 | standby | 回到常亮，包括原 C2 的 21.6–28 秒與 26–28 秒 hold。 |
| 28–29.533333… | 840–886 | listening | 常亮，沿用既有 INPUT／完整拒絕句五格；不改讀字時長。 |
| 29.533333…–39 | 886–1170 | saved | 常亮，沿用既有 SAVED 首格及開閂順序。29.517875 秒重播音訊的下一個可用影格為 f886。 |

燈可見範圍：`[21,210)`、`[240,330)`、`[360,420)`、`[537,600)`、`[648,904)`，每版共 658 格。其餘 512 格燈在鏡外，保持整格不變；包括 31–39 秒未拍到燈的已知構圖限制。狀態表仍涵蓋全片，不把鏡外 saved 狀態宣稱為可見證據。

兩次光暈脈衝各以首格作 smoothstep 的常亮端點，下一格達增亮值，窗口結束立刻回到常亮；因此 f540／f549 為漸亮起點，f541–545／f550–554 為較亮光暈。燈芯全程亮著；JSON、逐格 CSV 與 A/B 都使用這個相同定義。

燈位註冊在 JSON，以原始 1080×1920 plate 為座標；每格套用原來的 1.015→1.035 zoompan／逐鏡重置，B 的 flinch 另反解原 120-pixel mesh 的局部位移。寬景與特寫保留原有外殼差異，不修正 C1。光暈使用 `hybrid_motion.stage`，亮度過渡使用 `hybrid_motion.progress` 的 smoothstep，燈罩紋理重用既有 `indicator-element.png`，沒有 ImageGen、AI 修圖或重建場景。B 原咳嗽燈層的亮／暗結果只在燈區內被共用狀態覆蓋，保留鏡頭其餘像素。

重跑與輸出雜湊見 [freeze.md](freeze.md)，逐格結果與限制見 [temporal-qa.md](temporal-qa.md)。
