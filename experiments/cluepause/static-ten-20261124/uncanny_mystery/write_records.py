"""Assemble portable evidence after the main agent's decoded-frame inspection."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from run_local import pipeline, HERE, REPO, OUT

SHA='aef24410f8b45c8651fd922343aeb52db11bfc75'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def rel(p): return p.relative_to(REPO).as_posix()
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

index=['# Uncanny mystery — static photographic pilots','',
       'Three local fictional candidates. Story Quality Gate **PENDING**; Storyboard Quality Gate **PENDING**; Viewer Gate **HUMAN_TEST_PENDING**. Rights **pending_verification**. Market acceptance **NOT_TESTED**. No blind readers or humans tested these MP4s. No release approval is implied.','',
       f'Base Git SHA: `{SHA}`; branch `codex/cluepause-static-ten-20261124`. Files are uncommitted; this SHA is provenance for the base, not a claim that these new files are committed.','',
       '| ID | Title / MP4 (repository relative) | Duration | SHA-256 | ImageGen requests / generated bitmaps | Honest quality note |',
       '| --- | --- | --- | --- | --- | --- |']
for code in ('U01','U02','U03'):
    story=HERE/code; data=read(story/'shots.json'); meta=read(story/'editorial.json')
    out=OUT/data['story_id']; report=out/'qa/report.json'; inspection=story/'inspection.json'
    if not report.exists() or not inspection.exists():
        index.append(f'| {code} | {meta["title"]} | PENDING | — | — | Production or inspection incomplete |')
        continue
    review=read(inspection); qa=read(report); cost=read(out/'cost.json'); probe=read(out/'qa/probe.json')
    timeline=read(out/'timeline.json'); voice=read(out/'voice-production.json')
    ledger=[json.loads(x) for x in (out/'images.jsonl').read_text().splitlines()]
    bitmaps=sum(x['result_filename'].endswith('.png') for x in ledger)
    master=out/(data['story_id']+'.mp4'); duration=float(probe['format']['duration']); master_hash=digest(master)
    sampled=sum(len(read(out/'qa'/s['id']/'samples.json')['times']) for s in data['shots'])
    elapsed=(datetime.now(timezone.utc)-datetime.fromtimestamp((story/'editorial.json').stat().st_ctime,timezone.utc)).total_seconds()
    # Freeze every prompt actually used, including an initial reference payload overwritten by later exports.
    used=[]
    for row in ledger:
        candidates=list((out/'prompts').glob(row['sheet']+'*.json'))
        payloads=[read(p) for p in candidates]
        payloads.append(pipeline.build_prompt.__globals__['original_prompt'](data,read(story/'references.json'),row['sheet'],False))
        matched=next((x for x in payloads if hashlib.sha256(x['prompt'].encode()).hexdigest()==row['prompt_sha256']),None)
        used.append({**row,'prompt':matched['prompt'] if matched else 'UNRECOVERED',
                     'input_note':'Complete canonical sheet for shot generation; U01 rejected six-reference request produced no bitmap; correction additionally used its rejected sheet.'})
    pipeline.save(story/'image-prompts-used.json',used)
    assert all(x['prompt']!='UNRECOVERED' for x in used)
    text=f'# {code} — {meta["title"]}\n\nFICTION. Genre: uncanny_mystery. Rights: **pending_verification**.\n\n{meta["summary"]}\n\n'
    text+='Story Quality Gate **PENDING** (no blind readers this round). Storyboard Quality Gate **PENDING**. Viewer Gate **HUMAN_TEST_PENDING**. Market acceptance **NOT_TESTED**.\n\n'
    text+=f'Base Git SHA: `{SHA}`. This is the unchanged base, not a commit containing these files. Main-agent image inspection is not human viewer acceptance.\n\n'
    text+=f'Master: `{rel(master)}`. Duration **{duration:g} s**; SHA-256 `{master_hash}`. Sidecars: `{data["story_id"]}.en.srt` and `{data["story_id"]}.zh-Hant.srt` beside the master.\n\n'
    text+='## Shot functions and silent-storyboard intent versus observed frames\n\n'
    text+='Authored SILENT STORYBOARD was written in story.md before any ImageGen. The following observations were made by the main agent from the silent export and all dense decoded temporal contact strips, not inferred from the prompts.\n\n'
    text+='| Time | Shot / narrative function | Silent intent | What decoded frames actually show |\n| --- | --- | --- | --- |\n'
    for s,actual in zip(data['shots'],review['shots'],strict=True):
        text+=f'| {s["start"]:g}–{s["end"]:g} s | {s["id"]} / {s["function"]} | {s["conveys"]} | {actual} |\n'
    text+='\n'+review['silent_conclusion']+'\n\n## Continuity and story logic\n\n| Time | Impact class | Finding / consequence |\n| --- | --- | --- |\n'
    for f in review['findings']:text+=f'| {f["time"]} | {f["impact"]} | {f["finding"]} |\n'
    text+='\n'+review['continuity_summary']+'\n\n'
    text+=f'Visual correction passes: **{review["fix_passes"]}**. {review["fix_note"]} No further loop was run.\n\n'
    text+='## Engineering QA and commands\n\n'
    text+=f'Shared validator: VALID. Machine media QA: **{qa["engineering"]}**; this is a technical result, not a quality-gate decision. All {len(qa["checks"])} reported boolean checks: '+', '.join(f'{k}={v}' for k,v in qa['checks'].items())+'.\n\n'
    text+=f'Full decode and technical probe: 1080×1920, 30 fps, H.264 High/yuv420p, AAC 48 kHz stereo, faststart, no embedded subtitles. Dense temporal QA: **{sampled} decoded frames**, every 7 frames (4.286 fps) plus each shot final frame; all {len(data["shots"])} strips and the silent storyboard inspected by the main agent. Camera zoom is 1.005–1.025; no character animation.\n\n'
    text+='Caption/audio alignment is measured trimmed 24 kHz mono PCM plus exact sidecar-to-cue comparison and bounds validation. Revealing narration starts no earlier than the first reveal shot. This is not ASR, listening, a human comprehension test, or a commercial-rights clearance. Human playback with EN, zh-Hant, captions OFF and sound OFF remains unverified. Original synthetic SFX are illustrative; no borrowed recordings.\n\n'
    text+='Commands, from repository root (environment tool paths supplied externally, never written into inputs):\n\n```text\n'
    text+=f'python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/run_local.py validate {rel(story)}\n'
    text+=f'python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/run_local.py prompts {rel(story)} --supports-images\n'
    text+=f'python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/run_local.py run {rel(story)}\n```\n\n'
    text+='TTS was synthesized once per line with the existing read-only render environment using `prepare_voice.py U01 U02 U03`; render inputs use the saved per-line PCM files. Actual encode, decode, probe and loudness-measurement argument arrays, timings and exit codes are in the portable `commands.jsonl` beside the master. Each image request has a receipt in `images.jsonl`; exact prompts are frozen in this story’s `image-prompts-used.json`.\n\n'
    text+='## Counts, time and cost\n\n'
    text+=f'- ImageGen requests logged: **{len(ledger)}**; bitmap outputs generated: **{bitmaps}** (including rejected bitmaps); tool-validation rejections without an image: **{len(ledger)-bitmaps}**. Built-in ImageGen, no API fallback. Cost **UNKNOWN**; do not infer dollars from request count.\n'
    text+=f'- H.264 encode count: **{cost["encode_count"]}**, one per shot; one final stream-copy/AAC mux. Master render invocations: **1**. Pipeline measured wall time: **{cost["wall_seconds"]} s**.\n'
    text+=f'- Measured local TTS production: **{voice["seconds"]} s**, af_heart at 1.08. No hosted TTS or model download.\n'
    text+=f'- Elapsed from the initial editorial manifest creation to record assembly: **{elapsed:.1f} s**; includes tool waits and work on the other two stories, and is not exclusive labor or ImageGen service time.\n\n'
    text+='## Limits and acceptance\n\n'+review['quality_note']+'\n\n'
    text+='No blind readers, phone-scale human test, full human listening, external originality/similarity review or market measurement. Existing v2/v3 text-reader findings informed writing only; none transfers as a gate decision for these films. U01 retains the v3 English/Chinese lines and causal story; generated failures are expressly recorded above. U02 and U03 are new original-fiction candidates with distinct mechanisms. No commit, push, upload, YouTube access, memory edits, production engine changes or shared-pipeline edits.\n'
    (story/'record.md').write_text(text,encoding='utf-8')
    pipeline.save(out/'production-summary.json',dict(id=code,title=meta['title'],mp4=rel(master),duration=duration,sha256=master_hash,imagegen_requests=len(ledger),generated_bitmaps=bitmaps,encode_count=cost['encode_count'],render_wall_seconds=cost['wall_seconds'],elapsed_author_to_record_seconds=round(elapsed,1),base_git_sha=SHA,wrapper_sha256=digest(HERE/'run_local.py'),inspection_sha256=digest(inspection),story_quality_gate='PENDING',storyboard_quality_gate='PENDING',viewer_gate='HUMAN_TEST_PENDING',rights_status='pending_verification'))
    index.append(f'| {code} | {meta["title"]} — `{rel(master)}` | {duration:g} s | `{master_hash}` | {len(ledger)} / {bitmaps} | {review["quality_note"]} |')
index+=['','## Isolation and local workarounds','',
        '`run_local.py` imports the shared pipeline read-only and reroutes OUTPUTS to `artifacts/static-ten-20261124/uncanny_mystery/`. It confines Python/TTS/temp/provider caches to this genre folder, uses Python `-B`, and supplies the whole canonical sheet as one attached reference image because ImageGen accepts at most five reference paths while the pipeline can export six cells. No shared file was changed. ImageGen itself uses its tool-managed default image output; every project asset was copied into the allowed genre tree.','',
        'The wrapper appends a tall-cell layout instruction before prompt hashing. U01’s initial reference used the stock prompt; its exact prompt is recovered and frozen by hash. Its six-reference tool rejection is counted conservatively as a request, even though it generated no image. U01’s correction has an archived initial payload and a separate written correction instruction. No automatic image client or unlogged API fallback was used.','',
        'Kokoro models and FFmpeg/ffprobe were read from an existing installation using external environment bindings. Model and executable hashes are verified by the shared pipeline. Per-line WAVs were generated once, copied into each story’s assets, and measured for render timing. `author.py` is the initial authoring helper: rerunning it would reset the measured input file bindings; do not run it over a finished delivery.','',
        '## Verification and acceptance boundaries','',
        '`python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/uncanny_mystery/cache/pytest --basetemp artifacts/static-ten-20261124/uncanny_mystery/tmp/pytest` → **33 passed in 0.70 s**. All three inputs were VALID before ImageGen. Each completed master has its own probe, dense frames, measured timeline, sidecars, silent export, input hashes, commands and cost record.','',
        '`python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/verify_delivery.py` checks all three masters, input/receipt/prompt hashes, exact sidecars, image budgets, pending gate states, Python syntax, authored whitespace and personal-path confinement. Final evidence: `artifacts/static-ten-20261124/uncanny_mystery/verification.json`. U01’s nine EN/zh-Hant source lines were retained verbatim. Main agent inspected all **32 dense strips / 506 sampled decoded frames**, plus the three silent exports. This is visual inspection by the producing agent, not a blind or human viewer test.','',
        'Final local renders: U01 **38 s**, 12 cut encodes, 70.469 s pipeline wall time; U02 **36 s**, 10 cut encodes, 46.141 s; U03 **36 s**, 10 cut encodes, 44.312 s. Total **12 ImageGen requests / 11 generated bitmaps**; U01 includes one request rejected by tool validation before generation. ImageGen cost remains UNKNOWN. One visual correction pass each for U01 and U03, none for U02; one master render per story. Defects remain documented rather than looped.','',
        'Root engine/Node/governance commands were not rerun: their code was unchanged, and installing dependencies or writing their shared environments would exceed the explicit genre-only write boundary. No framework update or state-changing Git command was run. Engineering checks and market acceptance are recorded separately; all story/storyboard/viewer gates retain the pending states above.','',
        'All authored and generated project files are confined to the two authorized genre directories. The existing source installation was used read-only for preinstalled models/tools. No personal absolute paths are stored in this delivery. See each `<id>/record.md` for defects and unverified scope.']
(HERE/'README.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
