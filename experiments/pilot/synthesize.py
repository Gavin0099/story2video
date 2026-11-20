import argparse
import hashlib
import json
import math
import subprocess
import tempfile
import textwrap
import time
import wave
from array import array
from importlib.metadata import version
from pathlib import Path

RATE = 24_000
PUBLISHER = "https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0"
SPEED = 0.96


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write_json(output, filename, payload):
    (output / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def wav_write(path, pcm):
    with wave.open(str(path), "wb") as wav:
        wav.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        wav.writeframes(array("h", pcm).tobytes())


def to_ms(samples):
    return round(samples * 1000 / RATE)


def caption_clock(ms, separator):
    seconds, milliseconds = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}{separator}{milliseconds:03}"


def write_captions(output, rows, lang, suffix):
    field = "en_caption" if lang == "en" else "zh_caption"
    separator = "," if suffix == "srt" else "."
    heading = "WEBVTT\n\n" if suffix == "vtt" else ""
    cues = []
    for index, row in enumerate(rows, 1):
        start = caption_clock(row["caption_start_ms"], separator)
        end = caption_clock(row["caption_end_ms"], separator)
        cues.append(f"{index}\n{start} --> {end}\n{row[field]}")
    (output / f"{lang}.{suffix}").write_text(heading + "\n\n".join(cues) + "\n", encoding="utf-8")


def kokoro_voice(episode, model_dir):
    import numpy as np
    from kokoro_onnx import Kokoro

    model_path = model_dir / "kokoro-v1.0.int8.onnx"
    voices_path = model_dir / "voices-v1.0.bin"
    if model_path.stat().st_size != 92_361_271 or voices_path.stat().st_size != 28_214_398:
        raise ValueError("Provider file size differs from the pinned upstream release")
    with voices_path.open("rb") as stream:
        if stream.read(4) != b"PK\x03\x04":
            raise ValueError("Voice pack must be the NumPy ZIP container")
    # Reject pickled/object arrays. The provider below opens the same pinned local bundle.
    with np.load(voices_path, allow_pickle=False) as voice_pack:
        voice_values = voice_pack[episode["voice"]]
        if not np.issubdtype(voice_values.dtype, np.number) or not np.isfinite(voice_values).all():
            raise ValueError("Voice array is invalid")

    provider = Kokoro(str(model_path), str(voices_path))

    def speak(text):
        audio, rate = provider.create(text, voice=episode["voice"], speed=SPEED, lang="en-us")
        audio = np.asarray(audio).reshape(-1)
        if rate != RATE or not np.isfinite(audio).all():
            raise ValueError("Invalid audio from Kokoro")
        return audio.tolist()

    return speak, {
        "provider": "Kokoro-ONNX, local CPU",
        "provider_version": version("kokoro-onnx"),
        "runtime_version": version("onnxruntime"),
        "model": "Kokoro-82M v1.0, int8",
        "model_release": PUBLISHER,
        "model_sha256_observed": sha(model_path),
        "voice_pack_sha256_observed": sha(voices_path),
        "voice": episode["voice"],
        "speed": SPEED,
        "model_license_source": "https://huggingface.co/hexgrad/Kokoro-82M",
        "voice_list_source": "https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md",
    }


def flite_voice(output):
    def speak(text):
        with tempfile.TemporaryDirectory(dir=output) as directory:
            Path(directory, "text.txt").write_text(text, encoding="ascii")
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                "-i", "flite=textfile=text.txt:voice=slt", "-ar", str(RATE),
                "-af", "atempo=0.94", "-c:a", "pcm_s16le", "speech.wav",
            ], cwd=directory, check=True)
            with wave.open(str(Path(directory, "speech.wav")), "rb") as wav:
                if (wav.getframerate(), wav.getnchannels(), wav.getsampwidth()) != (RATE, 1, 2):
                    raise ValueError("Unexpected Flite PCM format")
                return [value / 32768 for value in array("h", wav.readframes(wav.getnframes()))]

    return speak, {
        "provider": "CMU Flite via local FFmpeg",
        "provider_version": subprocess.check_output(["ffmpeg", "-version"], text=True).splitlines()[0],
        "voice": "slt",
        "speed": 0.94,
        "voice_license_source": "https://github.com/festvox/flite/blob/master/COPYING",
        "voice_model_source": "https://github.com/festvox/flite/tree/master/lang/cmu_us_slt",
        "provider_choice": "Pilot fallback. Kokoro-FastAPI was not running.",
    }


def pcm16(audio, gain=1):
    return (max(-32767, min(32767, round(value * gain * 32767))) for value in audio)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=["kokoro", "flite"], required=True)
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--story-spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path)
    parser.add_argument("--voice")
    args = parser.parse_args()
    if args.provider == "kokoro" and args.model_dir is None:
        parser.error("--model-dir is required for Kokoro")
    start = time.perf_counter()
    episode = json.loads(args.episode.read_text(encoding="utf-8"))
    if args.voice:
        episode["voice"] = args.voice
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    speak, provider = kokoro_voice(episode, args.model_dir) if args.provider == "kokoro" else flite_voice(output)
    raw_directory = output / "segments"
    raw_directory.mkdir(exist_ok=True)
    audio, rows = [], []
    offset = 0
    for segment in episode["segments"]:
        clip_start = time.perf_counter()
        clip = speak(segment["text"])
        active = [index for index, value in enumerate(clip) if abs(value) >= 0.005]
        if not active:
            raise ValueError(f"No speech detected in {segment['id']}")
        speech = clip[max(0, active[0] - 960):min(len(clip), active[-1] + 2401)]
        pause = RATE * segment["pause_ms"] // 1000
        speech_end = offset + len(speech)
        next_offset = speech_end + pause
        wav_path = raw_directory / f"{segment['id']}.wav"
        wav_write(wav_path, pcm16(speech))
        audio.extend(speech)
        audio.extend([0.0] * pause)
        caption_start = speech_end if segment.get("caption_after_speech") else offset
        caption_end = next_offset if segment.get("caption_after_speech") else speech_end
        rows.append({
            "id": segment["id"],
            "scene": segment["scene"],
            "text_hash": hashlib.sha256(segment["text"].encode("utf-8")).hexdigest(),
            "source_audio_sha256": sha(wav_path),
            "audio_start_ms": to_ms(offset),
            "audio_end_ms": to_ms(speech_end),
            "duration_ms": to_ms(len(speech)),
            "caption_start_ms": to_ms(caption_start),
            "caption_end_ms": to_ms(caption_end),
            "en_caption": "\n".join(textwrap.wrap(segment["text"], width=32)),
            "zh_caption": segment["zh"],
            "seconds_to_synthesize": round(time.perf_counter() - clip_start, 2),
        })
        print(segment["id"], rows[-1]["duration_ms"], "ms", flush=True)
        offset = next_offset

    peak = max(map(abs, audio))
    active_audio = [value for value in audio if abs(value) > 0.005]
    active_rms = math.sqrt(sum(value ** 2 for value in active_audio) / len(active_audio))
    gain = min(10 ** (-18 / 20) / active_rms, 10 ** (-3 / 20) / peak)
    wav_write(output / "narration.wav", pcm16(audio, gain))
    reveal = next(row for row in rows if row["id"] == "reveal")
    write_json(output, "segments.json", {
        "episode_id": episode["episode_id"],
        "title": episode["title"],
        "visual_clue": episode.get("visual_clue"),
        "duration_ms": to_ms(len(audio)),
        "sample_rate": RATE,
        "timing_method": "actual_trimmed_pcm_sample_counts; segment-level",
        "reveal_ms": reveal["caption_start_ms"],
        "segments": rows,
    })
    write_json(output, "provenance.json", {
        "episode_id": episode["episode_id"],
        "story": episode["origin"],
        "visuals": "Original programmatic graphics in video/Root.tsx; no stock imagery or music.",
        **provider,
        "accent": "en-US",
        "publication_rights": "OWNER_REVIEW_PENDING",
        "voice_clone": False,
        "paid_ai_api_calls": 0,
        "narration_sha256": sha(output / "narration.wav"),
        "story_spec_sha256": sha(args.story_spec),
        "episode_sha256": sha(args.episode),
        "narration_seconds_to_prepare": round(time.perf_counter() - start, 2),
        "upload": "NOT_UPLOADED",
    })
    for language in ("en", "zh-Hant-TW"):
        for suffix in ("srt", "vtt"):
            write_captions(output, rows, language, suffix)
    print(f"Prepared {to_ms(len(audio))} ms of local narration.")


if __name__ == "__main__":
    main()
