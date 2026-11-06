# Analysis — Katalog Peka edisi #3, 6 November 2026, 13:00 WIB

## Harga (sumber tunggal: prices.json)
- `updated` 2026-11-04, umur 2 hari: gate kesegaran lulus (<=7 hari).
- 14 produk, rentang 4K-27K. Termurah: Alight Motion 1 Tahun 4K.
  Termahal: CapCut Pro privat 1 bulan 27K. Label tanggal di slide:
  "Rabu 4 November 2026" (date_label prices.json).
- Tidak ada harga/promo/garansi/testimoni/stok yang dikarang.

## Edisi sebelumnya
- #1, 31 Okt 2026 (5 produk): hook "Akun premium mulai 11K, ready
  hari ini." Tayang: Threads carousel, IG reels, FB reels, Story.
- #2, 3 Nov 2026 (5 produk): hook "Lima akun premium, mulai 11K aja."
  Snapshot 22:30: Threads 2 likes / 84 views / 0 balasan;
  IG 1 like / 30 views / 0 saves; FB 0 likes / 4 views;
  Story 13 viewers. Komentar 0 di semua platform: pertanyaan
  penutup belum memancing balasan penonton.
- Pre-build 4 Nov 2026 (14 produk, hook "14 akun premium, mulai 4K
  aja."): TIDAK PERNAH TAYANG, ditahan buat slot hari ini.
  Caption-nya masih pola reels (ada kredit musik di IG/FB) dan
  slide 5-nya cacat (lihat di bawah), jadi edisi ini dibangun
  ulang dari nol di folder 2026-11-06, bukan reuse mentah.

## Perubahan format edisi ini (perintah user 5 Nov 2026)
- IG + FB posting CAROUSEL (bukan reels) untuk berita + jualan,
  berlaku mulai 6 Nov 2026. Reel animasi HANYA buat paket TikTok
  (manual user). Caption IG/FB TANPA kredit musik.
- Instagram Story WAJIB tayang, dari desain slide Threads
  (story-9x16.png, compose cover ke kanvas 1080x1920). Bukan dari
  file reel. Threads + FB tidak punya publikasi story via CLI.

## Perbaikan slide
- Slide 5 (terakhir) cacat di build 4 Nov: catatan "Atau gabung
  grup WA: url.peka.ai.id" menabrak footer "GABUNG KE KOMUNITAS
  KAMI: URL.PEKA.AI.ID" karena halaman terakhir 14 produk terlalu
  tinggi (band CTA jatuh ke y=3180). Diperbaiki di copy
  katalog_slides.py edisi ini saja: band CTA di-cap di y=3100
  (band_y = min(y + 200, 3100)). Slide 1-4 tidak berubah
  (hash sama), slide 5 sudah dibaca ulang dan bersih.

## Hook edisi ini (rotasi framing)
- #1 dan #2 sama-sama hitung-dulu ("X akun premium, mulai Y").
  Edisi ini dibalik jadi harga-dulu: "Mulai 4K, ada 14 akun premium
  ready." (35 char, <=60). Tetap jujur: 14 produk, termurah 4K.
- Closing tag: #Mahasiswa (current_tag.txt; tag-watch 6 Nov:
  rata-rata 7 hari 4940.7 likes, n=10, >= 2x #AI 992.4, n=10).
- FYP learning 6 Nov: top post didominasi pertanyaan (23%) dan
  cerita (23%), hashtag rata-rata 0.6. Caption tetap bawa satu
  pertanyaan pilihan paksa ("Kamu mau yang mana dulu?") + ajakan
  save + cara order DM MAU [produk] di teks (caption mandiri,
  aturan 31 Okt). Tanpa link di teks postingan mana pun.
- Eksperimen minggu ini (HM / BLUEPRINT / Gratisan) tidak ada yang
  ditugaskan ke katalog; edisi ini tanpa eksperimen.

## Target metrik (snapshot laporan 22:30)
- Threads: balasan + repost > 0 (edisi #2: 0 balasan, 84 views).
- IG carousel (format baru buat katalog): likes + saves,
  bandingkan dengan reels #2 (1 like / 30 views).
- FB carousel (format baru): views + shares, bandingkan dengan
  reels #2 (4 views). Review 1 Nov: foto/carousel SPILL di FB
  jauh di atas reel-nya, jadi carousel FB diharapkan naik.
- Story: viewers vs #2 (13 viewers).
- Musik reel (paket TikTok): Volatile Reaction by Kevin MacLeod
  (pick_reel_track.sh tepat sekali, track.txt). Reel 31 detik:
  3 + 5*ceil(14/3) + 3, 744 frame @24fps, 2160x3840 yuv420p.
