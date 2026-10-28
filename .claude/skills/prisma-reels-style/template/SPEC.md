# SPEC: "Siapa dia?" (storyline B)

GOAL:    Penonton Reels kenal Nur Fatihah (Calon 08, PRISMA N9) dan ingat "Suara OKU, hak saksama, masa depan bersama".
OUTPUT:  HyperFrames, 1080x1920, 30 fps, Instagram Reels
TIME:    64.0 s x 30 = 1920 frames. Voice is the clock (assets/talk.mp4, 61.57 s after silence cuts). No music: add an IG-library track in the app.
LOOK:    ground = her own footage + her photos; brand plates from the poster: navy #16236E, white #FFFFFF,
         yellow #F7C600 (accent: one word or number per card), N9 red #D21F26 + black #111 only in the flag strip.
         Display: Montserrat 900, tracking -1%, names 96-120 px, numbers 220 px. Captions: Poppins 800, 62 px, white,
         active word yellow, 3 px dark stroke + 0 6px 18px rgba(0,0,0,.55) shadow.
         Medium: poster-style printed plates (solid boxes, no gradients, no glass, no glow).
MOTION:  plates wipe on scaleX from left 8 frames expo.out; text inside revealed by clip-path 6 frames, 3-frame stagger;
         exits wipe off to the right 6 frames power2.in. Numbers spring scale 1.35->1 (back.out(2)) 9 frames.
         Photo B-roll: hard cut in, push 1.00->1.08 linear over the shot. Jump cuts in the talk: alternate 1.00 / 1.10 scale, hard.
SHOTS:
  0.00-3.10   HOOK  4 photos hard-cut (pingat, catur, rtm, waghih ~0.75 s each), "KENAL / DIA?" plates already on frame 0, still. Voice: salam.
  3.10-10.70  talk  name plate "NUR FATIHAH / binti Jasmi" 3.45; "CALON / NEGERI SEMBILAN" + flag 6.05; "24 TAHUN" 9.25. whoosh on 3.10.
  10.70-22.0  talk  Asal KL / Menetap Selangor 11.9; "Kampung KUALA PILAH" 18.8.
  23.00-29.65 rtm photo; "OKU / kategori fizikal" 26.4.
  29.65-38.60 talk  "GRADUAN / Diploma Pengurusan / UMCCed" 31.8.
  38.60-41.35 waghih photo "Aktif dalam / KEPIMPINAN BELIA".
  41.35-44.95 catur photo "ATLET PARA CATUR / NEGERI SEMBILAN" (top band).
  44.95-55.02 talk  belief line; punch-in 1.12 on "berhak" 49.57; yellow words: berhak, peluang, berjaya.
  55.02-59.00 SLOGAN navy plate over dimmed talk: SUARA OKU, / HAK SAKSAMA, / MASA DEPAN / BERSAMA. each line on its word. impact on 55.02.
  59.00-64.00 END   poster wiped in from bottom, holds 3 s+. whoosh on 59.0.
SAFE:    no text above y 168; all words in y 168-1330; captions box y 1170-1320; nothing under the right rail (x > 960) for text.
BANNED:  dark void, glow, gradients, glass cards, fade+slide-up on everything, docked logo, text moving while read, three cards in a row.
QA:      frames 0.0, 1.2, 4.5, 9.6, 20.0, 27.5, 34.0, 40.0, 43.0, 50.0, 57.9, 62.5.
