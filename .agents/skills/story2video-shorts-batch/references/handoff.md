# 既有方法與版本

先按目前工作階段讀適用列。完整 SHA 鎖定各實驗的內容，分支名可能改變。從 repo 根目錄用 `git show <SHA>:<path>` 讀取。若淺層或單分支 checkout 缺少物件，使用下方的固定版本連結。製片需執行歷史 renderer 時，先核對來源、依賴及適用授權，再使用該版本的獨立 worktree。避免把其他版本的工具或測資混用。

| 使用階段 | 版本與入口 | 實際使用 |
| --- | --- | --- |
| 海龜湯選題、編輯 | [Story Generation b4320b0810d912d095e9d4b9ecfc5b44e11465c8](https://github.com/Gavin0099/story2video/blob/b4320b0810d912d095e9d4b9ecfc5b44e11465c8/.agents/skills/story-generation/SKILL.md) | 用答案倒推題面，列替代解釋及揭曉前能排除它的線索。保留 EN 旁白與 zh-Hant 字幕的揭曉時點。 |
| CluePause 權利及故事品質 | [Shorts Batch 1a30c369a2f06fcb7304aa2dc301d27bdab9f517](https://github.com/Gavin0099/story2video/tree/1a30c369a2f06fcb7304aa2dc301d27bdab9f517/.agents/skills/story2video-shorts-batch) | 隔離三位新讀者分段盲評，每位至少 90，核心因果均有線索支持，且無關鍵缺陷。保留凍結稿、逐輪原始證據和 AutoLoop 原有上限。權利查核逐篇對應 SHA-256，狀態用 approved、pending_permission、pending_verification 或 rejected。詳見 [既有權利規則](story-rights.md)。 |
| 首看及開場 | [Shorts Viewer Gate f21677f7a78d8e68fbb0c23fd12952640efda1fb](https://github.com/Gavin0099/story2video/blob/f21677f7a78d8e68fbb0c23fd12952640efda1fb/skills/shorts-viewer-gate/references/story2video.md) | 用未見同版腳本的觀眾核對開場及故事。有適用的既有海龜湯真人門檻時，五位有效同版首看中至少四位說對核心答案，且至少三位覺得反轉有趣並能說出理解改變。樣本不足就待驗。日常詭異和都市怪談的 [genre gate 草案](https://github.com/Gavin0099/story2video/blob/f21677f7a78d8e68fbb0c23fd12952640efda1fb/experiments/cluepause/genre-pilot-20261124/gates.md) 仍待採納，草案不能產生正式 PASS。 |
| WhyNest 科普 | [WhyNest 批次 067d103d07c7c5f5eb7bc5c795bdda893c041b1a](https://github.com/Gavin0099/story2video/blob/067d103d07c7c5f5eb7bc5c795bdda893c041b1a/experiments/science-shorts/script-library/batch-006/README.md) | 核心主張至少兩個獨立發布者支持，事實與圖解交不同 agent 審查。兩位讀者先各自鎖定開場分數，再看雙語定稿與分鏡。各至少 85 分且因果複述和遷移應用兩題都答對。分項沿用 15／25／25／20／10／5。圖解列控制條件、實拍與示意之別，保留實驗的可驗證限制。 |
| CluePause 分鏡與渲染 | [Static Storyboard 3170e0bab567007c6c5fc1fccf97e10fb02c3af1](https://github.com/Gavin0099/story2video/tree/3170e0bab567007c6c5fc1fccf97e10fb02c3af1/experiments/cluepause/static-ten-20261124/pipeline) | 按 pipeline 合約備 `story.md`、`shots.json`、`references.json`，使用 canonical 角色／道具／場景和 9:16 裁切。先執行 `python -B "<pipeline>/static_storyboard.py" validate "<job>"`，圖像和本機音訊就緒後用同工具 `run "<job>"`。參考 git 版本中的 tools lock 及 README 綁定 FFmpeg、ffprobe、字型、本機 Kokoro 或既有規格 WAV。輸出記實際 cue／切鏡時間及解碼結果。 |
| WhyNest 分鏡與渲染 | WhyNest 批次的各集「製片交接」及既有本機 Remotion／向量圖解 | 交付 EN／zh-Hant cue、逐鏡因果、示意限制、畫面標籤和控制條件。保留可編輯圖層供事實及圖解查核。先確認相容 composition 與素材，缺相容渲染入口就記 HOLD。 |

## 選題、開場與分鏡方法

按題型將下列方法填進既有選題表、線索圖及分鏡。方法來源、採用理由與限制見 [Issue #32 來源紀錄](../../../../experiments/issue-32/external-methods.md) 與 [S09 方法複核](../../../../experiments/issue-32/s09-method-evidence.md)。

| 新增的寫法 | 消費階段 | 正例與不適用情境 |
| --- | --- | --- |
| 把題材同行和可借鏡的呈現形式各自記錄，以一般案例對照突出的公開樣本。 | S03 有公開樣本時填入現有選題表。 | 錯視示範可提供固定鏡位的做法，同類日常詭異故事才用來比較敘事。候選理由寫成可測的呈現假設。 [Video Agent Skills 公開樣本發現方法](https://github.com/Melvynx/video-agent-skills/blob/f4542923f7f796a1fa0e544cbfc1109d5eec87d8/skills/outliers/references/discovery.md) |
| 用首畫面、旁白、必要字幕或標示交付同一觀眾問題。 | S05 編輯開場，以原有 viewer 方法檢查。 | 《第二個敲門聲》用手離開門把和兩個同步字幕交付同一異常；純視覺反差已足夠清楚時，可省重複的螢幕標題。 [Vyral 開場三層](https://github.com/vyralcontent/content-skills/blob/349e495d97029a3e6303a7510e3f39c73f36d8fe/skills/viral-hooks/references/three-layer-hook.md) |
| 每個必要答案都連到可辨認的提前線索和一個要排除的替代解釋。 | S04 寫進海龜湯與日常詭異的線索圖，S06 對實際分鏡。 | 先拍到玻璃裡的亮燈以排除熄燈；都市怪談的情緒結尾可以回扣角色抉擇，無須強套唯一謎底。 [Story Skills 謎題公平性](https://github.com/danjdewhurst/story-skills/blob/929d6a598de2d9ca9ae30bf85051b78a31d0a81b/skills/genre-craft/references/mystery-fair-play.md) |
| 用角色看到的證據改變他的下一個動作，鏡頭寫出前後狀態。 | S04 檢查動機，S06 寫進 shot 與 reference 交接。 | 閉館員看到反射裡的動靜才改變方向；科普對照實驗應依控制條件安排，無須虛構角色動機。 [Screenwriting Skills 場景](https://github.com/jtydhr88/screenwriting-skills/blob/81110874ee98d4415f86efb8310e06b0e778e2d9/plugins/screenwriting/skills/sw-scene-craft/reference.md) |

## 成片診斷與剪輯方法

製作與診斷沿用已驗證的本機路徑。用 FFmpeg／ffprobe 查檔案、聲軌和切點，以 Kokoro 或既有合規 WAV 排實際語音節拍。需要核對成片的配音與字幕時，可用已有的本機 ASR 從實際聲軌轉錄，對照 EN 逐字稿及繁中語意。外部 Skills 下列連結只供閱讀公開文字方法，不需安裝套件、執行上游腳本、上傳檔案或呼叫付費服務。

| 何時使用 | 把什麼寫進現有審片或剪輯紀錄 |
| --- | --- |
| 想定位成片何時缺少線索或證據，或核查新版是否真的修到。 | 用 Video Analysis 的逐段拉片方式對首畫面、中段轉折、揭曉截取實際畫面並記時間碼，再看片段與完整播放。分開描述可見狀態與對觀眾理解的推測。觀眾何時離開須有實際留存數據。 [逐段拉片](https://github.com/zhenwusw/video-analysis-skill/blob/4368b001b08f0caac369733ce2d2c8177d9a2059/references/workflow.md) |
| 開場動作或科普圖解似乎被景別、字幕或畫面元素蓋過。 | 借 Novoads `analyze-video` 的鏡頭欄位，針對問題鏡頭記切點、景別、主體動作、口白、螢幕文字及先後節拍，找出手機上應先看見的證據。 [Novoads 分析方法](https://github.com/novoads/agent-skills/blob/82e6d0628d848d36fcf441549d7d77c7b399396e/skills/analyze-video/SKILL.md) |
| 切鏡、留白、重複動作或音效讓線索難讀。 | 用 `short-drama-breakdown` 把實際鏡頭時長和轉場對到其敘事功能，先分辨必要讀圖時間、反應及重複資訊。用剪輯單標記移動、縮短或替換的位置，實際修片走原剪輯工具。 [鏡頭量測與解讀](https://github.com/zenstory-ai/drama-skills/blob/82a1ce5750138ada79be6904d1ec72d6a285105d/skills/short-drama-breakdown/references/measure-and-read.md) · [剪輯方法](https://github.com/zenstory-ai/drama-skills/blob/82a1ce5750138ada79be6904d1ec72d6a285105d/skills/short-drama-edit/references/editing-guide.md) |
| 角色、道具、空間或圖解跨鏡跳變，或需決定如何返工。 | 用 `short-drama-review` 查接點前後的同一參照。定位時間碼後標需重做素材、修剪或重排字幕，回驗時重看相鄰鏡頭與片尾。 [成片瑕疵與返工](https://github.com/zenstory-ai/drama-skills/blob/82a1ce5750138ada79be6904d1ec72d6a285105d/skills/short-drama-review/references/generated-media.md) |

## 最小適用範例與回退

[編輯例](editorial.md) 是一次無外部呼叫的回歸樣本。重新核對選定 hook 是否在前 3 秒提出腳本真的兌現的問題、揭曉證據是否對應到早於揭曉的 cue、雙語語意是否相同，及是否有權利／事實不足導致 HOLD。先驗證一個例子，再決定是否投入資產或渲染成本。樣本本身屬稿件證據。

每集只讀適用的角色／類型／渲染列與原有 Gate，工作紀錄寫實際讀取的版本。比較方法或範例不可用時，從原有批次入口的對應階段恢復。換用已驗證的渲染路徑時也要套用[頻道視覺規格](visual-style.md)。CluePause 缺符合規格的素材時依該規格處理。

## 既有市場工具與輸入

下表的固定版本是歷史入口。只延用檔案結構、程式和已授權的資料來源，填寫的表及分析輸出放在私有工作目錄。比對影片 ID、頻道、確切公開時間、成片 revision 和原始觀察窗後才接受數值。

| 工具與固定版本 | 輸入與命令 | 邊界 |
| --- | --- | --- |
| PR #19 `a5be360edfbb2b012ae5e373d6a5c01315f1b8f6` 的 `experiments/cluepause/performance-p0-20261124/` 下，沿用 `first-24h-and-timing.csv` 及 `other-windows.csv` 格式。 | 用原 CSV 標頭、UTF-8（可帶 BOM）、`code` 唯一鍵及對應的 `video_id`。首日檔的 `published_at_taipei`、`first_24h_cutoff_taipei`、`*_d1` 只接受首 24 小時；另一表保留 lifetime 擷取時間或報表日期範圍。欄位空白保留空白。 | 兩檔為源資料讀取介面。缺可驗證片齡時只記原時間窗。 |
| PR #29 [market-schema.json](https://github.com/Gavin0099/story2video/blob/0ded2d68c4d638a7a96728389a19c5028f370dc1/experiments/cluepause/market-quality-correlation-20261126/market-schema.json) 與 [分析目錄](https://github.com/Gavin0099/story2video/tree/0ded2d68c4d638a7a96728389a19c5028f370dc1/experiments/cluepause/market-quality-correlation-20261126) | 歷史環境中依序 `python -I build_index.py`、`python -I build_table.py`、`python build_gaps.py`。索引需既有凍結評閱 JSON，join 讀同目錄 `score-index.csv`、schema，另需歷史 `media-map.json`、各片凍結 `story.json`（或覆寫指定 JSON）與 #19 的兩檔。按故事欄位 first、second、reveal、english 的 SHA-256 連接評閱。輸出 `quality-vs-market.csv`、`correlations.txt`、`data-gaps.csv`。 | 此版本來源路徑寫死於原 Windows 工作樹／refs，另需本機 artifacts。乾淨 checkout 中只讀取契約，缺歷史資料時停止此分析，保留 SOURCE_UNAVAILABLE／VERSION_UNVERIFIED 或 INSUFFICIENT。`analyze_rubric.py` 屬暫停的既有評閱研究。 |
| PR #31 [收集表工具](https://github.com/Gavin0099/story2video/blob/b167778168fa0a3539a210fe9a872c15ff976689/experiments/cluepause/market-quality-correlation-20261126/build_collection_sheet.py) | 將工具和 UTF-8 `data-gaps.csv` 放同一私有資料夾，執行 `python -I build_collection_sheet.py`。CSV 欄位 `slice,scope,code,video_id,window,closes_taipei,state,what_to_read,note`，只接受已到期 `CLOSED_NOT_COLLECTED` 或待補確切發布時刻 `UNKNOWN_PUBLISH_TIME` 的帶 ID 列。輸出 `studio-collection-sheet.csv` 空白待填表。 | 檢查至少一列符合，才生成表。全無待辦時記空清單，歷史工具的空輸入會報錯。舊表 54 列是歷史快照，按新批實際到期及證據重建。 |

#29 把 D3／D7 當待補狀態，對應版本未提供已填 D3／D7 的分析欄，也沒有 D28。到期取得數字後沿用 #31 表頭逐列記到私有表，資料鍵為頻道、影片 ID、版本、D1／D3／D7／D28。同時帶窗起迄、擷取時間、來源及各欄狀態。#31 產出待填表，填回後用該表和週報欄位核對，毋須寫回 #19 舊 CSV 或重跑歷史評閱。缺來源、重複主鍵或時窗衝突時停止該列計算並保留理由。
