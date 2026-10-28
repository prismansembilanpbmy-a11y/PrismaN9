---
name: prisma-reels-style
description: House style for PRISMA (Parti Belia Sejahtera Malaysia) Instagram/Facebook Reels built with HyperFrames - candidate introductions AND leader speech / campaign calls (e.g. Jom Daftar ePBMY). Use whenever the user asks for another candidate intro / "video pengenalan calon", a speech or seruan video, a PRISMA reel, or "guna style yang sama" - it holds the v3 look (proof-wall hook, yellow iris transitions, serif-italic keyword captions, comment-box CTA), the structure, sound and the ready template from the Calon 08 Nur Fatihah video.
---

# PRISMA candidate Reels style (v3)

Proven on "Calon 08 Nur Fatihah" (Negeri Sembilan). v3 = the PRISMA brand look plus techniques the user liked from a Facebook reference reel. Load `/hyperframes` first; this skill fixes the choices so the next candidate's video matches.
The user is a beginner who writes in Bahasa Melayu: reply in simple Malay, explain each step, never assume coding knowledge.

## Inputs to ask for (only what is missing)
- One talking-head video of the candidate (usually a WhatsApp vertical clip) + 4 photos + the candidate poster.
- Spelling the transcript cannot know: full name, nickname, university, slogan. Show a "transkrip vs tekaan saya" table and ask.

## Format
1080x1920, 30 fps, Reels, ~60-65 s. Text only inside y 168-1330, nothing under the right rail (x > 960).

## Structure ("Siapa dia?")
| Beat | Time | Content |
|---|---|---|
| Hook | 0-3.1 s | Candidate's salam on screen (talking head). Proof wall: 4 photos as white-bordered tilted prints (250x330, +-6-8 deg) at the left/right edges, 2 on frame 0, 2 pop in (back.out). Title at top 180: navy kicker plate "CALON 08 · PRISMA" (Poppins 600 34 px, 0.3em tracking) + "Kenal dia?" Playfair Display italic 700 150 px yellow. Tilted (-3 deg) yellow highlighter plate "Atlet → Graduan → Pemimpin" at top 1190 with a pop. |
| Intro | ~3-11 s | talking head; cards: name, CALON + NEGERI (red) + flag + PRISMA, age as a big number. |
| Facts | ~11-45 s | one card per spoken fact; photo B-roll (hard cut, push 1.00->1.08) when a photo proves the line. |
| Belief | ~45-54 s | talking head; big Playfair italic yellow words (170 px, bottom 790) on the two key words ("berhak", "berjaya."); drop the caption group that would repeat a big word alone. |
| Slogan | ~4.8 s | navy 0.9 plate over the dimmed video, Montserrat 900 96 px lines snapping in on each spoken word, 2nd line yellow, red underline. Last line held >= 2 s. |
| End card | 5 s | poster (left 110, top 160, 860x1069) wiped up on navy + white comment-box CTA (top 1250, 860x76, yellow avatar dot, red heart) typing the campaign hashtag letter by letter (0.07 s/char) with typing.mp3. |

Transitions: `compositions/iris.html`, yellow #F7C600 disc grows (0.25 s power2.in) to fill the frame, then opens as a hole (radial mask, 0.33 s power2.out) onto the next chapter. Use it 3 times only: hook->intro, into the main B-roll chapter, into the slogan. Whoosh lands on each cut.

## Look
- Navy #16236E, white, yellow #F7C600, N9 red #D21F26, black only in the flag. Change flag/red for another state.
- Info cards = solid "printed plates" like the poster: Montserrat 900, sub-lines Poppins 700, wipe in from the left (clip-path 0.27 s expo.out, 0.1 s stagger), wipe off right. Talking-head cards anchored `bottom: 790px`; cards over a group photo go to the top (top 230).
- Captions (`tools/captions_v3.py`): Poppins 700 60 px white, 2 px dark stroke + soft shadow, box top 1170, max 3 words, place names never split. HOT words always in Playfair Display italic 700, 1.22em, yellow (names, numbers, places, key values). Hidden during hook/slogan/end card.
- Punch-ins: alternate 1.0/1.1 on every jump cut AND a punch every 3-4 s on a stressed word (root timeline `punches`).
- Banned: gradients as decoration, glow, glass, dark void, docked logo, everything fading/sliding up.

## Edit + sound
- Transcribe Malay: `npx hyperframes transcribe raw.mp4 --model small --language ms --json` (never the default small.en: it translates).
- `tools/cut.py`: cuts silences >= 0.6 s (pad 0.15 s), upscales to 1080x1920, -g 30, remaps word times. Edit its `sil` list from `silencedetect=noise=-35dB:d=0.4`.
- `tools/captions_v3.py`: edit FIX (index -> spelling), HOT, END (stop before a big word that repeats), no-break words.
- SFX (bundled library, start = picture time - file peak + 1 frame): whoosh on iris cuts/B-roll, pop on hook plate/name/age/award cards, impact-bass-1 on the slogan, typing on the CTA. Volume 0.3-0.5.
- Music: AI music (user's choice). `tools/musicgen.py <out.wav> <seconds>` in a venv with CPU torch + transformers + soundfile (`facebook/musicgen-small`, ~2-3 min on CPU). Volume lane: 0.14 under voice, 0.55 after the last word, fade to 0. No credit needed.

## Variant: speech / campaign call (template-ucapan/)
Proven on "Pesanan YB ADUN Ampangan - Jom Daftar ePBMY" (76 s from a 104 s speech in 2 parts). Use it for a leader's speech, a seruan or a registration push.
- Palette follows the campaign poster the user gives (this one: maroon #7A0F1E, deep #4A0710, gold #F5C22E, urgent red #D21F26). Logos are cropped from the poster's logo band (`convert poster.jpg -crop WxH+X+Y -resize 200% logos.png`).
- Speaker on a plain wall: cards and big serif words go on the empty wall ABOVE the head (top 220, bottom <= 570); captions sit on the shirt at top 1190 in a dark pill (`rgba(40,4,10,.62)`, Poppins 700 56 px, gold Playfair italic keywords).
- Hook (0 to end of salam): logo strip + "Gen Z," Playfair italic 150 px + one red plate with the urgent line, 2 meeting photos as tilted prints at the edges, name + title plates in the caption band.
- Meeting photos (landscape): keep them whole as a framed print (980x735) on the dark ground with a serif label, never cover-cropped to 9:16.
- Spelled words (e.g. "E, P, B, MY"): one plate per letter popping on each spoken letter, caption merged into one word.
- Iris (gold) at: end of salam, the date/registration chapter, the end card.
- End card: logo strip, "JOM DAFTAR!", serif subline, the guide poster + the IG profile screenshot as tilted prints, gold pill "Panduan ... → @handle", red "TUTUP HARI INI!" stamp when it is the last day, comment box typing the hashtag.
- `tools/cut2.py`: joins several clips, keeps chosen ranges (drop off-message parts such as lists of other parties: ask first, default drop), trims pauses >= 0.6 s, remaps each word to the segment it overlaps most. Words Whisper puts inside a trimmed pause are re-added by hand in `tools/captions_yb.py` (ADD).
- Speech recorded quietly: normalise the speech file before building (`ffmpeg -i talk.mp4 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 ...`); measure the render with ebur128.
- Never guess facts the speech garbles (a year, party names): ask, and in the post caption leave the uncertain part out.
- Also write the post caption (full + short version) and save it to `videos/CAPTIONS.md`.

## Practical notes
- iPhone photos come as HEIC: ImageMagick here cannot read them; use pillow-heif in the MusicGen venv (`~/.mgvenv/bin/pip install pillow pillow-heif`, then `ImageOps.exif_transpose(...)`).
- `whisper-cli crashed (SIGILL)` after the session moves to another machine: move `~/.cache/hyperframes/whisper/whisper.cpp/build` aside and transcribe again (it rebuilds).
- `transcribe` writes `transcript.json` next to the input file, not in the cwd; rename it per part.
- Store finished MP4s in `videos/` of this repo (GitHub max 100 MB per file); suggest Google Drive once the repo grows.

## Work loop the user expects
1. Confirm spellings, then copy `template/` into a new project and swap assets, text and times.
2. `npx hyperframes check`, snapshots at every changed moment (look for card/caption overlaps and faces under text).
3. Preview = low-quality render (`render -q draft --fps 15`, named PREVIEW_...): the Studio URL is not reachable from their phone.
4. Final render only when they say "render"; send the MP4 with SendUserFile; say audio was measured, not heard.
