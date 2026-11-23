# 四格圖像驗收

2026-11-23，主 agent 自行檢查，非獨立讀者試驗；未宣稱真人理解分數。

## 最終版

- 本機檔案：`artifacts/threads/science-comic-20261123/ice-comic-final.png`。
- 尺寸：1122×1402，直式約 4:5，四格由左至右、由上至下。
- SHA-256：`2bdeed5559d632b601a1d541ede1b5e43e346e749e51fa1dcdf2991f66d7d0ce`。
- 圖像使用內建 image_gen；初稿、分子數定向修訂、體積比較修訂的逐字提示均保存在此目錄。最終稿第二格改為等質量的液水／冰體積比較，不再使用可數的分子圖示，並標明「示意，非比例」。
- 繁中標題、對話、氫鍵、密度、質量、示意標籤與帳號逐項讀回，無發現錯字。第二格的「占」為可用字形，不為誤字。
- 以兩份來源核對日常一般冰密度較低、同質量體積變大及氫鍵造成較疏鬆晶體排列的解釋。
- 浮冰大部分在水線以下。畫面沒有把空氣泡、質量變少或分子變大當成浮起原因。
- 第三格是概念排列示意，並非精確的三維晶體或氫鍵原子幾何；貼文亦明說為概念示意，不宣稱所有高壓冰相都適用。

## 手機尺寸檢查

使用獨立 Edge headless profile 渲染本機 HTML，viewport 390×844，圖像固定 360 CSS px 寬，另存 `artifacts/threads/science-comic-20261123/mobile-preview.png`。主 agent 實際檢視截圖，標題與四格主要對話能閱讀；來源與科學補充放在貼文文字。圖內小型示意標籤縮小後偏小，可點開原圖放大閱讀。

```powershell
& 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe' --headless=new --disable-gpu --no-first-run --no-default-browser-check --user-data-dir='D:/story2video/artifacts/threads/science-comic-20261123/edge-qa-profile' --screenshot='D:/story2video/artifacts/threads/science-comic-20261123/mobile-preview.png' --window-size=390,844 --hide-scrollbars 'file:///D:/story2video/artifacts/threads/science-comic-20261123/mobile-preview.html'
Get-FileHash -LiteralPath artifacts/threads/science-comic-20261123/ice-comic-final.png -Algorithm SHA256
```

未驗證範圍：真實手機、Threads 上傳後壓縮／裁切、貼文實際讀回、真人理解度、市場流量與導流。

## 未採用版本

- v1 第二格左右分子數量不一致；未上傳。
- v2 雖改成九格規則排列，液態側仍未畫出相同分子數；未上傳。
- v3 以不含可數粒子的體積示意消除前述矛盾，為本次 final。
