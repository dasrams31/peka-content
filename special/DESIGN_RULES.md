# DESIGN RULES — Edisi Khusus Peka (special editions)

Berlaku untuk semua edisi khusus (model AI baru, dsb.) dan semua carousel/reel
Peka yang dibuat setelah 12 Nov 2026. Ditulis setelah audit visual edisi
Claude Fable 5.2 (12 Nov 2026), yang menemukan: teks meluber keluar kartu
(slide 2 "FABLE VS MYTHOS"), subtitle kolom kiri menabrak kolom kanan
(slide 5 "AUTOMATIONBENCH"), nomor halaman menabrak baris teks terakhir
(slide 5 "5/6"), dan ruang kosong mati ~500px di bawah headline (slide 6).

Aturan ini TERKUNCI: builder yang melanggar satu saja wajib render ulang,
tidak boleh diserahkan.

## 1. Grid tetap (4096x4096)
- Margin: 240px kiri/kanan, 200px atas (di bawah header), 260px bawah
  (di atas footer).
- Header: badge kiri + logo kanan + garis pemisah, posisi sama di semua slide.
- Footer: strip khusus 200px di bawah untuk teks kaki + nomor halaman
  ("n/N" di kanan bawah). Isi body TIDAK BOLEH masuk strip footer.
- Semua elemen menempel ke grid yang sama di semua slide.

## 2. Tanpa overflow, tanpa tabrakan
- Setiap blok teks wajib muat di dalam kartunya: ukur tinggi teks dulu,
  baru tentukan tinggi kartu (kartu mengikuti isi, bukan sebaliknya).
  Bila teks tidak muat: pendekkan teksnya atau pecah kartunya, JANGAN
  biarkan teks keluar garis kartu.
- Bounding box dua elemen TIDAK BOLEH saling bersinggungan. Render script
  WAJIB memeriksa persinggungan bounding box secara programatik sebelum
  menyimpan PNG; ada satu tabrakan saja = render ulang.
- Kolom: tiap kolom punya lebar sendiri; teks wrap di dalam kolomnya.
  Gutter antar kolom minimal 120px. Subtitle/judul kolom tidak boleh
  menyebrang ke kolom sebelah.

## 3. Satu ide per slide
- Maksimal 2 diagram batang per slide. Kalau konten tidak muat, PECAH
  SLIDE (7-8 slide tidak apa-apa), jangan perkecil teks atau memadatkan.
- Diagram batang: track selebar penuh konten, label sumbu (0% / 100%)
  sejajar ujung track, tinggi baris dan jarak antar baris konsisten,
  kolom nilai lebar tetap.
- Maksimal 3 ukuran teks per slide. Skala tetap di semua slide:
  headline, subtitle, judul kartu, body, caption kaki.

## 4. Ritme vertikal
- Jarak headline ke blok konten pertama maksimal 300px. Tidak boleh ada
  ruang kosong mati lebih dari 300px di tengah slide.
- Sisa ruang kosong dibagi rata (atau konten rata atas dengan jarak
  antar blok konsisten), jangan menumpuk semua di satu sisi.

## 5. Konsistensi
- Warna model di legenda SAMA di semua slide dan reel.
- Kartu-kartu dalam satu grid: radius, border, dan aksen yang sama.
- Judul slide: satu baris bila memungkinkan; subtitle maksimal 2 baris.

## 6. QA gate (wajib sebelum diserahkan)
- Cek visual tiap slide di preview 768px DAN zoom full-res pada area teks.
- Cek programatik: tidak ada teks keluar kartu, tidak ada bounding box
  bersinggungan, tidak ada teks menabrak nomor halaman/footer.
- Angka benchmark dicek ulang lawan fakta terverifikasi.
- Ada satu temuan saja: perbaiki rendernya, jangan serahkan.
