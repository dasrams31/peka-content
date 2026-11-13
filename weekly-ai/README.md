# AI Pekan Ini — seri mingguan Peka AI

Seri mingguan: tiap Minggu 16:00 WIB, satu topik bergantian BERITA AI
TERBARU / TUTORIAL AI, dalam format reel voiceover reel-v2 (peka-yellow,
45-60 detik, narasi "lo" +25%, subtitle karaoke sentence-first dengan
tanda baca, karakter Piko animasi 3 pose). Cron: `peka-weekly-ai`.

## Format (terkunci)

- Reel voiceover reel-v2, 2160x3840 yuv420p, tanpa musik (voiceover saja).
- Narasi ~130 kata, register "lo", santai kayak ngobrol, hanya fakta
  terverifikasi dari sumber resmi. 5-6 scene (hook, 2-3 beat, penutup).
- IG + FB = reel voiceover. Threads = cover frame + caption mandiri.
- Blog Peka: satu artikel per edisi (slug `ai-pekan-ini-<slug>`).
- Channel Telegram: broadcast `--type weekly` (label "AI Pekan Ini").
- TikTok: paket manual (reel + caption verbatim), posting oleh user.

## File

- `README.md` — file ini.
- `topics.md` — bank topik (antrean). Topik ditandai tayang setelah edisi
  tayang; jangan ulang. Bila bank habis, riset topik segar dan tambahkan.
- `series.txt` — nomor edisi berikut (mulai 1).
- `out/<YYYY-MM-DD>-<slug>/` — per edisi: `spec.json`, `sources.txt`,
  `voiceover/` (hasil build_reel.py), `weekly-reel.mp4`,
  `voiceover-cover.jpg`, `caption-reel-ig.txt`, `caption-reel-fb.txt`,
  `caption-threads.txt`, `caption-tiktok.txt`.

## Aturan terkunci (sama seperti pilar lain)

- TANPA link di teks caption mana pun (Threads/IG/FB/TikTok). Shortlink
  admin-DB hanya tercetak DI DALAM visual + tepat satu kalimat instruksi.
- TANPA perintah install/terminal di caption. Langkah pertama di caption
  ditulis bahasa awam, tanpa perintah terminal dan tanpa URL.
- TANPA em-dash/en-dash di semua copy.
- Bahasa santai + lugas, sebut "AI" bukan "mesin", satu pemicu interaksi
  per caption. Threads tutup tag #AI (dari tag-watch/current_tag.txt).
- Fakta hanya dari sumber resmi dan terverifikasi. Bila fakta kunci
  tidak terverifikasi, ganti topik, jangan bangun.
- TANPA CTA komen-untuk-link-via-DM (belum di-acc user).
- Kartu approval platform di tangan user; HTTP 429 = stop platform itu
  hari itu. Jangan posting ulang langkah yang sudah tercatat sukses.

## Catatan

- Late watch belum melacak slot mingguan ini (hanya slot harian +
  BLUEPRINT/Katalog/Gratisan). Bila user minta, tambahkan ke cron
  `peka-late-watch`.
- Render reel-v2 sekitar 40 menit (1.400 frame Playwright). Jangan
  turunkan fps untuk menghemat waktu.
