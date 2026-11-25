"""Record only U01 evidence; leave shared READMEs and memory untouched."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
U01 = HERE.parents[1]
REPO = HERE.parents[6]
OUT = REPO/'artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v2'

if __name__ == '__main__':
    proof = json.loads((HERE/'verification.json').read_text(encoding='utf-8'))
    cost = json.loads((OUT/'cost.json').read_text(encoding='utf-8'))
    first = json.loads((OUT/'attempt1/cost.json').read_text(encoding='utf-8'))
    calls = [json.loads(x) for x in (HERE/'images.jsonl').read_text(encoding='utf-8').splitlines()]
    inspection = {
        'master_sha256':proof['sha256'], 'reviewer':'producing main agent',
        'final_decoded_frames_reviewed':177, 'final_strips_reviewed':[f'shot-{i:02}' for i in range(1,13)],
        'sampling_fps':30/7, 'silent_storyboard_reviewed':True,
        'first_attempt_decoded_frames_reviewed':177, 'first_attempt_strips_reviewed':12,
        'first_attempt_silent_storyboard_reviewed':True,
        'observations':{
            'paper':'Rear views 06/11 show continuous dry downward apron covering entire rear vent entry width. Top sheet persists in 07/08/09; paper OOF in 10/12, never removed.',
            'hose':'Both black hoses attach to ivory inline connector in all relevant interior views 02/03/07/10/12; 03 has natural shoe occlusion.',
            'leak':'29-33.5: side-wall midpoint jet, not an end outlet. 35.5-38: no jet; small tray overflow reaches bottom seam.',
            'shoes_character':'Dry-looking canvas/laces wherever visible; wet soles established 03, dry reset 07, shallow water 10/12. Same black bob and rust/navy wardrobe.',
            'seams':'No generated white divider visible in final sampled frames after explicit measured sheet crops.',
            'disclosure':'Opening question only 1-3.5 seconds; connector inactive before 29; side-split jet and answer-bearing EN/zh-Hant text start at 29 or later.',
            'silent':'Locked dripping storage, sole droplets, plant/old-mark hypothesis, rear-apron test, dry reset/key, attached side leak, dry apron, tray-to-seam overflow can be seen. Recurrence and sole key ownership rely on narration.'
        },
        'independent_review':'PENDING', 'human_acceptance':'HUMAN_TEST_PENDING',
        'residuals':'See mechanism.md; especially partly occluded saucer footprint and inherited mineral-ring/streak mismatch.'
    }
    (HERE/'inspection.json').write_text(json.dumps(inspection,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    row1 = f"| U01 | The Shoes That Stayed Wet — `{proof['master']}` | 38 s | `{proof['sha256']}` | 4 / 4 (v2 only) | FIX-CANDIDATE pending independent review; not uploaded. Rear-route paper and attached side-split leak revised; residuals in U01 record. Gates PENDING / PENDING / HUMAN_TEST_PENDING. |"
    row2 = '| [U01](uncanny_mystery/U01/record.md) | The Shoes That Stayed Wet | FIX-CANDIDATE | v2: full rear-route paper and attached side-split leak revised; independent review PENDING, not uploaded; gates PENDING / PENDING / HUMAN_TEST_PENDING. |'
    (HERE/'proposed-readme-rows.md').write_text('# Proposed README rows (not applied)\n\nGenre README:\n\n'+row1+'\n\nBatch README:\n\n'+row2+'\n',encoding='utf-8')
    commands = '''```text
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/U01/revisions/v2/run_revision.py validate
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/U01/revisions/v2/run_revision.py run
python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v2/cache/pytest --basetemp artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v2/tmp/pytest
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/U01/revisions/v2/audit_revision.py
git diff --check
```'''
    text = f'''# U01 v2 — The Shoes That Stayed Wet

**FIX-CANDIDATE pending independent review; NOT_UPLOADED.** This is a new visual revision of U01, not an acceptance of v1. The original v1 story, shots, references, assets, narration and master are unchanged, verified by hashes. The original record is retained byte-for-byte at `revisions/v2/v1-record-snapshot.md`; its findings below remain historical v1 findings.

The new rear camera views show a continuous dry paper apron above the entire rear vent entry width. The sheet visibly persists on top through the intervening exterior/front shots. The leak close-up retains both black hose attachments and shows a jet from the ivory connector's side wall; the final view retains that assembly. These observations support the intended mechanism, subject to the residuals and independent review below.

Master: `{proof['master']}`. Duration **38.000 s**, 1140 frames, 1080x1920, 30 fps, H.264 High/yuv420p, AAC 48 kHz stereo, faststart, no embedded subtitles.

SHA-256: `{proof['sha256']}`.

Sidecars beside master: `uncanny-u01-v2.en.srt`, `uncanny-u01-v2.zh-Hant.srt`. Silent storyboard: `silent-storyboard.jpg` and companion JSON; no question/captions in the silent image. Final dense decoded evidence: `qa/shot-01-strip.jpg` through `qa/shot-12-strip.jpg` and per-shot `samples.json`.

Base Git SHA: `{proof['base_git_sha']}` on `codex/cluepause-static-ten-20261124`. This is provenance of the existing checkout, not a commit containing this revision. No commit, push, upload, YouTube operation, memory edit, other-story edit, shared-pipeline edit or README edit was performed. The separate source checkout was only read for pinned render executables. Tool paths are supplied externally through environment variables and scrubbed from saved command evidence.

Story Quality Gate **PENDING**. Storyboard Quality Gate **PENDING**. Viewer Gate **HUMAN_TEST_PENDING**. Independent review **PENDING**. Market acceptance **NOT_TESTED**. Rights **pending_verification**. No status here grants upload/publication authority.

## Mechanism states, per-shot changes and transitions

The complete table and all eleven adjacent-cut confirmations are maintained in [mechanism.md](revisions/v2/mechanism.md). OOF states are explicitly distinguished from direct visual evidence. The table is also included here for review.

'''
    mechanism = (HERE/'mechanism.md').read_text(encoding='utf-8')
    table = mechanism.split('## Per-shot state and changes\n\n',1)[1].split('\n## Transition confirmation',1)[0]
    text += table + '\n\n'
    text += f'''## Engineering acceptance and disclosure

Shared job validation: **VALID**. Final machine media QA: **PASS**, all 10 checks true, including full decode, expected video/frame/duration/audio, faststart, no embedded subtitles, both exact SRT comparisons and caption bounds. Source PCM is reused, not resynthesized: all nine original WAVs and all nine EN/zh-Hant narration lines match v1 byte-for-byte. All source/input, image result, conditioning-image and exact-prompt hashes match. See `revisions/v2/verification.json`, `inspection.json`, and artifact `qa/report.json`, `manifest.json`, `assets.json`, `commands.jsonl`.

The main agent inspected **all 12 final decoded strips / 177 frames at 4.286 fps plus shot-end samples**, and the final silent storyboard. First-attempt strips and silent storyboard were also inspected before the permitted corrections. No white sheet-divider exposure or additional camera clipping of the rear vent/apron, hose attachments or side jet was observed in final samples. Shot-11 holds at 1.0 zoom; the other shots retain gentle 1.005-1.025 zoom. Generated column widths are unequal, so explicit measured whole-sheet crops in `crop-evidence.json` replace an equal-grid assumption. No painted water, digital paper patches or explanatory diagrams were added.

Opening question remains only at 1.0-3.5 s. The same question and non-reveal narration do not disclose the answer. Connector is inactive before 29 s. Reveal line-08 and its EN/zh-Hant captions run **29.000-32.610625 s**; line-09 runs **33.500-36.266458 s**. Pump sound/caption starts 29.1 s. Exact SRT-to-PCM schedule comparison and text inspection found no early answer disclosure; this is not ASR or human listening evidence.

Pipeline pytest: **33 passed in 0.53 s**, using the U01-specific cache/basetemp directories above; `revisions/v2/pipeline-pytest.txt` contains the result. The initial test invocation had 31 fixture-setup errors and 2 passes because the basetemp parent did not exist; creating that parent fixed the setup and the same suite passed. The final audit's first path scan matched its own literal search pattern; splitting that literal fixed the scanner and it passed without changing media or story inputs.

Commands from repo root, with existing pinned tools/font and Git SHA supplied by environment:

{commands}

Results: validate VALID; final render PASS; pytest 33 passed; revision audit PASS; `git diff --check` PASS. Personal-path grep is implemented by `audit_revision.py` across U01 and its v2 output tree; final result PASS. No production source, video application, governance contract or framework version changed; their unrelated npm/core/governance suites were not rerun for this local story revision. The shared pipeline remains unchanged.

## ImageGen ledger, attempts and counts

**4 new built-in ImageGen calls / 4 bitmaps** for v2; cost **UNKNOWN**. Exactly one correction per sheet: mechanism attempts 1/2, resolution attempts 1/2. No API fallback or additional correction. Every call is recorded in `revisions/v2/images.jsonl` and the artifact ledger; exact prompts and conditioning hashes are frozen in `revisions/v2/image-prompts-used.json`. v1's historical five requests/four bitmaps remain unchanged; cumulative U01 history is nine requests/eight bitmaps, not four total.

| Call | Sheet / attempt | Disposition | Result SHA-256 |
| --- | --- | --- | --- |
'''
    for i,c in enumerate(calls,1):
        text += f"| {i} | {c['sheet']} / {c['attempt']} | {c['status']} | `{c['result_sha256']}` |\n"
    text += f'''
First master was technically valid but rejected after producer review for insufficiently explicit rear-fold geometry and a white seam at shot-08. Preserved with its inputs and full QA under artifact `attempt1/`, and as `uncanny-u01-v2-attempt1.mp4`; SHA-256 `d640bb33ffc3420ff18cfbf59507474b67a641183641838b574b5baffb3fe7de`. Original generated images are preserved as `mechanism-attempt1.png` and `resolution-attempt1.png`.

Two render invocations, 12 H.264 cut encodes and one stream-copy/AAC mux each: **24 cut encodes total**, two final muxes. First pipeline wall time **{first['wall_seconds']} s**; final pipeline wall time **{cost['wall_seconds']} s**. No new TTS. Image generation wait time and producer review are outside those render durations.

## Residuals and unverified acceptance

The entire paper footprint under the saucer is not exposed: shot-11 only slightly lifts it. The visible dry evidence is the surrounding top paper and uninterrupted rear apron across the whole entry opening. Rear-apron persistence in front-facing 07-09 is inferred from the continuously visible full top sheet and matching rear views 06/11; it is not directly visible behind the cabinet in those front views. Exact five-centimetre fold depth is unmeasured. Narrow side rails remain outside the paper, but no unpapered path from the saucer to the rear vent is visible. Independent review must assess the exclusion argument.

Inherited residuals: strongest mineral band remains on pot exterior (04), old streak remains on a side/front corner (05), neutral camera-facing expression remains in 02. Side jet arcs into the tray rather than visibly tracking down the rear wood. Static water and hand actions remain frozen. Recurrence, sole key ownership and elapsed time partly rely on narration. No new line was invented to excuse a visual problem.

No independent story/visual review, human phone-scale viewing, complete human listening, EN/zh-Hant/OFF playback acceptance, originality/commercial-rights clearance, or market measurement. Proposed genre and batch README rows are saved only in `revisions/v2/proposed-readme-rows.md`; shared READMEs were not edited.

---

## Archived v1 findings (historical; not observations of v2)

'''
    (HERE/'record.md').write_text(text,encoding='utf-8')
    original = (HERE/'v1-record-snapshot.md').read_text(encoding='utf-8')
    (U01/'record.md').write_text(text+original.split('\n',1)[1],encoding='utf-8')
    print('U01 record and revision evidence written; shared READMEs unchanged')
