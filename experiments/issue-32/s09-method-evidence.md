# S09 方法複核與取捨（v1.1）

2026-11-26（Asia/Taipei）。以 [S02 的 16 份固定 SHA 與授權登錄](external-methods.md) 為基線，逐份打開原始封存中的下列子檔。此表是第二次研讀所得的具體增量。上游程式、套件、素材與服務均未引入。

**證據層級。** D 為固定原檔所述方法或可讀程式行為。P 為公開播放器預覽中可辨認的剪輯片段。H 為本專案可測的應用假設。F 須有本專案成片或短動態樣帶的實際檢查。V 須有新觀眾實際首看記錄。M 須有合適片齡、指標分母與曝光資料的本專案成效。D 和 P 可解釋選擇，F 可驗證是否拍出，V 和 M 才可以談觀眾反應。

| 固定來源 | 複核所得（D） | 建議取捨（H） |
| --- | --- | --- |
| Vyral Content Skills | Bait check 將必須互動才拿到回報、堆疊多重 CTA、結尾未交付價值列為缺陷。它對演算法的擬人說法無實證。 [固定原檔](https://github.com/vyralcontent/content-skills/blob/349e495d97029a3e6303a7510e3f39c73f36d8fe/skills/viral-captions-and-ctas/assets/bait-check.md) | 題目承諾在正片內交付，結尾 CTA 可視必要性刪掉。 |
| Story Skills | 連續性文件把道具持有者、時間、角色當時可知事項分開。程式只查錄入狀態，角色是否合理理解要靠人判斷。 [固定原檔](https://github.com/danjdewhurst/story-skills/blob/929d6a598de2d9ca9ae30bf85051b78a31d0a81b/docs/continuity.md#prop-custody) | 針對唯一關鍵物件記交接前後及誰親眼看過。知道結局的人不能替盲看者補知識。 |
| Drama Skills | 動作計時把接近、接觸、施力與落定分開；指出有因果的動作不能留在同一個未分先後的提示。有效說話窗扣除反應與大動作。 [固定原檔](https://github.com/zenstory-ai/drama-skills/blob/82a1ce5750138ada79be6904d1ec72d6a285105d/skills/short-drama-video-prompts/references/performance-action-timing.md) | 分鏡標記道具收手到停止變化的時點。若是異常自行發生，畫面保留可見的手部退出與前後狀態。 |
| Screenwriting Skills | 階段 4 將每個場景起訖狀態寫成一對值。原文件同時用長片頁數計分。 [固定原檔](https://github.com/jtydhr88/screenwriting-skills/blob/81110874ee98d4415f86efb8310e06b0e778e2d9/plugins/screenwriting/skills/sw-workflow/reference.md) | 用單一可見狀態對分辨重複鏡有沒有推進；保留有用途的反應與讀圖停格。長片頁數比例不適用。 |
| YouTube Agent Skill | 程式用最大 x 值是否低於 100.5 判百分比軸，60 秒的秒軸會誤入同分支；固定前 30 秒對 30–60 秒素材也會覆蓋大量敘事。 [固定程式](https://github.com/Jakeschincariol/youtube-agent-skill/blob/a2feb2104981a375ffd4f87ee04f4f5344ac43c6/skills/yt-retention/retention.py) | 秒軸百分比由匯出標頭或資料說明指定，再對到本片時間碼。陡降附近的圖和 cue 是待人工檢查的位置，原因仍待比對。 |
| Social Media Skills | 梯階模板混合 75% 選擇觀看與「10–15 秒下跌」指標，並寫了約 70% APV 門檻及快剪間隔，來源條件未在該檔校準。 [固定原檔](https://github.com/social-media-skills/skills/blob/f28cef2b7067ec64e79c9d85421c022c06659e03/skills/youtube-shorts/references/the-retention-ladder.md) | 開場無聲可讀與片尾回扣可各當呈現選項。兩項數據依平台分母個別記，銷售橋接或迴圈提高重播的假說保留在原用途。 |
| Agentara Skills | 方法表將單一重要瞬間、因果事件鏈及允許留懸念的連載分開。 [固定原檔](https://github.com/agentara/skills/blob/950e1bfb11e1df67b46df19804ed85ada9012c33/skills/aigc/video-plan/references/story-arc.md) | 自足謎題採可推出解的短因果鏈，都市怪談可留世界觀未知但閉合本次可見後果。純瞬間型不靠補長支線填時。 |
| Video Agent Skills | 名單流程分「同行與規模」及「可轉移形式的大帳號」，並保留排除原因。其範例接 paid Exa／AnyAPI，以 Reels/TikTok 為主。 [固定原檔](https://github.com/Melvynx/video-agent-skills/blob/f4542923f7f796a1fa0e544cbfc1109d5eec87d8/skills/outliers/references/discovery.md) | 手記主題同類與形式近似兩種角色。Zach King 用於構圖，與日常詭異敘事需求推論分開。 |
| Cinema Skills | Cut List 先列目前、目標、差值，再列每一刀刪掉的用途。無真切點時必須註記估計。 [固定原檔](https://github.com/Benitoow/cinema-skills/blob/b3d96caaf90729f086ce8bfa96654f40fd98e4e5/skills/cut-list/SKILL.md) | 先剔除重複說明，保留觀眾必須辨認線索的停留。A/B 記原長、目標、差值與被替代鏡頭。 |
| Cinematic Skills | Review 清單要求全段查方向翻轉、地理和尺寸參照，單鏡成功仍可能接錯。 [固定原檔](https://github.com/AustinZ21/cinematic-skills/blob/0e5b3fe575740cd022d9ffdec7b7568684c885a5/skills/shot-director/references/review.md) | 重複操作鎖景別、水平面和方向。須故意改視角的反轉先選一個跨切點仍可辨的道具。 |
| Video Skills | Walkie 固定文件區分雲端聲型控制與 on-device WAV，後者忽略速度與語氣欄；每一新 take 可能重算用量。 [固定原檔](https://github.com/adamperlis/video-skills/blob/5187e6da83bd13106a0a024e3d603d71032c66bc/skills/walkie-voiceover/SKILL.md) | 採用配音前逐句朗讀、數字及縮寫確認和定稿后再錄。既有音源即可執行，剪輯比較使用同一 take。 |
| YouTube hooks/scripts | Callback 節拍把後段連回早期承諾；同一文件的頻率和留存節段明定為 15 分鐘以上的技術內容。 [固定原檔](https://github.com/jscraik/Agent-Skills/blob/29201925e182d5319920b1dc3835dda98b915feb/Infrastructure/references/deferred-skill-context/content-publishing-youtube-hooks-scripts/references/engagement-techniques.md) | 只取前後連回同一可視證據，用一個物件匹配。分鐘及比例標準不直接移植。 |
| Remotion Skills | Silence detection 先測輸入閾值再找靜音區間，底層 FFmpeg 量測本身不區分戲劇停頓或漏音。若源軌很安靜，還需以實聽核對。 [固定原檔](https://github.com/remotion-dev/skills/blob/a3f4098a2afd0e13f6a6f8c8760e275f75457ea9/skills/remotion-markup/silence-detection.md) | 用現有檢查標記可能漏音的區間，對上鏡頭意圖後再決定。推理停留與驚嚇前留白不可僅依音量自動刪除。 |
| Explainer Video | beats.py 依口白順序匹配重複提示詞；缺詞顯式失敗。英文 ASCII 正規化不適用繁中。 [固定程式](https://github.com/PaulLemaistre/explainer-video/blob/feb33d880bebfd82730534c1adc7443e711aa267/skills/explainer-video/scripts/beats.py) | 每個重要畫面用唯一或有順序的實測英語 cue，繁中於獨立 SRT 核對語意；缺可靠字時戳用整句或實聽確認。 |
| Awesome Video Skills | 目錄有載入外站素材的 demo 及投票，並自述星／數量或投票可能延遲。排名或人氣不能證明品質、成本或權利。 [固定原檔](https://github.com/ella-wang-opus/awesome-video-skills/blob/866838defd0e1c7586b0ca0dff60e4d8385ed1d0/README.md) | 現有輸出發生明確缺口時，沿索引到上游固定版本找可驗證介面。課例預覽本身沒有授權用途。 |
| Awesome Novel Skills | 發現程式依時間、星數及關鍵詞搜候選，先合併重複並保留忽略清單，預設過濾會漏掉小型或久未推送的方法。 [固定程式](https://github.com/UnderleveledBuilder/awesome-novel-skills/blob/1fb4f8bc00f569b42a524c002924a3c011f002e4/scripts/discover.py) | 「查無」僅限定被檢索範圍。研究紀錄留排除原因，避免重找，但可在資料或技術條件變動後重查。 |

## S09 公開樣本補充

六個當次可見 Shorts 清單各取五支。核對公開播放器的影片 ID、Shorts eligibility、觀看數與發布日，逐支看七張先後的公共預覽。只讀 30 支／210 格。高累計觀看有選樣偏誤，重複題材、片齡與創作者規模也會影響比較。剪輯確切時間、聲音細節、非取樣區間、真實觀眾留存與觀看成因不由格圖判定。 [30 支公開 Shorts 逐片觀察](s09-peer-observations.md)

| 類型 | 公開畫面觀察（P） | 待測假設（H） |
| --- | --- | --- |
| 海龜湯相近的圖像謎題 | 殭屍片 0s 題目／候選人同框，40s 明指一名候選人；警員謎題 0–2s 由校舍轉門口，較晚見警員。 [殭屍片](https://www.youtube.com/shorts/xJrtkK5JFlE) · [警員謎題](https://www.youtube.com/shorts/UOaGJWhitTI) | 早期可推理景別與結尾證據回看是可單獨修改的因素。 |
| 日常詭異的錯視參照 | 瑜伽片以白牆、藍墊和吊繩定位，末段換角。咖啡片直接並列台前台後。 [瑜伽片](https://www.youtube.com/shorts/UW2tv5OOpgI) · [咖啡片](https://www.youtube.com/shorts/svJlZpJ-_Hc) | 可先比是否看出異常，再比較是否看出機制。 |
| 都市怪談相近的短恐怖 | Ballerina 多次重現同房構圖，Bed Head 放大臉和被子。暗部樣本無法確認最後異常的確切動作。 [Ballerina](https://www.youtube.com/shorts/3XEYs8xwvpQ) · [Bed Head](https://www.youtube.com/shorts/xj_sF5r4a3A) | 保留怪異氣氛，盲測新觀眾是否看得到被打破的規律和後果。 |
| 科普示範與圖解 | 觸感顯微鏡由物面到三維表示；熱管用同框樣品及剖面；浴簾以旋轉箭頭回到生活物件。 [Steve Mould](https://www.youtube.com/shorts/7PJi9KSDVbQ) · [The Action Lab](https://www.youtube.com/shorts/ZEGazGMEhtw) · [MinuteEarth](https://www.youtube.com/shorts/c6rLd7vbS3A) | 優先測「能否用相同物件看懂因果」，只以獨立科學來源確認結論。 |

工程層記錄固定來源與公開影格，供重複讀取。下一批建議使用 `s09-methods-v1.1` 做範圍明確的單因素比較。版本的實際成片、首看和市場證據須各自補登。
