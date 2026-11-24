#!/usr/bin/env bash
# Keep readers outside the repository; never expose the reveal before guess lock.
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: bash run_blind_readers.sh --packet-root DIR --output-root DIR [options]

  --packet-root DIR        Contains SERIES/part1-setup.md and part2-reveal.md
  --output-root DIR        Outside this repository; reader directories must be new
  --series "NAME ..."      Default: puzzle uncanny_mystery urban_horror
  --readers "ID ..."       Reader labels per series; default: A B C
  --model MODEL           Default: gpt-6.1-sol
  --reasoning-effort LEVEL Default: high (minimal/low/medium/high/xhigh/max)
  -h, --help              Show this help

Requires Bash 4+, Codex CLI (authenticated), realpath, sha256sum and standard
Unix tools. Paths are relative to the invoking directory. Readers run serially.
USAGE
}

die() { printf 'error: %s\n' "$*" >&2; exit 1; }

packet_root= output_root=
series_list='puzzle uncanny_mystery urban_horror'
reader_list='A B C'
model=gpt-6.1-sol
effort=high
while (($#)); do
  case $1 in
    -h|--help) usage; exit 0 ;;
    --packet-root|--output-root|--series|--readers|--model|--reasoning-effort)
      (($# >= 2)) && [[ -n $2 && $2 != --* ]] || die "missing value for $1"
      case $1 in
        --packet-root) packet_root=$2 ;;
        --output-root) output_root=$2 ;;
        --series) series_list=$2 ;;
        --readers) reader_list=$2 ;;
        --model) model=$2 ;;
        --reasoning-effort) effort=$2 ;;
      esac
      shift 2 ;;
    *) die "unknown argument: $1 (see --help)" ;;
  esac
done
[[ -n $packet_root && -n $output_root ]] || die '--packet-root and --output-root are required'
case $effort in minimal|low|medium|high|xhigh|max) ;; *) die "invalid reasoning effort: $effort" ;; esac

# Resolve the CLI before changing cwd so a reader folder cannot shadow it.
# Executables and the inherited user configuration remain operator-managed.
for tool in realpath sha256sum sed cp mkdir; do
  command -v "$tool" >/dev/null || die "required command not found: $tool"
done
codex_bin=$(type -P codex) || die 'Codex CLI not found on PATH'
if command -v cygpath >/dev/null; then
  codex_bin=$(cygpath -u -- "$codex_bin")
  packet_root=$(cygpath -u -- "$packet_root")
  output_root=$(cygpath -u -- "$output_root")
fi
codex_bin=$(realpath -- "$codex_bin")
script_dir=$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo_root=$(cd -- "$script_dir/../../../.." && pwd -P)
packet_root=$(realpath -e -- "$packet_root")
output_root=$(realpath -m -- "$output_root")
[[ -d $packet_root ]] || die 'packet root must be a directory'

# Canonicalize symlinks before checking the boundary; Git Bash paths are folded
# for Windows' case-insensitive filesystem. No existing reader data is deleted.
outside_repo() {
  local candidate=$1 repo=$repo_root
  case ${OSTYPE:-} in msys*|cygwin*|win32*) candidate=${candidate,,}; repo=${repo,,} ;; esac
  [[ $candidate != "$repo" && $candidate != "$repo/"* ]]
}
outside_repo "$output_root" || die 'output root must be outside the repository'
# An output ancestor of the repository would mix source and reader directories.
[[ $repo_root != "$output_root"/* && $output_root != / ]] || die 'output root must not contain the repository'

read -r -a series_names <<< "$series_list"
read -r -a reader_names <<< "$reader_list"
((${#series_names[@]} && ${#reader_names[@]})) || die 'series and readers must be nonempty lists'
validate_labels() {
  local label seen=' '
  for label in "$@"; do
    [[ $label =~ ^[A-Za-z0-9_][A-Za-z0-9_.-]*$ ]] || die "invalid label: $label"
    [[ $seen != *" ${label,,} "* ]] || die "duplicate label: $label"
    seen+="${label,,} "
  done
}
validate_labels "${series_names[@]}"
validate_labels "${reader_names[@]}"
for series in "${series_names[@]}"; do
  for part in part1-setup.md part2-reveal.md; do
    [[ -s $packet_root/$series/$part ]] || die "missing or empty packet: $series/$part"
  done
  for reader in "${reader_names[@]}"; do
    target=$output_root/$series/$reader
    outside_repo "$(realpath -m -- "$target")" || die "reader directory resolves inside repository: $series/$reader"
    [[ ! -e $target && ! -L $target ]] || die "reader directory already exists: $series/$reader"
  done
done
mkdir -p -- "$output_root"

stage1_common='You are a first-time viewer of a 30-40 second vertical short video. The file part1-setup.md in this folder describes exactly what a viewer sees and hears up to a short pause; treat it as the video. You have no other information about this story. Do not look for or open any other file, and do not search the filesystem or the web.

Read part1-setup.md, then write guess.md in this folder with these sections:
1. What is the video asking? (one sentence)
2. Most likely answer, with confidence %, and the specific evidence from the video that supports it.
3. One or two reasonable alternative explanations, with confidence %.
4. Which clue (if any) changed your understanding while watching, and when.
5. Captions OFF: which parts of the main anomaly would still be clear from images and sound alone?
6. Would you keep watching to the end? (1-5) and why.
After writing guess.md, stop. Do not continue the story.'

stage1_horror='You are a first-time viewer of a 30-40 second vertical short video. The file part1-setup.md in this folder describes exactly what a viewer sees and hears up to a short pause; treat it as the video. You have no other information about this story. Do not look for or open any other file, and do not search the filesystem or the web.

Read part1-setup.md, then write guess.md in this folder with these sections:
1. What is the main conflict or threat? (one sentence)
2. The rules of this world as you understand them, and anything that seems inconsistent.
3. What you expect or fear will happen next, with your reasoning; alternatives welcome. A single correct answer is not required.
4. When did unease start, and what caused it?
5. Captions OFF: which parts of the threat would still be clear from images and sound alone?
6. Would you keep watching to the end? (1-5) and why.
After writing guess.md, stop. Do not continue the story.'

stage2_common='Your guess is locked in guess.md; do not edit it. Now read part2-reveal.md (the rest of the video) and write review.md with:
1. Did the reveal explain the earlier anomaly? Which earlier clues does it reuse?
2. Did the reveal introduce any NEW setup that was necessary to understand the answer but was not shown before? Quote it.
3. Critical causal defects (logic holes, unfair clues, early spoilers, impossible actions). Quote the exact line or timestamp for each. Write "none" if none.
4. Was the twist interesting, ordinary, or flat for you, and how did your understanding change?
5. Did the ending pay off the expectation set at the start? (1-5)
6. Overall story score 0-100 for: clear anomaly in the first seconds, fair reasoning clues, no early answer, reveal re-explains the evidence, interest. Give the score and one line of justification.
Be strict and independent.'

stage2_horror='Your expectations are locked in guess.md; do not edit it. Now read part2-reveal.md (the rest of the video) and write review.md with:
1. Were the world rules consistent from start to end? Quote any inconsistency.
2. Did the ending introduce any NEW rule or setup that was necessary but not shown before? Quote it.
3. Critical defects (rule breaks, confusing staging, early spoilers, unearned ending). Quote the exact line or timestamp. Write "none" if none.
4. Tension: how did it build and where did it drop?
5. Did the ending pay off the suspense built earlier? (1-5) Was it interesting, ordinary, or flat?
6. Overall exploratory score 0-100 for: clear threat early, consistent rules, tension, earned payoff, interest. Give the score and one line of justification.
Be strict and independent.'

# --json emits thread.started on both start and resume. Require exactly one UUID
# so a missing, ambiguous or different session can never silently pass.
session_from_log() {
  sed -nE '/"type"[[:space:]]*:[[:space:]]*"thread.started"/s/.*"thread_id"[[:space:]]*:[[:space:]]*"([0-9a-fA-F-]+)".*/\1/p' "$1"
}
valid_session() {
  [[ $1 =~ ^[[:xdigit:]]{8}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{12}$ ]]
}
guess_checksum() {
  local raw
  raw=$(sha256sum --binary -- guess.md) || return
  # GNU sha256sum defaults to a '*' marker on Windows. Hash raw bytes but
  # explicitly format the required portable, path-free two-space manifest.
  printf '%s  guess.md\n' "${raw%% *}"
}

run_reader() (
  # Explicitly enable errexit: the parent collects failures without aborting the
  # remaining readers. The EXIT trap emits exactly one status line per reader.
  set -e
  series=$1 reader=$2
  dir=$output_root/$series/$reader
  status='failed to prepare empty reader directory'
  trap 'rc=$?; printf "%s/%s: %s\n" "$series" "$reader" "$status"; exit "$rc"' EXIT
  mkdir -p -- "$output_root/$series"
  mkdir -- "$dir"
  cd -- "$dir"
  cp -- "$packet_root/$series/part1-setup.md" part1-setup.md
  p1=$stage1_common p2=$stage2_common
  if [[ $series == urban_horror ]]; then p1=$stage1_horror; p2=$stage2_horror; fi
  cli_dir=$dir
  if command -v cygpath >/dev/null; then cli_dir=$(cygpath -w "$dir"); fi

  # Keep logs in the series directory until guess lock, so stage 1 starts with
  # only part1-setup.md in the reader directory. Refuse existing log files too.
  log1=$output_root/$series/$reader.stage1.log
  log2=$output_root/$series/$reader.stage2.log
  status='FAILED: stage 1 CLI (see stage1 log)'
  (set -o noclobber; "$codex_bin" -a never exec --json --skip-git-repo-check \
    -m "$model" -c "model_reasoning_effort=$effort" -s workspace-write \
    -C "$cli_dir" "$p1" > "$log1" 2>&1 < /dev/null)
  status='FAILED: missing or invalid stage 1 session ID'
  sid=$(session_from_log "$log1")
  valid_session "$sid"
  printf '%s\n' "$sid" > session-id.txt
  status='FAILED: missing or empty guess.md'
  [[ -s guess.md && ! -L guess.md ]]
  guess_record=$(guess_checksum)
  printf '%s\n' "$guess_record" > guess.sha256

  status='FAILED: could not copy reveal after guess lock'
  cp -- "$packet_root/$series/part2-reveal.md" part2-reveal.md
  stage2_rc=0
  (set -o noclobber; "$codex_bin" -a never exec resume --json --skip-git-repo-check \
    -m "$model" -c "model_reasoning_effort=$effort" -c sandbox_mode=workspace-write \
    "$sid" "$p2" > "$log2" 2>&1 < /dev/null) || stage2_rc=$?
  # Compare against the in-memory lock as well as the manifest, even if the CLI
  # failed. A rewritten checksum file cannot conceal an edited guess.
  status='FAILED: GUESS CHANGED OR MISSING (including lock manifest)'
  [[ -s guess.md && ! -L guess.md && -f guess.sha256 && ! -L guess.sha256 ]]
  [[ $(guess_checksum) == "$guess_record" && $(<guess.sha256) == "$guess_record" ]]
  status='FAILED: stage 2 CLI; guess unchanged (see stage2 log)'
  ((stage2_rc == 0))
  status='FAILED: resumed session ID differs or is missing; guess unchanged'
  [[ $(session_from_log "$log2") == "$sid" ]]
  status='FAILED: missing or empty review.md; guess unchanged'
  [[ -s review.md && ! -L review.md ]]
  status='done, guess unchanged'
)

failed=0
for series in "${series_names[@]}"; do
  for reader in "${reader_names[@]}"; do
    # Do not put run_reader in an if/|| condition: Bash would disable errexit
    # inside its subshell and allow failed stages to proceed to the reveal.
    set +e
    run_reader "$series" "$reader"
    rc=$?
    set -e
    if ((rc != 0)); then failed=1; fi
  done
done
exit "$failed"
