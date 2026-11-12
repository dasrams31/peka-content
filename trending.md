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

## Experiments this week (refresh 2026-11-12)

DINILAI review Minggu 2026-11-15 20:00. Eksperimen refresh 2026-11-09
sudah dipindah ke Archive di bawah (1 VOID, 1 tidak jalan, 1 jalan
dan menunggu verdict review ini). Jangan jalankan ulang ketiganya
tanpa desain baru.

Three experiments, one variable each. The run that airs an experiment
MUST write its exp marker into its posted.log line the same day, with
the exact theme that aired. If the aired theme differs from the design,
the experiment is VOID, not a result, and the variable is not
re-proposed. The Sun 2026-11-15 20:00 review judges all three from
performance.log plus live read-backs. No experiment may break a locked
rule: brand design, exactly 1 closing hashtag per tag-watch.md, no
em-dash or en-dash, honest numbers only, fixed slots, no sales posts
on IG, no link in any post text.

1. Prompt Harian before/after prompt (pillar: Prompt Harian, slot:
   Fri 13 Nov 12:30). Variable: caption dibuka cerita relatable
   (aturan menang), lalu slide 1 dan caption membawa perbandingan
   sebelum/sesudah: satu prompt jelek vs satu prompt bagus untuk
   tugas yang sama, hasil sampingan, plus forced choice (prompt yang
   mana yang biasa kamu pakai, A atau B?). Control: Prompt #21
   (Threads 221 views, 1 like, 1 balasan) dan #20 (43 views).
   Hypothesis: format perbandingan mengalahkan median rotasi
   (Threads views sekitar 160, likes sekitar 3), karena format
   perbandingan menang besar di gelombang mahasiswa (reel IPK 3 vs
   Cum Laude 2,8 ribu likes, 11 Nov; postingan before/after prompt
   4.502 likes, 4 Nov). Log marker: "exp: prompt-before-after".
   Guardrail: kedua prompt benar-benar dicoba dan hasilnya jujur,
   jangan karang hasil; framing kejujuran akademik tetap; jangan
   salin cerita personal yang tidak terjadi.

2. HM Gemini 4 Carbon try-it step (pillar: HM, slot: Fri 13 Nov
   09:36). Variable: root caption membawa SATU langkah coba konkret
   (buka Gemini, minta Carbon kerjakan satu tugas agent panjang,
   bandingkan dengan model biasa) plus forced choice (tugas panjang
   apa yang mau kamu serahkan ke agent?). Control: HM 11 Nov RAISE
   Act (IG 1 like, FB 4 views) dan HM 10 Nov Anthropic IPO (IG 1
   like). Hypothesis: langkah coba konkret pada peluncuran model
   terbesar minggu ini mengangkat IG likes di atas median HM (1-2
   likes) dan menghasilkan save, karena topik try-it dengan titik
   bingung sudah terbukti menarik balasan untuk Oracle dan Meta AI x
   Komdigi. Log marker: "exp: hm-carbon-try-it". Guardrail: Carbon
   GA 10 Nov terverifikasi dari beberapa roundup; re-verifikasi di
   blog Google DeepMind pagi hari tayang; harga $2/$10 per juta
   token sampai 30 Nov lalu naik dua kali lipat, hanya sebut bila
   terverifikasi hari itu; jangan sajikan Carbon sebagai model
   gratis biasa bila aksesnya lewat API atau berbayar. NOTE: HM is
   frozen on Threads 7 Nov to 7 Dec, so this experiment is judged
   on IG, FB, and blog only, not Threads.

3. SPILL comparison slide (pillar: SPILL Repo, slot: Fri 13 Nov
   21:30, edisi #24). Variable: slide 1 membawa tabel perbandingan
   dua kolom dari dua repo paling kepakai di edisi itu (repo A buat
   X, repo B buat Y, satu baris beda kunci), caption tetap pola #11
   (repo paling kepakai + langkah pertama konkret + "Repo mana yang
   mau kamu coba duluan?"). Control: SPILL #22 (Threads 4 likes,
   257 views; IG 3 likes) dan #21 (Threads 5 likes, 168 views; IG
   4 likes, 24 jam 92 likes). Hypothesis: slide perbandingan
   mengangkat swipe-through dan IG likes di atas median SPILL hari
   yang sama (sekitar 3-4 likes), karena format perbandingan menang
   besar di gelombang mahasiswa (2,8 ribu likes, 11 Nov). Log
   marker: "exp: spill-comparison-slide". Guardrail: repo harus
   fresh dan terverifikasi, sudah ditambah ke tools.json dulu, star
   count jujur; OpenClaw tetap dikecualikan permanen dari roster
   SPILL.

## Hot topics (refresh 2026-11-12)

Corrections to the 9 Nov refresh, read before reusing old angles.
Gemini 4 Carbon SUDAH GA pada 10 Nov (bukan lagi terbatas ke
Fairwind; early access dua minggu buat security experts sudah
selesai, harga intro $2/$10 per juta token sampai 30 Nov lalu naik
ke $4/$20). Sora is still retired (consumer app closed 26 Apr 2026,
API shut 24 Sep 2026); do NOT recommend it. The "GPT-6.1 Terra"
scope from the 5 Nov refresh still stands: reported 26 Okt for
writing, visual reasoning and computer use, available through the
API and eligible paid access in ChatGPT Work and Codex, NOT in
ordinary Chat, at $1/$5 per million tokens. Verify on the OpenAI
changelog the day of use before naming it, and never present it as
an ordinary Chat model. Gemini Gems read-only 17 Nov tetap jalan,
5 hari lagi dari 12 Nov.

1. Gemini 4 Carbon rilis umum 10 Nov, model terkuat Google buat
   tugas agent panjang. Harga intro $2/$10 per juta token sampai 30
   Nov, lalu naik dua kali lipat. DeepMind juga memamerkan
   AlphaProof Code: agent bertenaga Carbon menulis 6 juta baris Lean
   dalam 4 minggu buat membuktikan properti keamanan kode Signal
   yang sebenarnya. Angle for Peka: HM explainer di eksperimen 2,
   dan Prompt Harian prompt tugas agent panjang. Guardrails:
   re-verifikasi di blog Google DeepMind pagi hari pakai; harga
   hanya bila terverifikasi hari itu.

2. Claude jadi kantor, ChatGPT jadi etalase bisnis. Anthropic
   meluncurkan Claude Meetings, Sheets, Whiteboards, dan Data
   (beta, 10-11 Nov) plus konektor interaktif Adobe, Atlassian, dan
   Box; OpenAI meluncurkan Businesses in ChatGPT (beta, 10 Nov):
   perusahaan bisa klaim profil dan pasang Business Agent di dalam
   jawaban. Anthropic juga mulai roadshow IPO 10 Nov, kisaran
   $70-78 per saham, ticker ANT. Angle for Peka: HM explainer
   "Claude sekarang bisa rapat dan bikin spreadsheet" dengan satu
   langkah coba konkret, tutup debat dua sisi (kemajuan atau ancaman
   buat kerjaan kita?). Guardrails: fitur masih beta, jangan
   janjikan akses yang belum dibuka di Indonesia; angka IPO dari
   Reuters, re-cek bila dipakai.

3. Gelombang mahasiswa masih panas, formatnya geser ke
   perbandingan. Bukti segar 5-11 Nov: carousel "10 AI Tools untuk
   Skripsi" 18 ribu likes (5 Nov, @trik_farilhumam07); reel "IPK 3
   vs Cum Laude" 2,8 ribu likes (11 Nov, @bantuwisuda.id); carousel
   PPT sidang AI 2,9 ribu likes dan 46 komentar (6 Nov,
   @ibuiramira); carousel Bab 2 1,4 ribu likes dan 71 komentar
   (6 Nov, @dafnisfaz_); reel "AI buat Bab 1-3" 720 likes (6 Nov,
   @mydata_id). Google AI Plus masih dibuka: gratis 12 bulan buat
   mahasiswa, klaim sampai 31 Des 2026 (49 hari lagi dari 12 Nov),
   verifikasi SheerID, perpanjang Rp75.000/bulan bila tidak
   dibatalkan. Angle for Peka: eksperimen 1 dan 3, plus Gratisan
   14 Nov dengan sudut PPT sidang atau Bab 2. Guardrails: framing
   kejujuran akademik tetap, jangan janji jalan pintas; harga
   perpanjang hanya bila terverifikasi hari itu.

4. Chatbot diuji pura-pura nyontek, hasilnya beda-beda. Tren viral
   X 2 Nov: pengguna pura-pura nyontek ujian matematika lalu
   pura-pura jadi guru; ChatGPT awalnya menutupi lalu berbalik,
   Claude memberi jawaban benar tapi mengajak jujur dan menawarkan
   mengajari materinya, Grok menolak dengan sarkasme, Gemini tidak
   menyerahkan muridnya langsung. Survei Pew: 54% remaja AS sudah
   pakai AI buat tugas sekolah. Angle for Peka: HM debat dua sisi
   ("AI mana yang paling bisa dipercaya saat ditanya dosen?")
   dengan framing kejujuran, bukan tutorial nyontek. Guardrails:
   tes ini bukan eksperimen terkontrol, sebut itu; jangan ajarkan
   cara nyontek; jangan jadikan satu chatbot sebagai pemenang
   mutlak.

5. Gems Gemini dibekukan 17 Nov, diganti Skills. Akun personal:
   Gems jadi read-only 17 Nov (5 hari dari 12 Nov) dan dihapus
   permanen 17 Des. Angle for Peka: HM explainer Senin 16 Nov
   ("pindahin Gems kamu ke Skills sebelum 17 Nov") dengan satu
   langkah migrasi konkret. Guardrail: re-verifikasi di halaman
   bantuan Google pagi hari tayang; jangan tulis langkah migrasi
   yang belum terverifikasi.

Carried, still true and still not aired: Images 2.6 GIF (4 Nov,
gratis di semua paket; dua kali VOID sebagai eksperimen karena
topik tayang bukan Images 2.6, jadi jangan ajukan lagi sebagai
eksperimen slot, tapi tetap layak jadi topik HM biasa bila ada slot
kosong). The shared robots.txt token "__usage_ai-training" (Hot
topic 5, 5 Nov refresh) is still a draft with staggered timelines
and nobody honors it yet as of 3 Nov; keep for a future HM slot
only if a concrete reader step exists, do not force it. Mistral
Large 4 "Le Chonk" (1T parameter, open weights, klaim coding
terkuat open-weight), Cursor Live Apps (deskripsi jadi app live
dengan database), dan Google Canvas (sketsa tangan jadi app jalan)
jadi kandidat SPILL atau BLUEPRINT; verifikasi repo dan angka di
hari pakai. Meta Muse Ember 1.0 (9 Nov, model kecil buat subtask
agent) jadi latar, bukan topik utama.

Format note, still winning: checklist and self-score formats keep
winning in the student wave (steps, checklists, boleh vs tidak-boleh,
red flags vs green flags, this-or-that) because they give the reader
a score or a side to pick. NEW: format perbandingan dua kolom (X vs
Y, sebelum vs sesudah) bergabung sebagai format menang, dibuktikan
reel IPK 3 vs Cum Laude 2,8 ribu likes (11 Nov) dan postingan
before/after prompt 4.502 likes (4 Nov). Copy the comparison
structure inside the locked design system and the two-sided
pick-a-side close where the playbook allows it. Tag-watch 12 Nov
adds: #Kuliah kini memimpin rata-rata likes (1577,9, n=7) di atas
#AI (1391,5, n=11), tapi tag penutup tetap #AI karena kunci manual
user 6 Nov; story 33%, question 30% di REST; top post hari ini
#Mahasiswa 44 ribu likes soal Hari Pahlawan, bukan AI, jangan
ditumpangi. Note on this refresh: the V2EX hot list checked 12 Nov
shows no strong AI trend in the top 10 (dominated by non-AI life
topics). Do NOT turn a complaint thread into a claim about a
vendor's pricing without an official source.

## Moments and calendar to ride this week

- Thu 12 Nov: Hari Kesehatan Nasional dan Hari Ayah Nasional; trend
  watch refresh 08:15 (this file); HM 09:36; Prompt Harian 12:30;
  SPILL #23 21:30.
- Fri 13 Nov: HM 09:36 (experiment 2 slot, Carbon try-it step);
  Prompt Harian 12:30 (experiment 1 slot, before/after prompt);
  katalog Peka 13:00; BLUEPRINT 20:00; SPILL #24 21:30
  (experiment 3 slot, comparison slide).
- Sat 14 Nov: Gratisan AI 14:00 (sudut PPT sidang atau Bab 2 +
  AI Plus 49 hari); LOG PEKA 16:00 (internal only, text summary
  to chat, no posting).
- Sun 15 Nov: engagement review 20:00 judges the three experiments
  above.
- Mon 16 Nov: HM slot Gems-to-Skills (Hot topic 5).
- Tue 17 Nov: Gemini Gems read-only (Hot topic 5). Kiro Pro
  cancellation reminder is 29 Nov 10:00, first bill $20 on 1 Dec.
- Wed 25 Nov: Hari Guru Nasional. Same rule: note only, no forced
  content.
- Wed 31 Dec 2026: Google AI Plus student claim deadline (49 days
  from 12 Nov).
- Ongoing locks: jualan FROZEN, Pancingan OFF, giveaway ON HOLD, HM
  freeze on Threads 7 Nov to 7 Dec (IG, FB, blog, and channel still
  air), all with no new date until the user says otherwise. No link
  in any post text on any platform; the edition link lives printed
  inside the visual as an admin-owned s.peka.ai.id shortlink, with
  one instruction sentence in the caption. Every new external link
  goes through s.peka.ai.id first; if shortening fails, STOP before
  posting. SPILL on Facebook stays one format per edition, default
  carousel.

## Archive (experiments judged by Sunday review)

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
  sebagai bukti sebelum verdict.

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
  atau ajukan varian baru dengan pencatatan yang sama.
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
