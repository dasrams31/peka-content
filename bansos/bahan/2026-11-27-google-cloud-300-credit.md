# Bahan terverifikasi: Google Cloud Free Trial, kredit $300, 90 hari

Sumber resmi dibaca langsung 27 Nov 2026:
- https://cloud.google.com/free (halaman penawaran)
- https://cloud.google.com/free/docs/free-cloud-features (dokumentasi resmi program Free Trial + Free Tier)

## Fakta terverifikasi

- Program: Google Cloud Free Trial buat pelanggan baru.
- Nilai: kredit sambutan $300, berlaku 90 hari sejak daftar.
- Syarat lolos: belum pernah jadi pelanggan berbayar Google Cloud, Google Maps Platform, atau Firebase; belum pernah daftar Free Trial sebelumnya.
- Cara daftar: buka cloud.google.com/free, klik mulai trial, daftar pakai akun Google, siapkan kartu atau metode pembayaran lain yang valid selama masa trial.
- Selama trial: tidak ada tagihan sama sekali, tidak ada auto-charge. Kartu dipakai buat verifikasi identitas dan cegah penipuan. Google mengirim authorization request berupa hold sementara $0,00-1,00 USD, BUKAN tagihan, dananya tidak ditarik, hold lepas dalam beberapa hari sampai sebulan.
- Kredit bisa dipakai buat produk yang tercakup Free Trial, termasuk Compute Engine, Cloud Run, Cloud Storage, BigQuery, dan pemakaian di atas batas Free Tier.
- Free Tier terpisah: 20+ produk gratis selamanya dalam batas bulanan (contoh: 1 instance e2-micro per bulan, Cloud Run 2 juta request/bulan, BigQuery 1 TB query/bulan, Cloud Storage 5 GB-months, Cloud Build 120 menit build/hari). Free Tier tetap jalan setelah trial bila upgrade ke akun berbayar.
- Kalau trial habis (90 hari lewat atau kredit $300 habis) dan tidak upgrade: akun billing trial ditutup, semua resource berhenti, masuk masa tenggang 30 hari, lalu resource dihapus permanen kalau tetap tidak upgrade.
- Kalau upgrade ke akun berbayar selama trial: trial berakhir, sisa kredit tetap bisa dipakai sampai 90 hari sejak daftar, resource tetap jalan tanpa putus, dan tagihan cuma buat pemakaian di luar sisa kredit dan Free Tier.

## Catch yang WAJIB disebut

- Butuh kartu pas daftar (cuma hold $0-1, bukan tagihan).
- Kredit hangus setelah 90 hari atau habis dipakai; resource berhenti dan dihapus permanen setelah masa tenggang 30 hari kalau tidak upgrade.
- Selama trial TIDAK BISA: tambah GPU ke VM, pakai Google Cloud Marketplace, minta naik kuota, bikin VM berbasis Windows Server, menambang kripto.
- Kredit $300 TIDAK BISA dipakai buat layanan Gemini platform (dulu Vertex AI) kalau daftar trial atau upgrade pada/setelah 16 Nov 2026, dan tidak bisa buat biaya Gemini API di AI Studio. Jadi jangan klaim kreditnya bisa dipakai buat semua layanan AI Google.
- Upgrade ke akun berbayar mengakhiri trial dan mengaktifkan tagihan buat pemakaian di luar kredit.

## Bar seleksi

- LOLOS (a): trial gratis dengan durasi jelas 90 hari, di atas minimal 1 bulan.
- LOLOS (b): nilai $300 dari nama besar (Google).
- Belum pernah tayang di Bansos (cek posted.log 27 Nov 2026: tidak ada Google Cloud).
- Tidak bentrok dengan pilar 27 Nov (Bandingin Model GPT vs Gemini, Prompt Harian #34, Coba Dulu Pollinations).

## Shortlink

- Target resmi: https://cloud.google.com/free
- Kode dibuat langsung di DB shortlink sebagai admin (user_id 1), 6 karakter unik, verifikasi redirect 307.
