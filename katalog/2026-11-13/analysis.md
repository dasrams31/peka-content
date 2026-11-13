# Analysis — Katalog Peka edisi #5, 13 November 2026, 13:00 WIB

## Harga (sumber tunggal: prices.json)
- `updated` 2026-11-10, umur 3 hari: gate kesegaran lulus (<=7 hari).
- 23 produk, rentang 4K-75K. Termurah: Alight Motion 1 Tahun 4K.
  Termahal: Prompt Automation selamanya 75K. Label tanggal di slide:
  "Selasa 10 November 2026" (date_label prices.json, belum ada list
  baru dari user; daftar sama persis dengan edisi #4).
- Tidak ada produk baru vs edisi #4 dan tidak ada perubahan harga.
  Tidak ada harga/promo/garansi/testimoni/stok yang dikarang.

## Edisi sebelumnya
- #1, 31 Okt 2026 (5 produk): hook "Akun premium mulai 11K, ready
  hari ini." Tayang: Threads, IG reels, FB reels, Story.
- #2, 3 Nov 2026 (5 produk): hook "Lima akun premium, mulai 11K aja."
  Snapshot 22:30: Threads 2 likes / 84 views / 0 balasan (mingguan
  138 views); IG 1 like / 30 views; FB 0 likes / 4 views;
  Story 13 viewers. Komentar 0 di semua platform.
- #3, 6 Nov 2026 (14 produk): hook harga-dulu "Mulai 4K, ada 14 akun
  premium ready." FORMAT BARU: IG/FB carousel, reel hanya paket
  TikTok, Story dari desain slide. Mingguan: Threads 2 likes /
  40 views; IG 2 likes / 39 views; FB 0 likes / 7 views.
- #4, 10 Nov 2026 (23 produk): hook sudut baru "Ada 9 produk baru di
  katalog hari ini." Metrik awal saat tayang belum tersedia di
  performance.log (Threads tayang 19:55, IG 13:27, FB 19:56,
  Story 13:27; tayang tertunda, kartu approval user 19:16 WIB).
  Channel Peka: t.me/peka_aichannel/180.

## Hook edisi ini (rotasi framing)
- #1/#2 hitung-dulu, #3 harga-dulu, #4 produk-baru. Edisi ini sudut
  PERBANDINGAN (format menang minggu ini, trending.md 12 Nov:
  format perbandingan dua kolom / sebelum vs sesudah menang besar
  di gelombang mahasiswa, reel IPK 3 vs Cum Laude 2,8 ribu likes):
  "Viu setahun 5K, Lifetime cuma 8K." (33 char, <=60).
  Jujur dan terverifikasi: Viu 1 Tahun 5K dan Viu Lifetime 8K,
  keduanya dari prices.json.
- Andalan yang disebut di caption: Viu 1 tahun 5K, Viu Lifetime 8K,
  Alight Motion 1 tahun 4K (termurah katalog).
- Closing tag: #AI (current_tag.txt; lock manual user 6 Nov 2026,
  auto-switch mati; tag-watch 13 Nov: #AI avg 1183,4 likes n=13,
  #Kuliah 1440,7 n=7 memimpin tapi kunci manual tetap #AI).
- FYP learning 13 Nov: TOP didominasi cerita (19%), pertanyaan
  cuma 5%, hashtag rata-rata 0,6. Caption katalog tetap pakai
  pertanyaan pilihan paksa yang terkunci ("Kamu mau yang mana
  dulu?") + ajakan save + cara order DM MAU [produk] di teks
  (caption mandiri, aturan 31 Okt). Tanpa link di teks postingan
  mana pun; link hanya di dalam visual (slide terakhir).
- Eksperimen minggu ini tidak ada yang ditugaskan ke katalog;
  edisi ini tanpa eksperimen (sudut perbandingan dipakai sebagai
  rotasi hook biasa, bukan eksperimen tercatat).

## Build
- 7 slide 4096x4096 (1 cover + 6 halaman produk, pagination
  generik dari katalog_slides.py). Template disalin dari edisi
  2026-11-10 (bukan 2026-10-31 seperti bunyi body): satu-satunya
  beda adalah perbaikan cap band CTA y=3100 dari edisi #3,
  jadi menyalin 2026-10-31 akan menghidupkan lagi bug overflow
  yang sudah diperbaiki. Desain tidak diubah.
- Reel paket TikTok: 3 + 5*ceil(23/3) + 3 = 46 detik, 1104 frame
  @24fps, 2160x3840 yuv420p. Musik: pick_reel_track.sh tepat
  sekali, hasil di track.txt.

## Target metrik (snapshot laporan 22:30)
- Threads: balasan + repost > 0 (edisi #2: 0 balasan, 84 views;
  #3 mingguan 40 views; #4 belum tercatat).
- IG carousel: likes + saves, bandingkan dengan carousel #3
  (2 likes / 39 views) dan #4.
- FB carousel: views + shares, bandingkan dengan carousel #3
  (7 views) dan #4.
- Story: viewers vs #2 (13 viewers).
