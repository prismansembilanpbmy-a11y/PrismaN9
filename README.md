# PrismaN9: Video Reels Calon PRISMA

Repo ini menyimpan **gaya video** untuk video pengenalan calon PRISMA (Instagram/Facebook Reels), supaya setiap video calon kelihatan sama.

## Cara guna (dalam Claude Code)
1. Buka chat baru di **claude.ai/code** dan pilih repo **PrismaN9**.
2. Taip: **"Jalankan scripts/setup.sh"**. Ia memasang HyperFrames, Chrome, Whisper dan MusicGen. Ambil masa ~10 minit.
3. Muat naik video calon bercakap, 4 gambar dan poster calon.
4. Taip: **"Buat video calon baru guna style yang sama"**.

Claude akan semak ejaan nama dengan anda, beri video pratonton, dan render bila anda kata "render".

## Isi repo
| Folder | Isi |
|---|---|
| `.claude/skills/prisma-reels-style/` | Panduan gaya (SKILL.md), templat video calon (v3), templat video ucapan/kempen, dan kesan bunyi |
| `.claude/skills/prisma-reels-style/tools/` | Alat potong jeda senyap, buat sari kata dan jana muzik AI |
| `scripts/setup.sh` | Pasang semua alat dalam sesi baru |

## Gaya v3 (ringkas)
- Hook "Kenal dia?" dengan gambar-gambar calon di sekeliling wajahnya
- Peralihan bulatan kuning antara bab
- Sari kata pendek, kata kunci dalam serif italic kuning
- Kad maklumat gaya poster (navy, kuning, merah)
- Slogan besar dan poster penutup dengan kotak komen hashtag
- Muzik latar AI (tiada kredit diperlukan)
