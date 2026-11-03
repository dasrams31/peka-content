# Analysis - Katalog Peka, Selasa 3 November 2026, 13:00 WIB

Edisi katalog kedua dalam seri katalog mingguan (Selasa + Jumat 13:00 WIB).
Template generik dari edisi 2026-10-31, tidak di-redesign. Satu-satunya
perubahan path: `OUT` di `katalog_slides.py` diarahkan ke folder edisi ini
agar tidak menimpa slide edisi 31 Okt; path baca harga `../prices.json`
tidak diubah.

## Gate harga
- `prices.json`: `updated` 2026-10-31, hari ini 2026-11-03 = 3 hari lalu,
  di dalam batas 7 hari. Gate LULUS, lanjut build + posting.
- Harga HANYA dari prices.json: Gemini Pro 3 bln 15K, CapCut Pro privat
  1 bln 27K, Canva Edu 6 bln 11K, Muse Spark AI lifetime 24K
  (3-4 Milyar token), Microsoft 365 1 thn 26K. Tidak ada harga/promo/
  garansi/testimoni/stok yang dikarang.
- Tidak ada list harga baru dari user sebelum jadwal, jadi prices.json
  tidak diubah sebelum tayang (kecuali `last_posted` setelah semua posting
  sukses). `date_label` di visual tetap "Sabtu 31 Oktober 2026" mengikuti
  prices.json apa adanya.

## Bacaan wajib
- `engagement-playbook.md`: hook <=60 char keuntungan pembaca, 1 pemicu
  interaksi, caption mandiri (aturan view 31 Okt, TERKUNCI), pertanyaan
  penutup pilihan paksa, tanpa link di teks postingan, DM keyword
  "DM MAU [produk]" untuk jualan.
- `learnings.md`: nilai per platform dengan ukurannya sendiri (IG likes+
  saves, Threads replies+reposts, FB views+shares); keputusan dari snapshot
  22:30, bukan angka menit awal; jangan hapus + repost bila ada masalah.
- `trending.md` (review 1 Nov): eksperimen tanpa-link LANJUT; SPILL #11
  pola caption (repo paling kepakai + langkah pertama konkret + pertanyaan
  pilihan) MENANG; katalog bukan cerita personal, andalannya daftar harga
  yang save-worthy.
- `tag-watch/tag-watch.md` (update 3 Nov, 73 post 7 hari, 12 baru hari ini)
  + `tag-watch/fyp-learning.md` (3 Nov: TOP didominasi question 22% +
  story 22%, hashtag rata-rata 0,6): caption pendek, 1 pertanyaan, hashtag
  sedikit. `current_tag.txt` berisi "AI".

## Edisi sebelumnya (31 Okt, dari posted.log + performance.log)
- Tayang tertunda antrean approval: Threads ~14:25, IG/FB/Story ~14:35-14:37
  WIB; percobaan pertama IG reels terputus restart service, retry sekali
  berhasil tanpa dobel (terverifikasi).
- Metrik snapshot mingguan: Threads 1 like, 1 komentar, 40 views, 34 reach,
  0 repost. IG 1 like, 0 save, 25 views. FB 0 like, 3 views.
  Baseline sangat rendah; pembandingnya edisi ini sendiri, bukan pilar lain.
- Hook 31 Okt: "Akun premium mulai 11K, ready hari ini." (38 char).
  Caption mandiri + pertanyaan "Kamu mau yang mana dulu?" + daftar harga
  + DM keyword sudah dipakai; tidak ada balasan rantai (aturan view 31 Okt).

## Hook edisi ini (rotasi framing saja, tanpa promo karangan)
- Hook baris pertama (33 char): "Lima akun premium, mulai 11K aja."
  Rotasi: jumlah produk di depan ("Lima...") + "aja" santai, menggantikan
  framing "ready hari ini" edisi lalu. Rentang harga tetap eksplisit di
  caption (11K sampai 27K lewat daftar 5 produk) + cara order
  (DM: MAU [nama produk]) di teks caption, sesuai aturan view 31 Okt.
- Pertanyaan penutup tetap pilihan paksa: "Kamu mau yang mana dulu?"
- Pemicu interaksi: pertanyaan pilihan + ajakan save + DM keyword.
  Tidak ada balasan rantai.

## Closing tag
- Threads ditutup TEPAT 1 tag: #AI (CURRENT CLOSING TAG, tag-watch.md
  3 Nov). #Mahasiswa rata-rata likes lebih tinggi (5956,0 vs #AI 1398,6)
  tapi n=8, belum memenuhi syarat pindah (2x rata-rata #AI dengan n>=10).
  Jadi tetap #AI.

## Perbedaan vs edisi sebelumnya
- Hook dirotasi (lihat di atas); daftar harga, template slide/reel, urutan
  posting, dan pola caption sama.
- Musik reel: track baru dari `pick_reel_track.sh` (dipanggil TEPAT SEKALI,
  dicatat di track.txt), bukan Crypto edisi lalu.
- Slide/reel di-build ulang dari template yang sama (bukan aset daur ulang),
  dengan verifikasi frame seperti edisi perdana.

## Target metrik (untuk snapshot 22:30, bukan vonis menit awal)
- Threads: replies + reposts > 0; views di atas 40 (baseline 31 Okt).
- IG: likes + saves; views di atas 25.
- FB: views + shares; views di atas 3.
- Setelah posting: catat ID/link tiap platform di posted.log +
  performance.log; edisi Jumat membandingkan metrik edisi ini sebelum
  memilih hook berikutnya.
