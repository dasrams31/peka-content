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

## Experiments this week (refresh 2026-10-26)

State of the fleet this week, so experiments only use ACTIVE pillars:
HM news is paused 26 Okt sampai 1 Nov (reactivation job 2 Nov 09:00,
first HM back 2 Nov 09:36), Pancingan is OFF with no reactivation,
jualan is FROZEN until the user says otherwise, giveaway announcement
is ON HOLD with no new date. Active pillars: SPILL Repo daily 21:30,
Prompt Harian daily 12:30, Gratisan AI Wed + Sat 14:00, bansos ad hoc.
All three experiments below are judged Sun 2026-11-01 at the 20:00
review. Log the experiment variant in the run's posted.log line,
or the review cannot judge it (lesson from the 25 Okt review).

1. SPILL Repo #06 (Mon 2026-10-26, 21:30, roster: Claude). Use-case
   framing test. Pillar SPILL Repo. Variable: slide 1 + hook =
   use-case framing ("repo ini dipakai buat X, begini alurnya") vs
   the plain repo-spec framing (name, stars, what it is). Hypothesis:
   a use-case first slide earns more saves and implementation
   questions than a spec first slide, because social evidence this
   week shows creator-skill reels (YouTube skill for Claude, 4.4K
   likes, 290 comments) win on "dipakai buat apa", not on spec
   lists. Rules: repo must genuinely do the use case claimed;
   standard close ("Repo mana yang mau kamu coba duluan?") stays;
   link stays in the first reply; series number + follow trigger
   stay; exactly one #AI hashtag; no "komentar LINK biar dikirimi
   link" bait, Peka never gates links behind a comment keyword.

2. Prompt Harian #04 (Tue 2026-10-27, 12:30). Hot-topic prompt test,
   RETRY done properly. Pillar Prompt Harian. Variable: prompt
   theme = this week's hot topic ("cek foto/video AI asli atau
   palsu", SynthID angle, building on the ICT Watch tutorial wave)
   vs the normal day_of_year % 6 category rotation. Hypothesis: a
   prompt tied to a topic people are already arguing about earns
   more saves and show-your-result replies. Why a retry: the 24 Okt
   attempt did not run as designed (edition #02 aired the rotation
   theme "caption jualan", not the SynthID theme), so the variable
   is still untested. This time the run MUST write the theme in the
   posted.log line; if the theme is not the hot topic, the run
   reports the experiment as not run, not as a result. Rules: slide
   1 keeps the yellow giant-typography design, slide 2 the black
   prompt bubble; one #AI hashtag only; prompt must be honest about
   what SynthID can and cannot prove (no watermark is not proof a
   file is real).

3. Gratisan AI (Wed 2026-10-28, 14:00, Hari Sumpah Pemuda).
   Audience-segment test. Pillar Gratisan AI. Variable: offer =
   segmented for Indonesian students (Google AI Plus gratis setahun
   buat mahasiswa, campus tour angle) vs a general free tool for
   everyone (the Copilot Free control, which scored Threads 15
   likes, 7 reposts, 514 views on 24 Okt). Hypothesis: a segmented
   offer earns more shares and tags than a general offer, because
   readers tag classmates who qualify. Rules: VERIFY on the official
   page during the run before posting (what is free, until when,
   card needed or not, Indonesia eligibility); never invent a
   deadline or quota; if eligibility for Indonesia is unclear,
   write it as unclear or pick another offer; standard Gratisan
   ticket design and kicker stay; one #AI hashtag only.

## Hot topics (refresh 2026-10-26)

1. Agent AI proaktif jadi arus utama. Anthropic opened the waitlist
   21 Okt for Claude Duet, a standalone app where Claude works on
   its own (morning brief, background tasks, approval before it
   sends, pays, signs, or deletes anything), built on Claude Opus
   5.5. Catch for the audience: preview is US Pro and Max
   subscribers only, so manage expectations, do not present it as
   available in Indonesia. Same wave: Anthropic donated the Agent
   Skills standard (used by 70+ agent platforms) to the Linux
   Foundation, and agent memory system Hindsight passed 53K GitHub
   stars. Angle for Peka: SPILL #06 Claude edition rides this wave
   honestly (see experiment 1), plus a "agent yang kerja sendiri"
   explainer angle for a later bansos-style post. V2EX is also
   debating Codex vs Claude for coding agents (29 replies), so
   agent-coding rivalry is live discussion fuel.

2. Cek foto dan video AI asli atau palsu makin ramai. Google opened
   SynthID verification to the public, and Indonesian literacy
   account ICT Watch already ran a tutorial carousel (synthid.com
   upload, what a watermark proves, what it does not). Same week,
   Kemkomdigi (23 Okt) said it is watching AI mini dramas carrying
   pornographic and gambling content that funnel viewers to paid
   platforms, and the Meta AI and Komdigi story is still echoing
   (Espos, 24 Okt: observers asking both sides to be transparent).
   Angle for Peka: the verifiability angle that already worked for
   the Meta AI special edition, now as a practical checklist
   ("cara cek foto AI") and as Prompt Harian #04 (see experiment
   2). Guardrails: keep framing informational and verifiability
   focused, never partisan, never graphic detail about the mini
   drama content itself, playbook bans rage bait on party politics.

3. AI gratis buat mahasiswa Indonesia. Google AI Plus gratis setahun
   buat mahasiswa (campus tour Aug to Okt 2026 reached 47 ribu
   students at 9 campuses, 400 GB storage, claim window reported
   sampai 31 Des 2026) plus GitHub Copilot Student for verified
   students. This fits the Gratisan AI winning recipe exactly
   (permanent-feeling free offer + concrete claim steps) and lands
   on Hari Sumpah Pemuda, a student-youth moment. Angle: Gratisan
   AI Wed 28 Okt (see experiment 3). Verification is mandatory
   during the run: confirm the offer, the deadline, and Indonesia
   eligibility on the official page before posting.

4. Gelombang model baru bikin bingung: model mana yang lagi kamu
   pakai. GPT-6 tiers (Astra, Sol, Luna), Claude 5.5 trio (Opus,
   Sonnet, Haiku), Gemini 4 Argon public 13 Okt, and at the same
   time Gemini free app access narrowed to Flash-Lite from 9 Okt.
   Coverage this week is full of "which app runs what" guides
   because model names change weekly. Angle for Peka: a dated,
   save-worthy "model mana yang lagi kamu pakai" explainer
   (date-stamp it, since it expires fast) and a two-sided debate
   hook for a later edition (gratis vs bayar: worth it or not).
   Honest-numbers rule: quote only what the run verifies that day.

5. Format yang menang di sosmed minggu ini: listicle tools gratis
   dan tutorial skill agent buat kreator. Indonesian account
   @aigrowth.id ran a "10 tools GitHub gratis" carousel, and
   creator-skill reels (Claude YouTube skill, Claude agent
   frameworks) are pulling implementation questions in comments
   across languages. What Peka copies: the listicle structure and
   the use-case framing (see experiment 1). What Peka does NOT
   copy: "komentar LINK biar dikirimi link" DM gating, which is
   cheap engagement bait under the playbook; Peka links stay in
   the first reply (SPILL format) and on the blog.

## Moments and calendar to ride this week

- Mon 26 Okt: SPILL Repo #06 Claude 21:30 (experiment 1 slot).
  HM paused, Pancingan off, jualan frozen, giveaway on hold.
- Tue 27 Okt: Prompt Harian #04 12:30 (experiment 2 slot, hot-topic
  retry, must be logged in posted.log).
- Wed 28 Okt: Hari Sumpah Pemuda + Gratisan AI 14:00 (experiment 3
  slot, student-segment offer).
- Thu 29 Okt: trend watch refresh 08:15 (next cycle, Thu edition).
- Sat 31 Okt: Gratisan AI 14:00 (Halloween: light optional angle
  is "cek foto AI" hoax-spotting, only if the offer fits; never
  force a holiday tie-in onto an unrelated offer).
- Sun 1 Nov: engagement review 20:00 judges this week's 3
  experiments (SPILL #06, Prompt #04, Gratisan 28 Okt).
- Mon 2 Nov: HM reactivation job 09:00, first HM back 09:36
  (lookahead, not this week's slot).

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
  masih belum teruji, hence the 27 Okt retry in this week's list.

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
