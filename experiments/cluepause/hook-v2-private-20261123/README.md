# CluePause｜〈尋人啟事〉Hook v2 私人試看

2026-11-23 台灣時間，Owner 在詢問可否上傳後指示「好的 幫我把做好的上傳」。依前序交付，執行範圍為 CluePause 的 54.8 秒完整版 Hook v2 私人試看。

以既有 A/B 實驗的新版母片上傳。來源為公開 26M B 版的 720×1280、30 FPS 下載檔。新版只變更前 4.833 秒的開場及銜接，後段 1,499 個解碼影格相同。另上傳兩份 SRT，各 12 段，起始 0 秒，片末 54.8 秒。

本機技術基底為 `9f2324b2180402a840edb5a5c3ef91e99d3a9e16`，從試看片目錄執行 `python -X utf8 render.py`、`python -X utf8 prepare-studio.py`，以 ffprobe 核對兩份字幕的段數與時間。交付證據分支基底為 `d7b319187026ef383068f13799f1d05fc202d871`，`uv sync --locked`、`uv run --locked pytest`（61 項）、`npm ci` 和 `npm run typecheck` 通過。npm 執行於 Node 24，顯示專案指定 Node 22 的版本提示。

工程驗收以 Studio 重開影片詳細資料及字幕頁的結果為準。市場驗收與真人第一次觀看另立紀錄。
