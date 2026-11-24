# Isolated AI blind readers

## Usage

Run from the repository root in Bash 4+ (Git Bash on Windows), with an authenticated
Codex CLI on `PATH`, GNU `realpath`/`sha256sum`, and standard Unix tools:

```bash
bash experiments/cluepause/genre-pilot-20261124/readers/run_blind_readers.sh \
  --packet-root experiments/cluepause/genre-pilot-20261124/readers-v3 \
  --output-root "${TMPDIR:-/tmp}/cluepause-readers-v3-run1" \
  --series "puzzle uncanny_mystery urban_horror" \
  --readers "A B C" --model gpt-6.1-sol --reasoning-effort high
```

Packet layout is `<packet-root>/<series>/{part1-setup.md,part2-reveal.md}`.
The series, reader labels, model and effort above are the defaults. Use `--help`
for options. The output root must be outside this repository; choose a fresh
output root for reruns. Existing reader directories are rejected, never deleted.

Each reader runs serially in a new `<output-root>/<series>/<reader>/` directory,
initially containing only `part1-setup.md`. Stage 1 writes `guess.md`; the tool
saves `session-id.txt` and `guess.sha256` (`<hash>  guess.md`) before copying the
reveal. Stage 2 resumes that exact session to write `review.md`, then verifies
the original guess and checksum manifest are unchanged. `urban_horror` uses the
horror prompts; other series use the common prompts, verbatim from the reference.
Logs remain beside reader directories as `<reader>.stage1.log` and
`<reader>.stage2.log`. One status line is printed per reader; any reader failure
makes the tool exit nonzero, while other readers still run.

Isolation uses separate folders, fresh sessions and the reference prompts; it
does not provide an OS-level read barrier. Codex user configuration, authentication
and executables are operator-managed. These are AI editorial diagnostics, not
human-viewer or market validation.
