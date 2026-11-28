# Komik Peka episode #04 — prep (dibuat 28 Nov 2026, mode libur)

## Status
- `series.txt` di `~/workspace/peka-content/animate/series.txt` sudah `4` (batch #01–#03 habis).
- Cron `peka-komik-peka` (interval 72 jam, anchor 22 Nov 19:00) nonaktif selama libur;
  sesudah diaktifkan lagi 30 Nov 06:00, slot berikut jatuh sekitar 1 Des 19:00.
  Cron wajib BANGUN episode baru dulu sebelum posting (lihat cron body).
- File ini HANYA prep topik + fakta terverifikasi. Bukan episode jadi.
  Builder cron tetap wajib: baca engagement-playbook + learnings + tag-watch +
  fyp-learning, bangun via skill Animate gaya `peka-komik`, 30 detik,
  voiceover id-ID-ArdiNeural, render berurutan, verifikasi visual + ffprobe
  (1080x1920, yuv420p, 30 detik), lalu posting dari chat interaktif
  (IG reel + Threads carousel 6 still + FB reel, kartu approval).

## Topik yang diusulkan: harga Gemini 4 Carbon naik 2x tanggal 1 Des
- Alasan: timely persis di slot 1 Des 19:00; angka konkret; belum pernah dipakai
  seri Komik (#01 Fable 5.2, #02 DeepSeek, #03 tier-list skripsi) maupun
  Bandingin Model #02 (Astra vs Neon). Bukan perbandingan model, tapi
  peringatan harga — sudut beda.
- Fakta terverifikasi (28 Nov 2026, dua sumber sekunder independen):
  - Gemini 4 Carbon GA 10 Nov 2026, harga perkenalan $2 input / $10 output
    per 1 juta token, naik jadi $4 / $20 mulai 1 Des 2026.
  - Sumber: https://tecadmin.net/november-2026-ai-model-releases/ (tabel
    "Gemini 4 Carbon | 10 Nov (GA) | $2 / $10, rising to $4 / $20 on 1 Dec")
    dan https://applescoop.org/story/every-ai-model-in-order-gpt-claude-gemini-llama-release-dates
    ("Gemini 4 Carbon was on an introductory price that ends November 30, 2026").
  - WAJIB verifikasi ulang di halaman pricing resmi Google sebelum posting;
    bila angka tidak cocok, ganti topik atau berhenti dan lapor (aturan
    model-watch: tak terverifikasi = jangan bangun).

## Beats (gaya peka-komik, Piko + panel komik, 30 detik)
1. Piko senang pakai Gemini 4 Carbon yang murah ($2/$10), tag harga kecil.
2. Kalender balik ke 1 Des, tag harga membesar 2x ($4/$20), Piko kaget
   ("Loh, kok naik?").
3. Peka muncul: harga perkenalan habis 30 Nov; yang sudah pakai, cek tagihan
   dan pemakaian sebelum 1 Des; kalau cuma buat coba-coba, pindah ke tier
   gratis / model yang lebih murah (sebut yang konkret + terverifikasi
   saat build, jangan karang).
4. Penutup: pertanyaan pilihan paksa ("Kamu tetap pakai Carbon, atau pindah?").

## Voiceover draf (ArdiNeural, Bahasa Indonesia natural ala Peka)
- "Gemini 4 Carbon itu lagi murah, dua dolar per sejuta token. Tapi ingat,
  harga perkenalannya habis tiga puluh November."
- "Mulai satu Desember, harganya naik dua kali lipat. Jadi cek dulu
  pemakaian kamu sebelum tagihan bulan depan kagetin."
- Tutup: "Kamu tetap pakai Carbon, atau pindah?"

## Catatan jujur
- Klaim harga di atas dari sumber sekunder (dua roundup), BUKAN halaman
  resmi Google. Builder wajib cek pricing page resmi dulu.
- Jangan sebut nama tema/desain di karya final; tanpa link dan tanpa
  perintah install di caption (aturan terkunci).
