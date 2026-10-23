# Pancingan: text-only engagement posts for empty slots

Status: ACTIVE (approved by user 2026-10-23). Daily cron peka-pancingan 16:00 WIB. First post went live 2026-10-23 ~16:52 (manual, VERSUS).

## Concept
Short text-only posts whose only job is interaction: comments first,
then likes and follows. AI topic only. Posted in slots not used by the
standing pillars (09:36 news, 12:30 prompt, 19:00 store, 21:30 spill).
Proposed slot: 16:00 WIB daily.

Platforms: Threads + Facebook only. Instagram feed has no native
text-only format, so IG sits this one out (same precedent as sales
posts skipping IG, mirrored).

## Rules (from engagement-playbook.md, locked rules still apply)
- Exactly ONE interaction trigger per post, ending with a question
  that is trivial to answer.
- Threads: exactly 1 hashtag #AI, no other hashtags, no links in body.
- No em dash, no en dash.
- FORBIDDEN: cheap engagement bait ("like kalau setuju"), fake
  clickbait, rage bait, SARA, party politics.
- Post length: max ~280 chars on Threads so it reads like a native
  text post, not a mini article.

## Rotating formats (day_of_year % 7)
1. VERSUS: two-sided pick ("tim mana?") + ask for the reason.
2. PENGALAMAN: first/personal AI moment, invite their version.
3. LENGKAPI: fill-in-the-blank sentence, funniest/most relatable wins.
4. PREDIKSI: one confident guess about AI's near future.
5. HOT TAKE: one honest bold claim, agree or disagree + why.
6. REKOMENDASI: crowd-source tools, best ones can become content.
7. KEBIASAAN: light relatable AI habit confession.

## Stock
See stock.md. The cron must log used posts to posted.log and never
repeat a stock item verbatim within 30 days; when stock runs out,
generate a fresh one in the day's format, same rules.
