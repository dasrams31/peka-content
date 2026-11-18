# POSTING HANDOFF — Komik Peka #01 (prepared 2026-11-18 ~18:00 WIB, worker run)

## Episode
- #01 — Claude Fable 5.2: termurah, kok nomor satu?
- Video: `~/workspace/peka-content/animate/pieces/peka-komik-fable-30s/renders/share.mp4`
  (verified: 1080x1920, yuv420p, h264+aac, 30.016s, 12.99 MB)
- Cover: `.../renders/cover.jpg` (frame detik ke-1, 1080x1920 JPEG, diekstrak run ini)
- Captions: `caption-ig.txt`, `caption-fb.txt`, `caption-tiktok.txt` (same folder)
- State: `~/workspace/peka-content/animate/series.txt` = `1` (dibuat run ini, belum ada sebelumnya)
- Anti-dobel: `posted.log` bersih, belum ada baris komik-peka.

## PENTING — jalankan dari chat interaktif, BUKAN worker latar
Badan tugas: posting CLI memunculkan kartu approval (batas 30 menit) yang
hanya muncul ke user dari chat interaktif. Worker TIDAK menjalankan perintah
posting apa pun di run ini. Jalankan dua perintah di bawah dari main chat,
ketuk tiap kartu saat muncul. Bila satu kartu kedaluwarsa: verifikasi live
dulu apakah postingan sebenarnya sudah tayang, jangan posting ulang membabi
buta. Bila posting gagal total: JANGAN naikkan nomor di series.txt.

## Threads: SKIPPED (jeda 18-19 Nov, perintah user 18 Nov 09:49)
JANGAN jalankan threads-cli, JANGAN minta kartu approval Threads, JANGAN
tulis URL Threads di laporan/broadcast/log. Di posted.log tulis
`threads SKIPPED (jeda 18-19 Nov)` sebagai ganti URL. Threads kembali
normal mulai 20 Nov 2026.

## 1. Instagram reel (account-id 17841426380826261)
```
instagram-cli post-feed --account-id 17841426380826261 \
  --file ~/workspace/peka-content/animate/pieces/peka-komik-fable-30s/renders/share.mp4 \
  --cover ~/workspace/peka-content/animate/pieces/peka-komik-fable-30s/renders/cover.jpg \
  --caption "$(cat ~/workspace/peka-content/animate/pieces/peka-komik-fable-30s/caption-ig.txt)"
```
Hasil JSON berisi `media_fbid`; ambil URL-nya:
```
instagram-cli post --account-id 17841426380826261 --id <media_fbid>
```

## 2. Facebook reel (Page PekaAI, page-id 1399217353266190)
```
facebook-cli pages posts create --page-id 1399217353266190 \
  --text "$(cat ~/workspace/peka-content/animate/pieces/peka-komik-fable-30s/caption-fb.txt)" \
  --privacy PUBLIC \
  --file ~/workspace/peka-content/animate/pieces/peka-komik-fable-30s/renders/share.mp4
```
Hasil JSON berisi `post_id` / `post_url`; bila `post_url` kosong, resolve:
```
facebook-cli post read --post-id <post_id>
```

## Setelah IG + FB berhasil
1. Tulis ke `~/workspace/peka-content/posted.log` satu baris (jam = jam posting aktual):
   `2026-11-18 HH:MM|komik-peka|episode #01 Claude Fable 5.2: termurah, kok nomor satu? | ig <url> | threads SKIPPED (jeda 18-19 Nov) | fb <url>`
2. Tulis `2` ke `~/workspace/peka-content/animate/series.txt` (episode berikutnya #02 DeepSeek).
3. Lapor ke chat: nomor episode, judul, link IG + FB, Threads dilewati karena jeda, paket TikTok sudah disampaikan.
4. Paket TikTok (manual user, jangan posting ke TikTok): video `share.mp4` + caption di `caption-tiktok.txt` + link IG/FB di atas.
5. TIDAK ada broadcast channel (tidak diminta badan tugas; channel juga jeda s.d. 19 Nov 12:48).

## Temuan visual (dilaporkan, tidak memblokir)
Strip caption l1 di render berbunyi "Termurah, kok nomor satu" — tanda "!"
dari source (`src/scenes.js` stripAt: 'Termurah, kok nomor satu?!')
terpotong di tepi kanan strip. Terlihat di frame detik ke-1 (cover) dan
0-3.18 detik video. Klaim review 16 Nov "text 0 cut-off" tidak akurat
untuk strip ini. User sudah acc episode ini 17 Nov 22:09 ("post besok"),
jadi rekomendasi: tayang apa adanya; perbaiki lebar strip saat render
episode berikut, bukan re-render #01 sekarang.
