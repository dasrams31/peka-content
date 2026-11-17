# Analysis — Katalog Peka edisi #6, 17 November 2026, 13:00 WIB

## Harga (sumber tunggal: prices.json)
- `updated` 2026-11-16, umur 1 hari: gate kesegaran lulus (<=7 hari).
- 22 produk, rentang 2,4K-75K. Termurah: Referral Muse 1 B
  1 Milyar Token 2,4K. Termahal: Prompt Automation selamanya 75K.
  Label tanggal di slide: "16 November 2026" (date_label prices.json).
- Tidak ada harga/promo/garansi/testimoni/stok yang dikarang.
- Catatan: harga di cover slide dirender template sebagai "2.4K."
  (titik, dari float price_num), sementara prices.json menulis "2,4K"
  (koma). Nilai sama; caption memakai "2,4K" persis prices.json.
  Bukan redesign, template tidak diubah.

## Edisi sebelumnya
- #1, 31 Okt 2026 (5 produk): hook "Akun premium mulai 11K, ready
  hari ini."
- #2, 3 Nov 2026 (5 produk): hook "Lima akun premium, mulai 11K aja."
  Snapshot 22:30: Threads 2 likes / 84 views / 0 balasan;
  IG 1 like / 30 views; FB 0 likes / 4 views; Story 13 viewers.
- #3, 6 Nov 2026 (14 produk): hook harga-dulu "Mulai 4K, ada 14 akun
  premium ready." FORMAT BARU: IG/FB carousel, reel hanya paket
  TikTok, Story dari desain slide. Mingguan: Threads 2 likes /
  40 views; IG 2 likes / 39 views; FB 0 likes / 7 views.
- #4, 10 Nov 2026 (23 produk): hook sudut baru "Ada 9 produk baru di
  katalog hari ini." Tayang tertunda (kartu approval user 19:16 WIB).
- #5, 13 Nov 2026 (23 produk): hook sudut PERBANDINGAN "Viu setahun
  5K, Lifetime cuma 8K." Tayang: Threads, IG carousel, FB carousel,
  Story 13:40 WIB; channel Peka t.me/peka_aichannel/198.
  Metrik awal edisi #5 belum tercatat di performance.log
  (tidak ada baris katalog 13 Nov di log saat analisis ini ditulis).
- Draf auto-20261116-1001 (25 produk, TIDAK tayang, build-only
  watcher): hook draf "Referral Muse 1 B 1 Milyar Token 2,4K,
  Alight Motion 1 Tahun 3K." Sudah basi: 3 produk habis 16 Nov
  (Gemini AI 1000 Flow 28K, Gemini Plus AI 6 Bulan 35K,
  ChatGPT Plus 1 Bulan VCC 80K; pruned.json), jadi edisi ini
  DIBANGUN ULANG dari prices.json hari ini, bukan memakai draf itu.

## Perbedaan vs edisi #5
- 22 produk (was 23): 3 produk di atas habis dan ter-prune,
  tidak ada produk baru masuk. ChatGPT Plus 80K sudah tidak ada
  di katalog hari ini.
- Termurah turun: 2,4K Referral Muse 1 B (was Alight Motion 4K,
  kini 3K). Rentang bawah katalog makin murah, itu yang diangkat.

## Hook edisi ini (rotasi framing)
- #1/#2 hitung-dulu, #3 harga-dulu, #4 produk-baru, #5 perbandingan.
  Edisi ini sudut HITUNG + HARGA TERMURAH BARU: "22 akun premium,
  mulai 2,4K aja." (32 char, <=60). Angka jujur dari prices.json:
  22 produk, termurah 2,4K.
- Andalan yang disebut di caption: Referral Muse 1 B 1 Milyar Token
  2,4K, Alight Motion 1 Tahun 3K, Canva Pro 1 Bulan 5K.
- Closing tag: #AI (current_tag.txt; lock manual user 6 Nov 2026,
  auto-switch mati; tag-watch 17 Nov: #AI avg 792,8 likes n=12,
  median 382,5, tetap teratas; #Kuliah avg 785,0 n=8).
- FYP learning: TOP didominasi cerita (19-27%) dan pertanyaan
  (18-25%), hashtag rata-rata 0,5-0,6. Caption katalog tetap pakai
  pertanyaan pilihan paksa yang terkunci ("Kamu mau yang mana
  dulu?") + ajakan save + cara order DM MAU [produk] di teks
  (caption mandiri, aturan 31 Okt). Tanpa link di teks postingan
  mana pun kecuali caption WA (link grup, sesuai body);
  link hanya di dalam visual (slide terakhir).
- Playbook 15 Nov: hook SPILL wajib stack spesifik + angka resmi;
  untuk katalog, angka spesifiknya adalah hitungan produk + harga
  termurah, keduanya dari prices.json. Segmen mahasiswa
  (Gratisan learning 15 Nov) tercermin di andalan murah
  2,4K-5K, tanpa mengarang segmen/promo.

## Build
- 7 slide 4096x4096 (1 cover + 6 halaman produk, pagination
  generik dari katalog_slides.py). Template disalin dari
  auto-20261116-1001 (bukan 2026-10-31 seperti bunyi body):
  folder itu membawa fix pagination slide-7 (LAST_PAGE_BUDGET +
  split_section, 16 Nov); menyalin 2026-10-31 akan menghidupkan
  lagi bug overflow yang sudah diperbaiki. Desain tidak diubah.
  Semua 7 slide dibaca: bersih, tanpa overflow/tabrakkan,
  CTA band slide 7 jauh dari footer.
- Reel paket TikTok: 3 + 5*ceil(22/3) + 3 = 46 detik, 1104 frame
  @24fps, 2160x3840 yuv420p. Musik: pick_reel_track.sh tepat
  sekali, hasil di track.txt (Oppressive Gloom by Kevin MacLeod).

## Target metrik (snapshot laporan 22:30)
- Threads: balasan + repost > 0 (edisi #2: 0 balasan, 84 views;
  #3 mingguan 40 views; #5 belum tercatat).
- IG carousel: likes + saves, bandingkan dengan carousel #3
  (2 likes / 39 views) dan #5.
- FB carousel: views + shares (bukan reactions), bandingkan
  dengan carousel #3 (7 views) dan #5.
- Story: viewers vs #2 (13 viewers).
