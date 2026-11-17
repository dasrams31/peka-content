# Strategi Facebook Otomatis Peka (2026-11-17, perintah user)

Tujuan: Facebook Page PekaAI berhenti stuck. Yang dikejar BUKAN like.
Like di FB itu 0 di hampir semua postingan sejak dulu, di semua pilar.
Yang bergerak di FB: views dan shares.

## Diagnosis (angka terverifikasi 17 Nov 2026)

- 202 baris FB di `performance.log`: total like FB cuma belasan, tersebar.
  Live 10 postingan terakhir: reactions 0, shares 0, comments 0 semua.
- Page cuma ~29 pengikut (15 Nov 2026). Distribusi FB bergantung ke
  shares dan rekomendasi, bukan follower.
- Bukti format, SPILL: carousel #06 1.345 views / 10 shares, #07 626
  views / 5 shares; reel-nya sendiri 29 dan 22 views. Tapi body cron
  SPILL masih pakai aturan reels-saja 27 Okt buat FB, jadi #27 tayang
  sebagai reel dan cuma 2 views. Aturan carousel yang sudah di-acc
  1 Nov belum pernah dipasang ke cron (diperbaiki 17 Nov 2026).
- HM: carousel FB median 3 views (mati), tapi reel benchmark ekstra
  188 views. Prompt: reel FB paling hidup belakangan (#26: 205 views).
- Caption FB selama ini tanpa ajakan share sama sekali.

## Skor FB (definisi baru, menggantikan playbook butir 7 untuk FB)

FB = views + shares. Reactions dicatat di performance.log tapi BUKAN
target dan BUKAN vonis. Satu edisi FB dinilai dari median views dan
median shares pilar itu, bukan dari like.

Baseline 17 Nov 2026: median views per pilar 3-40, shares median 0.
Target 4 minggu: median views FB >= 100 dan >= 1 share per edisi.

## Format FB per pilar (dikunci dari data)

| Pilar | Format FB | Alasan |
|---|---|---|
| SPILL | Carousel 8 slide | #06/#07 carousel 626-1.345 views vs reel 2-29 |
| HM | Carousel + reel benchmark ekstra bila ada angka | Carousel median 3 views; reel benchmark 188 views |
| Prompt Harian | Reel | #26 reel 205 views, terbaik belakangan |
| Gratisan AI | Reel | Tawaran besar + reel jalan di FB |
| Katalog | Carousel | Aturan 6 Nov 2026, tetap |
| BLUEPRINT | Reel | #01 reel 231 views |
| Tutorial Mirror / AI Pekan Ini / Tutorial Agent | Reel | Voiceover reel, 43-91 views |
| Bansos | Carousel bila ada foto bukti, reel bila tidak | Foto names.co.uk 388 views / 8 shares |

SATU format per edisi per pilar di FB. Jangan tayang reel DAN carousel
untuk edisi yang sama.

## Resep caption FB (semua pilar, maks 1024 char)

Urutan: hook (<=60 char, keuntungan pembaca) + isi mandiri (fakta inti
+ langkah pertama konkret) + TEPAT SATU kalimat instruksi link-di-visual
("Linknya ada di slide terakhir." / "Link tiap repo ada di slide-nya
masing-masing." / "Linknya ada di akhir video.") + SATU pertanyaan
pilihan paksa + SATU ajakan share ("Share ke teman yang lagi butuh
<topik>."). Tanpa hashtag, tanpa link, tanpa perintah install di teks
caption (aturan terkunci tetap berlaku).

Ajakan share itu pemicu distribusi FB. Tanpa itu, Page 29 pengikut
tidak punya mesin sebar.

## Loop otomatis (ukur, putuskan, terapkan)

1. `fb_analyzer.py` (mingguan, sebelum review 20:00): baca
   `performance.log` 28 hari terakhir + cek live 10 postingan FB
   terbaru via `facebook-cli pages posts list`. Hitung median views
   dan shares per (pilar, format). Tulis `fb-state.json`.
2. Vonis yang ditulis analyzer ke `learnings.md` (bagian FB) hanya
   bila ada perubahan: pemenang format baru, kill rule terpicu, atau
   penyimpangan format dari peta di atas.
3. Cron `peka-fb-strategy` (mingguan 19:00): jalankan analyzer, lalu
   terapkan perubahan format/hook/CTA ke body cron yang bersangkutan.
   Lingkup auto-apply sama dengan review mingguan: format, hook, CTA,
   topik saja. Harga, jadwal, akun, dan aturan terkunci TIDAK disentuh
   tanpa kata user.
4. Review mingguan 20:00 membaca vonis FB dari `fb-state.json` seperti
   biasa.

## Aturan promote / kill

- Promote: satu format median views-nya >= 2x format lain di pilar yang
  sama (n >= 3 edisi) jadi format FB default pilar itu.
- Kill: satu format yang kalah >= 2x dari format lain di pilar yang
  sama DAN median views-nya < 10 selama 2 bacaan mingguan berturut-turut
  dihentikan; format pemenang tidak pernah di-kill.
- Guard: analyzer cek blog JSON edisi 7 hari terakhir; bila link
  facebook-nya `/reel/` padahal peta bilang carousel (atau sebaliknya),
  itu penyimpangan format. Laporkan ke chat, jangan diam.

## Yang tetap manual (otomatisasi tidak bisa menggantikannya)

- Nambah pengikut Page (invite teman, share dari akun pribadi).
- Balas komentar FB (manual, Dipa-kun).
- Keputusan ubah aturan terkunci (mis. format pilar yang dikunci user).

## File

- Strategi ini: `~/workspace/peka-content/fb-strategy.md`
- Analyzer: `~/workspace/peka-content/fb_analyzer.py`
- State: `~/workspace/peka-content/fb-state.json`
- Aturan di playbook: bagian "STRATEGI FACEBOOK OTOMATIS" di
  `~/workspace/peka-content/engagement-playbook.md`
- Cron: `peka-fb-strategy`, mingguan 19:00 WIB
