"""Write evidence from existing outputs; does not generate or modify media."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from build_inputs import STORIES

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
OUT=REPO/'artifacts/static-ten-20261124/urban_horror'
SHA='aef24410f8b45c8651fd922343aeb52db11bfc75'

OBS={
 'H02':[
  'Extra grey figure is visible only in the oval mirror; Mira, white coat, green sweater and lit phone are clear.',
  'Grey fingertips appear on the far side of the large mirror. They remain there throughout the camera move.',
  'Mira looks alarmed, coat half removed, lit phone in hand. The door-open button is mostly lost in portrait extraction; pressing it is not demonstrated clearly.',
  'White coat covers the oval mirror; Mira now wears only the green sweater. Cloth creases are visible, but pressure underneath is not an independently clear event.',
  'Black phone screen and the still-covered large mirror are both visible. The doors closing are outside this tight framing.',
  'Grey fingers occupy the phone screen while the large mirror remains covered. The depth cue is ambiguous: a viewer could still read this as an image/reflection rather than fingers entering real space.'
 ],
 'H03':[
  'Smoke, hammer silhouette and wrapped wrist are visible across the shaft; the same black-handled hammer is on the near sill.',
  'Single wrapped hand appears behind the opposite window after the correction. This removes the near-glass mirror reading, though palm anatomy appears to switch handedness.',
  'Recognizable Lea braces a grey trunk against a cream doorway. Face, bun, sweater and wrist wrap match; the bolt is mostly outside portrait crop.',
  'Smoke visibly emerges at the vent over the barricaded door. Lea grips the same trunk. The silver sliding bolt differs from the brass barrel bolt in the corrected previous shot.',
  'Lea is recognizable behind smoky glass, holding the matching hammer and showing the wrist wrap: the supposed attacker is the protagonist seeking air.',
  'The glass is broken, Lea leans into fresh air and lowers the hammer. No wounds or flames are shown. Window pane proportions/subject scale drift from the opening.'
 ],
 'H04':[
  'Final edit opens on signed book and a hat-wearing silhouette beyond wired glass, showing a possible threat immediately.',
  'Pencil EVA is readable; a blue sheet edge is present beneath the cream page. This follows the establishing view as a detail insert.',
  'Pink eraser removes readable lettering; eraser dust remains. The blue sheet edge stays under the same page stack.',
  'Eva closes the brown book; the outside doorway is empty. Her pixie hair, cardigan, blouse and face match the reference.',
  'Blank rubbed top leaf is lifted, blue copying sheet folded aside, intact dark-blue EVA on cream duplicate below. No explanatory warning text.',
  'Intact blue EVA remains visible and the visitor stands inside directly behind Eva. Her outer cheek/right edge is cropped, but both eyes, mouth, hair, clothing, book and visitor remain readable.'
 ]
}

FINDINGS={
 'H02':[
  ('11.000–16.967','confusing','Door-open button/press is largely outside the portrait crop. The coat-removal reaction is visible, but the safe open-door state depends on narration.'),
  ('17.000–22.967','confusing','Cloth creases do not clearly demonstrate something pushing underneath; threat location is suggested rather than shown.'),
  ('23.000–28.467','confusing','Door closure is off-frame, so the rule trigger is carried by narration and edit timing.'),
  ('28.500–35.967','confusing','Grey fingers on black glass have weak physical depth; the payoff could be interpreted as another reflection. Covered wall mirror and phone states remain coherent.')
 ],
 'H03':[
  ('5.500–10.967','confusing','The corrected wrapped palm appears anatomically right-handed although the canonical wrap is left. This weakens the matching-wrist clue; no additional correction allowed after the single fix pass.'),
  ('11.000 → 17.000','cosmetic','Door hardware changes from brass barrel bolt to silver sliding bolt between sheets. Both remain closed; the trunk continues to block the door.'),
  ('0.000 → 23.000–35.967','confusing','Window pane proportions and protagonist scale differ between the distant opening and exterior payoff, weakening an exact visual match.'),
  ('11.000–16.967','cosmetic','The close portrait extraction hides most of the bolt, though the trunk against the door is visible.')
 ],
 'H04':[
  ('28.500–35.967','cosmetic','Right edge trims Eva outer cheek/shoulder. Both eyes and mouth remain visible; the visitor and blue name are retained through the move.'),
  ('0.000–16.967','confusing','Blue copying-sheet edge is small on a phone-sized view. It is present but may not be noticed as a fair clue without replay.')
 ]
}

NOTES={
 'H02':'Clear mirror-to-phone state progression; crossing depth and off-frame door trigger remain ambiguous.',
 'H03':'Hammer re-explains the opening as escape; wrist handedness and window geometry remain inconsistent.',
 'H04':'Readable erasure/copy payoff; opening reordered to expose threat; blue clue is small and final cheek is cropped.'
}

def read(p): return json.loads(p.read_text(encoding='utf-8'))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.relative_to(REPO).as_posix()
def stamp(t): return datetime.fromtimestamp(t,timezone.utc).isoformat()

def main():
    index=[]
    for sid,s in STORIES.items():
        folder=ROOT/sid
        data=read(folder/'shots.json')
        out=OUT/data['story_id']
        qa=read(out/'qa/report.json'); cost=read(out/'cost.json'); time=read(out/'timeline.json')
        master=out/(data['story_id']+'.mp4')
        assert digest(master)==qa['master_sha256']
        assert qa['engineering']=='PASS' and all(qa['checks'].values())
        images=[json.loads(x) for x in (out/'images.jsonl').read_text().splitlines()]
        sample_count=sum(len(read(out/'qa'/x['id']/'samples.json')['times']) for x in data['shots'])
        duration=float(read(out/'qa/probe.json')['format']['duration'])
        begun=(folder/'story.md').stat().st_ctime
        finished=(out/'qa/report.json').stat().st_mtime
        elapsed=round(finished-begun,3)
        prior=read(OUT/'h04-static-v1/cost.json') if sid=='H04' else None
        encodes=cost['encode_count']+(prior['encode_count'] if prior else 0)
        render_seconds=cost['wall_seconds']+(prior['wall_seconds'] if prior else 0)
        evidence={'story_id':data['story_id'],'title':s['title'],'duration_seconds':duration,
                  'master':rel(master),'sha256':qa['master_sha256'],'imagegen_calls':len(images),
                  'imagegen_provider':'built-in image_gen','imagegen_billed_cost':'UNKNOWN',
                  'unique_tts_syntheses':6,'tts_provider':'local Kokoro ONNX','voice':'af_heart','speed':1.08,
                  'final_encode_count':cost['encode_count'],'cumulative_encode_count':encodes,
                  'final_render_wall_seconds':cost['wall_seconds'],'cumulative_render_wall_seconds':round(render_seconds,3),
                  'observed_production_span_seconds':elapsed,'span_start_utc':stamp(begun),'span_end_utc':stamp(finished),
                  'span_definition':'Input-file creation to final QA completion; includes TTS, generation, waits and work on other stories; excludes initial repository reading. Overlapping spans must not be summed.',
                  'dense_decoded_frames_inspected':sample_count,'git_sha':SHA,
                  'local_wrapper_sha256':digest(ROOT/'job.py'),'story_quality_gate':'PENDING',
                  'storyboard_quality_gate':'PENDING','viewer_gate':'HUMAN_TEST_PENDING',
                  'market_acceptance':'NOT_TESTED','rights':'pending_verification'}
        (out/'production-cost.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
        (out/'continuity-review.json').write_text(json.dumps({'reviewer':'authoring agent, visual inspection; not a blind reader or human viewer',
             'reviewed':['canonical sheet','all selected source cells','silent-storyboard.jpg','all six dense decoded strips including final samples'],
             'findings':[dict(zip(['timestamps','impact_class','observation'],x)) for x in FINDINGS[sid]],
             'unverified':['human listening','phone playback','independent comprehension','external originality/rights verification'],
             'gate_status':{'story':'PENDING','storyboard':'PENDING','viewer':'HUMAN_TEST_PENDING'}},indent=2)+'\n',encoding='utf-8')
        lines=[f'# {sid} — {s["title"]} production record','',
          'FICTION — original invented urban-horror candidate. Rights: pending_verification.',
          f'Git SHA: `{SHA}`. Working files are uncommitted. No publication authorization is implied.',
          '', '## Story and rule',s['rule'],s['alternative'],s['clues'],
          '', '## Delivered files',f'Master: `{rel(master)}`',f'Duration: {duration:.3f} s; SHA-256: `{qa["master_sha256"]}`.',
          f'EN sidecar: `{rel(out/(data["story_id"]+".en.srt"))}`',
          f'Traditional Chinese sidecar: `{rel(out/(data["story_id"]+".zh-Hant.srt"))}`',
          f'Silent storyboard: `{rel(out/"silent-storyboard.jpg")}`; timestamped strips: `{rel(out/"qa")}/shot-01-strip.jpg` through `shot-06-strip.jpg`.',
          '', '## Shot table: silent intent versus decoded result',
          '| Shot | Seconds | Narrative function | Silent intent | What the frames show |',
          '|---|---|---|---|---|']
        for shot,obs in zip(data['shots'],OBS[sid]):
            lines.append(f'| {shot["id"]} | {shot["start"]:.1f}–{shot["end"]:.1f} | {shot["function"]} | {shot["conveys"]} | {obs} |')
        lines += ['', 'The initial SILENT STORYBOARD check was generated before ImageGen by build_inputs.py. Delivered story.md also records subsequent staging revisions; H04 initial inputs are preserved in the v1 input-archive. The core object-state event is visible; the precise supernatural rule still requires narration. This author review is not a blind silent-viewer test.',
          '', '## Engineering QA',
          f'Pipeline validator: VALID. Final technical QA: all {len(qa["checks"])} checks true. 1080×1920, 30 fps, 1080 frames, H.264 High/yuv420p, AAC 48 kHz stereo, faststart, no embedded subtitle stream; complete decode succeeded.',
          f'Dense output: {sample_count} decoded samples across six shots at 30/7 fps plus each final frame. All six timestamped strips were visually inspected for face, hair, clothing, prop geometry/state, set, crop and camera continuity.',
          'Opening editorial question is visible only at 1.0–3.5 s. No burned narration captions or fiction labels. In-world text is limited to the declared evidence. Six measured narration WAVs and three synthesized nonverbal SFX are represented in both sidecars.',
          f'Caption alignment: measured trimmed source PCM, exact SRT-content comparison and bounds checks; no ASR/listening claim. Mix peak: {time["peak_dbfs"]:.2f} dBFS. Audio loudness/peak diagnostics are in commands.jsonl.',
          f'QA and hash evidence: `{rel(out/"qa/report.json")}`, `{rel(out/"qa/probe.json")}`, `{rel(out/"timeline.json")}`, `{rel(out/"manifest.json")}`.',
          '', '## Continuity and story-logic findings',
          '| Timestamps | Impact class | Observed finding |','|---|---|---|']
        lines += [f'| {t} | {impact} | {finding} |' for t,impact,finding in FINDINGS[sid]]
        lines += ['', 'No additional confirmed causal rule violation was identified in this author inspection. This is a limited observation, not proof of a passed story gate. All listed residual issues remain in the delivered master.',
          '', '## Calls, corrections, encodes and wall time',
          f'Built-in ImageGen: {len(images)} calls; one canonical sheet first, then two canonical-conditioned shot sheets'+(' and one shots-a correction.' if sid=='H03' else '.'),
          f'Every completed call has a receipt in `{rel(out/"images.jsonl")}`. Exported prompts and their hashes are in `{rel(out/"prompts")}/`. Original generated sheets are retained in assets; no external paid TTS call. Image billed cost UNKNOWN; no invented dollar figure.',
          'Six narration lines synthesized once with the existing local Kokoro model, voice af_heart, speed 1.08; trimmed PCM reused by all renders. Three local mathematical SFX WAVs (pulse/click/chime), no downloaded recordings.',
          f'Final render: {cost["encode_count"]} libx264 shot encodes + one stream-copy/AAC mux; {cost["wall_seconds"]:.3f} s. Cumulative production: {encodes} shot encodes, {render_seconds:.3f} s of render invocations.',
          f'Observed production wall span: {elapsed:.3f} s, from {stamp(begun)} to {stamp(finished)}. Boundary is initial story-file creation through final QA; includes queue time and other-story work, excludes initial repository reading. Do not sum overlapping story spans. See production-cost.json for the machine-readable cost record.']
        if sid=='H02':
            lines += ['Fix passes: 0. Pre-generation staging removed hinted fingers from shot-05 so the phone mechanism is not shown before the payoff. Door/crossing ambiguities recorded above were left as review findings.']
        elif sid=='H03':
            lines += ['Fix passes: 1 before encoding. Initial shots-a.png produced a near-glass mirror reading in the wrist insert; shots-a-fix.png replaces it with a single distant palm. Original and correction both retained and logged (initial accepted receipt was later superseded). Remaining handedness/hardware/geometry issues were not looped.']
        else:
            lines += ['Fix passes: 1 after v1 QA; first two source cells swapped to show the figure immediately, with no new ImageGen/TTS. Original h04-static-v1 master, QA, cost, and input-archive preserved; final h04-static-v2 reuses the three historical image receipts, documented in image-reuse.json. Cumulative encode count includes both renders.']
        lines += ['', '## Acceptance and unverified scope',
          'Story Quality Gate PENDING (no blind readers this round). Storyboard Quality Gate PENDING. Viewer Gate HUMAN_TEST_PENDING. Market acceptance NOT_TESTED; no retention, viewer preference, public data, or revenue evidence.',
          'Not verified: human listening, EN/zh-Hant phone playback, independent silent comprehension, emotional effect, external originality and commercial-rights review. Technical QA cannot establish these.',
          'Reproducible validation: `python -B experiments/cluepause/static-ten-20261124/urban_horror/job.py validate '+sid+'`. Production invocation: same entry point with `run '+sid+'`; existing master protection refuses overwriting, so a future rerender needs a new revision id.',
          'Shared pipeline regression: `python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/urban_horror/pytest-cache --basetemp artifacts/static-ten-20261124/urban_horror/pytest-temp` → 33 passed. `git diff --check` → exit 0.',
          'Root README installation/core/video commands were not run: no core/video changes, uv is absent from PATH, and rebuilding shared environments would violate the job-only write boundary. This is isolated pipeline/media engineering verification, not full core-engine acceptance.',
          'No commit, push, upload, YouTube action or memory edit. Only the two authorized urban_horror trees were written.']
        (folder/'record.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
        index.append(evidence)
    lines=['# Urban horror — static photographic batch','',
       'Three original fictional local videos, H02–H04. H01 was not reused. Rights pending_verification. English narration, separate English and Traditional Chinese SRTs, basic camera moves, local SFX, no character animation.',
       'Story Quality Gate PENDING; Storyboard Quality Gate PENDING; Viewer Gate HUMAN_TEST_PENDING. Technical QA success is separate from story or market acceptance.',
       '', '| ID | Title | MP4 (repository-relative) | Duration | SHA-256 | ImageGen | Honest quality note |',
       '|---|---|---|---|---|---|---|']
    for x in index:
        sid=x['story_id'][:3].upper()
        lines.append(f'| [{sid}]({sid}/record.md) | {x["title"]} | `{x["master"]}` | {x["duration_seconds"]:.3f} s | `{x["sha256"]}` | {x["imagegen_calls"]} | {NOTES[sid]} |')
    lines += ['', '## Scope and provenance',f'Branch: codex/cluepause-static-ten-20261124. Git SHA: `{SHA}`. No state-changing git commands; no commit, push, upload, YouTube, or memory edits.',
       'Owner authorization is the current request for three new urban_horror static photographic films. PLAN.md M0 limits were read; this is the explicitly authorized isolated content experiment, not an engine milestone expansion.',
       'Read: shared pipeline README, genre gates, readers-v2/results-v2.md, and the v3 findings via a read-only `git -c safe.directory=... -C ... show` on the specified v3 branch. No configuration change was made. The v3 report still found the H01 trap predictable; these candidates use different rules and avoid replaying the same final explanation. Originality remains externally unverified.',
       '', '## Local pipeline wrapper and operational limits',
       'job.py imports the shared pipeline unchanged, then overrides OUTPUTS to the authorized urban_horror artifact subtree. This is required because the shared default places story ids directly under the batch root; no shared pipeline file was modified.',
       'The existing read-only TTS environment has Kokoro/Pillow but lacks jsonschema. Inputs were validated with the normal Python, then audio mode used the existing TTS environment to synthesize six per-line WAVs per story. The normal Python rendered from those prerecorded trimmed WAVs. Both operations use shared pipeline functions. No package/environment installation or source-tree cache write was needed.',
       'Image reference sheets sometimes arranged examples differently than requested. Registry canonical cell/crop bindings were corrected to actual visible character/prop/set regions before conditioned shot calls. Reference-call-01.json preserves the exact original prompt; images.jsonl retains its original prompt hash. The reference sheet itself was not altered.',
       'The first H02 image receipt attempt correctly refused while the audio invocation owned the per-story lock. No lock was removed; logging was retried after synthesis finished. Every completed image call is now recorded exactly once per story revision (H04 v2 copies historical receipts, not new calls).',
       'build_inputs.py records the initial pre-image draft and creates local Foley. It is not a safe rebuild command for delivered edits: rerunning it resets final shot/canonical bindings. Delivered story.md/shots.json/references.json are the final inputs. write_records.py only regenerates records from existing media.',
       'All explicit caches/temp, including TTS, pytest and proposed uv cache location, are beneath the authorized urban_horror paths. Existing model/tool files were read only. Executable/model hashes were verified by the pipeline; local installation paths were supplied through environment variables and are not stored in written records.',
       '', '## Verification',
       'All three final inputs: VALID. All three final masters: all ten technical QA checks true; 1080×1920, 30 fps, 36.000 s, H.264 High/yuv420p, AAC 48 kHz stereo, separate EN/zh-Hant sidecars, faststart, complete decode. Each final master has 162 dense decoded samples inspected by the authoring agent, six source plates and a silent storyboard export.',
       'Pipeline test command: `python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/urban_horror/pytest-cache --basetemp artifacts/static-ten-20261124/urban_horror/pytest-temp` → 33 passed in 0.64 s.',
       'Delivery audit: `python -B experiments/cluepause/static-ten-20261124/urban_horror/audit_delivery.py` checks final input/master/image/prompt hashes, WAV formats, duration, sample counts, untracked-source whitespace and personal absolute paths in text; result retained in `artifacts/static-ten-20261124/urban_horror/delivery-audit.json`.',
       'Per-story validate: `python -B experiments/cluepause/static-ten-20261124/urban_horror/job.py validate H02` (also H03/H04). Render: replace validate with run after supplying the environment bindings from the shared README. Existing masters are protected; use a new revision id for any new encode.',
       'Root README uv/core/video acceptance was not run because this task modifies neither engine nor video source and may not rebuild shared state. uv was not present on PATH. No standalone smoke render was needed: real stories exercised the shared render/QA path. Story-level cost.json, production-cost.json, commands.jsonl, images.jsonl, manifest.json and qa/ retain evidence.',
       f'Unique image calls: {sum(x["imagegen_calls"] for x in index)}. Unique local TTS line syntheses: 18. Cumulative shot encodes: {sum(x["cumulative_encode_count"] for x in index)} (includes preserved H04 v1); four final mux invocations. Image billing UNKNOWN, no dollar estimate. Per-story observed wall spans include shared queue time and must not be summed.',
       '', '## Unverified acceptance',
       'Human listening, physical phone playback, independent comprehension/emotional response, external originality/rights verification and all market evidence remain uncollected. Per-video records list residual continuity and visual-logic ambiguities with timestamps and impact classes. No quality gate is claimed passed.']
    (ROOT/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (OUT/'index.json').write_text(json.dumps(index,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(index,indent=2))

if __name__=='__main__': main()
