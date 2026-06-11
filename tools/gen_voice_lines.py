#!/usr/bin/env python3
"""Generate per-line narration audio for avatar scripts — in your own voice.

The avatar component plays a per-line ``audio:`` URL with real waveform
lip-sync; this tool produces those files from the script lines themselves,
so the markdown stays the single source of truth (P11).

Synthesis is zero-shot voice cloning via Chatterbox TTS — the same engine
behind VoiceClone Studio (https://github.com/GeorgesZam/voice_cloning_local):
give it a short, clean reference clip of your voice and every script line
is spoken in it.

Usage:
  python3 tools/gen_voice_lines.py docs/components/examples/avatar.md \
      --ref my_voice.m4a [--avatar prof_avatar] [--lang fr] [--write]

  --ref          reference voice sample (wav/mp3/m4a, ~10-20 s, no noise)
  --avatar ID    only this avatar block (default: every .avatar on the page)
  --lang CODE    use the multilingual model with this language id (e.g. fr)
  --exaggeration / --cfg-weight   Chatterbox dials (defaults 0.5 / 0.5)
  --engine silence   plumbing test: writes 1 s silent wavs, no model needed
  --out-root DIR     where the site lives (default: docs)
  --force        regenerate lines that already have an audio: URL
  --dry-run      list the lines that would be generated, then stop
  --write        update the page in place; default prints the new YAML

Requires (for real synthesis):  pip install chatterbox-tts torchaudio
First run downloads the model weights from Hugging Face.
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

# fenced yaml block followed by its {: .avatar #id ... } IAL line
BLOCK_RE = re.compile(
    r"^```yaml\n(.*?)^```\n\{:\s*\.avatar\s+([^}]*)\}",
    re.M | re.S,
)


def find_avatar_blocks(text):
    """Yield (match, avatar_id, cfg_dict) for each avatar block on the page."""
    for m in BLOCK_RE.finditer(text):
        ial = m.group(2)
        idm = re.search(r"#([\w-]+)", ial)
        if not idm:
            continue
        try:
            cfg = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError as e:
            print(f"  ! skipping #{idm.group(1)}: bad YAML ({e})", file=sys.stderr)
            continue
        yield m, idm.group(1), cfg


def lines_to_voice(cfg, force):
    """Indexes of script lines that need an audio file."""
    todo = []
    for i, line in enumerate(cfg.get("script") or []):
        if isinstance(line, str):
            todo.append(i)
        elif isinstance(line, dict):
            if line.get("video"):
                continue  # recorded take: it IS the voice
            if line.get("audio") and not force:
                continue
            if str(line.get("say") or line.get("text") or "").strip():
                todo.append(i)
    return todo


def make_silence(path, seconds=1.0, rate=24000):
    import wave

    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"\x00\x00" * int(rate * seconds))


class Chatterbox:
    def __init__(self, ref, lang, exaggeration, cfg_weight):
        self.ref, self.lang = ref, lang
        self.exaggeration, self.cfg_weight = exaggeration, cfg_weight
        try:
            import torch

            device = (
                "cuda" if torch.cuda.is_available()
                else "mps" if torch.backends.mps.is_available()
                else "cpu"
            )
            if lang:
                from chatterbox.mtl_tts import ChatterboxMultilingualTTS as TTS
            else:
                from chatterbox.tts import ChatterboxTTS as TTS
            print(f"  loading Chatterbox on {device} …")
            self.model = TTS.from_pretrained(device=device)
        except ImportError as e:
            sys.exit(
                f"Chatterbox not installed ({e}).\n"
                "  pip install chatterbox-tts torchaudio\n"
                "or use George's UI: https://github.com/GeorgesZam/voice_cloning_local\n"
                "(--engine silence tests the wiring without the model)"
            )

    def say(self, text, path):
        import torchaudio as ta

        kwargs = dict(
            audio_prompt_path=self.ref,
            exaggeration=self.exaggeration,
            cfg_weight=self.cfg_weight,
        )
        if self.lang:
            kwargs["language_id"] = self.lang
        wav = self.model.generate(text, **kwargs)
        ta.save(str(path), wav, self.model.sr)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("page", help="markdown page with .avatar blocks")
    ap.add_argument("--ref", help="reference voice sample (your voice)")
    ap.add_argument("--avatar", help="only this avatar id")
    ap.add_argument("--lang", help="language id for the multilingual model")
    ap.add_argument("--exaggeration", type=float, default=0.5)
    ap.add_argument("--cfg-weight", type=float, default=0.5)
    ap.add_argument("--engine", choices=["chatterbox", "silence"], default="chatterbox")
    ap.add_argument("--out-root", default="docs")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    page = Path(args.page)
    text = page.read_text(encoding="utf-8")
    blocks = [
        (m, aid, cfg)
        for m, aid, cfg in find_avatar_blocks(text)
        if not args.avatar or aid == args.avatar
    ]
    if not blocks:
        sys.exit(f"no .avatar blocks{' #' + args.avatar if args.avatar else ''} in {page}")

    if not args.dry_run and args.engine == "chatterbox" and not args.ref:
        sys.exit("--ref is required: a short clean sample of the voice to clone")

    engine = None
    edits = []  # (match, new_yaml)
    for m, aid, cfg in blocks:
        todo = lines_to_voice(cfg, args.force)
        print(f"#{aid}: {len(todo)} line(s) to voice")
        for i in todo:
            line = cfg["script"][i]
            say = line if isinstance(line, str) else str(line.get("say") or line.get("text"))
            print(f"  line_{i + 1:02d}: {say[:70]}")
        if args.dry_run or not todo:
            continue

        out_dir = Path(args.out_root) / "assets" / "audio" / aid
        out_dir.mkdir(parents=True, exist_ok=True)
        if engine is None:
            engine = (
                Chatterbox(args.ref, args.lang, args.exaggeration, args.cfg_weight)
                if args.engine == "chatterbox"
                else None
            )
        for i in todo:
            line = cfg["script"][i]
            say = line if isinstance(line, str) else str(line.get("say") or line.get("text"))
            path = out_dir / f"line_{i + 1:02d}.wav"
            if engine:
                engine.say(say, path)
            else:
                make_silence(path)
            url = f"/assets/audio/{aid}/{path.name}"
            if isinstance(line, str):
                cfg["script"][i] = {"say": say, "audio": url}
            else:
                line["audio"] = url
            print(f"  ✓ {path}")

        new_yaml = yaml.safe_dump(
            cfg, sort_keys=False, allow_unicode=True, width=1000
        )
        edits.append((m, new_yaml))

    if args.dry_run or not edits:
        return
    if args.write:
        for m, new_yaml in reversed(edits):  # back to front keeps offsets valid
            text = text[: m.start(1)] + new_yaml + text[m.end(1):]
        page.write_text(text, encoding="utf-8")
        print(f"updated {page}")
    else:
        print("\n— updated YAML (re-run with --write to apply) —")
        for m, new_yaml in edits:
            print(new_yaml)


if __name__ == "__main__":
    main()
