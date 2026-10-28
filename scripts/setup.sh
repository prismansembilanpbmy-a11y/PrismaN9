#!/usr/bin/env bash
# Installs everything a PRISMA Reels edit needs in a fresh Claude Code cloud session.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "1/4 HyperFrames skills"
npx -y skills add heygen-com/hyperframes -a claude-code -s '*' -y --copy < /dev/null

echo "2/4 Chrome for rendering"
npx -y hyperframes browser ensure < /dev/null

echo "3/4 Whisper (built on first transcribe; warm it up)"
tmp=$(mktemp -d)
ffmpeg -loglevel error -f lavfi -i "sine=frequency=440:duration=2" -ar 16000 "$tmp/tone.wav"
(cd "$tmp" && npx -y hyperframes transcribe tone.wav --engine whisper --model small --json < /dev/null > /dev/null)
rm -rf "$tmp"

echo "4/4 MusicGen for AI background music"
if [ ! -x "$HOME/.mgvenv/bin/python" ]; then
  python3 -m venv "$HOME/.mgvenv"
  "$HOME/.mgvenv/bin/pip" install -q --index-url https://download.pytorch.org/whl/cpu torch
  "$HOME/.mgvenv/bin/pip" install -q transformers soundfile numpy
fi

npx -y hyperframes doctor < /dev/null || true
echo "Setup selesai."
