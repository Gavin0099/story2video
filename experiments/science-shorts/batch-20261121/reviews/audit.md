# 科普三支 pilot：獨立事實與科學圖解審查

審查者：`/root/fact_visual_audit`；模型：inherited native agent（API未提供精確版本）。這是 AI 獨立審查，不是真人、領域專家或觀眾驗收。未取得 tokens／成本資料，沒有估算或杜撰。

目前九個核心主張及 29 組英中台詞均為 **SUPPORTED**；兩項圖解阻擋缺陷已修正。允許進入本機配音及影片製作，前提是兩位獨立理解讀者也各自達到 gate-policy 的門檻。這份記錄不授權上傳、公開、建立頻道，也不代表最終 MP4 或市場通過。

完整逐主張來源、逐句限定詞與因果判斷、訪問結果和缺陷歷史，見 [fact-visual-v1.json](fact-visual-v1.json)。

| 集數／主張 | 判斷 | 兩個獨立機構與定位 |
|---|---|---|
| ice.c1：普通冰排列更開放、規則 | SUPPORTED | [USGS](https://www.usgs.gov/water-science-school/science/water-density)「Ice is less dense than water」，L59–68；[IAPWS](https://iapws.org/faqs/faq1)「Why does liquid water have a density maximum?」，L177–192 |
| ice.c2：同質量、更大體積導致較低密度 | SUPPORTED | USGS L27–33 的密度定義與 L67；IAPWS L180–191 的凍結膨脹與密度結果。固定質量的結論亦是密度定義的數學推論。 |
| ice.c3：密度較低而浮在液態水上 | SUPPORTED | USGS L59–68；IAPWS L188–191，兩者皆直接連結密度與浮起。 |
| sky.c1：白色陽光包含多種可見色 | SUPPORTED | [NASA Space Place](https://spaceplace.nasa.gov/blue-sky/en/) L26；[NOAA/NWS](https://www.weather.gov/fgz/SkyBlue) L161–164 |
| sky.c2：空氣分子散射藍光強於紅光，側散射進眼睛 | SUPPORTED | NASA L33–43；NOAA L165–168。只接受藍與紅的比較，沒有主張藍比紫更強。 |
| sky.c3：日落路徑更長，直射光相對更紅 | SUPPORTED | NASA「What makes a red sunset?」，L50–57；NOAA「So why are sunrises and sunsets red?」，L170–171 |
| space.c1：聲音需要物質介質，理想真空不傳聲 | SUPPORTED | [NASA EM anatomy](https://science.nasa.gov/ems/02_anatomy/) L241–244；[ESA LISTEN UP!](https://www.esa.int/articles/about-us/directorates/science/listen-up) L201 |
| space.c2：無線電是電磁波，可穿過真空 | SUPPORTED | NASA EM anatomy L247–249 及同機構 [Radio Waves](https://science.nasa.gov/ems/05_radiowaves/) L242–247 合併支持；ESA L202 獨立支持。NASA 兩頁只算一個機構。 |
| space.c3：接收設備透過喇叭轉回局部可聽聲音 | SUPPORTED | NASA Radio Waves L247；ESA L202 |

以上一手機構頁面均實際開啟並讀取相關段落，屬機構自有科普資料，不是原始研究論文。NASA Cosmicopia 的舊 URL 兩次 `web.open` 都回報 `(400) Timeout fetching`，因此不列入已核實證據。主代理已將 space.c2 改用可讀取的現行 NASA 頁面並補上 Radio Waves 來源卡；旁白、字幕、所有 cues 與 visual_constraints 沒有改寫。來源卡仍保留舊卡不代表本審查認可其內容或成功讀取狀態。

必要限定詞均保留：冰為日常壓力的普通水冰，不能擴及所有固態或其他冰相；天空為地球晴朗白天天空，且日落只是同一散射機制的選定例子，沒有涵蓋每一種夕陽、氣膠或色覺問題；太空為理想真空且沒有繩索或共享固體的間隔，艙內及頭盔內仍可有聲音。「same amount／同樣多」先口語表達，後面英中都明確收斂到 same mass／同樣質量。逐句未見英中限定詞流失、顛倒因果或把不確定性改成確定。

初次圖解審查為 **BLOCK**。太空篇的 AIR 分子小圖原本正好占據兩名太空人之間，同時又標示真空；主代理已將小圖移到兩人下方獨立框，中央保持空白並標 VACUUM GAP。重新開啟 space-3.png 核實。接收端也補上喇叭、局部空氣、耳形與 speaker → air → ear，再開啟 space-8.png 核實。

其後代碼審查再度 **BLOCK**：夕陽散射箭頭向上，藍光脈衝卻隨時間向下且不在線上。現改為 `phase=(t*.4+x*.001)%1`，位置 `(x+20*phase,730-130*phase)`，在每次循環內沿箭頭從直射路徑向外傳播。這是從凍結代碼確認，尚未宣稱看過實際 MP4 動畫。首次缺陷與修正前後 SHA 均保留在 JSON 歷史。

冰的比較使用兩組各九點、相同大小，只有排列及占用範圍改變，沒有以分子變大或加空氣解釋膨脹；浮冰大半浸水。天空使用並行混色入射光、分子散射點、側散射到眼睛與另一條直射紅光路徑；日落在同一層大氣內呈現較短與較長路徑。程式圖解有 schematic／not to scale 標記，不能從點數、線數、面積或路徑長度讀取物理比例。

畫法保留限制：冰的點陣只代表排列，並非二維冰晶模型；大氣採平面示意層，省略 storyboard 的地球曲率及完整分割收尾；沒有完整六色光譜小圖。這些屬分鏡實現的簡化，核心因果仍成立。聲音以局部粒子振動表示，無線電以電磁波線條及文字區分；實作配色與文字分鏡不同，但沒有僅靠顏色辨識機制。程式未讀取來源網站圖像；配音模型、字型、音訊與商業發布的權利不在本次科學圖解審查範圍內。

工程驗收與市場驗收分開：本次只完成製作前的內容／圖解 gate，未執行 README 的 pytest、npm 或治理命令，也沒有改動正式 Episode、SQLite 或 src。主代理仍須留下整體工程驗收命令、結果及未驗證範圍。本次預覽只是實際繪圖函式加暫估時間的 PNG，不能證明 TTS 自然度、字幕同步、動態播放、手機可讀性或影片規格。最終 MP4 仍需重審，五位首次真人的機制重述驗收、另行授權的公開測試及 D7/D28 市場證據均未完成。AI 的 85 分門檻不構成科學證據或市場成功。

Git HEAD：`2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`。目前腳本 SHA-256：`d0b7de7d7ac4c1aa9986840999721c83735fea615703b0ba3479648f00a73cf8`。最終 renderer SHA 與來源卡 hash 以 JSON 的凍結欄位為準。實際檢查包含 PowerShell `Get-Content`／`Get-FileHash`、`git rev-parse HEAD`、機構網頁開啟與定位、以及 PNG `view_image`；本審查者沒有生成配音或影片。

2026-11-21 timing-only 補審：主代理實測舊版 sky 語音加停頓只有 44.73 秒，低於 45 秒下限，已正常阻止影片生成。逐欄遞迴比較新舊 JSON，只見 revision、timing_change 說明及 sky 最後一個 cue 的 pause 從 0.8 變 2.1；英中台詞、來源主張、scene、claim_ids、visual、visual_constraints 及其他所有停頓都相同。renderer 仍為 `432700a6bc30e8295ccaeda13c98599c66335b888a704df202e065853cedd1d8`。增加的是 39 格／1.3 秒非語音收尾 hold，沒有加速語音或改寫科學內容，因此沿用既有來源及理解評分；預估 sky 46.03 秒仍須重製後實測。原 audit 以 `fact-visual-v1-pre-timing.json` 原樣保存，新結果另有 `timing-only-review.json`。已有 ice 舊版影片不作為新 batch 的最終證據，成片抽驗待重製及新 provenance。

