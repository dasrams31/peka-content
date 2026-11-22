# Bahan Bansos — Altare Always Free (Sandbox Linux / VPS Gratis)

Sumber bahan: user, 22 Nov 2026 17:15 WIB (pesan WA).
Slot rencana: Bansos 25 Nov 2026 20:00 (23 Nov 20:00 sudah Caffeine AI).
Status: TERVERIFIKASI — dengan DUA koreksi wajib (Singapura + spek pool).
Jangan pakai bahan mentah apa adanya.

## Bahan mentah dari user (verbatim)

bahan bansos

Sanbox Linux, alternative VPS Always Free

Altare.
1 core, 1 GiB RAM, 5 GiB disk, Ubuntu 24.04 (ada Debian, Alpine, dll).
Persistent, akses root via SSH.

Region bisa pilih, ada Singapore dan Jakarta.
https://console.altare.gg/register

## Verifikasi (22 Nov 2026 ~17:20 WIB, halaman resmi altare.gg)

### TERBUKTI — pricing https://altare.gg/en/pricing
- Always Free $0 per tim: 6 GB memory, 150% CPU (satu setengah core),
  10 GB disk, sampai 4 server. Plus 10 GB U3 storage + 5 bucket,
  1 GB KV + 3M reads/bulan.
- "Every team starts on the Always Free plan... You only spend bolts
  if you choose to add more resources, and Altare Plus is entirely
  optional."
- Altare Plus $7.99/tim/bulan (opsional): +4 GiB memory, +20 GiB disk,
  +100% CPU, 2 slot server, akses lokasi Plus-only seperti London.

### TERBUKTI — compute https://altare.gg/en/platform/compute
- Sandbox: "A Linux box you keep and SSH into as root" — Ubuntu,
  Debian, Alpine, Fedora, Arch, image Docker Hub, atau saved image.
- "A sandbox is yours until you delete it" (persistent).
- "No. Apps, bots and servers stay online around the clock on every
  plan." (tidak tidur saat idle).
- Ubuntu 24.04 muncul di contoh resmi (Go machine + Workstation).
- Bonus gratis lain: 1 Postgres + 1 MySQL (256 MB), Edge Functions
  3M request/bulan, 5 cron job, 5 DNS zone, U3 tanpa egress fee.

### TERBUKTI — lokasi https://altare.gg/en/help/other-games/choose-server-location
- Asia Pacific: Bangkok, Bishkek, JAKARTA, Ulaanbaatar, Brisbane.
- "Location capacity can change. A city appearing on the website does
  not guarantee that it has room for a new server at every moment."
- Beberapa lokasi hanya untuk Plus/Business (London). Jakarta lokasi
  standar.

### KOREKSI 1 — Singapura TIDAK ADA, jangan disebut
- Klaim user "ada Singapore dan Jakarta": separuh salah. Daftar resmi
  Asia Pacific TIDAK memuat Singapura. Yang ada: Bangkok, Bishkek,
  Jakarta, Ulaanbaatar, Brisbane. Jakarta benar, Singapura hapus.

### KOREKSI 2 — spek itu POOL bersama, bukan per server
- Klaim user "1 core, 1 GiB RAM, 5 GiB disk": itu SATU kemungkinan
  pembagian pool, bukan jatah per server. Paket gratis per tim = 6 GB
  RAM + 150% CPU + 10 GB disk untuk MAKSIMAL 4 server, dibagi sesuka
  hati ("Run one big server with all 6 GB, or four smaller ones").
- Jadi jangan tulis "dapat 1 core 1 GB 5 GB" sebagai spek paket.
  Tulis pool-nya, lalu contoh: satu sandbox bisa ambil 1 core +
  1 GB RAM + 5 GB disk, sisa pool masih bisa untuk server lain.

### TIDAK TERBUKTI — jangan dipakai
- "Tanpa kartu kredit": halaman register
  (https://console.altare.gg/register) hanya menampilkan pembuatan
  akun tanpa kolom kartu, tapi TIDAK ADA pernyataan resmi "tanpa kartu".
  Jangan klaim tanpa kartu. Sampaikan apa adanya: daftar gratis,
  Plus berbayar opsional.
- Performa hardware: "Processor model, storage and available capacity
  vary by node; we do not promise that every location uses the same
  CPU or delivers identical performance." Jangan janjiin kecepatan.

### Catatan kecil (boleh disebut sebagai catch)
- Bolts/rewards/store butuh akun Discord yang terhubung ("Bolts,
  rewards and the store need a linked Discord account"). Paket gratis
  sendiri tidak butuh bolts.

## Versi yang boleh tayang (koreksi)

- Judul: Altare — VPS gratis selamanya (sandbox Linux, root via SSH).
- Fakta: paket Always Free per tim: 6 GB RAM, 1,5 core CPU, 10 GB
  disk, sampai 4 server, dibagi sesuka hati. Sandbox Linux persisten
  (punya kamu sampai dihapus), SSH sebagai root, tidak tidur saat idle.
  OS: Ubuntu (24.04), Debian, Alpine, Fedora, Arch, atau image Docker.
  Lokasi Asia Pasifik termasuk Jakarta (juga Bangkok, Bishkek,
  Ulaanbaatar, Brisbane).
- Contoh: satu sandbox 1 core + 1 GB RAM + 5 GB disk, sisa pool masih
  bisa dipakai server lain (bot, web, game server).
- Bonus gratis: storage 10 GB tanpa biaya egress, 1 database Postgres
  + 1 MySQL, Edge Functions, cron job.
- Cara: daftar di console.altare.gg/register → buat tim → buat
  sandbox → pilih lokasi (Jakarta) → SSH sebagai root.
- Catch (wajib disebut): spek di atas itu pool bersama satu tim,
  bukan per server; hardware beda-beda tiap node; kapasitas lokasi
  bisa penuh sewaktu-waktu; lokasi tertentu (London) hanya untuk
  Plus $7,99/bulan; Plus sepenuhnya opsional.
- JANGAN sebut: Singapura, "1 core 1 GB 5 GB" sebagai spek paket,
  "tanpa kartu kredit", janji performa.
- Link: https://console.altare.gg/register (shortlink admin dibuat
  saat build edisi).
