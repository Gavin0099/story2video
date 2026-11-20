import argparse
import hashlib
import json
import re
import subprocess
import wave
from fractions import Fraction
from pathlib import Path

def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def ffprobe(path):
    return json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path),
    ], text=True))


def parse_tracks(path):
    content = path.read_text(encoding="utf-8")
    if path.suffix == ".vtt":
        assert content.startswith("WEBVTT\n\n"), "Missing VTT header"
        content = content.removeprefix("WEBVTT\n\n")
    stamps = []
    for index, cue in enumerate(content.strip().split("\n\n"), 1):
        lines = cue.splitlines()
        assert lines[0] == str(index) and len(lines) >= 3 and any(lines[2:]), f"Invalid cue {index}"
        match = re.fullmatch(r"(\d\d:\d\d:\d\d[,.]\d{3}) --> (\d\d:\d\d:\d\d[,.]\d{3})", lines[1])
        assert match, f"Invalid timing for cue {index}"

        def time_ms(stamp):
            hour, minute, second, ms = map(int, re.split("[:,.]", stamp))
            return ((hour * 60 + minute) * 60 + second) * 1000 + ms

        stamps.append((time_ms(match[1]), time_ms(match[2])))
    return stamps


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--spoiler-term", action="append", default=[], help="Word or phrase prohibited before reveal")
    args = parser.parse_args()
    output = args.output
    video_path = output / "render.mp4"
    timeline = json.loads((output / "segments.json").read_text(encoding="utf-8"))
    probe = ffprobe(video_path)
    video = next(stream for stream in probe["streams"] if stream["codec_type"] == "video")
    audio = next(stream for stream in probe["streams"] if stream["codec_type"] == "audio")
    duration = float(probe["format"]["duration"])
    video_s, audio_s = float(video["duration"]), float(audio["duration"])
    with wave.open(str(output / "narration.wav"), "rb") as wav:
        wav_format = (wav.getframerate(), wav.getnchannels(), wav.getsampwidth())
        wav_s = wav.getnframes() / wav.getframerate()
    measure = subprocess.run([
        "ffmpeg", "-hide_banner", "-nostdin", "-xerror", "-i", str(video_path),
        "-vf", "blackdetect=d=0.15:pix_th=0.04:pic_th=0.98",
        "-af", "silencedetect=noise=-45dB:d=0.40,volumedetect",
        "-f", "null", "-",
    ], text=True, capture_output=True, check=True)
    (output / "media-measurement.txt").write_text(measure.stderr, encoding="utf-8")
    black_intervals = re.findall(r"black_start:([0-9.]+) black_end:([0-9.]+)", measure.stderr)
    silence_starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", measure.stderr)]
    silence_lengths = [float(x) for x in re.findall(r"silence_duration: ([0-9.]+)", measure.stderr)]
    max_volume = float(re.search(r"max_volume: (-?[0-9.]+) dB", measure.stderr)[1])
    expected = [(row["caption_start_ms"], row["caption_end_ms"]) for row in timeline["segments"]]
    reveal = next(row for row in timeline["segments"] if row["id"] == "reveal")
    prereveal = [row for row in timeline["segments"] if row["caption_start_ms"] < timeline["reveal_ms"]]
    tracks = [output / f"{lang}.{ext}" for lang in ("en", "zh-Hant-TW") for ext in ("srt", "vtt")]
    checks = {
        "vertical_1080x1920_h264_30fps": (
            (video["width"], video["height"], video["codec_name"]) == (1080, 1920, "h264")
            and Fraction(video["avg_frame_rate"]) == 30
        ),
        "aac_48khz_mono": (audio["codec_name"], audio["sample_rate"], audio["channels"]) == ("aac", "48000", 1),
        "duration_30_to_60_seconds": 30 <= duration <= 60,
        "narration_pcm_24khz_mono": wav_format == (24000, 1, 2),
        "audio_and_video_duration_match": abs(video_s - audio_s) < 0.08 and abs(wav_s - video_s) < 0.08,
        "all_frames_and_audio_decode": measure.returncode == 0,
        "no_black_intervals_detected": not black_intervals,
        "speech_has_headroom": -14.0 <= max_volume <= -1.0,
        "silences_within_thinking_pause_budget": max(silence_lengths, default=0) < 3.7,
        "no_blank_tail": duration * 1000 - timeline["segments"][-1]["audio_end_ms"] < 700,
        "four_caption_tracks_match_actual_wav_timeline": all(parse_tracks(path) == expected for path in tracks),
        "caption_cues_monotonic": all(
            0 <= start < end <= duration * 1000 and (idx == 0 or expected[idx - 1][1] <= start)
            for idx, (start, end) in enumerate(expected)
        ),
        "aligned_reveal_not_ahead_of_speech": reveal["audio_end_ms"] <= timeline["reveal_ms"] == reveal["caption_start_ms"],
    }
    if args.spoiler_term:
        captions = [" ".join(row["en_caption"].split()) + "\n" + row["zh_caption"] for row in prereveal]
        checks["no_pre_reveal_spoiler_terms"] = all(
            term.casefold() not in caption.casefold()
            for term in args.spoiler_term for caption in captions
        )
    qa = {
        "technical_pass": all(checks.values()),
        "checks": checks,
        "duration_seconds": duration,
        "video_duration_seconds": video_s,
        "audio_duration_seconds": audio_s,
        "asset_sha256": digest(video_path),
        "narration_max_volume_dbfs": max_volume,
        "silences_seconds": [{"start": start, "length": length} for start, length in zip(silence_starts, silence_lengths)],
        "reveal_ms": timeline["reveal_ms"],
        "timing_method": timeline["timing_method"],
        "independent_story_review": "NOT_RUN",
        "human_playback_review": "REVIEW_REQUIRED",
        "upload": "NOT_UPLOADED",
    }
    (output / "qa.json").write_text(json.dumps(qa, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(qa, indent=2))
    raise SystemExit(0 if qa["technical_pass"] else 1)


if __name__ == "__main__":
    main()
