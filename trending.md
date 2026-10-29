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

## Experiments this week (refresh 2026-10-29)

State of the fleet this week, so experiments only use ACTIVE pillars:
HM news is paused sampai 1 Nov (reactivation job 2 Nov 09:00,
first HM back 2 Nov 09:36), Pancingan is OFF with no reactivation,
jualan is FROZEN until the user says otherwise, giveaway announcement
is ON HOLD with no new date. Active pillars: SPILL Repo daily 21:30,
Prompt Harian daily 12:30, Gratisan AI Wed + Sat 14:00, bansos ad hoc.
All three experiments below are judged Sun 2026-11-01 at the 20:00
review, together with the three pending experiments from the 26 Okt
refresh listed below them. Log the experiment variant in the run's
posted.log line, or the review cannot judge it (lesson from the
25 Okt review, repeated on 26 and 27 Okt).

1. SPILL Repo #09 (Thu 2026-10-29, 21:30, roster: Antigravity).
   First-step framing test. Pillar SPILL Repo. Variable: slide 1 +
   hook = one concrete first step the reader can try in minutes
   ("langkah pertama: X, hasilnya Y") vs the plain repo-spec
   framing (name, stars, what it is). Hypothesis: a first step
   earns more implementation questions than a spec list, because
   Peka learnings show topics with a real step and a real
   confusion point earn replies, while spec lists stay quiet.
   Rules: the first step must be real for this repo, not invented;
   standard close ("Repo mana yang mau kamu coba duluan?") stays;
   links stay in the first reply, now as shortlinks via
   s.peka.ai.id plus the tools.peka.ai.id line (rule 28 Okt);
   series number + follow trigger stay; exactly one #AI hashtag;
   the run MUST write "exp: first-step" in the posted.log line.

2. Prompt Harian (Fri 2026-10-30, 12:30). Student-task prompt test.
   Pillar Prompt Harian. Variable: prompt theme = a concrete
   student task that is all over Indonesian social this week
   ("bikin PPT sidang dari materimu sendiri, bukan upload skripsi
   mentah-mentah") vs the normal day_of_year % 6 category
   rotation. Hypothesis: a prompt tied to a task students are
   actually doing this week earns more saves and show-your-result
   replies than a rotation theme, because social evidence this
   week is dominated by student AI use (see hot topic 3).
   Why this slot matters: the hot-topic prompt variable has now
   failed to run twice (24 Okt aired rotation theme "caption
   jualan", 27 Okt aired rotation theme "kalender konten"), so
   this run MUST write the theme in the posted.log line; if the
   theme is not the student task, the run reports the experiment
   as not run, not as a result. Rules: slide 1 keeps the yellow
   giant-typography design, slide 2 the black prompt bubble;
   one #AI hashtag only; the prompt must tell the reader to
   decide the content themselves first (the viral PPT reel's own
   warning: AI-made slides are spotted because they are generic,
   not because they use AI), never promise a pass or a grade.

3. Gratisan AI (Sat 2026-10-31, 14:00). Confusion-point framing
   test. Pillar Gratisan AI. Variable: caption + slide framing =
   offer plus the one failure point readers most often hit
   ("yang sering bikin gagal klaim: X, cara lewatinnya Y") vs a
   plain offer list (what is free, steps, deadline). Hypothesis:
   naming the failure point earns more replies from people who
   tried and got stuck, the exact reply pattern behind the
   Oracle bansos win (67 replies, mostly people hitting claim
   problems). Rules: the offer itself is NOT pre-locked here;
   the run MUST verify on the official page during the run
   (what is free, until when, card needed or not, Indonesia
   eligibility); never invent a deadline or quota; if the
   failure point cannot be verified, write it as unclear or
   pick another offer; standard Gratisan ticket design and
   kicker stay; one #AI hashtag only; Halloween tie-in only if
   the offer genuinely fits, never forced.

## Experiments awaiting verdict (from the 2026-10-26 refresh, NOT yet judged)

These three go to the same Sun 2026-11-01 20:00 review. They are
listed here so they are not lost and not mistaken for judged
experiments. Early numbers below are snapshots from
performance.log, not verdicts; the review decides.

- SPILL #06 (Mon 26 Okt, Claude, use-case framing test):
  posted.log does NOT record the experiment variant, so the
  use-case variable is still unjudged. Early snapshot: Threads
  5 likes, 1 comment, 90 views, 2 reposts; IG 1 like plus
  reels 7 likes. Weaker than SPILL #05 (Threads 11 likes,
  242 views) and #07 (Threads 7 likes, 2 comments, 7 reposts),
  but topic differs per edition, so no conclusion yet.
- Prompt #04 retry (Tue 27 Okt, hot-topic SynthID test):
  NOT RUN as designed for the second time. The edition that
  aired 27 Okt was #05 "kalender konten 7 hari" (Threads 8
  likes, 1 comment, 86 views, 6 reposts), a rotation theme,
  not the SynthID theme. Variable still untested.
- Gratisan AI (Wed 28 Okt, student-segment test, Google AI
  Plus gratis setahun buat mahasiswa): RAN as designed and
  logged ("exp: student-segment"). Early snapshot: Threads
  15 likes, 1035 views, 917 reach, 7 reposts, matching the
  Copilot Free control on likes (15) and roughly doubling its
  views (514). Note honestly: the 1 Threads comment on this
  edition was spam from another account (tawaran aktivasi 20K),
  not a real interaction, so the early signal is reach, not
  replies. Review judges it 1 Nov.

## Hot topics (refresh 2026-10-29)

1. Model nomor 1 yang belum bisa dipakai kebanyakan orang.
   Google DeepMind announced Gemini 4 Carbon 28 Okt: first on
   the Artificial Analysis Intelligence Index v5 with 59,
   ahead of Claude Opus 5.5 at 58, GPT-6 Astra at 57, and
   Gemini 4 Argon at 50. Catch for the audience, and the whole
   angle: access starts with vetted cyber defenders through
   the Fairwind Program, with no date given for developers,
   businesses, or consumers. Do NOT present Carbon as available
   in Indonesia. Angle for Peka: the honest-expectation explainer
   ("nomor 1, tapi kamu belum bisa pakai") plus a two-sided
   debate hook for the HM return 2 Nov (worth waiting for, or
   use what is available now). Honest-numbers rule: quote only
   what the run verifies that day, and say clearly which scores
   come from Google's own table vs the independent index.
   Note: a low-credibility post claiming a "GPT-6.1 Terra"
   launch 26 Okt conflicts with the credible timeline (GPT-6.1
   Sol shipped late Sep, Ultrafast tier 8 Okt); do NOT use the
   Terra claim until an official source confirms it.

2. Dunia AI yang bisa diubah sambil jalan, tapi juga belum
   bisa dipakai umum. Google DeepMind announced Genie 4 on
   27 Okt: a real-time world model that builds an explorable
   world from a text or image prompt, now with native audio
   (music, ambient sound, dialogue) and mid-simulation steering
   (change the weather, camera, or objects with text while the
   scene runs). Reported consistent scenes last up to about
   2 minutes, double Genie 3. Catch: research preview for
   trusted testers only, "coming soon" to Google AI Ultra
   subscribers via Project Genie and to API early-access
   partners, waitlist open, no firm date. Angle for Peka: a
   "nonton vs masuk ke dalam" explainer (video generator vs
   world model) for the HM return, or a Prompt Harian about
   describing a scene change in one sentence. Guardrail: never
   present demo footage as something the reader can try today.

3. AI buat mahasiswa masih jadi gelombang paling ramai di
   sosmed Indonesia. Social evidence this week: a pelajarin.ai
   study-from-PDF-and-YouTube reel at 15K likes, a "PPT sidang
   yang benar" reel at 5.2K likes warning against uploading a
   thesis raw, and an 8-slide "nyesel 4 tahun kuliah ga tau
   tools AI" carousel at 9.6K likes, plus a flood of Google
   Student Ambassador carousels for Google AI Plus gratis
   setahun buat mahasiswa (claim window reported sampai
   31 Des 2026, 400 GB storage). This is the demand behind
   experiment 2 (Prompt Harian student task) and the reason the
   28 Okt Gratisan student edition reached 1035 Threads views.
   Angle for Peka: student tasks with a real step (belajar dari
   PDF, susun PPT dari materi sendiri), not another generic
   "tools AI gratis" list. Guardrail: academic honesty framing
   stays (AI helps draft and study, the student decides the
   content), never a shortcut promise.

4. Indonesia nomor 2 dunia untuk pemakaian AI multimodal
   harian. Ericsson ConsumerLab report released 28 Okt, covering
   27 markets: 22% of Indonesian consumers use AI daily across
   formats (text, image, video, voice, documents), second only
   to China. Same report projects intensive multimodal use in
   Indonesia reaching 45% by 2030 (global projection 30%) and
   agentic AI adoption rising from 8% now to 44% by 2030.
   Angle for Peka: a local-pride, save-worthy HM return piece
   2 Nov ("kenapa Indonesia pakai AI beda dari negara lain")
   built on the multimodal shift (teks saja sudah ketinggalan)
   and the agent wave, with the numbers dated and sourced.
   This replaces the older "model mana yang lagi kamu pakai"
   confusion angle as the lead HM angle, because it is local,
   dated, and has a clear reader benefit (which format to learn
   next: voice, image, video, not just text).

5. Format yang menang minggu ini: checklist yang bisa
   dicentang dan "nilai dirimu sendiri". Evidence: the viral
   student carousels above are structured as steps and
   checklists, not essays, and the broader carousel literature
   keeps pointing to gamified formats (rate yourself, red
   flags vs green flags, this-or-that) because they give the
   reader a score or a side to pick. What Peka copies: the
   checklist structure inside the locked design system, and
   the two-sided pick-a-side close where the playbook already
   allows it (HM debate question, SPILL standard close).
   What Peka does NOT copy: "komentar LINK biar dikirimi link"
   DM gating, which is cheap engagement bait under the
   playbook; Peka links stay in the first reply as shortlinks
   and on the blog. V2EX note, for discussion fuel only: the
   hottest thread this week is AI vs doctor on a major medical
   decision (190 replies), which confirms two-sided debate
   drives replies, but Peka must NOT turn it into medical
   advice content; keep health topics out unless from an
   official health source and framed informationally.

## Moments and calendar to ride this week

- Thu 29 Okt: trend watch refresh 08:15 (this file); separate
  custom REA package 17:00 (not a Peka pillar slot, do not
  confuse with SPILL); SPILL Repo #09 Antigravity 21:30
  (experiment 1 slot).
- Fri 30 Okt: Prompt Harian 12:30 (experiment 2 slot, student
  task theme, must be logged in posted.log).
- Sat 31 Okt: Gratisan AI 14:00 (experiment 3 slot,
  confusion-point framing; Halloween angle only if the offer
  fits, never forced).
- Sun 1 Nov: engagement review 20:00 judges all six
  experiments (three from 26 Okt refresh, three from this
  refresh). This review also carries the format-test verdict
  for 24 Okt sampai 6 Nov.
- Mon 2 Nov: HM reactivation job 09:00, first HM back 09:36.
  Lead angles ready: Gemini 4 Carbon honest-expectation
  explainer (hot topic 1) or Ericsson Indonesia multimodal
  piece (hot topic 4). Pick one, date-stamp it, verify numbers
  that morning.
- Ongoing locks: jualan FROZEN, Pancingan OFF, giveaway ON
  HOLD, all with no new date until the user says otherwise.
  SPILL #10 follows the roster after Antigravity (Claude),
  and every new external link goes through s.peka.ai.id
  first; if shortening fails, STOP before posting.

## Archive (experiments judged by Sunday review)

Judged Sun 2026-10-25 (first review). No experiment won, so nothing
was promoted to the playbook this week.

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
