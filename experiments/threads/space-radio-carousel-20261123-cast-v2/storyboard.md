# 太空人怎麼聊天？｜8 格輪播｜照片特徵版

改編自 repo 的[太空通話定稿](../../science-shorts/batch-20261121/scripts-final.md#隔著真空太空人怎麼通話)。載入既有畫風及[新版角色設定圖](../../../skills/science-four-panel-comics/references/dad-and-daughter-v2.png)。女孩主動試驗，爸爸用反應與玩笑收尾。畫面為四張 4:5 圖，每張上下兩格。

| 圖 | 格 | 逐字文字 | 畫面與科學檢查 |
| --- | --- | --- | --- |
| 1 | 1 | 爸，你聽得到嗎？ | 女孩在密閉頭盔內喊話。太空中保留可見空隙。 |
| 1 | 2 | 看得見，聽不見。 | 爸爸看向女孩，抬手表示聽不到。 |
| 2 | 3 | 咦？我聽得到自己啊！ | 只在女孩自己的頭盔內畫藍色聲波符號。 |
| 2 | 4 | 聲音需要物質的振動才能傳遞。 | 兩頂頭盔間為真空，沒有聲波越過頭盔或出現在間隙。 |
| 3 | 5 | 試試無線電！ | 女孩按下胸前的通訊鍵。 |
| 3 | 6 | 無線電訊號能穿過真空。 | 橘色箭頭從女孩天線指到爸爸天線。 |
| 4 | 7 | 耳機把訊號變回聲音。 | 耳機與藍色聲波符號在爸爸密閉頭盔裡。 |
| 4 | 8 | 收到！晚餐吃什麼？ | 爸爸說話，女孩笑，頭盔仍然密閉。 |

圖解為概念示意。頭盔中的聲音是機械波。穿越兩人之間的真空的是無線電電磁波，接收設備再透過耳機發聲。查核來源為 [NASA](https://science.nasa.gov/ems/02_anatomy/) 和 [ESA](https://www.esa.int/articles/about-us/directorates/science/listen-up)。

本版於 2026-11-23 發布。市場成效與真人理解度待量測。[發布紀錄](../science-comics-02-04-carousel-20261123/README.md)。

## 交付與驗收

- 依序使用 [第 1 張](cards/01.png)、[第 2 張](cards/02.png)、[第 3 張](cards/03.png)和[第 4 張](cards/04.png)。各為 1080 × 1350 PNG，另附[配文](caption.txt)。
- 女孩依照片採黑色直髮、眉上齊瀏海、低馬尾與笑眼，日常版穿奶油白小紅愛心上衣。爸爸採棕色側分短髮、無眼鏡與淡鬍鬚。 [角色設定](../../../skills/science-four-panel-comics/references/series-cast.md)
- 照片用於第一次角色設定圖生成。四頁以新版插畫角色設定圖搭配各頁原無字底圖做人物修圖。[生圖提示](image-prompts.txt)及[可編輯排版](preview.html)。工具未提供費用。
- 與原樣板比對，八格逐字對白、配文及排版相同。於桌面 Edge 實看四張各 360 CSS px 的[手機圖寬預覽](../../../artifacts/threads/space-radio-carousel-20261123-cast-v2/all-four-360px.png)，確認女孩和爸爸造型一致、藍色聲波留在頭盔中，橘色箭頭由女孩天線指向爸爸天線。真人試讀與 Threads 壓縮後畫面未驗證。
- 角色設定已同步至本機 Codex skill，兩份 skill 皆通過 quick_validate。基準 Git SHA 為 8b449a6927e9b04de2e32c22fb2791336b52ff5a。執行 `uv run --locked --offline pytest --tb=line`，61 項通過。
