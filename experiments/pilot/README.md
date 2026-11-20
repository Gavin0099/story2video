# 本機 Shorts 試作程式

這組獨立試作程式用於英文旁白、英繁字幕、視覺審查與直式合成。故事、已選圖片、模型、旁白與輸出皆使用本機 `artifacts/`。工作分支提供程式碼及合成測資，可在另一台電腦先跑測試再接續。

## 安裝與驗證

程式需要 Python 3.11 以上。實際合成需要已加入 PATH 的 FFmpeg、ffprobe，且 FFmpeg 要包含 `libass`。Kokoro 本機生音另需 Python 工具套件與模型。

```powershell
python -X utf8 experiments/pilot/test_visual_poc.py
ffmpeg -hide_banner -filters | Select-String subtitles
```

## 接續同一支試片

使用自己的檔案傳輸方式，保留故事、圖片及產物目錄的相對結構。`visual-consistency-poc/` 應含 `story.json`、`scene-bible.json`、`shot-manifest.json` 與 manifest 所指的 `images/`。`out/v2-B/` 需要 `segments.json`、`provenance.json`、`narration.wav` 與英繁 SRT、VTT 四份字幕。已有核對過的 B 版音檔可直接用。`test_visual_poc.py` 的 `build_project` 也示範了新的故事、場景及鏡頭資料結構。

```powershell
$pilot = 'artifacts/issue-1-pilot'
$code = 'experiments/pilot'
$out = "$pilot/out/handoff-preview"

python -X utf8 "$code/visual_poc.py" --root "$pilot/visual-consistency-poc" check
python -X utf8 "$code/render_visual.py" --project-root "$pilot/visual-consistency-poc" --voice-dir "$pilot/out/v2-B" --output $out
python -X utf8 "$code/qa.py" --output $out
```

合成會先即時核對視覺 Gate、劇本及旁白雜湊。選一個新輸出目錄即可重跑。成品 `render.mp4` 使用 1080 × 1920、30 FPS，並將英文字幕內嵌。繁中 SRT 另存。需要檢查字幕是否提前提到特定詞，可在 `qa.py` 重複加上 `--spoiler-term`。

## 重做圖像或旁白

`visual_poc.py --root <本機場景目錄> prepare <鏡頭ID>` 會依場景與鏡頭資料組裝 Prompt 和參考圖清單。用任一影像工具產出直式 PNG 後，執行 `visual_poc.py --root <本機場景目錄> capture <鏡頭ID> <PNG>` 會保留新版本並重設該圖審查狀態。使用 `check` 確認每張圖和每項空間關係都具有目前資產對應的人工審查紀錄。

重做 Kokoro 旁白時，安裝 `kokoro-onnx==0.6.1` 與 `onnxruntime==1.32.0`，把模型 `kokoro-v1.0.int8.onnx` 和 `voices-v1.0.bin` 放進指定的 `models/`，以同一份 `story.json` 餵給 TTS，維持與視覺 Gate 的劇本版本一致。[模型資產版本](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0)

```powershell
python -X utf8 "$code/synthesize.py" --provider kokoro --episode "$pilot/visual-consistency-poc/story.json" --story-spec "$pilot/story-spec-v2-preview.json" --model-dir "$pilot/models" --voice am_michael --output "$pilot/out/voice-handoff"
```
