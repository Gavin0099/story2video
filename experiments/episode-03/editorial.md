# Episode 03〈她把扣眼縫死了〉評審紀錄

## 謎底

裁縫在兩片衣襟內側縫上成對的暗扣。舊扣眼用不到了，她把它們縫起來，再把原鈕扣釘在上面遮住縫線。從外面看，制服就像照原本的方式扣好。

試穿時，客人嘴巴才要張開請她幫忙，左手已經把兩片衣襟按在一起。一聲「喀」。剩下幾顆，他自己扣完。

## 評分

依 [Story Quality Lab 編輯量表](../story-quality-lab/README.md#怎麼判) 評分。版本為繁中題卡 v1。總分為各項原始分除以 5 後乘以權重。這次是作者編輯自評。

| 項目 | 權重 | 分數（1–5） | 加權 | 依據 |
|---|---:|---:|---:|---|
| 懸念 | 20% | 5 | 20 | 第一句就有兩個相衝的要求。扣眼封了，原鈕扣卻一顆都得留下。 |
| 反轉與重新理解 | 25% | 4 | 20 | 本來用來扣住制服的鈕扣變成外觀，扣衣的功能移到內側。有改衣經驗的讀者可能很快想到。 |
| 動機與情感 | 20% | 4 | 16 | 客人要回櫃檯，制服外觀有要求。最後由他自己扣完，回應前面的挫折。 |
| 因果 | 15% | 4 | 12 | 左手操作時缺少另一手固定衣襟。暗扣讓他按合，封扣眼也提供固定原鈕扣的位置。 |
| 公平性 | 10% | 4 | 8 | 揭曉前給出單手試扣失敗、原鈕扣還在與試扣聲。黏扣帶等替代做法解釋得了單手穿衣，但較難解釋「喀」一聲。 |
| 可視覺化 | 10% | 5 | 10 | 失手、縫扣眼與單手按上都能以手部特寫呈現。 |
| **合計** | | | **86／100** | |

## 修訂與關卡

構想初稿把單手不便留到謎底才說，讀者只能猜裁縫在修壞掉的制服。定稿把石膏和試扣失敗放進第一段，再讓試扣的聲音出現在提問前。這樣讀者可以先推到「外觀照舊、單手就能扣」，即使說不出暗扣的名稱，也算猜中核心。

| 既有關卡 | 狀態 | 下一筆證據 |
|---|---|---|
| 海龜湯品質 | PENDING | 只給新讀者題卡，記下首猜、鎖定答案、信心與線索。確認他們有辦法猜到單手扣衣，以及「喀」是否使謎底過早變得明顯。 |
| 短片敘事品質 | PENDING | 記錄新讀者願不願意讀到最後，揭曉後是否能解釋封扣眼的用途。後續改編另驗英語口播與畫面。 |

讀者鎖定猜測後才給謎底。若試讀結果顯示答案難推或太早被猜中，優先調整第二段試扣聲露出的時機。

## 英文文字初稿

*She Sewed the Buttonholes Shut*

The tailor sewed every buttonhole shut. But her customer had asked her to keep every original button.

He was due back at the front desk tomorrow. His right hand was still in a cast. He tried to button the jacket with his left hand, but the fabric kept slipping away.

The tailor moved the old buttons onto the stitched-up holes. Then she pressed two scraps of cloth together. Click.

When he came back, the jacket looked just as it had before. Why had she sewn the holes shut?

She'd hidden snap fasteners under the front of the jacket. The original buttons covered the stitches. He opened his mouth to ask for help, then pressed the first snap shut with one hand. He did the rest himself.

## 驗收

2026-11-21。基準 Git SHA 為 `2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`，使用目前工作樹。

- 工程驗收：`uv sync --locked` 成功，`uv run --locked pytest` 通過 61 項，`uv run --locked python experiments/story-quality-lab/verify.py` 通過既有題庫結構檢查，`git diff --check` 通過。另逐項重算本集 6 項權重與加權分數。
- 故事驗收：本集已完成編輯自評，真人首次試讀與影片成品驗收待進行。
- 市場驗收：待正式發布後開始。
