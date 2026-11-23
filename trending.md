# Peka Trending Watch

Refreshed twice a week (Mon + Thu 08:15 WIB) by the peka-trend-watch cron.
Every content run reads this file (via the engagement playbook) and may
test ONE experiment from the list below. The Sunday engagement review
judges the experiments from real metrics.

## Current evergreen formats (baseline, until trend data replaces them)

- Save-worthy carousels: cheat sheets, prompt packs, repo lists. Saves
  and shares are the strongest ranking signals we can earn.
- Numbered daily series (SPILL Repo, Prompt Harian) build appointment
  viewing and follow intent: always state the next edition time.
- Questions that are trivial to answer outperform open-ended ones.
- Threads rewards reply chains: our own first reply carries the value
  (links, the full prompt), the main post carries the hook.

## Experiments this week (refresh 2026-11-23)

Three experiments, one variable each. All three are CAPTION level on purpose: the last four refreshes lost every slot experiment that needed a NEW slide layout, because the generator aired the standard slide instead (Prompt before/after 13 Nov, SPILL comparison slide 13 Nov, HM try-it VOID three times), and the 16 Nov set lost both topic-locked designs the same way (see archive). Do NOT design an experiment that needs a slide the generator has never built, and do NOT design an experiment that needs one specific news topic to air. The run that airs an experiment MUST write its exp marker into its posted.log line the same day, with the exact theme that aired. If the aired theme differs from the design, the experiment is VOID, not a result, and the variable is not re-proposed. No experiment may break a locked rule: brand design, exactly 1 closing hashtag per tag-watch.md, no em-dash or en-dash, honest numbers only, fixed slots, no sales posts on IG, no link in any post text. This week is SHORT: libur 26-29 Nov, so all three slots fall 23-25 Nov. Judged by the first Sunday review after libur.

1. Coba Dulu hook hasil-dulu (slot Senin 23 Nov 17:00, debut seri, marker "exp: coba-dulu-hasil-dulu"). VARIABLE: baris pertama caption adalah hasil jujur percobaan ("Aku coba X gratis, hasilnya Y dalam Z menit") bukan nama tool atau janji manfaat. Caption lain tetap standar reel-v2 (isi mandiri + satu pertanyaan pilihan paksa + kredit musik). WHY: seri debut, belum ada kontrol sendiri; FYP 23 Nov: story 30% di TOP vs question 17%, dan baris pertama yang membawa hasil konkret + angka spesifik adalah bentuk cerita yang paling dekat dengan pola menang. HYPOTHESIS: Threads views >= 212 (median Prompt Harian, keluarga caption cerita yang sama) dan minimal 1 balasan penonton. CONTROL: Prompt Harian median Threads 212 views. Guardrail: hasil harus dari percobaan beneran hari itu (seri ini memang coba beneran); jangan klaim hasil yang tidak terjadi. If the hook line names the tool first instead of the result, mark VOID.

2. Tanya Jawab Nyata buka kutipan asli (slot Selasa 24 Nov 17:00, debut seri, marker "exp: tanya-jawab-kutipan-asli"). VARIABLE: caption root dibuka kutipan persis pertanyaan penonton (1 kalimat, dalam tanda kutip) sebelum ringkasan jawaban, bukan parafrase redaksi. WHY: pertanyaan nyata dalam suara penanya sendiri terbaca sebagai cerita/pengakuan, bukan pertanyaan generik (pertanyaan generik cuma 17% di TOP 23 Nov vs story 30%); ini juga yang membedakan seri ini dari Prompt Harian. HYPOTHESIS: minimal 1 balasan penonton dan Threads views >= 212. CONTROL: Prompt Harian median Threads 212 views. Guardrail: kutipan harus kata-kata asli penanya (dari sumber pertanyaan nyata yang dipakai edisi itu); jangan karang kutipan. If the opener is a paraphrase instead of a quote, mark VOID.

3. Komik Peka #03 pengakuan-opener (slot Selasa 25 Nov 19:00, marker "exp: komik-pengakuan-opener"). VARIABLE: baris pertama caption adalah pengakuan relatable dari tokoh komik ("Aku kira ..., ternyata ...") bukan hook topik. Caption lain tetap standar (isi mandiri + satu pertanyaan pilihan paksa). WHY: Komik #02 sudah dapat 1 balasan penonton (@hannqeerty), pertama di seri ini; FYP 23 Nov story 30% di TOP. HYPOTHESIS: minimal 1 balasan penonton (ulangi #02) dan Threads views kalahkan kontrol #02. CONTROL: Komik #02 Threads 1 like / 81 views (snapshot) / 87 views (24j), 1 balasan penonton. If the first line is a topic hook instead of a confession, mark VOID.

NOT re-proposed: SPILL first-reply 5-minute challenge (VOID 19 Nov, balasan pertama tidak pernah tayang). Variabelnya masih belum teruji, tapi jangan ajukan ulang sebelum ada gate eksekusi: run yang mengusulkan wajib grep file balasan pertama dan memastikan baris tantangan ada SEBELUM posting; tanpa bukti itu, variabel tetap parkir. Slot SPILL minggu ini (23, 24, 25 Nov 21:30) jalan dengan pola #11 standar.

## Hot topics (refresh 2026-11-23)

Corrections to the 19 Nov refresh. Anthropic IPO sudah tayang sebagai HM 22 Nov (IG 1 like / 48 views, datar, jangan ulangi sudut IPO). Klaim Riemann sudah tayang sebagai HM 21 Nov ("Claude buktikan hipotesis Riemann", IG 4 likes 24j); sudut yang tersisa adalah verifikasi + lomba manusia vs AI (topik 1 di bawah), bukan klaimnya lagi. Gemini 4 Neon dan GPT-6.2 Astra/Sol sudah tayang di blog sebagai edisi khusus; sudut yang tersisa adalah debat pindah model + perang harga (topik 2). Gemini 4 Carbon intro pricing $2/$10 berakhir 30 Nov, lalu naik ke $4/$20.

1. Klaim Riemann belum terverifikasi, dan bukti manusia muncul di hari yang sama. Matematikawan Anthropic Levent Alpoge bilang Claude membantunya membuktikan hipotesis Riemann (20 Nov), bukti formal Lean 250.000 halaman, progres pengecekan publik 99%, arsip 228 MB, tapi belum diverifikasi matematikawan independen. Di hari yang sama Ravi Vakil memposting bukti Generalized Riemann Hypothesis tulisan manusia (Alessandro Masullo, Stanford), dan Alpoge + Tristan Buckmaster merilis klaim bukti Navier-Stokes (79 halaman, sekitar 600.000 baris Lean). Postingan #AI teratas 23 Nov membahas ini (1.241 likes). Angle for Peka: HM debat dua sisi "bukti 250 ribu halaman, siapa yang ngecek?" + SATU langkah coba konkret (cek progres pengecekan Lean di situs publik). Guardrails: labeli KLAIM di semua copy, bukan "terbukti"; jangan sebut hadiah $1 juta seolah sudah dimenangkan; HM tetap freeze di Threads sampai 7 Des, jadi IG + FB + blog saja.

2. Perang harga model murah, pindah model jadi perdebatan. GPT-6.2 Astra 20% lebih murah dari pendahulunya ($8/$40 per juta token), Gemini 4 Neon $3/$15 dengan skor AA Index 61 (peringkat 3, di atas Opus 5.5 skor 59 dan Sol 57), MAI Code 2 klaim 96% kualitas coding Opus 5.5 dengan 5% harga, Qwen4-Max konteks 1 juta token. V2EX terpanas: "pakai GPT-6.2 langsung batal langganan pindah ke Gemini" (54 balasan). Angle for Peka: Bandingin Model debut Selasa 24 Nov 10:30 (sudah terjadwal, reel-v2 navy-tech) + reel benchmark ekstra bila ada angka perbandingan; sudut "pindah atau bertahan?" dengan pertanyaan pilihan paksa. Guardrails: semua angka adalah klaim vendor, labeli begitu; verifikasi di pengumuman resmi hari pakai; jangan jadikan satu model pemenang mutlak.

3. AI lokal di laptop makin gampang, dan itu sudut menang akun ini. Thinking Machines rilis Inkling 2 Mini 20 Nov (26,4 miliar parameter, 3,4 miliar aktif, dirancang jalan di laptop); Hacker News front page 23 Nov: panduan local AI pakai Qwen + Unsloth (173 points). BLUEPRINT #03 Ollama menang besar 20 Nov (Threads 51 likes / 4.590 views, 7 balasan penonton, 9 follows) dengan sudut gratis + lokal. Angle for Peka: BLUEPRINT lanjutan sudut gratis-lokal (slot berikut 4 Des, karena 27 Nov libur) atau SPILL repo local-AI dengan hook stack + angka resmi. Guardrails: verifikasi repo dan angka di hari pakai; jangan klaim "jalan di laptop apa pun" tanpa cek kebutuhan minimum.

4. Black Friday AI dan deadline yang makin dekat. V2EX terpanas minggu ini: promo Gemini Black Friday 1 tahun 100 yuan (80 balasan, plus kekhawatiran akun kena ban). Google AI Plus buat mahasiswa masih dibuka sampai 31 Des 2026 (38 hari lagi dari 23 Nov), perpanjang Rp75.000/bulan bila tidak dibatalkan; carousel ambassador Google AI Plus masih ramai di IG. Gemini 4 Carbon harga intro berakhir 30 Nov. Angle for Peka: Gratisan atau Bansos "mana yang gratis beneran" dengan harga perpanjang jujur di caption (praktik menang 11 Nov); kandidat Gratisan Mahasiswa debut 3 Des. Guardrails: verifikasi tiap promo di sumber resmi hari pakai (harga Black Friday beda tiap region); patuhi bar seleksi Bansos (gratis permanen atau minimal 1 bulan); jangan janji promo tanpa sumber.

5. Gelombang skripsi AI Indonesia masih panas. Bukti segar: workshop gratis "Skripsi 1 Bulan Kelar Pakai AI?" 5 Des (100 pendaftar pertama, Educativa x KelasRiset); promo SkripsiLab AI di Threads; reel Telkom Open Library (cara akses jurnal Scopus gratis, 520 likes, 21 Nov); studera.ai membandingkan 29 app AI buat belajar (17 Nov, Gemini Notebook dan Pelajarin.ai nilai tertinggi 4,3). Angle for Peka: Gratisan Mahasiswa debut 3 Des + Prompt Harian checklist skripsi ("AI buat skripsi, mana yang gratis beneran"). Guardrails: framing kejujuran akademik tetap (AI itu asisten, bukan penulis skripsi); sebut batasan gratis tiap tool; jangan janji "skripsi selesai 1 hari".

Carried, still true and still not aired: Gemini Decision 1 (11 Nov, model keputusan pertama Google, $0,10 per juta token input, sampai 1.000 pertanyaan per request): kandidat HM singkat atau BLUEPRINT, verifikasi di halaman Google hari pakai. Claude Meetings, Sheets, Whiteboards, Data (beta, 10-11 Nov) plus konektor Adobe, Atlassian, Box; Businesses in ChatGPT (beta, 10 Nov); Claude for Manufacturing (12 Nov, 17 workflow skills); Claude Managed Agents self-hosted private beta (12 Nov). GitHub Copilot pensiunkan beberapa model Claude dan GPT (16 Nov): kandidat SPILL atau Prompt Harian praktis, verifikasi daftar model di changelog GitHub hari pakai. Agent AI yang jalan sendiri (California gugat OpenAI 17 Nov; ChatGPT Wallet AS saja; Perplexity Multiagent sampai 16 agent): kandidat HM debat dua sisi, verifikasi di sumber primer hari pakai, jangan klaim Wallet tersedia di Indonesia. Images 2.6 GIF (4 Nov, gratis di semua paket; dua kali VOID sebagai eksperimen karena topik tayang bukan Images 2.6, jadi jangan ajukan lagi sebagai eksperimen slot, tapi tetap layak jadi topik HM biasa bila ada slot kosong). The shared robots.txt token "__usage_ai-training" (Hot topic 5, 5 Nov refresh) is still a draft with staggered timelines and nobody honors it yet as of 3 Nov; keep for a future HM slot only if a concrete reader step exists, do not force it. Mistral Large 4 "Le Chonk" (1T parameter, open weights, klaim coding terkuat open-weight), Cursor Live Apps (deskripsi jadi app live dengan database), dan Google Canvas (sketsa tangan jadi app jalan) jadi kandidat SPILL atau BLUEPRINT; verifikasi repo dan angka di hari pakai. Meta Muse Ember 1.0 (9 Nov, model kecil buat subtask agent, $0,10 per juta token input) jadi latar, bukan topik utama. DeepSeek harness dan gelombang open-weight coding sudah dicover Komik Peka #02 yang tayang 22 Nov; jangan ulangi sebagai HM.

Format note, still winning: checklist and self-score formats keep winning in the student wave (steps, checklists, boleh vs tidak-boleh, red flags vs green flags, this-or-that) because they give the reader a score or a side to pick. Format perbandingan dua kolom (X vs Y, sebelum vs sesudah) bergabung sebagai format menang, dibuktikan reel IPK 3 vs Cum Laude 2,8 ribu likes (11 Nov) dan reel benchmark HM Hydrogen 13 Nov (IG 23 likes / 1.817 views). Format TIER-LIST / ranking (S/A/B/C/D) menang di niche mahasiswa Indonesia (reel 3,3 ribu likes 11 Nov, FB reel 2,3 ribu likes); format DAY-COUNTER ("DAY 1: ...") MATI di TOP (0% TOP 23 Nov, turun dari 4-8% seminggu sebelumnya; top post #AI "DAY 1: Mecut AI" 3.445 likes masih bertahan tapi tidak naik). Story makin dominan di TOP (30% 23 Nov, naik dari 25%); question cuma 17% di TOP vs 36% di REST, jadi pertanyaan generik tetap kalah. TOP posts 23 Nov rata-rata 40 kata dan 1,7 hashtag. Tag-watch 23 Nov: #AI median likes 131 (n=13) di atas #Kuliah median 95 (n=9); tag penutup tetap #AI karena kunci manual user 6 Nov. Postingan #AI teratas 23 Nov: Apple "missed AI" bubble (2.194 likes); #Mahasiswa teratas: cerita intro personal (20.372 likes), bukti story/pengakuan masih yang terkuat. Format listicle bernomor ("8 AI gratis...") dan reel janji besar ("TOP AI buat skripsi selesai 1 hari") masih jalan di niche mahasiswa, tapi jaga guardrail kejujuran akademik dan jangan tiru janji "1 hari". Copy the comparison and ranking structures inside the locked design system and the two-sided pick-a-side close where the playbook allows it. Do NOT turn a complaint thread into a claim about a vendor's pricing without an official source.

## Moments and calendar to ride this week

- 23 Nov: trend watch refresh 08:15 (this file); Prompt Harian 12:30; Coba Dulu debut 17:00 (experiment 1 slot); SPILL 21:30.
- 24 Nov: Bandingin Model debut 10:30; Tutorial Mirror 15:36; Tanya Jawab debut 17:00 (experiment 2 slot); SPILL 21:30.
- 25 Nov: Hari Guru Nasional. Same rule: note only, no forced content. Prompt Harian 12:30; Coba Dulu 17:00; Komik Peka #03 19:00 (experiment 3 slot); Bansos Altare 20:00; SPILL 21:30.
- 26-29 Nov: LIBUR (27 job konten + bot off, kembali 30 Nov 06:00). No slots, no experiments.
- 29 Nov 10:00: Kiro Pro cancellation reminder, first bill $20 on 1 Dec.
- 30 Nov: libur ends 06:00; Gemini 4 Carbon intro pricing ends ($2/$10 naik ke $4/$20).
- 3 Des: Gratisan Mahasiswa debut 14:00.
- 5 Des: workshop skripsi gratis (Educativa x KelasRiset, 100 pendaftar pertama).
- 7 Des: HM Threads freeze ends, Threads HM kembali normal mulai edisi 8 Des tanpa perintah baru.
- 17 Des: Gemini Gems deleted permanently (read-only since 17 Nov).
- 31 Des 2026: Google AI Plus student claim deadline (38 hari dari 23 Nov).
- Ongoing locks: jualan FROZEN, Pancingan OFF, giveaway ON HOLD, HM freeze on Threads 7 Nov to 7 Dec (IG, FB, blog, and channel still air), all with no new date until the user says otherwise. No link in any post text on any platform; the edition link lives printed inside the visual as an admin-owned s.peka.ai.id shortlink, with one instruction sentence in the caption. Every new external link goes through s.peka.ai.id first; if shortening fails, STOP before posting. SPILL on Facebook stays one format per edition, default carousel.

## Archive (experiments judged by Sunday review)

Judged Sun 2026-11-22 (weekly review, fresh CLI metrics 22 Nov ~20:00 WIB;
pillar medians this week: SPILL Threads 12 likes / 604 views, IG 15 likes /
711 views; Prompt Threads 5 likes / 191 views; HM IG 2,5 likes / 58,5 views;
Bansos Threads 7 likes / 257 views; Gratisan Threads 14 likes / 635,5 views;
Tutorial Mirror Threads 3,5 likes / 151,5 views; BLUEPRINT #03 51 likes /
4.590 views):

- SPILL first-reply 5-minute challenge (slot 19 Nov 21:30, edisi #30):
  TIDAK JALAN / VOID. Balasan pertama berisi tantangan 5 menit TIDAK PERNAH
  tayang: `fetch-post-comments` root #30 (id 17875021917648704) total_count 0,
  tidak ada teks tantangan di folder out edisi, tidak ada marker exp di
  posted.log. Angka root #30 (Threads 12 likes / 246 views, IG 10 likes /
  505 views) tidak menguji hipotesis. Variabel belum teruji; jangan ajukan
  ulang desain slot yang sama tanpa memastikan balasan pertama benar-benar
  dibangun + terkirim sebelum dinilai.
- HM try-it step as the hook line (slot 20 Nov 09:36, IG + FB + blog):
  VOID. Hook caption IG yang tayang (media Df8ndq5j38U) adalah headline
  berita biasa ("Apple lagi bikin agen AI yang bisa menjalankan Mac kamu
  sendiri."), bukan langkah coba konkret; blok COBA SEKARANG di badan caption
  pun hanya persiapan ("catat 3 tugas berulang"), bukan eksekusi di tool.
  Angka (IG 2 likes / 34 views, Threads 1 like / 47 views) tidak menguji
  hipotesis. VOID kelima beruntun buat desain slot HM; jangan ajukan ulang
  desain slot yang sama tanpa memastikan hook benar-benar ditulis sebagai
  langkah coba sebelum tayang. Pelajaran yang dipetik dicatat di learnings.md
  22 Nov: COBA SEKARANG wajib langkah yang bisa dieksekusi, bukan persiapan.
- Gratisan AI free-vs-paid comparison caption (slot 21 Nov 14:00,
  JetBrains Student Pack): MENANG PARSIAL. JALAN sesuai desain (caption
  Threads memuat "Gratis dapat completion + trial AI chat dan agent. Pro
  $10/bulan dapat 10 kredit AI/bulan + Junie, Claude Agent, Codex." +
  "Tim gratis atau tim Pro?"). Threads 6 likes / 398 views, 2,5x kontrol
  Gamma (162 views), hipotesis views TERPENUHI; tapi 0 balasan penonton,
  hipotesis balasan GAGAL, dan views tetap di bawah target pilar 562 serta
  jauh di bawah Figma (873) dan AI Plus (1.619). Verdict: perbandingan
  gratis-vs-berbayar mengangkat views di atas kontrol lemah tapi bukan
  pendongkrak reach dan tidak menarik balasan. Dipromosikan ke playbook
  Gratisan sebagai varian caption OPSIONAL (bukan pengganti seleksi tawaran:
  segmen mahasiswa + nama besar + tawaran besar tetap didahulukan).

Checked 2026-11-19 (trend watch refresh, from posted.log and
performance.log; Sunday review 22 Nov 20:00 confirms the verdicts):

- Prompt Harian day-counter opener (slot 17 Nov 12:30, edisi #27):
  NOT RUN. Caption #27 aired with the story opener ("Deskripsi produk
  yang bikin pembeli langsung checkout", Threads 174 views, 8 likes,
  8 reposts); posted.log records "exp: prompt-day-counter NOT RUN
  (desain ganti pembuka cerita, bentrok aturan terkunci)". The variable
  conflicts with the locked story-opener rule (won 8 Nov), so it cannot
  run as a replacement opener in this slot design. Do not re-propose
  the same design. A day-counter SERIES LABEL that keeps the story
  opener intact is a different variable and may be proposed fresh.
- HM two-sided provocation "AI udah mentok?" (slot 18 Nov 09:36):
  VOID. HM 18 Nov aired "Bos AI Meta bikin deepfake Sam Altman, malah
  lolos aturan" (IG 2 likes, FB gate 403, Threads frozen), no
  "exp: hm-two-sided-provocation" marker in posted.log. Fourth
  topic-dependent VOID in a row for HM slot experiments (6 Nov
  Perplexity, 10 Nov Anthropic IPO, 13 Nov Hydrogen, 18 Nov deepfake).
  Lesson carried into the 19 Nov refresh: slot experiments must be
  VARIABLE-level (caption/reply pattern), independent of which news
  topic the HM run picks, or they keep going VOID. Do not re-propose
  a topic-locked HM slot design.

Judged Sun 2026-11-15 (weekly review, fresh CLI metrics 15 Nov 20:00 WIB;
pillar medians this week: SPILL Threads 42 likes / 1.533 views, IG 24,5
likes; Prompt Threads 3 likes / 135 views; HM IG carousel 3 likes;
Bansos Threads 9 likes; Gratisan Threads 7 likes):

- Prompt Harian before/after prompt (slot Fri 13 Nov 12:30, edisi
  #23): TIDAK JALAN sesuai desain. Caption Threads #23 ("Foto udah
  bagus, captionnya malah mentok...") + slide 1 (cover standar + satu
  prompt) TIDAK membawa perbandingan sebelum/sesudah sama sekali, dan
  posted.log tidak memuat marker "exp: prompt-before-after". Angka
  #23 (Threads 1 like / 127 views, IG 2 likes) tidak menguji hipotesis.
  Variabel belum teruji; jangan ajukan ulang desain slot yang sama
  tanpa memastikan generator benar-benar membangun slide + caption
  perbandingan sebelum tayang.
- HM Gemini 4 Carbon try-it step (slot Fri 13 Nov 09:36): VOID. HM
  13 Nov yang tayang bertopik Gemini 4 Hydrogen, bukan Carbon; marker
  di posted.log mencatat VOID. Ini pola berulang: variabel try-it
  model baru VOID ketiga kalinya karena topik tayang bukan model yang
  dirancang (6 Nov Perplexity, 10 Nov Anthropic IPO, 13 Nov Hydrogen).
  Jangan ajukan ulang desain slot yang sama; topik Carbon sendiri
  tetap layak jadi HM biasa.
- SPILL comparison slide (slot Fri 13 Nov 21:30, edisi #24): TIDAK
  JALAN sesuai desain. Slide 1 #24 adalah cover standar (daftar 5
  repo + star), tanpa tabel perbandingan dua kolom; caption pola #11
  biasa; posted.log tidak memuat marker "exp: spill-comparison-slide".
  Angka #24 (Threads 20 likes / 808 views, IG 32 likes / 39 saves /
  1.309 views) tidak menguji hipotesis. Variabel belum teruji; jangan
  ajukan ulang desain slot yang sama tanpa memastikan generator
  benar-benar membangun slide perbandingan sebelum tayang. Catatan
  samping: format perbandingan TERBUKTI menang di luar eksperimen ini
  lewat reel benchmark HM Hydrogen 13 Nov (IG 23 likes / 1.817 views
  vs carousel HM median 3 likes), jadi formatnya dipromosikan lewat
  jalur HM, bukan SPILL.
- Gratisan AI honest renewal price (slot Wed 11 Nov 14:00, dari
  refresh 9 Nov): MENANG PARSIAL. Jalan sesuai desain (harga perpanjang
  Rp75.000/bulan + sisa 50 hari + garpu SheerID). Threads 11 likes /
  1.619 views / 4 reposts, dan 1 komentar TERBUKTI balasan penonton
  asli ("Mauuu", Azmi Hafizharahman, terverifikasi via
  fetch-post-comments). Views setara kontrol #28 (1.654) dan 5x kontrol
  7 Nov (308), tapi likes di bawah #28 (18) dan IG/FB lemah (IG 2 likes
  / 1 save / 210 views, FB 18 views). Verdict: harga perpanjang jujur
  TIDAK membunuh reach dan menarik balasan penonton, tapi bukan
  pendongkrak reach. Dipromosikan ke playbook Gratisan sebagai praktik
  transparansi (cantumkan harga perpanjang jujur), bukan sebagai
  pendongkrak views.
- BLUEPRINT first-step framing on agent memory (retry Threads 13 Nov
  22:20): MENANG. Retry Threads edisi #02 claude-mem tayang: Threads
  3 likes / 307 views / 3 reposts; IG 7 likes / 7 saves / 353 views
  vs kontrol #01 (2 likes / 558 views), FB 231 vs 117 views. Framing
  langkah pertama menang di IG (likes + saves) dan FB (views), dan
  Threads retry solid. Dipromosikan ke playbook sebagai aturan
  BLUEPRINT: caption + slide wajib bingkai langkah pertama konkret.

Experiments from the 2026-11-09 refresh (checked 12 Nov from
posted.log and performance.log; judged Sun 2026-11-15 20:00 unless
noted VOID or not run):

- HM GIF try-it step on ChatGPT Images 2.6 (slot Tue 10 Nov 09:36):
  VOID. HM 10 Nov yang tayang bertopik Anthropic IPO (IG 1 like,
  FB views tidak tersedia), bukan Images 2.6; marker di posted.log
  mencatat VOID. Ini VOID kedua buat variabel yang sama (6 Nov juga
  VOID dengan topik Perplexity Teammates). Jangan ajukan ulang
  desain slot yang sama; topik Images 2.6 sendiri tetap layak jadi
  HM biasa bila ada slot kosong, lihat Hot topic carried di atas.
- Prompt Harian thesis Bab 3 checklist (slot Wed 11 Nov 12:30):
  TIDAK JALAN sesuai desain. Prompt #21 yang tayang bertema bisnis
  ("follow-up pembeli yang belum bayar", Threads 221 views, 1 like,
  1 balasan), tanpa marker "exp: prompt-bab3-checklist" di
  posted.log. Variabel belum teruji; jangan ajukan ulang desain
  slot yang sama tanpa memastikan tema tayang sesuai desain.
  Catatan: angka #21 (views 221, likes 1) jadi kontrol tambahan
  buat eksperimen before/after di atas.
- Gratisan AI honest renewal price (slot Wed 11 Nov 14:00): JALAN
  sesuai desain, menunggu verdict review Minggu 15 Nov 20:00.
  Caption membawa harga perpanjang Rp75.000/bulan + sisa 50 hari +
  garpu SheerID. Hasil snapshot 22:30: Threads 7 likes, 1 komentar,
  1.295 views, 1 repost; IG 0 likes; FB 0 likes, 9 views.
  Bandingkan kontrol 7 Nov (Threads 14 likes, 308 views, 2 balasan)
  dan #28 (18 likes, 1.654 views): views jauh di atas kontrol 7 Nov
  tapi likes setengahnya, IG 0. Hipotesis balasan (minimal 1 balasan
  penonton) terpenuhi secara angka komentar, tapi review Minggu
  yang memutuskan apakah komentar itu balasan penonton asli dan
  apakah verdictnya MENANG, PARSIAL, atau KALAH. Jangan kutip
  sebagai bukti sebelum verdict. VERDICT review 15 Nov 20:00:
  MENANG PARSIAL (lihat arsip 15 Nov di atas): komentar TERBUKTI
  balasan penonton asli ("Mauuu"), views 1.619 setara #28, tapi
  likes di bawah kontrol; harga perpanjang jujur dipromosikan ke
  playbook sebagai transparansi, bukan pendongkrak reach.

Judged Sun 2026-11-08 (weekly review, fresh CLI metrics 8 Nov 20:00 WIB;
pillar medians this week: SPILL Threads 14 likes, IG 31 likes; Prompt
Threads 3 likes; HM Threads 3 likes):

- HM gemini-try-it-step (slot Fri 6 Nov 09:36): VOID. HM 6 Nov yang
  tayang bertopik Perplexity Teammates (Threads 3 likes, 42 views,
  rantai 5/5 lengkap), bukan Gemini file editing; marker di posted.log
  mencatat VOID. Variabel tidak teruji dan tidak dipromosikan. Jangan
  ajukan ulang desain slot yang sama tanpa memastikan topik tayang
  sesuai desain.
- BLUEPRINT first-step framing on agent memory (slot Fri 6 Nov 20:00):
  TIDAK TERUJI di Threads. Edisi #02 claude-mem tayang di IG + FB
  dengan framing first-step SESUAI desain di caption ("Langkah
  pertama: pisahin aturan dan riwayat keputusan ke file terpisah"),
  tapi Threads gagal 429 dan belum tayang (retry diusulkan sebelum
  21:00 WIB 8 Nov). Sinyal parsial IG/FB: IG 7 likes / 353 views /
  7 saves vs kontrol #01 (2 likes / 558 views, usia seminggu), FB
  231 views vs #01 117 views. Hipotesis Threads tidak bisa dinilai;
  TIDAK dipromosikan ke playbook. Uji ulang lewat retry Threads,
  atau ajukan varian baru dengan pencatatan yang sama. UPDATE review
  15 Nov 20:00: retry Threads tayang 13 Nov 22:20 (3 likes / 307 views
  / 3 reposts) - verdict kini MENANG (lihat arsip 15 Nov di atas),
  aturan first-step dipromosikan ke playbook BLUEPRINT.
- Gratisan AI deadline plus verification catch, Threads re-test (slot
  Sat 7 Nov 14:00): MENANG PARSIAL. Jalan sesuai desain (deadline
  31 Des 2026 + sisa 54 hari + catch SheerID + garpu "mentok di
  langkah berapa?"). Threads 14 likes / 308 views / 8 reposts /
  2 balasan, dan 1 balasan penonton ASLI menanyakan titik gagal yang
  dirancang ("Yang bikin ribet SheerID-nya, email kampus aktif doang
  yang lolos?"), hipotesis balasan TERBUKTI. Tapi reach jauh di
  bawah kontrol #28 (1.654 views / 18 likes) dan IG/FB di bawah #31
  (IG 3 likes / 1 save / 171 views vs 8 / 8 / 353; FB 52 vs 117).
  Verdict: mekanisme garpu confusion-point dipromosikan ke playbook
  Gratisan (balasan terverifikasi); hitung mundur deadline saja
  tidak dipromosikan sebagai pendongkrak reach.
- Prompt Harian pembuka cerita relatable (izin user 4 Nov, edisi #14
  mulai 5 Nov, dinilai review ini): MENANG. Caption Threads dibuka
  1-2 kalimat cerita pengalaman mencoba di #14, #16, #17, #18:
  Threads views 111-260 (median ~215) dan likes median 4,5, vs
  #11-#13 tanpa cerita views median 58 dan likes median 2.
  Dipromosikan ke playbook sebagai aturan Prompt Harian.

Experiments from the 2026-11-02 refresh, NOT run as designed
(checked 5 Nov from posted.log and performance.log, before the
Sun 2026-11-08 review; recorded here so the new experiments above
do not re-propose them):

- HM two-sided close on the robots.txt opt-out (slot Tue 3 Nov
  09:36): VOID. HM 3 Nov aired "Claude Code dilarang bikin klon
  game" (Threads 323 views, chain complete) with no "exp:
  robots-two-sided" marker in posted.log. The designed test
  produced no result and the hypothesis was not judged. The topic
  itself was not aired, so it is carried to Hot topic 5 above as a
  first explainer, not as a judged experiment. Do not re-propose
  the same two-sided slot design.
- Prompt Harian student confusion-point (slot Tue 3 Nov 12:30):
  DROPPED. Prompt #12 that aired was the interview theme ("jawaban
  interview yang bikin HRD ingat kamu", Threads 55 views), with no
  "exp: prompt-student-confusion" marker. This was the fourth
  failure to run this variable (24 Okt, 27 Okt retry, 30 Okt, 3
  Nov). Per the 2 Nov refresh rule, the variable is DROPPED with
  no further re-proposal in this slot design. The student
  confusion-point content itself continues through other pillars
  (Gratisan experiment 3 above, Hot topic 2), but not as a Prompt
  Harian slot experiment.

Judged Sun 2026-11-01 (weekly review, fresh CLI metrics 1 Nov 20:00 WIB; pillar medians this week: SPILL Threads 8.5 likes, Prompt Threads 6.5 likes).

- SPILL Repo #09 first-step framing (29 Okt): TIDAK JALAN sesuai desain. posted.log has no "exp: first-step" marker and the #09 caption is plain spec framing with no first step, so the designed test produced no result. NOT promoted on #09 evidence. BUT the tactic itself was used unplanned in SPILL #11 (caption names the most-useful repo hermes-lcm + one concrete first step) and #11 broke out: Threads 121 likes, 4.149 views, 33 reposts, 19 follows, 2 viewer replies. Verdict: tactic MENANG on #11 evidence; promoted to the playbook SPILL rule 1 Nov. Do not cite #09 as the proof.
- Prompt Harian #08 student-task test (30 Okt, PPT sidang): TIDAK JALAN sesuai desain, third failure to run this variable (24 Okt, 27 Okt retry, 30 Okt). The edition that aired was rotation theme "harga jualan" (Threads 6 likes, 58 views). Variable still untested; no verdict on the hypothesis. Stop re-proposing the same slot design; run it explicitly with the theme logged, or drop the variable.
- Gratisan AI #31 confusion-point framing (31 Okt, Gemini API): JALAN sesuai desain (caption + spec carry the verified failure point "limit dihitung per project, bukan per key"). Threads result UNVERIFIED (429, post not found via search/profile), so the replies hypothesis is untested on Threads. IG (8 likes, 8 saves, 353 views) and FB (117 views) are the best Gratisan numbers on those platforms, but the IG reel format also changed (first animated 4K reel), so the win is confounded. Verdict: MENANG PARSIAL di IG/FB; confusion-point sentence pattern promoted to the playbook Gratisan rule with the Threads caveat; re-test on Threads next edition with the variant logged.
- SPILL #06 use-case framing (26 Okt): TIDAK DINILAI. The variant was never recorded in posted.log, so the variable cannot be verified as applied. Fresh numbers are strong (Threads 11 likes/391 views; IG 19 likes/1.400 views; FB photo 1.345 views) but topic (Claude, 431 ribu star) and FB photo format confound them. Not promoted.
- Prompt #04 retry SynthID hot-topic (27 Okt): TIDAK JALAN sesuai desain, second failure. The edition that aired was #05 "kalender konten 7 hari" (Threads 8 likes, 106 views), a rotation theme. Variable still untested; no verdict on the hypothesis.
- Gratisan AI #28 student-segment (28 Okt, Google AI Plus): JALAN sesuai desain. Threads 18 likes, 1.654 views, 7 reposts vs Copilot Free control (15 likes, 514 views, 7 reposts): likes +20%, views 3,2x. The single Threads reply was spam, so viewer replies = 0; IG stayed weak (2 likes, 45 views, carousel only). Verdict: MENANG di reach Threads, KALAH di balasan; student-segment targeting promoted to the playbook Gratisan rule with the reply caveat.
- Eksperimen tanpa-link (31 Okt, locked rule, judged at this review per playbook): LANJUT. Clean no-link editions topped Threads views (SPILL #11: 4.149; bansos ChatGPT Pro: 1.020); the one broken no-link edition (HM 31 Okt, empty root caption + 429 chain failure, 17 views snapshot) was the bottom. Fix execution (caption files must not live only in /tmp; retry 429 chains next day), keep the rule. Recorded in learnings.md 1 Nov.


- (seed, paused, NOT JUDGED) Store: test the choice question
  ("tim bulanan atau tahunan?") against the tag-a-friend close.
  PAUSED: jualan is FROZEN per user order 26 Okt 03:38 (the
  reactivation job for 29 Okt was disabled, no store posts until
  the user says otherwise), so the old "resumes 29 Okt" note is
  void. No verdict yet, do not run until jualan is unfrozen.

Experiments from the 2026-10-22 refresh, all judged Sun 2026-10-25:

- SPILL Repo #03 hook test (honest topical tie-in vs plain
  specific-number hook): verdict KALAH. Hipotesisnya balasan
  Threads naik; nyatanya komentar 1, sama dengan #04, dan IG likes
  2 di bawah #02 (9) dan #04 (7). Sinyal samping: FB views #03 708,
  tertinggi di pilar Spill, layak diuji ulang dengan desain yang
  lebih bersih, bukan dipromosikan sekarang.
- HM save-trigger add-on test (23 Okt, OpenAI): verdict KALAH,
  tidak terbukti. Saves tidak terekspos CLI manapun, komentar
  Threads tetap 0, dan edisi terganggu (IG tayang tanpa caption,
  rantai Threads terpotong), jadi uji ini tidak mengukur
  hipotesisnya.
- Prompt Harian hot-topic test (24 Okt, SynthID angle): verdict
  KALAH, tidak jalan sesuai desain. Edisi #02 yang tayang memakai
  tema rotasi "caption jualan" (bisnis), bukan tema hot-topic
  SynthID, jadi angkanya yang bagus (Threads 9-10 likes, 1 balasan,
  3 repost, 183 views) tidak menguji hipotesis. Variabel hot-topic
  masih belum teruji, hence the 27 Okt retry in the 26 Okt list,
  which itself failed to run as designed (see awaiting-verdict
  section above).

Seed experiments judged 25 Okt:

- (seed) HM closing debate question style (choice vs prediction):
  verdict KALAH, tidak terbukti. Varian per edisi tidak tercatat di
  posted.log, dan HM minggu ini tetap datar (Threads likes 5-7,
  balasan 0-4) tanpa pola varian yang jelas. Do not reuse as a
  tested tactic; log the variant per edition if retried.
- (seed) Prompt Harian Threads question (pain-point vs
  show-your-result): verdict KALAH, tidak terbukti. Edisi #01
  (pain-point) tidak tertangkap snapshot harian (snapshot mulai
  23 Okt), dan #03 yang memakai pertanyaan pain-point ("tugas apa
  yang paling sering kamu tunda?") meraih 0 balasan penonton.
