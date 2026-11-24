# 下一次 H01 的共用 reference library 規格

**SPEC ONLY / NOT IMPLEMENTED / HUMAN_TEST_PENDING**。2026-11-24；基準 HEAD `e189e294a09120588006885ddbe40ac837928c34`。不生成圖片、不修正或重渲染已凍結的 STILL／MOTION。下列是下次另行授權製作時的候選規格，尚未建立 library、canonical multi-angle sheets、比對工具或通過檢查。既有圖片有矛盾，不能因列入候選就宣稱已成為一致 reference。

## 候選來源（本次只讀及核對 SHA-256）

下表每項 path 都以 repo 根目錄為基準；PNG 是既有 plate／element，不是新抽幀生成的 reference。`R*` 可供後面的規格表引用。影格對照見 [temporal-qa.md](temporal-qa.md)。

| ID | repo-relative source path | SHA-256 | 候選用途／排除範圍 |
| --- | --- | --- | --- |
| R1 | `artifacts/genre-pilot-20261124/h01-v2.1/shared/plates/uncovered.png` | `753cc1b126539d12df2a16b28f94caedc7da8c02b21e8115af60c7a748db8eec` | Nia 臉、鬆捲髮輪廓、衣服；旁邊窄對講機不可作 prop canonical。 |
| R2 | `artifacts/genre-pilot-20261124/h01-v2.1/shared/plates/mother-nearby.png` | `eff0ea1724758b8a51b5901503abe0a408d454d5db40bae35587b61a677b2046` | 室內位置、木門、母親／沙發／暖光；對講機比例不是 canonical。 |
| R3 | `artifacts/genre-pilot-20261124/h01-v2.1/shared/plates/intercom-plate.png` | `70b69906c5faa080af9c68b87787b404d2131a9d444b2fd77346d9a87abb3d00` | 對講機外殼、橫向螢幕孔、單燈、格柵；底圖燈暗不是待機 reference。 |
| R4 | `artifacts/genre-pilot-20261124/h01-v2.1/shared/plates/device-rules.png` | `a190ec4d95720c15ca10b6beeaaa9feb920f827fda1466d1a9c385e6acc52490` | 螢幕 RULES 排版與亮燈候選。 |
| R5 | `artifacts/genre-pilot-20261124/h01-v2.1/shared/plates/device-saved.png` | `69f0e8549f3bdcfdb29d494489cdbbd4b632b997e5f65d5c94943a4ec9fefff7` | SAVED 排版候選，不能替代 input 全狀態。 |
| R6 | `artifacts/genre-pilot-20261124/h01-v2.1/shared/plates/indicator-element.png` | `5a1cc7dc58805226a21dee3a54867e22c1e5ce00a79e4fae9f920597bf61fe58` | 單一聆聽燈圖層候選；安裝位置須綁 R3。 |
| R7 | `artifacts/genre-pilot-20261124/h01-v2.1/shared/plates/latch-hold-static.png` | `71e4c17aa1271a56f26324789770e7f30217c327f8daf795663f16af302e7b30` | 薄矩形鎖舌扣住的幾何。 |
| R8 | `artifacts/genre-pilot-20261124/h01-v2.1/shared/plates/latch-plate.png` | `efd0f050c1291b4c7c14dbb5c427f0bffd23c6f93f0647a93c099d2fbe3828ac` | 同門閂縮回底圖／固定 strike，須與 R7 綁同一座標系。 |
| R9 | `artifacts/genre-pilot-20261124/h01-v2.1/shared/plates/handle-element.png` | `35d012368319c66c1b39cca8ef7cf965019ce64f0ae41111209d8f52cb91abcf` | 把手本體元素；不能只用拆掉把手的底板當完整把手 reference。 |
| R10 | `artifacts/genre-pilot-20261124/h01-v2.1/shared/plates/handle-plate.png` | `9af370badfd2a4e93a5e6647ab06168b2387534c8d137e1d8db4590fa3d5e9dd` | 圓底座、門紋、把手軸位置，與 R9 合用。 |
| R11 | `artifacts/genre-pilot-20261124/h01-v2.1/shared/plates/brace.png` | `6e1c8c7817bfeaf6bd6ded70f877eb7e8fea71a9a60f1e70df26fac864780645` | 門右側黑暗窄縫、室內位置；髮髻不可與 R1 混成角色 canonical。 |
| R12 | `artifacts/genre-pilot-20261124/h01-v2.1/shared/plates/foot.png` | `189e1ac7bf161c385b7c05dbaa78fe035640ff67d9f34a4ea8eac603035b24bc` | 深色褲／淺色鞋、木地板與門縫候選。 |
| R13 | `artifacts/genre-pilot-20261124/h01-v2.1/shared/plates/device-input-wait.png` | `e29153b309ebb75811cc261931956d1e4ba694f4ae71cd215a0e29578d9b7524` | INPUT 等候狀態候選。 |
| R14 | `artifacts/genre-pilot-20261124/h01-v2.1/shared/plates/device-input-prefix.png` | `2a17baf448c52b63dd87845f1f3602540c5e42e18e837b5cb2bcaebdc8ae0a6f` | INPUT prefix 狀態候選。 |
| R15 | `artifacts/genre-pilot-20261124/h01-v2.1/shared/plates/device-input-full.png` | `72a02a63bc317cd8c9e8de07744ac9377df5418d5c1a7ab865f5bc9b65af6c92` | INPUT 完整拒絕句狀態候選。 |

## 每項資產的 invariant 與使用鏡頭

Shot name 沿用既有 `shared/shots.json`；下次若改分鏡須重建 asset-to-shot 清單。比例、座標等數值要從 Owner 選定的 reference 實量後鎖定，這份 spec 不虛構尚未量測的值。

| 項目 | 任何鏡頭不可改變的特徵（允許的狀態變化另列） | 使用鏡頭／時間 | 候選來源或缺口 |
| --- | --- | --- | --- |
| Nia：臉 | 同一張臉、膚色、眼眉鼻唇比例、耳部與小金耳環；表情可變，身份不可變。 | mother-nearby、covered、lips、eyes、flinch、hand-slipped、question-reaction、listening-hold、nia-reply、brace、final-brace。 | R1 臉部候選；**needs a new reference**：同一角色的正／側／背面與 action reference，目前沒有一致的全角度角色表。 |
| Nia：髮 | 建議鎖 R1 臉旁鬆捲髮、分線及後部輪廓；不可突然變成 R11 的高髻。最終髮型仍待 Owner 選定。 | 同上所有可見頭部鏡頭；foot 不可用來驗髮型。 | R1 候選；**needs a new reference**：髮型背面／受力動作輪廓，現有 R1 與 R11 不能同時通過。 |
| Nia：衣服 | 燕麥色羅紋針織衫的領口、袖口、織紋／版型；深色褲、淺色鞋與鞋帶；不因鏡頭改衣色或配件。 | 所有人像；door-check 手袖；brace／foot／final-brace 下身。 | R1 上身、R12 下身；全身裝束整合 **needs a new reference**。 |
| 對講機：shape | R3 的刷紋金屬長方外殼、四角螺絲、大橫向黑／teal 螢幕、螢幕下單一圓燈、下部橫格柵；外殼／螢幕／燈相對比例和安裝位置一致，透視可變。 | mother-nearby、covered、flinch、hand-slipped、question-reaction、listening-hold、nia-reply；所有 device-* closeups。 | R3；寬景目前不匹配，**needs a new reference**：同外殼的已批准寬景／斜視 projection。 |
| 對講機：screen | 僅文字狀態可變，screen 孔／邊框／透視固定；RULES → CONSENT → COUGH → INPUT wait/prefix/full → SAVED；不能提早露出尾詞答案。完整拒絕與保存尾詞須能區分。 | device-rules 8–11、device-consent 12–14、device-cough 18–20、nia-reply 28–28.3、device-input-* 28.3–29.533333、device-saved 29.533333–30.133333。 | R4、R5、R13–R15；CONSENT／COUGH 延用同一 R3 幾何，下一次 manifest 須另納入各狀態 hash。手機可讀時長尚須重新設計／真人核對，不能把現有 5 格當通過。 |
| 對講機：listening light | 一顆同位置、同色、同直徑圓燈；明確定義 OFF／LISTENING steady／COUGH pulse／INPUT／SAVED 狀態。脈衝後回 listening，**26–28 秒全程 steady ON**，不是說話才啟動。狀態只能由預定事件切換。 | 所有看見裝置的鏡頭，特別 device-cough、question-reaction、listening-hold、nia-reply、device-input-*／saved。 | R6 + R3 定位，R4 亮燈視覺候選；**needs a new reference**：同裝置各狀態的批准色票／曝光表，不能把 R3 暗底圖當待機。 |
| 門閂 | R7 薄平矩形舌、矩形 housing／strike、固定螺絲與門縫；舌厚、寬不可改。解鎖只沿同軸縮回，strike／housing 不移動；重播前不得縮回。 | door-check 14–15、latch-hold 15–16、latch-retract 30.133333–31。 | R7 engaged、R8 retracted；14 秒現有 door-check 厚舌拒作 canonical，**needs a new reference**：帶手的同幾何版本。 |
| 門把 | 刷紋金屬 lever、圓底座、同旋轉軸／長度／厚度；不是門鈕；轉動不扭曲底座、木紋或手。 | opening-handle 0–0.7、mother-nearby／人像可見段、harder-handle 20–21.6。 | R9 + R10；寬景 lever 與 canonical 的角度／比例須量測對齊，未宣稱已一致。 |
| 門 | 同 walnut 木色／木紋方向、門框、把手／門閂高度關係；門為剛體，門縫只由門的轉動改變。前段關閉；解鎖後右側窄縫，不能多出第二塊門或 hardware。 | opening、door-check／latch、harder-handle、所有門旁人像、brace／foot／final-brace。 | R2 室內門、R10 紋理細節、R11 門縫；**needs a new reference**：含軸線與 hardware 的完整門正／反／開啟圖，現有裁切圖不足以定整體幾何。 |
| 場景：hallway／室內方位 | 室內為暖光、母親睡沙發的位置固定；門外只見右側黑暗窄縫。鏡頭反打仍維持同一空間，不增加光源或可見走廊道具。 | mother-nearby、mother-cough、brace／foot／final-brace；其餘鏡頭保留方位。 | R2 室內、R11／R12 門縫；**needs a new reference**：沒有既有一致的走廊全貌或平面配置，不能從黑縫臆造。 |
| 場景：lighting | 相同深夜暖色 practical、門／金屬高光方向、角色臉部曝光；螢幕／燈可按狀態發光，不整面漂色或瞬間日光。 | 全 26 shots（含特寫）。 | R2 作氛圍候選、R3 看 hardware 受光；**needs a new reference**：跨角度批准的燈位／曝光表，尚未實量。 |

## 下一次製作的機械檢查提案（尚未存在）

1. 建立 repo-relative `reference-manifest`：asset ID、批准版本、source hash、角色／道具 invariant、允許狀態、shot 使用清單；每個 shot 必須列全部 asset IDs。缺 hash、缺角色背面、寬／近景引用不同 intercom ID 或薄／厚 latch 混用，先停在製作前，不靠最後 contact sheet 補救。
2. 每鏡 shot checklist 記錄：臉／髮／衣、intercom 外殼及 screen 四角、燈中心／半徑、格柵、latch 厚度／strike、handle 軸、門縫側別／寬度、母親位置、照明。將批准 reference 透視對齊後作邊緣疊圖與 landmark 差異；閾值須先量測並批准。像素差不等於身份或敘事一致，仍需人檢。
3. 按時間表機械驗燈：在每鏡已標定 ROI 量測亮度／色彩與 OFF reference 的差，核對 listening steady、咳嗽脈衝及恢復。26–28 秒所有格都必須符合 ON，不能僅測第一／最後一格；遮擋須列明不可測。OCR／手動覆核 screen 字樣及狀態順序，不讓保存尾詞出現在拒絕前。
4. 動作窗逐格驗證：手掌／手指從遮嘴到下移有持續軌跡；肩先接近、接觸、受力，門以固定軸轉動；門閂沿軸縮回而 housing 不變。檢查不能只問「有無像素動」，照片 mesh deformation 不等於角色動作。
5. 合片後全片至少 4 fps，**關鍵動作窗每一格**，加所有剪接前後格；檢查人物／道具狀態跨鏡延續。沿用本次 temporal_qa.py 的全片 30 fps 抽幀方式可供人工看時序，但它目前不會自動判斷上述語意或 invariant，不能宣稱機械 gate 已實作。
6. 最後由真人以手機 1× 同步看聲畫及字幕，記理解、動作自然度、閱讀時長與錯誤位置；用未曝光觀眾做下一輪探索時重新規劃。任何新修正版不能混入本次已凍結 cut 的答案，曝光名單分開管理。這份規格沒有授權製作、重測或公開。

工程：spec 可審閱，reference library 與上述機械 gate **NOT IMPLEMENTED**；現有連續性問題仍未修。市場：**HUMAN_TEST_PENDING**。90 分既有規則保持原樣；建立 library 不等於成片品質通過。
