"""Write delivery evidence from rendered files plus the primary agent's frame observations."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
OUTPUT=REPO/'artifacts/static-ten-20261124/puzzle'
SHA='aef24410f8b45c8651fd922343aeb52db11bfc75'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def portable(p): return p.relative_to(REPO).as_posix()
def iso(t): return datetime.fromtimestamp(t,timezone.utc).isoformat()

OBS={
'P01': [
'Separated thread ends and scissors are clear. This is a frozen post-snip state, not visible severing motion.',
'Lower-left needle, rim dent and three gold pieces are visible. No high-to-low needle motion occurs within the opening second.',
'High needle and pointing hand visible. Second seller hand is pushed to the right crop edge, weakening the two-hands evidence.',
'Purse is on floor after correction; knot under pan and counter hole are visible in the upper portion.',
'Empty brass ring and thread to its right are separate after correction. Bottom support is hidden as intended.',
'High needle and receipt-sliding hand visible. Other seller hand is outside crop; buyer face partially clipped.',
'Buyer retrieves scissors from purse. Seller raised heel and brass cylinder are lost from the portrait crop.',
'Lower reading and same distinctive gold set visible, with leftmost round/oval piece partly clipped by crop.',
'Cylinder clearly stands on shelf and ring is empty. Thread crosses horizontally behind cylinder, unlike vertical route shown earlier.',
'Black shoe toe loop and taut diagonal line are visible. Upper line appears to terminate at front wooden counter edge, not visibly continue to pan hole.',
'Lower reading and three pieces return. Pan thread stump is visible. Gold oval is more circular than the written invariant throughout.',
'Buyer with scissors and seller face each cropped near frame edges; both retain original clothes and hair. Cylinder now appears at counter height in background.'
],
'P02': [
'Same auburn maker inks raised wooden letters using brayer; block, face, cardigan and apron read clearly.',
'Envelope and partial letters visible, but right corner nick and end letters are clipped by cover crop.',
'Raking macro shows raised M/O and ink on top; the reversed E and full word are outside crop, weakening the backwards-letter clue.',
'Blank cream sheet remains clean; same maker holds it above half-inked block.',
'Blackened block and blank sheet are visible. Raised lettering remains visibly legible by sheen; it has not literally vanished as narration says.',
'Paper is pressed against block using wooden baren; action state is readable without words.',
'Corrected sheet puts peel in cell 0; whole HOME proof is readable in portrait crop, with fully black block below.',
'Corrected cell 1 shows whole HOME and maker holding proof; black block below maintains inked state. Green-ribbon envelope mostly outside portrait crop.'
],
'P03': [
'Both people, ivory vase and diagonal line are visible. The thin line already looks like a shadow; alternative cracked-vase inference may be weak.',
'Buyer insists with open hand; potter looks puzzled. Same navy clothing, rust apron, hair and faces.',
'Blue dot and line passing to its right are clear. Continuation onto tabletop is less obvious after portrait crop.',
'Same wire ring, brass disk, window direction and vase visible; tabletop continuation can be seen at bottom.',
'Hand approaches without contact; line still visible, blue dot and vase geometry stable.',
'Broad hand shadow replaces thin line, with blue dot unchanged. Fine shadow geometry is approximate: thin line disappears even outside the darkest hand silhouette.',
'Buyer holds apparently smooth vase away from wire. Right contour is clipped in portrait crop, limiting whole-surface inspection.',
'Buyer holds vase and potter smiles. Wire remains above. Most empty tabletop/shadow is lost below portrait crop; closing proof relies on prior hand-shadow shot.'
],
'P04': [
'Maker, orange scissors and low flag visible. Flag tip near right crop edge, circle and both eyelets retained.',
'Taut cream line, blue restraint and low flag show clearly. Flag edge is partly clipped but identity marker remains.',
'Maker studies rig, does not pull. Teal shirt, beige trousers and wavy dark hair match reference.',
'Two rope legs and brass pulley visible; right rope disappears behind bench apron, with bag concealed.',
'Scissors, severed blue tip and intact cream line visible. Cut is a frozen after-state; lower flag eyelet remains above.',
'Corrected tight reveal shows tan X-stitched bag on floor and right cream rope; contradictory low flag removed.',
'Flag is now high, but left cream tail still appears to reach bench cleat; bag itself is below portrait crop. Intended complete rig is incomplete in output.',
'Maker open hands, scissors on bench and high flag visible. Left cream tail still at cleat, bag cropped below frame. Flag-to-floor-bag causality is inferred across cuts.'
]}
FINDINGS={
'P01': [
('0.0–3.5','confusing','No visible needle movement or earlier high baseline in first second; opening anomaly depends on narration until the 3.5 s flashback.'),
('3.5–7.0; 15.0–19.0','confusing','Portrait crop prevents a clear simultaneous view of both seller hands, weakening the alternative ballast explanation.'),
('19.0–23.0','confusing','Raised heel clue is outside the crop; silent viewers lose the pre-reveal foot hint.'),
('23.0–27.0','cosmetic','Oval/round gold partly clipped at left; all three pieces can still be counted. Oval is visually round across the sequence.'),
('27.0–32.0','breaks story logic','Thread routing changes: vertical pan-to-hole setup becomes horizontal cylinder pass and a diagonal line apparently attached to the front counter edge at toe reveal. No single continuous force path to the moving pan is demonstrated; a fixed counter attachment would not load the pan.'),
('34.0–36.0','confusing','Cylinder appears at counter height in final background rather than clearly on the under-counter shelf. Confrontation faces cropped.')],
'P02': [
('5.0–15.0','confusing','Central cover crop loses the distinctive nick and reversed E; central M/O alone do not establish backwards writing.'),
('0.0–27.0','confusing','Brayer and raised type may expose printing explanation early; lettering remains visible at 21–27 despite narration saying it vanished. No reader evidence measures predictability.'),
('30.0–39.0','cosmetic','Paper dimensions and block nick depiction vary slightly between stills; readable proof and fully black block state are retained after one correction.')],
'P03': [
('0.0–21.0','confusing','Line has a visibly shadow-like softness and mobile is shown early, so the apparent-crack alternative may not hold. No blinded evidence collected.'),
('10.0–16.0; 33.0–39.0','confusing','Portrait cover reduces tabletop continuation in close-up and removes most final empty-table shadow proof.'),
('27.0–30.0','confusing','Generated hand-shadow geometry is approximate; thin line disappears beyond its darkest silhouette, so exact optical causality is imperfect.'),
('30.0–33.0','cosmetic','Right vase contour clipped; blue dot, clothing and hairstyle remain consistent. No confirmed prop-state contradiction observed.')],
'P04': [
('0.0–10.0','cosmetic','Flag tip cropped at right edge; circle and two eyelets still readable.'),
('22.0–27.0','confusing','Blue snip is readable but relation of loose cream tail to the blue knot is not fully resolved in the still.'),
('30.0–39.0','breaks story logic','After flag rises, left running-rope tail still reaches/appears anchored at original bench cleat. A fixed flag on that same rope should carry its free lower tail upward too. The added/remaining rope length makes the demonstrated counterweight state inconsistent.'),
('30.0–39.0','confusing','Floor bag is outside portrait crop; no final decoded frame shows high pennant and floor bag together. Separate close-up and high-flag cuts carry only part of the intended causal proof.')]
}
NOTES={
'P01':'Force-path discontinuity remains; heel/two-hand clues weakened by portrait crop.',
'P02':'Readable printed reveal; backwards-letter clue cropped and printing may be predictable.',
'P03':'Shadow reveal readable; approximate shadow geometry and cropped final tabletop proof.',
'P04':'High flag reveal present; left rope-tail geometry inconsistent and final bag cropped.'}
CORRECTIONS={
'P01':'One shots-a correction separated thread from brass ring and placed purse on floor. The original rejected sheet is preserved. One earlier tool invocation rejected six reference paths without producing an image; a complete reference sheet replaced the six separate attachments.',
'P02':'One shots-b correction fixed ignored cell assignments, portrait proof legibility and black block state. Original rejected output preserved. Separately, initial audio scheduling failed before any encode because narration exceeded 36 s; final timeline extended to 39 s using copies of all seven already-trimmed PCM cues, without resynthesis.',
'P03':'No visual correction used (3 generated sheets total). Reference mobile’s small brass disk was registered before shot generation. No confirmed hair/clothing/face or vase-state break; optical/crop limitations still recorded.',
'P04':'One shots-a correction replaced the floor-bag plus still-low-flag contradiction with a tight bag-only shot. Original rejected sheet retained. Remaining left-tail/final-crop defect was not corrected again.'}

rows=[]
for key in OBS:
    story=ROOT/key
    data=read(story/'shots.json')
    out=OUTPUT/data['story_id']
    qa=read(out/'qa/report.json'); probe=read(out/'qa/probe.json'); cost=read(out/'cost.json')
    timeline=read(out/'timeline.json')
    assert qa['engineering']=='PASS' and all(qa['checks'].values())
    assert digest(out/(data['story_id']+'.mp4')) == qa['master_sha256']
    assert len(OBS[key])==len(data['shots'])
    ledger=[json.loads(x) for x in (out/'images.jsonl').read_text(encoding='utf-8-sig').splitlines()]
    completed=sum('result_sha256' in r for r in ledger)
    duration=float(probe['format']['duration'])
    frames=sum(1 for p in (out/'qa').glob('shot-*/*.png'))
    start=(story/'story.md').stat().st_ctime
    finish=(out/'qa/report.json').stat().st_mtime
    title=(story/'story.md').read_text(encoding='utf-8').splitlines()[0].split(': ',1)[1]
    summary=next(x.split(': ',1)[1] for x in (story/'story.md').read_text(encoding='utf-8').splitlines() if x.startswith('Story summary:'))
    table='\n'.join(f"| {sh['id']} | {sh['start']:g}–{sh['end']:g} | {sh['function']} | {sh['conveys']} | {actual} |" for sh,actual in zip(data['shots'],OBS[key]))
    issues='\n'.join(f'| {t} | {impact} | {desc} |' for t,impact,desc in FINDINGS[key])
    cues='\n'.join(f"| {c['id']} | {c['start']:.3f} | {c['end']:.3f} | {c['samples']} | {c['reveal']} |" for c in timeline['cues'])
    checks='; '.join(f'{k}={v}' for k,v in qa['checks'].items())
    record=f'''# {key} — {title} — production record

Original fictional puzzle. Rights: pending_verification. No claim of a real event, person, business or external originality clearance.

{summary}

Story Quality Gate PENDING (no blind readers in this round).
Storyboard Quality Gate PENDING (primary-agent observations below are not independent approval).
Viewer Gate HUMAN_TEST_PENDING. Market acceptance NOT_TESTED.

## Delivered files and engineering acceptance

- MP4: `{portable(out/(data['story_id']+'.mp4'))}`
- Duration: {duration:g} s; 1080×1920; 30 fps; H.264 High/yuv420p; AAC stereo 48 kHz; faststart.
- SHA-256: `{qa['master_sha256']}`
- EN sidecar: `{portable(out/(data['story_id']+'.en.srt'))}`
- zh-Hant sidecar: `{portable(out/(data['story_id']+'.zh-Hant.srt'))}`
- Source Git SHA: `{SHA}` (uncommitted genre additions; SHA identifies unchanged worktree base).
- Shared schema validator: VALID. Pipeline engineering result: {qa['engineering']}. Checks: {checks}.
- {frames} dense decoded frames sampled every 7 video frames plus each shot’s last frame; all {len(data['shots'])} timestamped strips personally inspected by the primary agent. Also inspected the ordered source `silent-storyboard.jpg` export. This is AI visual inspection, not human testing.
- Opening question only at 1.0–3.5 s; captions remain separate; photographed evidence text only P02 HOME.
- Alignment is measured trimmed PCM timing plus exact SRT-content/bounds comparison, not ASR, independent listening or human comprehension.

## Shot table: silent intent versus actual frames

The SILENT STORYBOARD check was written in story.md before the first ImageGen. State changes across cuts replace continuous character/object motion.

| Shot | Seconds | Function | Intended silent observation | Actual dense-frame / source observation |
| --- | --- | --- | --- | --- |
{table}

## Continuity and story-logic findings

Impact classes describe observed limitations; none is a gate decision. Hairstyles/clothes/identities generally match their canonical sheet. Minor pose, size and facial perspective changes between photographs are expected; failures of evidence/state are recorded explicitly.

| Timestamp(s), seconds | Impact class | Finding |
| --- | --- | --- |
{issues}

## Calls, timing and corrections

- ImageGen invocations: {len(ledger)}; completed images: {completed}; correction pass count: {1 if key!='P03' else 0}. Every accepted/rejected image has a ledger receipt; failed input validation has its own no-image entry.
- Local libx264 encode count: {cost['encode_count']}; final stream-copy/AAC mux recorded separately. One final master per story, preserved without replacement.
- Render invocation wall time: {cost['wall_seconds']} s. Image dollar cost UNKNOWN (tool did not expose charges). Local Kokoro uses existing verified model bytes; no hosted TTS call. No dollar total invented.
- Elapsed input-creation to completed QA: {finish-start:.1f} s, from {iso(start)} to {iso(finish)}. This includes waiting while earlier stories were produced and is not active labor/provider latency. Late record writing is excluded. Pipeline wall time above is separately measured.
- Foley: deterministic local 24 kHz mono PCM tick/noise, mixed softly as snip or contact, with bilingual accessibility cue. It is synthetic foley; source room ambience and every original P01 needle/purse sound were not recreated.

{CORRECTIONS[key]}

Reference sheet was produced first. Shot sheets were conditioned on extracted canonical cells when at most five were required; P01/P04 used the whole six-cell reference sheet because the image tool accepts only five image paths. P02 correction additionally attached its already-inspected setup sheet. Prompt hashes and output hashes are in images.jsonl. No second correction loop was run.

## Measured narration / caption schedule

| Cue | Start s | End s | Trimmed PCM samples at 24 kHz | Reveal |
| --- | --- | --- | --- | --- |
{cues}

The first reveal shot starts at {next(s['start'] for s in data['shots'] if s['function']=='reveal'):g} s. Audio and captions marked reveal are guarded against an earlier start. Foley has its own timed bilingual caption.

## Reproduction commands and unverified scope

From repository root, with existing local tool/model paths supplied by S2V environment variables (see ../README.md):

```powershell
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py validate experiments/cluepause/static-ten-20261124/puzzle/{key}
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py run experiments/cluepause/static-ten-20261124/puzzle/{key}
```

The run command was executed successfully for this master. It deliberately rejects replacing an existing MP4; reproduction requires a new revision id in an isolated copy. Detailed successful subprocess commands, exits, times and diagnostics: `{portable(out/'commands.jsonl')}`. Technical probe, report, cost, source/tool hashes, source storyboard, image ledger and caption provenance all remain under this output folder.

Not verified: full spoken-audio listening in both caption modes, ASR, actual phone readability, blind story/visual comprehension, external originality/rights review, audience retention, market demand. No public/private upload, YouTube access, commit, push or memory modification. Core src/video/governance unchanged; full engine uv pytest/npm checks were not rerun for isolated content. Shared pipeline offline suite: 33 passed; pytest caches/temp confined to puzzle artifacts.
'''
    (story/'record.md').write_text(record,encoding='utf-8')
    rows.append(dict(id=key,title=title,story_id=data['story_id'],mp4=portable(out/(data['story_id']+'.mp4')),duration=duration,
      sha256=qa['master_sha256'],imagegen_calls=len(ledger),completed_images=completed,encode_count=cost['encode_count'],render_wall_seconds=cost['wall_seconds'],
      creation_to_qa_seconds=round(finish-start,1),quality_note=NOTES[key],findings=[dict(timestamp=t,impact=impact,finding=desc) for t,impact,desc in FINDINGS[key]],
      story_gate='PENDING',storyboard_gate='PENDING',viewer_gate='HUMAN_TEST_PENDING',rights='pending_verification',market_acceptance='NOT_TESTED'))

(ROOT/'delivery.json').write_text(json.dumps(dict(git_sha=SHA,reviewed_at_utc=datetime.now(timezone.utc).isoformat(),videos=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
index='\n'.join(f"| [{r['id']}]({r['id']}/record.md) | {r['title']} | `{r['mp4']}` | {r['duration']:g} | `{r['sha256']}` | {r['imagegen_calls']} ({r['completed_images']} images) | {r['quality_note']} |" for r in rows)
(ROOT/'README.md').write_text(f'''# Puzzle static-still delivery — 2026-11-24 batch

Four complete local videos, finished across 2026-11-24/25 Asia/Taipei. English Kokoro narration, clean photographic masters with basic camera moves, synthetic foley, separate EN/zh-Hant sidecars. P01 retains v3 story and all eight narration lines; P02–P04 are original-fiction candidates using printing context, optical shadow and counterweight release mechanisms respectively.

All four pipeline technical reports report engineering PASS. This is file/timing acceptance. P01 and P04 retain material visual story-logic defects after their one allowed correction; P02/P03 also have documented clue/predictability limitations. All Story Quality Gates PENDING, all Storyboard Quality Gates PENDING, all Viewer Gates HUMAN_TEST_PENDING. Rights pending_verification. Market acceptance NOT_TESTED. No gate is claimed passed.

| Record | Title | MP4 path (repository-relative) | Duration s | SHA-256 | ImageGen invocations | Honest quality note |
| --- | --- | --- | --- | --- | --- | --- |
{index}

Total: {sum(r['imagegen_calls'] for r in rows)} tool invocations, {sum(r['completed_images'] for r in rows)} completed image sheets, {sum(r['encode_count'] for r in rows)} libx264 cuts, four final stream-copy/AAC muxes. P01 includes one rejected tool input with no generated image. P01/P02/P04 each used one visual correction pass; P03 used none. No quota failure occurred. Charges are UNKNOWN; no cost estimate represented as actual charges.

## Scope, isolation and shared-pipeline workarounds

Only this experiment puzzle folder and `artifacts/static-ten-20261124/puzzle/` were written by this job. No shared pipeline edits, state-changing Git commands, memory edits, commits, pushes, uploads or YouTube actions. The image service itself saves tool-managed generation outputs; selected assets were copied here immediately and all local caches/temp were redirected to puzzle artifacts. No personal absolute path is stored in authored records/configuration.

`run.py` imports the unchanged shared pipeline and changes OUTPUTS to the puzzle artifacts subtree. All Python runs use -B. TEMP/TMP, HF_HOME, XDG_CACHE_HOME, NUMBA_CACHE_DIR and UV_CACHE_DIR are confined there. It also loads the already-installed base Python schema dependencies, since render Python supplies Pillow/Kokoro but lacks jsonschema; the repo environment’s rpds extension targets a different Python ABI. No dependencies were installed and the read-only source checkout was not edited.

This adapter adds central-portrait crop instructions and explicit unused-cell instructions to exported prompts, because the first P02 sheet otherwise ignored cell assignments. It does not change rendering/validation/audio/QA algorithms. The model still did not reliably keep all mechanical evidence inside cover crops; records distinguish the intended framing from the decoded result.

Image tool input cap: five image paths. Six P01/P04 canonical cells are attached as one complete reference sheet, preserving all canonical visual information. P04’s reference came back as six scene studies rather than isolated objects; its canonical cell crops were remapped to the actual visible maker/flag/rig/bag/scissors/set before shot generation. This does not prove every generated rope state is consistent.

P02 audio rejected the 36 s plan before encoding. Its failure cost/manifest are preserved as `cost-timing-attempt1.json` and `manifest-timing-attempt1.json`. All seven PCM files were copied into P02 assets and reused. Final P02/P03/P04 durations are 39 s, P01 is 36 s. No speech was cut to fit.

`prepare.py` preserves the initial authoring plan and refuses to overwrite existing final inputs. Authoritative final inputs are each story.md/shots.json/references.json; do not regenerate them from the initial draft. `finalize.py` derives hashes, timings and records from existing media plus explicit frame observations; it does not generate media.

## Validation evidence and commands

Git base SHA: `{SHA}`; branch `codex/cluepause-static-ten-20261124`. Uncommitted content additions are not represented by that base SHA; manifest hashes bind exact story inputs and shared pipeline bytes. Each story was schema/cross-reference validated, rendered and fully decoded with the shared pipeline. Every decoded dense strip (36 shots total) and each silent storyboard was inspected by the primary agent. This is AI inspection, not independent/human approval.

Supply existing trusted installations as environment variables: S2V_RENDER_PYTHON, S2V_FFMPEG, S2V_FFPROBE, S2V_QUESTION_FONT, S2V_KOKORO_MODELS, S2V_GIT_SHA. No paths or credentials are embedded here. Read the shared pipeline README for hash-pinned binaries/model requirements.

```powershell
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py validate experiments/cluepause/static-ten-20261124/puzzle/P01
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py prompts experiments/cluepause/static-ten-20261124/puzzle/P01 --supports-images
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py run experiments/cluepause/static-ten-20261124/puzzle/P01
```

The same validate/run commands were executed for P02, P03 and P04. Run intentionally refuses to overwrite an existing master: choose a fresh revision for reproduction. Do not log another ImageGen receipt unless a call actually occurred.

Shared offline suite executed with bytecode disabled and test temporaries confined here:

```powershell
& $env:S2V_SCHEMA_PYTHON -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/puzzle/pytest-cache --basetemp artifacts/static-ten-20261124/puzzle/pytest-temp
```

Result: 33 passed in 0.51 s. `git diff --check -- experiments/cluepause/static-ten-20261124/puzzle` exited zero (new untracked content was separately scanned). Four concrete full media runs substitute for the synthetic smoke; no extra smoke output written outside scope. Full core engine `uv run --locked pytest`, npm install/typecheck and governance verify were not run because those code paths/contracts were not modified. No code from src/video/memory/governance was edited.

Per-output evidence includes master and sidecars, timeline.json, probe/report, every dense decoded sample, source silent storyboard, images.jsonl, prompts, assets/manifest hashes, commands.jsonl and cost.json. Engineering acceptance and market acceptance are recorded separately. Remaining work is independent story/storyboard review, human viewing/listening/phone checks, external rights clearance and any later owner-authorized revision/publication.

Final integrity evidence: `artifacts/static-ten-20261124/puzzle/delivery-audit.json` checks all four input/master/shared-pipeline hashes, all 16 exact historical prompt hashes, every generated image and reference attachment hash, P01's eight unchanged English lines, and absence of personal absolute paths in authored/output text. `call-prompts/` preserves every matched historical prompt, including rejected calls; `delivery.sha256` binds each master, sidecars, ledger, timeline and manifest. P01’s frozen source is [source-p01-v3.md](P01/source-p01-v3.md); the current work remains uncommitted as requested.
''',encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False,indent=2))
