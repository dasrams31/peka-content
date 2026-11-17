# BAHAN BANSOS — Model AI Coding Hy4 Flash Gratis di OpenCode

- Diterima dari user: 17 Nov 2026 14:48 WIB ("bahan bansos hari ini")
- Sumber bahan: teks user (mentah di bawah)
- Status: TERVERIFIKASI di halaman resmi provider, SIAP OLAH untuk edisi 17 Nov 2026 18:00

## Fakta dari bahan (terverifikasi)

- Provider: OpenCode (opencode.ai) — model **Hy4 Flash** dari Tencent (Tencent Hunyuan)
- Promo: model **Hy4 flash Free** (`hy4-flash-free`) GRATIS di dalam OpenCode, "hampir tanpa batas", sekitar 2 minggu, kira-kira sampai **30 Nov 2026**
- Konteks 1 juta token, bisa baca gambar (multimodal)
- Tanpa daftar, tanpa API key, tanpa kartu
- Cara pakai: install OpenCode (`curl -fsSL https://opencode.ai/v2/install | bash`), jalankan `opencode`, ketik `/models`, pilih Hy4 flash Free
- Bisa dikontrol dari HP pakai app OpenCode; di VPS: `opencode service start`, `opencode pair --remote --yes`, tempel link di app (berlaku 5 menit)
- Hanya jalan di dalam OpenCode, tidak bisa dijadikan API key buat bot lain
- Tips dari bahan: satu tugas satu sesi baru; jangan buka folder yang ada private key wallet

## Status verifikasi (17 Nov 2026, halaman RESMI)

- OpenCode docs resmi https://opencode.ai/v2/docs/console/models/ (dibaca langsung): tabel model resmi memuat **"Hy4 flash Free | hy4-flash-free"**. Halaman yang sama: "Free-tier chat models require OpenCode; use paid models or Go from other clients." — TERKONFIRMASI: model gratisnya ada + cuma jalan di dalam OpenCode.
- Siaran pers resmi Tencent https://www.tencent.com/tencent-launches-hy4-flash-to-power-high-speed-cost-efficient-ai-deployment-for-everyday-workflows/ (16 Nov 2026): Hy4 flash rilis 16 Nov 2026, 224B total / 12B aktif, konteks sampai 1M token, input multimodal, harga $0.07 per 1M token input. "From now till November 30, users can access Hy4 flash for free on WorkBuddy, and get 50 percent off standard pricing via Tencent Cloud TokenHub." — TERKONFIRMASI: modelnya baru (16 Nov), konteks 1M, multimodal, dan tanggal ~30 Nov cocok.
- Akun resmi OpenCode di X (dikutip digest 17 Nov): Hy4 flash "nearly unlimited and free for the next two weeks", juga tersedia di OpenCode Go tanpa memotong jatah Go — TERKONFIRMASI: frasa "hampir tanpa batas" + "2 minggu" itu kata vendor sendiri.
- Tanpa daftar / API key / kartu: TERKONFIRMASI via desain free tier OpenCode (provider built-in, tanpa akun) + pengujian independen (bigiron.cc, aifrontierpost.com) yang menjalankan model gratis tanpa akun apa pun.
- Perintah install `curl -fsSL https://opencode.ai/v2/install | bash`: TERKONFIRMASI (juga tercantum di docs aplikasi mobile getopencode.app).
- Pairing HP: TERKONFIRMASI sebagian di docs getopencode.app — `opencode service start` + `opencode pair`, link pairing kedaluwarsa setelah 5 menit dan sekali pakai, `opencode pair --remote` ada (expose lewat OpenTunnel setelah konfirmasi eksplisit).
- BUKAN ulangan: cek posted.log bansos — belum pernah ada edisi Hy4 / OpenCode sebagai bansos. SPILL #28 malam ini (21:30) memang OPENCODE, tapi itu showcase repo/skill, bukan tawaran model gratis; sudut beda, bukan bentrok dengan Gratisan AI/HM hari ini.

## KOREKSI dari bahan (JANGAN cetak versi bahan mentah)

1. **Developer aplikasi HP TIDAK terverifikasi.** Bahan bilang "app OpenCode (Play Store, developer Anomaly Innovations)". FAQ resmi aplikasi mobile getopencode.app menyatakan aplikasi itu "open-source, community-built companion for OpenCode and is not affiliated with the OpenCode team" — jadi BUKAN produk resmi / bukan dari tim OpenCode. JANGAN tulis "developer Anomaly Innovations" di edisi. Tulis saja "aplikasi OpenCode Mobile" tanpa klaim developer, atau sebut sebagai aplikasi pendamping komunitas.
2. **Langkah password HILANG dari bahan.** Docs pairing mewajibkan `opencode service set password` SEBELUM expose server ke internet ("Never publish an unauthenticated OpenCode port to the internet"). Bahan user langsung `opencode service start` + `pair --remote` tanpa password. Edisi WAJIB menyertakan langkah set password, atau minimal peringatan: jangan expose server tanpa password.
3. **"Hampir tanpa batas" bukan tanpa batas.** Itu kata vendor ("nearly unlimited"). Kuota free tier itu kuota komunitas bersama; pengujian independen pernah kena `FreeUsageLimitError` di jam sibuk. Jangan janji "unlimited".

## CATCH yang WAJIB tercetak DI SLIDE (aturan bansos)

- Gratis cuma sampai sekitar 30 Nov 2026 (tawaran waktu terbatas, roster model gratis bisa berubah tanpa pemberitahuan).
- Kuota bersama: bisa kena limit di jam sibuk, bukan benar-benar tanpa batas.
- Cuma jalan di dalam OpenCode; tidak bisa dipakai sebagai API key di bot/tools lain.
- Jangan buka folder berisi private key wallet (dari bahan user, tetap dicetak sebagai peringatan).

## Angle yang disarankan

- Kicker: INFO BANSOS (terkunci)
- Judul arah: "Model AI Coding Gratis 2 Minggu, Tanpa Daftar" / tekankan Hy4 Flash (Tencent) di OpenCode, konteks 1 juta token, bisa baca gambar
- Manfaat langsung: ngoding dibantu AI gratis tanpa API key, dari HP juga bisa
- Langkah klaim di slide 2/3 + blog versi lengkap (install, /models, pairing HP + password, peringatan wallet, FAQ: kenapa cuma di OpenCode, apa yang terjadi setelah 30 Nov)

## Teks asli bahan (mentah, dari user)

MODEL AI CODING GRATIS 2 MINGGU

OpenCode lagi ngasih model Hy4 Flash (Tencent) GRATIS, hampir tanpa batas, kira-kira sampai 30 Nov.

Kelebihannya:
- Tanpa daftar, tanpa API key, tanpa kartu
- Konteks 1 juta token
- Bisa baca gambar juga

Cara pakai:
1. Install OpenCode di PC/VPS:
curl -fsSL https://opencode.ai/v2/install | bash
2. Jalanin: opencode
3. Ketik /models, pilih Hy4 flash Free
4. Langsung suruh ngoding

Bisa juga dikontrol dari HP pakai app OpenCode (Play Store, developer Anomaly Innovations). Di VPS jalanin:
opencode service start
opencode pair --remote --yes
lalu tempel link-nya di app (berlaku 5 menit).

Catatan:
- Cuma jalan di dalam OpenCode, nggak bisa dijadiin API key buat bot lain
- Satu tugas satu sesi baru, biar nggak error
- Jangan buka folder yang ada private key wallet
