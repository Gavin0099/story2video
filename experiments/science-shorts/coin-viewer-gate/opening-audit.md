# WhyNest Lab 已公開 Shorts 開場抽查

抽查 10 支已公開影片對應的本機上傳原檔。每支查看 0.2、1、2、3、5 秒的畫面。觀察三件事：前三秒能否看到事件或對比、畫面有沒有支持旁白正在提出的問題、靜音時能否辨認變化。下表是製作端對首看的假設，真人停留與 YouTube Studio 留存待測。

兩張逐幀圖可在本機查看：[冰、天空、太空、吸管、硬幣](../../../artifacts/science-shorts/coin-viewer-gate/openings-1.jpg) · [金屬、紙、風乾、吸盤、書](../../../artifacts/science-shorts/coin-viewer-gate/openings-2.jpg)

| 成片 | 前三秒觀察 | 視覺上的待驗證假設 |
| --- | --- | --- |
| 冰 | 冰塊從杯口落到水中，已有可見事件。 | 「落下」很清楚，「停在部分露出水面的位置」值得檢查。 [上線版](https://www.youtube.com/shorts/a-tHhhJhNG8) |
| 天空 | 0.2 到 3 秒仍是同一個藍天構圖，5 秒切到光譜圖。 | 顏色醒目，開場多靠標題建立問題。 [上線版](https://www.youtube.com/shorts/EVWSVM3KBzA) |
| 太空聲音 | 兩個太空人和真空區持續到 5 秒。 | 空間配置容易辨認，聲音傳不過去這個對比仍主要靠文字。 [上線版](https://www.youtube.com/shorts/cezLqruPBzQ) |
| 吸管 | 先是飲料插畫，約 3 秒切到吸管圖，5 秒前後才顯示壓力標示。 | 首圖交代物件，尚未交代飲料何時被推動。 [上線版](https://www.youtube.com/shorts/cHh2x9hWWDs) |
| 硬幣 | 0.2–2 秒俯視圖已看見硬幣。約 3 秒才切到光路遭杯緣擋住的剖面。 | 首圖跟「硬幣被擋住」的旁白打架。固定視角的倒水揭露能否改善首看，適合做第一輪 A/B。 [上線版](https://www.youtube.com/shorts/NsZLF8Qeryo) |
| 金屬 | 先交代尺和木頭，接著並排顯示手指與兩種材質。 | 比較對象一目了然，溫度感受差異難從首圖看出。 [上線版](https://www.youtube.com/shorts/sbYYwZ5dvog) |
| 紙 | 展開與揉皺的紙從首圖就能比較，約 3 秒的下落圖有位置差，到 5 秒有先落地的結果。 | 已具備「同樣材料、不同結果」的視覺問題，可當作後續設計參考。 [上線版](https://www.youtube.com/shorts/_Ab2h9g4zhE) |
| 風乾 | 先看見晾衣，約 3 秒有靜風與送風對照，抽查至 5 秒兩側藍色濕區輪廓相近。 | 風向標示易讀，需等較後的變化才能從畫面判斷哪件乾得快。 [上線版](https://www.youtube.com/shorts/Gnjv-OT0LHA) |
| 吸盤 | 首圖有手拉吸盤，約 3 秒的圖解已標出拉力方向。 | 動作清楚，首看能否看出吸盤「被拉但仍貼住」待測。 [上線版](https://www.youtube.com/shorts/eeoDtRKgBsk) |
| 書 | 先看手推書，2–3 秒切換到書與桌面圖解，5 秒放大接觸面。 | 日常動作易懂。「手離開後書繼續滑、然後停」可作為日後有需要時的測試方向。 [上線版](https://www.youtube.com/shorts/sqMni_nnJ3k) |

可重用的工具

- 已有的真人首看流程可以沿用匿名與獨立試看方法。 [本 repo 的 Shorts Viewer Gate](../../story-quality-lab/shorts-viewer-gate.md)
- jsPsych 可做分派、記錄試驗反應和播放影片。有多支影片或需要跑正式研究時可考慮接入。滑動離開需自行實作。 [jsPsych repo](https://github.com/jspsych/jsPsych) · [影片反應插件](https://www.jspsych.org/v8/plugins/video-button-response/)
- PySceneDetect 能批次找轉場，適合先篩出長時間沒換情境的開場。張數或切點數無法估計觀眾理解或停留。 [PySceneDetect 文件](https://www.scenedetect.com/docs/latest/api/detectors.html)
- vidIQ Retention Analysis 可在有可讀的頻道數據後，把留存變化與成片時間點對照。 [vidIQ skill](https://vidiq.com/agent-skills/vidiq-retention-analysis/) · [YouTube 留存文件](https://support.google.com/youtube/answer/9314415)

