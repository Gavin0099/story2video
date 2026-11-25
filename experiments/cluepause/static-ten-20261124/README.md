# CluePause static ten — 2026-11-24 batch

Ten local fictional videos: four puzzles, three uncanny mysteries and three urban horrors. Records updated 2026-11-25 Asia/Taipei on branch `codex/cluepause-static-ten-20261124`; base Git SHA `aef24410f8b45c8651fd922343aeb52db11bfc75`. These additions remain uncommitted; the SHA identifies the base, not their contents. Genre READMEs retain master paths, hashes and engineering evidence.

| Video | Title | Status | Reason / retained limitation |
| --- | --- | --- | --- |
| [P01](puzzle/P01/record.md) | The Thread Under the Scale | HOLD | Changing thread force path breaks story logic. |
| [P02](puzzle/P02/record.md) | The Blackened Message | UPLOAD-CANDIDATE private | Printing causality survives; opening makes it predictable and blackened letters remain legible by relief/sheen. |
| [P03](puzzle/P03/record.md) | The Crack That Crossed the Table | HOLD | At 27–30 s the wire shadow disappears outside the hand shadow on still-lit areas; breaks story logic. |
| [P04](puzzle/P04/record.md) | The Rope He Refused to Pull | HOLD | Rope tail/anchor survives flag rise, breaking the release mechanism's story logic. |
| [U01](uncanny_mystery/U01/record.md) | The Shoes That Stayed Wet | HOLD | Paper coverage/disappearance and connector/hose changes break story logic. |
| [U02](uncanny_mystery/U02/record.md) | The Chair That Came to Breakfast | UPLOAD-CANDIDATE private | Towing sequence is coherent; attachment is cropped/occluded and the culprit is strongly telegraphed. |
| [U03](uncanny_mystery/U03/record.md) | The Man in the Pantry Door | HOLD | High shadow persists after its source is lowered, breaking projection logic. |
| [H02](urban_horror/H02/record.md) | The Smallest Mirror | UPLOAD-CANDIDATE private | Mirror/phone states are coherent; door trigger and finger crossing remain visually ambiguous. |
| [H03](urban_horror/H03/record.md) | The Woman with the Hammer | UPLOAD-CANDIDATE private | Lea's escape remains understandable; wrist handedness and window geometry drift. |
| [H04](urban_horror/H04/record.md) | The Name Underneath | HOLD | Opening question "Why did erasing her name fail?" discloses failure before the 17–23 s false relief. |

All HOLD videos remain not uploaded. UPLOAD-CANDIDATE private means a candidate for a private review copy, not Owner authorization or completed upload. This update performed no upload or other YouTube action.

## Upload results

On 2026-11-25 (Asia/Taipei), four videos were uploaded by hand in YouTube Studio on CluePause: U02 `S34P69d9R7w`, H02 `QIftXOzmkQc`, H03 `ou7vZTG66Sg`, P02 `ywcvdupwbFQ`. All are **UPLOADED_PRIVATE**, private, not made for kids, with "altered or synthetic content / AI used" set to yes. The metadata's English titles and descriptions were applied; zh-Hant titles/descriptions were not applied and no captions have been uploaded yet.

U02/H02/H03 used their unchanged master MP4s. P02 used `artifacts/static-ten-20261124/puzzle/puzzle-p02-static-v1/puzzle-p02-static-v1-upload.mp4` because the browser upload tool caps files at 10 MB: 9,358,260 bytes, SSIM versus master mean 0.994005 / min 0.991581. Uploaded paths and SHA-256 values are recorded in [upload-metadata.json](upload-metadata.json). YouTube processing/checks results were not confirmed at upload time. Story and Storyboard Quality Gates remain **PENDING**, Viewer Gate **HUMAN_TEST_PENDING**; private upload is neither a quality-gate pass nor publication approval. Market acceptance remains **NOT_TESTED**.

Records-only engineering validation at base Git SHA `103e47eda11c0137f1d96e2857e4d3cd92eb6ff8`: `python -B -` JSON/fact assertions and trailing-whitespace scan, plus `git diff --check`, passed. Media, core-engine acceptance and YouTube processing/checks were not reverified.

## Independent review and acceptance

The [2026-11-25 independent review](../../../artifacts/independent-review-static-ten-20261125/REVIEW.md) returned **REQUEST_CHANGES** for the records. Its six-film inspection recommended private review copies for P02/U02/H02/H03 and HOLD for P03/H04; the other four exclusions were checked for candid records rather than independently re-reviewed from MP4. The P03 severity correction and H04 omitted spoiler are now recorded. This is not a new independent approval verdict and does not fix either film.

Engineering acceptance: existing reports record technical PASS/VALID for all ten; independent probes/full decodes cover the six inspected films. This update changes records only and does not rerun media or core-engine acceptance. Story Quality Gate **PENDING**, Storyboard Quality Gate **PENDING**, Viewer Gate **HUMAN_TEST_PENDING** for every video. Rights **pending_verification**. Market acceptance **NOT_TESTED**; no human comprehension, retention, demand or revenue acceptance is claimed.

## Lessons for the next batch

- Recurring failure: generated stills break physical continuity of the plot mechanism itself—threads, ropes, shadows, paper and hoses. Give the mechanism prop its own reference and check its state in every shot: attachment/force path, position, illumination/occlusion, coverage and before/after evidence.
- Check opening question text against the spoiler boundary, including outcomes that must stay unknown through false relief. For a future H04 revision, ask whether erasing the name will save her without asserting failure; keep current inputs aligned with the retained render.
- Future SHOULD-FIX items: match H03's wrist insert to the canonical left-wrist wrap; show H02's door closure and fingers physically crossing the phone plane. These revisions were not performed.

## Records-only verification scope

At the base SHA above, `git diff --check` exited 0. A read-only `python -B -` scan covered 182 files (the three genre trees plus this README), including 77 UTF-8 text files: no trailing whitespace, space-before-tab indentation, conflict markers, blank lines at EOF or personal absolute paths were found. The untracked-file scan supplies the whitespace coverage absent from tracked Git diff. SHA-256 comparison against the pre-edit genre snapshot found only six changed Markdown records/summaries; all other genre files, including shots.json, stayed unchanged. This README is the sole new file.

No source/video/governance code changed; root README pytest/npm/governance acceptance commands were not rerun. Media listening, phone playback, human/blind tests, external rights/originality checks, YouTube behavior and market evidence remain unverified. No commit, push, memory edit, rerender or ImageGen was performed.
