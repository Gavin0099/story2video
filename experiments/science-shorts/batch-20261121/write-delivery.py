"""Write final public copy and an evidence-based local delivery ledger."""
import hashlib
import json
from pathlib import Path

BATCH=Path(__file__).resolve().parent
REPO=BATCH.parents[2]
MEDIA=REPO/'artifacts/science-shorts/batch-20261121'
def load(path): return json.loads(path.read_text(encoding='utf-8'))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
script=load(BATCH/'scripts-final.json')
gate=load(BATCH/'editorial-gate.json')
qa=load(MEDIA/'qa.json')
visual=load(BATCH/'reviews/final-video-review.json')
assert qa['status']=='PASS' and qa['media_status']=='PASS'
assert len(qa['media'])==3
assert len(visual['episodes'])==3 and all(not e['critical_defects'] for e in visual['episodes'])
assert all(e['status'].startswith('PASS') for e in visual['episodes'])
copy=['# 一分鐘科普：最終雙語文案','',
      '2026-11-21 本機試片。兩位獨立AI讀者按事先固定的85分理解度門檻評分，另有雙來源事實與科學圖解硬門檻；已完成影片抽樣科學畫面審查。真人首次理解度與市場驗收尚待完成。', '',
      '[逐主張來源及審查](reviews/audit.md) · [成片抽驗](reviews/final-video-review.md) · [驗收紀錄](validation.md)', '']
rows=[]
hashes=[]
for episode in script['episodes']:
    eid=episode['id']
    scores=next(e['scores'] for e in gate['episodes'] if e['id']==eid)
    provenance=load(MEDIA/eid/'provenance.json')
    clip=MEDIA/eid/f'{eid}-zh.mp4'
    assert provenance['script_sha256']==sha(BATCH/'scripts-final.json')
    assert provenance['media'][clip.name]['sha256']==sha(clip)
    duration=float(provenance['media'][clip.name]['duration'])
    copy += [f"## {episode['title_zh']}",'',
             f"英文標題：{episode['title_en']}。成片 {duration:.2f} 秒；文字/分鏡評分 {scores[0]}／{scores[1]}。",'',
             f'[繁中字幕試看片](../../../artifacts/science-shorts/batch-20261121/{eid}/{eid}-zh.mp4)', '',
             '### 英文旁白','', ' '.join(c['en'] for c in episode['cues']),'',
             '### 繁中字幕','', ''.join(c['zh'] for c in episode['cues']),'',
             '### 來源','']
    urls=list(dict.fromkeys(url for c in episode['claims'] for url in c['source_urls']))
    names={s['url']:s['publisher']+' — '+s['title'] for s in load(BATCH/'source-cards.json')['sources']}
    copy += [f'- [{names[url]}]({url})' for url in urls]
    copy += ['',f"適用範圍：{episode['scope']}",'']
    rows.append(f"| {eid} | {duration:.2f}s | {provenance['frames']} | {scores[0]}/{scores[1]} | {provenance['render_seconds']:.2f}s |")
    hashes.append(f'| `{eid}-zh.mp4` | `{sha(clip)}` |')
(BATCH/'scripts-final.md').write_text('\n'.join(copy)+'\n',encoding='utf-8')
ledger=['# 科普試片驗收紀錄','',
        'Git HEAD：`2d63c2d2fa70d43e1a60b3fa7ec5a11664d341ea`。本輪交付為未提交工作樹；保留進場前其他未提交內容。範圍為使用者授權的三支科普本機pilot，不代表完整SC-00/01產品化、M1完成或公開核准。','',
        '## 工程驗收','',
        '| 影片 | 最終MP4容器時長 | 影格 | 文稿分數A/B | 最終一次本機處理 |','| --- | --- | ---: | --- | ---: |',*rows,'',
        '處理時間以各片provenance記錄為準，含該次本機合成/字幕/渲染/初步解碼；冰重跑有重用音檔，不能與其他兩片直接比較。時間不含完整研究、修正、獨立審查及人工工時，不能當成總生產成本。','',
        '| 命令/檢查 | 結果 |','| --- | --- |',
        '| `uv sync --locked`；`uv run --locked pytest` | 成功；61 passed。實際uv為artifacts/tooling/bin/uv.exe，UV_CACHE_DIR指定同磁碟artifacts/uv-cache |',
        '| `video/`: `npm.cmd ci`；`npm.cmd run typecheck` | 成功；Node24.13.0對repo要求22.x有EBADENGINE警告 |',
        '| `python -I experiments/science-shorts/batch-20261121/finalize-gate.py` | 來源機構去重、兩讀者分項重算、public words/visual等值、hash全部相符 |',
        '| README渲染命令加`--reuse-audio` | 三集成功；45–60秒。前次sky44.73秒在影片前被拒，調結尾非語音停留後重審/重跑 |',
        '| `artifacts/render-venv/Scripts/python.exe -X utf8 experiments/science-shorts/verify.py --mode all` | PASS；10個實際main負面案例+1正控制；12個MP4規格/完整解碼/音量、雙語字幕/內嵌字幕回讀，實際MP4逐cue抽格 |',
        '| `artifacts/render-venv/Scripts/python.exe -I artifacts/science-shorts/batch-20261121/check-black-silence.py` | 三支繁中試看片無blackdetect片段；只有sky結尾43.88075–46.1秒的2.21925秒靜音，與加長非語音收尾一致，無中途長靜音 |',
        '| 獨立事實/科學圖解審查與最終MP4抽格 | 九核心claim、29組英中cue與三片抽樣科學畫面無critical defect；保留首次BLOCK和修正 |','',
        '驗收原始argv、stdout/stderr、exit code與file hashes在 `artifacts/science-shorts/batch-20261121/qa.json` 和 `qa-evidence/commands/`。[詳細工程審查](engineering-review.md) · [媒體抽驗](reviews/final-video-review.md) · [成本/素材權利](rights-and-cost.md)','',
        '初次以預設C槽uv cache執行README命令因暫存跨磁碟WinError17失敗；改設同磁碟UV_CACHE_DIR後sync與61項測試成功。黑畫面/靜音補驗argv與結果另存black-silence-qa.json及各片log。完整影音主觀聽感仍待真人。','',
        '| 試看片 | SHA-256 |','| --- | --- |',*hashes,'',
        f"最終ScienceScript SHA-256：`{sha(BATCH/'scripts-final.json')}`。Renderer：`{sha(BATCH.parent/'render.py')}`。QA腳本：`{sha(BATCH.parent/'verify.py')}`。",'',
        '未驗證：手機實際播放/字幕與喇叭聽感、真人五人首次理解度、獨立專業科學家認證、YouTube播放器字幕/上傳、跨平台重建、全新clone無資產重現。FFmpeg/ffprobe已綁定binary；Python環境、套件與Windows/DLL沿用本機信任，沒有整體信任鏈認證。原生AI讀者是提示隔離，沒有CLI沙箱認證。沒有修改src、Episode v1、SQLite、video或治理版本。','',
        '## 市場驗收','',
        '**PENDING**。真人樣本0；D7/D28、自然有效觀看、受眾重疊與回訪均N/A。未建立頻道、未上傳、未公開。AI分數與工程通過不代表市場成功。建議目前先不開第二頻道；若真人及持續產能驗證通過，一般科普定位傾向獨立。[頻道判斷與後續決策條件](channel-decision.md) · [主持包](viewer-test.md)','']
(BATCH/'validation.md').write_text('\n'.join(ledger),encoding='utf-8')
print('Wrote scripts-final.md and validation.md from final QA/provenance.')
