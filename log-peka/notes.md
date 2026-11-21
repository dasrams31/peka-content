# LOG PEKA — dated observations

Appended by every LOG PEKA edition run. Facts only: what changed, what
the numbers showed, where the number came from. Never invent metrics.

## 2026-10-31

- Aturan TANPA LINK DI TEKS POSTINGAN dikunci ~17:06 WIB, diperluas
  17:19 WIB ke semua platform (Threads, IG, FB, TikTok), slide maupun
  reels. Link edisi dicetak di visual; caption membawa satu kalimat
  instruksi. Playbook + 5 template reel + generator + cron diperbarui
  sore itu juga.
- Data 31 Okt KOTOR buat menilai eksperimen: caption root HM kosong
  (file caption di /tmp hilang saat service restart) + Threads 429
  memblokir balasan rantai HM dan carousel Gratisan AI. Views katalog
  tidak terekspos di read-back Threads.
- Tayang 31 Okt: katalog Peka perdana (~14:25-14:37 WIB, Threads
  carousel + IG/FB reels + IG Story), Prompt #09, HM + Gratisan AI
  (IG/FB reels + blog, Threads kena 429), bansos ChatGPT OSS 19:36,
  BLUEPRINT Cindy 20:00 (5 slide + reel halaman repo), SPILL #11
  HERMES 21:30.
- Aturan view 1-3 dikunci malam 31 Okt (perintah user "Boleh 1-4"):
  caption mandiri, pertanyaan pilihan paksa, rantai maks 5 + balas
  komentar. Berlaku semua cron konten mulai edisi berikutnya.
- Seri LOG PEKA dibuat 31 Okt malam. Edisi perdana: Sabtu 7 Nov 2026
  16:00 WIB = Hari ke-7 eksperimen ini (hari penuh pertama 1 Nov).

- Edisi #01 tayang TELAT 18:03-18:19 WIB (re-run dari chat atas perintah user "boleh"). Threads carousel 4 slide + rantai 3 balasan, IG/FB reel 15 dtk. Penyebab telat: kartu approval run cron 16:10 habis waktu (timed out 16:36), bukan konten. Series 1->2.

## 2026-11-14 — Edisi #02, Hari ke-14 (hari terakhir) eksperimen #1 "Tanpa link di teks postingan"

- Verdict eksperimen #1 sudah tercatat di learnings.md 1 Nov 2026: LANJUT. Aturan tanpa-link jadi aturan permanen, bukan lagi eksperimen. experiment.json baru diperbarui hari ini: status "running" sejak 31 Okt ternyata basi, verdict sudah ada tapi state tidak ikut berubah.
- 3 angka kunci (semua dari performance.log snapshot 22:30 + live read 14 Nov 16:00 WIB):
  1. Median Threads views 14 edisi bersih tanpa-link 8-13 Nov: 156 views (rentang 43-1.295). Baseline pra-eksperimen 28-30 Okt: SPILL #10 21 views, Prompt #07 24 views. Median naik sekitar 7x dari titik terendah.
  2. Gratisan AI 11 Nov (Google AI Plus, exp renewal-price): Threads 1.295 views, 7 likes, 1 komentar, 1 repost. Edisi tanpa-link terkuat minggu ini di luar SPILL #11 (4.149 views).
  3. SPILL #24 live read 14 Nov 16:00: 19 likes di Threads, naik dari 5 likes saat snapshot 22:44 13 Nov. Views tidak terekspos di read-back (no_data di performance.log). IG SPILL #21: 92 likes di snapshot 24 jam, naik dari 4 likes awal.
- Perbandingan vs baseline: tidak ada lagi edisi bersih tanpa-link di bawah 43 views minggu ini; sebelum eksperimen, dua edisi beruntun mentok di 21-24 views. Views pulih dan bertahan selama 2 minggu.
- Temuan:
  1. Tanpa-link itu lantai, bukan mesin. Semua edisi minggu ini tanpa-link, tapi hasilnya menyebar dari 43 views (Prompt #20) sampai 1.295 views (Gratisan 11 Nov). Yang membedakan tetap kekuatan tawaran + pola caption #11 (repo paling kepakai + langkah pertama konkret).
  2. HM masih bisa ramai di Threads meski freeze: HM Hydrogen 13 Nov lolos ke Threads (padahal freeze 7 Nov-7 Des) dan meraih 301 views + 5 komentar, di atas median minggu ini. Sinyal topik model baru masih kuat, tapi kebocoran freeze-nya perlu ditutup.
  3. Rantai distribusi masih bocor di gate: SPILL #22 FB reel ditolak 11 Nov 21:49 dan belum tayang ulang; SPILL #23 nyangkut di approval gate sejak 21:33 12 Nov; SPILL #24 IG/FB/blog belum tayang per 22:44 13 Nov. Aturannya jalan, eksekusinya yang sering putus.
- LOG PEKA #01 sendiri: tidak ditemukan di read-back Threads live 14 Nov 16:00 (count 0), sama seperti laporan 7 Nov (tidak ditemukan di daftar instagram-cli, snapshot awal 0 like). Metrik edisi #01 tetap belum terukur.
- Pergantian eksperimen: eksperimen #2 "Format perbandingan dua kolom (X vs Y / sebelum vs sesudah) di caption + slide 1" dikunci 14 Nov, mulai 15 Nov, verdict di review Minggu 22 Nov 20:00. Hipotesis: format perbandingan mengangkat median Threads views Prompt di atas 103 (median 9-13 Nov) dan likes SPILL di atas 5 (median snapshot 9-13 Nov). Gate: pilot slot 13 Nov (Prompt before/after + SPILL comparison slide) dinilai review Minggu 15 Nov 20:00; bila keduanya KALAH atau VOID, eksperimen #2 dibatalkan sebelum edisi pertamanya dan diganti topik lain dari trending.md. Edisi LOG PEKA berikutnya (21 Nov) = Hari ke-7 eksperimen #2.

## 2026-11-21 — Edisi #03, Hari ke-7 eksperimen #2 "Format perbandingan dua kolom (X vs Y / sebelum vs sesudah) di caption + slide 1"

- Status: eksperimen masih "running" di experiment.json; verdict baru jatuh di review Minggu 22 Nov 20:00. Edisi ini TIDAK memberi verdict, hanya mencatat hari ke-7.
- 3 angka kunci (semua dari performance.log snapshot 22:30 + live read threads-cli 21 Nov 16:00 WIB):
  1. Median Threads views Prompt Harian 15-20 Nov: 212 views (edisi terukur: #25 247, #27 177, #29 408, #30 71; #26 tidak tercatat di performance.log, #28 tidak tayang karena jeda Threads 18-19 Nov). Baseline median 9-13 Nov: 103 views.
  2. Likes SPILL Threads: median snapshot 22:30 edisi #27-#30 = 8 likes (#27 8, #28 8, #29 13, #30 8); SPILL #31 live read 21 Nov 16:00 naik ke 27 likes (dari 2 likes saat snapshot 22:30 20 Nov, baru 16 menit tayang) + 3 repost. Baseline median snapshot 9-13 Nov: 5 likes. Views SPILL tidak terekspos di read-back.
  3. Variabel perbandingan: 0 dari 13 edisi Prompt (#25-#31) + SPILL (#26-#31) 15-21 Nov yang membawanya. posted.log 15-21 Nov tanpa satu pun marker exp perbandingan; caption Threads ketujuh Prompt terverifikasi memakai pembuka cerita standar, keenam SPILL memakai pola #11 standar; grep caption tidak menemukan struktur sebelum/sesudah atau dua kolom.
- Perbandingan vs baseline: angka minggu ini di atas baseline di kedua pilar (views Prompt 212 vs 103, likes SPILL 8 vs 5, SPILL #31 live 27 likes), TAPI kenaikan ini tidak boleh dibaca sebagai bukti format perbandingan, karena formatnya tidak pernah tayang. Penjelasan yang lebih jujur: aturan yang sudah menang (pembuka cerita Prompt 8 Nov, pola #11 + hook stack SPILL 15 Nov) yang bekerja.
- Temuan:
  1. Eksperimen #2 TIDAK TERUJI sampai hari ke-7. Pilot 13 Nov sudah TIDAK JALAN sesuai desain (Prompt #23 dan SPILL #24, arsip review 15 Nov), dan minggu 15-21 Nov mengulang pola yang sama: generator mengeluarkan format standar, bukan slide + caption perbandingan. Gate di experiment.json (batalkan bila pilot KALAH atau VOID) tidak ditegakkan di review 15 Nov, eksperimen jalan tanpa variabel yang teruji.
  2. Angka minggu ini tetap naik tanpa variabel, jadi review 22 Nov berisiko salah baca bila hanya membandingkan median. Verdict yang jujur untuk eksperimen #2 adalah TIDAK TERUJI, bukan MENANG atau KALAH; bila mau diuji sungguhan, generator perbandingan harus dibangun dan diverifikasi dulu sebelum tayang, atau topik diganti dari trending.md.
  3. Data minggu ini kotor di dua tempat: FB gate 403 sejak 17 Nov (0 postingan FB 18-21 Nov; Prompt #30, HM 20 Nov, SPILL #31 semua gagal atau unknown di FB) dan jeda Threads 18-19 Nov (Prompt #28 tidak tayang sama sekali). Sisi terang: eksperimen lain di luar #2 justru jalan, Gratisan JetBrains 21 Nov 14:00 tayang dengan caption gratis vs Pro sesuai desain (marker exp: gratisan-free-vs-paid di posted.log, caption terverifikasi live: 4 likes / 4 repost saat live read 16:00, views belum terukur karena tidak terekspos read-back). Itu bukti eksperimen level caption bisa jalan bila variabelnya tidak butuh slide baru.
- LOG PEKA #02 sendiri: tetap belum terukur (edisi internal, tidak diposting; sesuai perintah user, tidak ada metrik postingan untuk edisi internal).
