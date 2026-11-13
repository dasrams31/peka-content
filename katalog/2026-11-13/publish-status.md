# Publish status — Katalog Peka edisi #5, 13 November 2026 (SEBAGIAN)

## Tayang (terverifikasi live lewat read-back)
- Threads carousel 7 slide: https://www.threads.com/@peka.ai.id/post/Dfq_QmtD75y
  (post_id 18130949953848787, caption terverifikasi, tepat 1 #AI)
- Instagram carousel 7 slide: https://www.instagram.com/p/Dfq_wCxjzgV/
  (media 18127336642908025, caption terverifikasi, 1 like / 0 komentar
  saat read-back)

## DITOLAK user (jangan retry tanpa perintah eksplisit)
- Facebook carousel: kartu approval DITOLAK user
  (approval_denied, approval_id
  connector-attempt-c2fe049207a5fcaff0fb882768778890bc2b4ad3c965c34e1ae4d1fc1b1549bc).
  Script publish berhenti di langkah ini (exit 3).

## Belum jalan
- Instagram Story (story-9x16.png sudah siap, terverifikasi bersih):
  tidak sempat dijalankan karena script berhenti di FB.
- Broadcast channel Telegram: DITAHAN (butuh semua platform tayang).
- prices.json `last_posted` BELUM diupdate (tetap 2026-11-10).
- posted.log / performance.log BELUM ditambah entri edisi ini
  (aturan body: hanya setelah SEMUA posting sukses).

## Langkah berikut (butuh kata user)
- Re-run dari chat: FB carousel + IG Story saja (post-done.txt sudah
  mencatat Threads + IG, script idempotent, tidak akan dobel).
  Lalu broadcast channel + pencatatan log seperti biasa.
- Preseden: SPILL #22 (FB reel ditolak 11 Nov 21:49) juga ditahan
  sampai re-run dari chat; kartu yang ditolak butuh re-run baru
  untuk muncul lagi.
