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
