# Running the editorial experiment

Use a new evidence directory for each user-authorized run. Save successive drafts as JSON with these fields.

| Field | Meaning |
|---|---|
| `story`, `version`, `parent` | Two-digit story ID, revision ID and source Git SHA or previous draft SHA |
| `first`, `second`, `reveal`, `english` | Exact texts. Put the question at the end of `second`. |
| `cores` | Labels and definitions for answers the card must support. Keep later details of execution and emotional payoff out of these requirements. |
| `hypothesis`, `change`, `belief_shift` | Before testing, record what the Writer changed and what new inference should become possible. |

Run with the repository's Python and an absolute path to the trusted, already installed Codex binary. Supply the digest of that binary at setup. The approved local profile uses existing ChatGPT CLI authentication and disables project/user config, shell, image, memory, network tools and delegation. Each stage runs in a new empty working directory. The prior stages are passed forward verbatim as text. Neither answer material nor previous feedback goes into the first two prompts. The harness records engine IDs and audits CLI events for every stage.

```powershell
$runner = Join-Path $skillRoot 'scripts/autoloop.py'
uv run --locked python $runner run draft.json evidence-dir --base-sha $baseSha --codex $codexPath --sha256 $codexDigest --credentials keyring
uv run --locked python $runner verify evidence-dir
```

Use the directory containing this skill's `SKILL.md` as `$skillRoot`. Freeze `$baseSha` from `git rev-parse HEAD` at the start. Use that SHA for first proposals and the archived draft's SHA-256 from the ledger for follow-up revisions. Keep the original source and the writer's replacement text available for comparison.

The default cohort reserves three formal readers. Use `--mode explore` for two diagnostic readers whose results never qualify a version. For an invalid formal session only, use `--readers 1` within the remaining budget. The gate does not round scores. A CLI process failure, unknown event, tool use, loss of a prior turn or missing raw output invalidates that reader. Resume with the same drafts and evidence directory. If a process was interrupted and no orchestrator remains, remove its `.lock` file only after confirming no job still uses the directory. Reservations without transcripts count toward the limit.

The verifier recalculates the gate and checks all reader evidence against frozen drafts and this rubric. It verifies an evidence bundle's internal consistency. It does not provide cryptographic attestation against a person who can rewrite every local file. The trusted runtime uses CLI controls plus a denied-access probe and rejects any reader run showing tool activity. Sessions from other runtimes require an equivalent verified profile.

New ledgers use protocol v2. The prompt distinguishes material defects from score reasons such as a reveal being easy to guess. Previous ledgers keep their original rubric, prompts and decisions. Use new draft versions for subsequent testing.
