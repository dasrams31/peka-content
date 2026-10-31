# Analysis — Katalog Peka, Sabtu 31 Oktober 2026, 13:00 WIB

Edisi katalog pertama dalam seri katalog Peka (desain Peka, kuning-hitam).
Perintah user 31 Okt 06:30 (cron mingguan) + 06:49 ("sekarang jam 1 nanti"):
edisi ini tayang 31 Okt 13:00 WIB. Teks FROZEN di playbook/trending.md
adalah teks lama sebelum perintah seri katalog ini; perintah user yang berlaku.

## Aset (terverifikasi, tidak di-rebuild)
- Slide: peka-katalog-01.png, peka-katalog-02.png, peka-katalog-03.png — 4096x4096.
- Reel: peka-katalog-reel.mp4 — ffprobe: h264, 2160x3840, yuv420p, 15.000 dtk, aac.
  Cover: peka-katalog-reel-cover.jpg (2160x3840).
- Musik: Crypto by Kevin MacLeod (track.txt, tidak dipanggil pick_reel_track.sh lagi).
- Caption: caption-ig.txt / caption-fb.txt / caption-threads.txt /
  caption-tiktok.txt / caption-wa.txt, apa adanya dari folder edisi.
- Harga HANYA dari prices.json (updated 2026-10-31): Gemini Pro 3 bln 15K,
  CapCut Pro privat 1 bln 27K, Canva Edu 6 bln 11K, Muse Spark AI lifetime
  24K (3-4 Milyar token), Microsoft 365 1 thn 26K. Tidak ada harga/promo/
  garansi/testimoni/stok yang dikarang.

## Hook yang dipakai
Hook baris pertama (38 char, sesuai playbook <=60 char, keuntungan pembaca):
"Akun premium mulai 11K, ready hari ini."
Pemicu interaksi: satu pertanyaan pilihan mudah ("Kamu mau yang mana dulu?")
+ ajakan save ("Save dulu biar nggak hilang.") + DM keyword
("DM: MAU [nama produk]") sesuai pola store di playbook.
Threads: 296 char, diakhiri TEPAT 1 hashtag #AI, tanpa em-dash.
IG: 8 hashtag relevan. FB: tanpa hashtag. TikTok: caption siap salin
di caption-tiktok.txt (manual oleh user).

## Closing tag
CURRENT CLOSING TAG dari tag-watch.md (31 Okt): #AI (default; n per tag
belum >=10, #AI n=3, avg likes 552.0). current_tag.txt juga berisi "AI".
Tag lain (#Kuliah, #Coding) avg likes lebih tinggi tapi n=2-4, belum
memenuhi syarat pindah (2x rata-rata likes #AI dengan n>=10). Jadi
Threads tetap ditutup #AI, sesuai aturan.

## Pola FYP / trending yang relevan
- fyp-learning.md 31 Okt: top post didominasi cerita personal + day-counter;
  katalog ini bukan cerita personal, jadi andalannya adalah daftar harga
  yang save-worthy (checklist/list, pola yang menang minggu ini di
  trending.md: checklist + nilai-dirimu-sendiri) dan pertanyaan pilihan
  yang gampang dijawab.
- trending.md: format checklist / pick-a-side menang; katalog memakai
  daftar 5 produk + pertanyaan "mau yang mana dulu" sebagai padanannya.
- learnings.md: nilai per platform dengan ukurannya sendiri
  (IG likes+saves, Threads replies+reposts, FB reactions+shares);
  keputusan berbasis snapshot laporan 22:30, bukan angka menit awal.
  Jangan hapus + repost bila ada masalah; perbaiki lewat balasan/komentar.

## Pembagian format (dikunci user)
- Threads: carousel 3 slide.
- Instagram: reels + story dari file reels yang sama (tanpa editor).
- Facebook: reels (Page PekaAI).
- TikTok: manual user dari reel + caption-tiktok.txt.
- Tanpa blog, tanpa DM, tanpa pembayaran.

## Target metrik (awal, untuk snapshot 22:30)
- Threads: replies + reposts > 0; bandingkan dengan median likes HM 1-4
  dan Gratisan AI 15 likes sebagai pembanding, bukan vonis.
- IG: likes + saves (saves tidak terekspos CLI; catat likes bila ada).
- FB: views + shares dari pages posts list (reactions biasanya 0-2).
- Tidak ada metrik awal yang dikarang sebelum snapshot; metrik awal
  hanya dicatat bila CLI mengeksposnya saat verifikasi posting.
