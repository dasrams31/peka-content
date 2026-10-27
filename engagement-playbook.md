# Peka Engagement Playbook

Goal: every Peka post is engineered to earn likes, comments, saves, shares,
and follows, in line with how the IG / Threads / FB algorithms rank content.
Read this file at the START of every Peka content run, together with
learnings.md (data-driven lessons) and performance.log (raw metrics).

## How the algorithms weigh things

- Meaningful interaction beats passive likes. Rough weight order:
  share > save > comment > like. Design posts that are easy to SAVE
  (dense info, cheat sheets, lists) and easy to SHARE (useful or relatable
  for someone else, not just the reader).
- Carousels: the more people swipe to the last slide, the wider the
  distribution. Slide 1 is a promise, middle slides deliver, last slide
  carries the CTA and a reason to follow.
- The first hour matters. Strong first-line hook, and questions that are
  trivial to answer, get the conversation started.
- Fixed daily slots (09:36 news, 19:00 store, 21:30 spill) train both the
  audience and the algorithm. Never post two series in the same slot.
- Links do NOT go in the Threads post body (reach drops); links live in
  the first reply/comment, which is already the SPILL format. On IG,
  caption links are not clickable: point to the blog and the comments.

## Caption anatomy (every pillar)

1. Line 1 = HOOK (max ~60 chars). Pick one pattern:
   - specific number ("5 repo, 300 ribu star")
   - a question the reader feels ("Agent AI kamu masih gitu-gitu aja?")
   - a bold but TRUE claim ("Bukan modelnya yang bikin agent pinter")
   - a common mistake ("Kebanyakan orang install skill asal comot")
   - a curiosity gap ("Yang nomor 3 yang paling kepakai, ternyata")
2. Body: short lines, one idea per line. No walls of text.
3. Close with exactly ONE interaction trigger (rotate them):
   - opinion question that is easy to answer ("Kalau kamu, tim mana?")
   - experience ask ("Ada yang udah coba? Ceritain di komentar.")
   - tag a friend who needs it (bansos / store posts)
   - save trigger ("Save dulu, ilmunya kepakai nanti")
   - follow trigger for series ("Edisi #NN besok jam 21:30, follow biar nggak ketinggalan")
4. FORBIDDEN: fake clickbait, invented numbers/testimonials, cheap
   engagement bait ("like kalau setuju"), rage bait on SARA or party
   politics. Honest urgency only.

## Model bahasa (standing order from the user, 2026-10-26)

Selalu pakai bahasa santai kayak ngobrol, di SEMUA konten Peka:
caption, teks slide, teks reels, dan copy lainnya. Referensi:
caption revisi tools-launch 26 Okt 2026
(peka-content/tools-launch/out/2026-10-26/caption-*.txt).

- "udah" (bukan "sudah"), "sampe" (bukan "sampai"), "kalo"
  (bukan "kalau"), "sama" ganti "dan" di daftar, "nggak"
  (bukan "tidak"). Subjek sering dibuang, kalimat pendek.
- DILARANG bahasa kaku gaya siaran pers ("sudah live", "berisi",
  "dilengkapi dengan", "dapat dilakukan", kalimat pasif panjang).
- Aturan lain tetap berlaku: tanpa em-dash/en-dash, Threads tepat
  1 #AI, angka jujur, satu pemicu interaksi per caption.

## Bahasa awam lembut (standing order from the user, 2026-10-28,
  berlaku untuk SEMUA konten Peka ke depan, melengkapi model bahasa
  26 Okt; contoh acuan: carousel + reels Huashu Design gaya Japanese,
  di-ACC 28 Okt 02:03 WIB)

Kalimat harus langsung dimengerti orang awam, pendek, dan tidak
terasa maksa. Perintah keras diganti ajakan bersyarat:
- Judul dan ajakan pakai kalimat biasa, bukan teriakan perintah:
  "Ketik satu kalimat, jadi desain." bukan "SATU KALIMAT. JADI
  DESAIN."; "Follow, kalau kamu suka." bukan "FOLLOW DAN GABUNG."
- Ajakan follow/grup/save selalu bersyarat dan santai: "kalau
  kontennya kepakai", "kalau mau ngobrol", "Save dulu, biar
  gampang dicari lagi." (di sini "kalau" dipakai utuh, bukan
  "kalo", supaya ajakannya terasa lembut, bukan perintah singkat).
- Jargon teknis diterjemahkan ke bahasa awam, tanpa mengubah fakta:
  star -> "Disukai 27 ribu orang", MIT -> "Gratis", thumbnail ->
  "contoh", prototipe -> "contoh App", diedit -> "diubah",
  "skill desain buat agent AI" -> "Kamu ketik, dia yang gambar.",
  "bukan mockup" -> "Ini contoh hasil aslinya. Bukan gambar
  tempelan, ini beneran jadi."
- Pertanyaan penutup tetap tepat satu, dengan nada santai:
  "Kamu pengin bikin apa dulu? Web, App, atau PPT? Coba komen ya."

## Per platform

- Threads: replies are king. End with a question (before the single #AI
  hashtag), and make our own first reply carry extra value (links, extra
  fact). Exactly 1 hashtag #AI stays mandatory.
- Instagram: saves and shares weigh most. Every carousel ends with a CTA
  slide. 5-10 relevant hashtags, no spam. Sales posts stay OFF Instagram.
- Facebook: native carousel + a question; when replying to comments, end
  the reply with a follow-up question so the thread keeps living.

## Per pillar

- HM news: close the caption with a light two-sided debate question about
  the story ("Menurutmu ini kemajuan atau ancaman buat kerjaan kita?").
  Never on SARA or party-political fights.
- Store (jualan): comment trigger is the DM keyword ("DM MAU [produk]")
  plus a low-effort choice question ("Tim bulanan atau tahunan?") and a
  tag-a-friend line. Honest stock/price urgency only.
- SPILL Repo: close with "Repo mana yang mau kamu coba duluan?" and invite
  the audience to spill their own favorite repo in the comments (best ones
  can become a community edition). Series number in the caption + follow
  trigger, because numbered series build appointment viewing.
- Bansos: tag a friend + save trigger (deadlines) + "Ada yang udah
  berhasil daftar?" experience ask.

## After posting / weekly loop

- Every post goes to posted.log (already standard) so the weekly review
  can find it again.
- Weekly review cron (peka-engagement-review, Sunday 20:00): pull
  like/comment/share metrics for the last 7 days of posts from whatever
  the platform CLIs expose, append the numbers to performance.log,
  distill 1-3 lessons into learnings.md (OBSERVED / INFERRED format),
  and report the top 3 and bottom 3 posts to the chat. Never invent
  metrics the CLI does not expose; say which platform data was missing.

## Improvisation mandate (standing order from the user, 2026-10-20)

The user wants this system to keep improvising on its own so content
follows trends and keeps earning comments, likes, saves, shares, and
follows. Standing rules:

- Read trending.md (same folder) at the start of every run. It is
  refreshed twice a week (Mon + Thu) by the peka-trend-watch cron with
  what is currently working in the AI niche: hot topics, formats, and
  hook styles, plus 2-3 concrete experiments for the week.
- Every run MAY run ONE experiment: a new hook pattern, a format twist
  inside the locked design system, a new question style, a trend tie-in.
  Log the experiment in the run's posted.log line or report so the
  weekly review can judge it.
- Experiments may NEVER break locked rules: brand designs and lockups,
  the single #AI hashtag on Threads, the no em/en-dash rule, honest
  numbers only, fixed daily slots, sales posts off Instagram.
- The weekly review promotes winning experiments into this playbook and
  learnings.md, and kills losing ones. That loop is the improvement
  engine: trend watch feeds ideas, daily runs test them, Sunday data
  decides what stays.

## ATURAN JOIN KOMUNITAS DI DESAIN (2026-10-21, perintah user)
- SEMUA desain konten Peka WAJIB memuat elemen join komunitas ke **url.peka.ai.id** (halaman hub semua link + komunitas).
- Sudah tertanam di generator: hm/designer.py footer (pola seragam semua desain: tulisan web peka.ai.id DIHAPUS dari footer, diganti kalimat "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID" abu-abu regular di kiri, nomor halaman di kanan; semua slide berita + edisi khusus), buzzer_design social_row (teks web = url.peka.ai.id), spill/spill.py footer (pola sama), prompt/prompt_harian.py (strip slide 1: CTA dipendekkan "GESER BUAT PROMPTNYA" + kalimat gabung kanan; footer slide 2 ringkas), bansos/bansos_design.py (stub tiket tanpa peka.ai.id: "gabung ke / komunitas kami: / url.peka.ai.id" + CTA slide 3 "Gabung ke komunitas kami: url.peka.ai.id"), store/make_slides.py footer (pola sama).
- Desain baru di luar generator ini: tambahkan elemen setara (kecil, rapi, tidak mendominasi desain) sebelum tayang.
- BARIS SOSMED SLIDE PENUTUP/BUKTI (2026-10-22, perintah user): baris bawah di slide penutup dan bukti edisi khusus (buzzer_design.social_row) = ikon platform (IG/FB/Threads) TETAP ADA, teksnya cukup "peka.ai.id" TANPA awalan "url." — berlaku untuk semua edisi khusus (buzzer, metaai, warganet, dan berikutnya).
- AUDIT BENTROK FOOTER (2026-10-22, perintah user): footer teks mulai di y=1015 (skala 1080); tombol GESER (tinggi 78) AMAN maks di y=918 (bawahnya 996). Warganet cover awalnya 942 = bentrok, sudah diperbaiki ke 912 + jendela SS dipendekkan. Store footer: label edisi panjang menabrak "HAL i/n", sudah diperbaiki dengan auto-shrink font (36 turun bertahap sampai muat). Cover HM tema MAJALAH dan TERMINAL memang TANPA kalimat gabung (di majalah tombol GESER-nya di 950 dan ruang bawahnya penuh; di terminal ada ticker) — kalimat gabung tetap ada di slide detail + penutup kedua tema itu. Tema frame, koran, layar, bansos, spill, prompt, buzzer/metaai terverifikasi bersih lewat render contoh.

## ATURAN REELS SAJA DI IG + FB (2026-10-27, perintah user, MENGGANTIKAN dual-versi 2026-10-25)

Mulai sekarang, konten Peka di IG dan FB tayang REELS SAJA, tanpa
versi carousel/feed post lagi:

- Versi REELS: MODEL ANIMASI (perintah user 2026-10-25, berlaku
  untuk FB, IG, dan TikTok). Reels adalah motion-graphics beneran:
  elemen bergerak di dalam scene (headline stagger, badge pop, bar
  tumbuh, gambar geser masuk), BUKAN slideshow dan BUKAN Ken Burns.
  Pipeline: desain HTML/CSS vertikal + render frame per frame
  (Playwright, window.renderAt(t), 24fps) lalu ffmpeg + musik.
  Template pertama: peka-content/hallmark/animated/ (scene.html +
  render.py, mendukung scale 1.3333 untuk 2K). Template per pilar
  lain dibangun mengikuti pola yang sama.
- Resolusi reels: 2K 1440x2560 (perintah user 2026-10-25), yuv420p,
  cover dari frame detik ke-1. Slideshow lama (make_reel.sh) hanya
  jadi fallback kalau render animasi gagal, supaya slot tidak kosong.
- FYP (FB + IG + TikTok): hook visual dalam 3 detik pertama, durasi
  15 detik (bagus buat completion rate), TEPAT SATU pertanyaan
  penutup, ajakan save, hashtag relevan per platform (IG 5-10,
  TikTok campur #fyp + niche, FB tanpa hashtag), dan ending yang
  nyambung kalau di-loop. TikTok: file yang sama dipakai manual oleh
  user; kalau mau kejar audio trending, mute musik file di aplikasi
  dan pakai sound trending (musik bawaan tetap CC-BY dan aman).
- ATURAN COPY (perintah user 2026-10-25, berlaku ke depan): kata
  "mesin" diganti "AI" di semua copy Peka. Tulis "terjemahan AI"
  dan "buatan AI", bukan "terjemahan mesin" atau "buatan mesin".
- SLIDE/Scene PENUTUP FOLLOW + KOMUNITAS (perintah user 2026-10-25,
  berlaku ke depan): setiap carousel ditutup satu slide "Follow dan
  gabung" (Follow @peka.ai.id di IG/Threads/TikTok + gabung grup WA
  lewat url.peka.ai.id + save/share), dan setiap reels ditutup satu
  scene yang sama. Sudah diterapkan di template SPILL dan spotlight
  naskah-id; generator pilar lain (HM, Prompt, Store, Bansos,
  Gratisan) menyusul retrofit yang sama.
- IG: post-feed 1 file MP4 + cover = Reels saja, TANPA carousel.
- FB: pages posts create dengan MP4 TERBIT SEBAGAI REEL (terverifikasi
  2026-10-25: URL facebook.com/reel/), jadi FB hanya dapat reel post,
  TANPA carousel post.
- Musik: CYBERPUNK, BEDA TIAP REELS (perintah user 2026-10-25).
  Semua reels ke depan pakai lane cyberpunk saja (9 track CC-BY
  Kevin MacLeod di brand/music/CYBERPUNK_TRACKS.txt: Aitech,
  Mechanolith, Oppressive Gloom, Volatile Reaction, Crypto,
  Tech Live, Black Vortex, Vortex, Darkling). Tiap render reels
  panggil SATU KALI ~/workspace/peka-content/brand/music/pick_reel_track.sh
  (counter persisten + flock, jadi reels berurutan selalu beda lagu
  sampai lane 9 lagu itu muter penuh). IG dan FB mempublish file
  yang sama, jadi satu pick per konten, bukan per platform.
  Kredit "Music: <Judul> by Kevin MacLeod" ditulis di caption reel
  (judul = nama file tanpa "-kevin-macleod.mp3", dash jadi spasi,
  title case). Jangan pakai musik berhak cipta lain. Lagu ceria lama
  (Carefree, Cheery Monday, dst) sudah pensiun dari rotasi reels.
- Caption reel: gaya FYP, hook keuntungan pembaca + catatan jujur
  (deadline, syarat) + ajakan save + TEPAT SATU pertanyaan + hashtag
  relevan (IG) / tanpa hashtag (FB) + kredit musik.
- Threads TIDAK berubah: tetap carousel/teks seperti biasa, tidak ada
  reels lewat tools.
- Carousel/slide tetap diproduksi sebagai bahan reels + untuk Threads +
  blog, tapi TIDAK diposting ke IG/FB.
- Pilar yang belum punya pipeline reels animasi memakai fallback
  slideshow (make_reel.sh) yang disebut di laporan, sampai reels
  animasinya dibangun; carousel TIDAK diposting ke IG/FB.
- Catat media id/link reels (IG/FB) + carousel (Threads) di posted.log
  dan laporan run.
- CARVE-OUT yang tetap berlaku: (1) Pancingan adalah pilar teks-only
  tanpa IG, tetap teks di Threads + FB saja, tidak dibuatkan reel.
  (2) Jualan (Store/Spotlight) TETAP TIDAK KE IG (aturan 2026-10-20):
  untuk jualan, FB hanya reels (tanpa post carousel), dan
  Threads seperti biasa. Aturan reels-saja ini TIDAK membatalkan
  larangan jualan di IG.
  (3) PROMPT HARIAN + GRATISAN AI (pilihan user 2026-10-27, opsi 2):
  kedua pilar ini TETAP CAROUSEL di IG/FB sampai pipeline reels
  animasi masing-masing dibangun, baru pindah ke reels-saja.
  Pengecualian ini mengalahkan baris fallback slideshow di atas
  untuk kedua pilar ini: jangan pakai slideshow fallback, jangan
  tahan tayangannya menunggu reels. Cron peka-prompt-harian dan
  peka-gratisan-ai sengaja TIDAK diubah selama pengecualian ini
  berlaku.
- Berlaku untuk edisi BARU mulai perintah ini, bukan backfill edisi
  lama, kecuali user minta backfill eksplisit.

## ATURAN DARI DATA (2026-10-23, dikunci user)

Tujuh aturan ini hasil analisis angka nyata akun ini (Oracle 13.994 views vs Tencent 0 views di hari yang sama) dan WAJIB dipatuhi semua cron konten:

1. **DILARANG hapus + repost konten mirip dalam waktu dekat.** Konten yang sudah tayang diperbaiki lewat balasan/komentar, bukan recreate. Revisi besar dilakukan SEBELUM posting.
2. **Hook = keuntungan pembaca, bukan berita tentang brand.** Pengumuman brand (kantor, fitur, milestone) adalah konten komunitas: distribusi utamanya grup WhatsApp dan follower setia, bukan target reach.
3. **Utamakan topik dengan langkah nyata dan titik bingung** (orang mencoba lalu bertanya) karena replies adalah bahan bakar distribusi Threads. Pertanyaan pemicu harus lahir dari pengalaman mencoba, bukan opini generik.
4. **Topik dua sisi (dua versi cerita) adalah format pemancing komentar yang terbukti.** Pertanyaan generik tipe "gimana menurutmu" terbukti menghasilkan 0 komentar; jangan jadikan pemicu utama.
5. **Keputusan berbasis snapshot laporan harian 22:30**, bukan angka menit awal (metrik Threads telat dan berbatch). Tidak ada keputusan hapus/revisi sebelum ada snapshot beberapa jam.
6. **Jam posting bukan penentu.** Kekuatan tawaran dan caption mengalahkan jam tayang; jangan menggeser jadwal demi mengejar jam ramai.
7. **Nilai per platform dengan ukurannya sendiri:** IG = likes + saves, Threads = replies + reposts, FB = reactions + shares. Satu angka dari satu platform tidak memvonis konten.
