# Peka Homeless Media (HM)

Automated AI-news pipeline for @peka.ai.id socials + blog. 1 topic/day, full-auto.
Replaces the old peka-ai-content-siang/malam crons (retired 2026-10-20).

## The 4 agents

1. **Scout** (`scout.py`) — ingests RSS into `news.db` (SQLite, dedupe by URL).
   8 feeds, AI-focused, mixed ID+EN:
   - EN: TechCrunch AI, The Verge, Ars Technica, MIT Tech Review, Google Blog, OpenAI Blog
   - ID: CNN Indonesia Tech, Antara Tekno
   - Dropped (dead/empty/blocked): VentureBeat, DetikInet, Kompas Tekno, Liputan6 Tekno
2. **Filter** (`filter.py`) — viral score 0-100 per unused item:
   recency 30 + AI-keyword relevance 35 + source tier 15 + hook signals 20.
   `filter.py --top N` prints top N as JSON. Mark used: UPDATE items SET used=1 WHERE id=?
3. **Writer** — the cron worker (AI): headline ID (<=90ch), sub-headline, 3-4 points,
   Threads (<=500ch, ends with exactly #AI), IG caption + hashtags, FB text,
   blog JSON. Natural Peka voice, no em/en-dash, anti AI-slop, facts only from source.
4. **Designer** (`designer.py`) — 2K (2048x2048) carousel PNGs, Peka header standard
   (yellow badge top-left, mascot lockup + peka.ai.id top-right). Cover =
   AI-generated cinematic visual (full-bleed + bottom scrim) with headline
   overlay; source URL rendered on cover (wrap_url breaks at / and -).
   Detail slides reuse the same visual heavily dimmed (72% black) as cover
   background with bullet text overlaid. Adaptive cover layout: headline
   auto-shrinks so nothing overlaps the footer.
   Always visually verify the cover before posting. Visuals generated per-topic
   via media.generate_image (dark tech aesthetic, yellow accents, no text).
   Layout: cover TETAP `frame` (keputusan user 2026-10-20), badge TETAP `ghost`
   (keputusan user 2026-10-20: kotak transparan outline kuning, teks kuning),
   `--detail-style` = dim|cards; `auto` (default) rotates detail daily by day-of-year.
   Cover TIDAK menampilkan URL (keputusan user 2026-10-20, biar tidak ramai):
   hanya nama sumber + tombol kuning "GESER →" di bawah.
   Header lockup TERKUNCI (keputusan user 2026-10-20, "konsisten untuk kedepannya"):
   top-right, vertical center cy=95 sejajar badge, tepi kanan teks x=1010,
   maskot tinggi 46, gap maskot-teks 12, teks 34px bold kuning; alignment
   vertikal dihitung dari font metrics + optical nudge antena 3% (lihat
   konstanta LOCKUP_* di designer.py). Jangan ubah tanpa perintah user.
   text_block() never overflows and never cuts a sentence
   mid-way (sub shown whole or dropped; headline auto-shrinks).
   via media.generate_image (dark tech aesthetic, yellow accents, no text).

## Cron

`peka-hm-daily` — daily ~09:36 WIB (flexible_time shifted 09:00), full-auto:
scout -> filter -> writer -> designer -> post IG carousel + Threads carousel +
FB Page -> blog JSON sync -> posted.log -> report to side chat.

Note: Threads/FB posts always pop a user approval card (platform rule, cannot
be bypassed). The run waits for the tap; IG may be granted a lasting allow
by the user in Settings.

Durable caption files: keep captions in the goal workspace
(goals/peka-ai-public-brand/hidden_files/hm-YYYY-MM-DD/), NOT in /tmp —
a platform service restart wiped /tmp mid-run on 2026-10-20 (captions lost;
had to rewrite and re-verify no double-post before retrying). Verify via
instagram-cli posts / threads-cli profile-threads / facebook-cli pages posts
list that nothing went out before any retry.

## Layout

- `hm/venv/` — python venv (feedparser)
- `hm/news.db` — SQLite items (url UNIQUE, used flag, score)
- `hm/out/YYYY-MM-DD/` — carousel PNGs per run
- `hm/review/` — reserved for manual review mode (currently unused, full-auto)

## ATURAN SHORTLINK (terkunci, perintah user 27 Okt 2026)

Mulai sekarang, SEMUA link yang akan dishare di edisi Homeless Media WAJIB
dipendekkan dulu lewat shortlink Peka (s.peka.ai.id) SEBELUM masuk ke desain
dan caption. Berlaku untuk semua permukaan: slide carousel, caption IG,
rantai Threads, teks FB, dan blog.

Cara kerja di tiap run HM:

1. Kumpulkan dulu semua link yang akan dishare di edisi itu (link sumber
   berita, link blog Peka, dan link lain apa pun yang tampil ke publik).
2. Pendekkan tiap link lewat API shortlink lokal:
   `POST http://127.0.0.1:8095/api/shorten` dengan body
   `{"url": "<url-panjang>", "slug": "<slug-bebas-opsional>"}`.
   Pakai jalur tamu lokal (limit 5 link/IP/hari di bucket localhost, cukup
   untuk 1-2 link per edisi). Simpan pasangan url-panjang -> short-url di
   folder out edisi itu (misalnya `shortlinks.json`) agar bisa dilacak.
3. Yang tampil di desain (teks slide) dan caption (IG/Threads/FB/blog)
   HANYALAH versi pendek s.peka.ai.id. URL panjang TIDAK BOLEH tampil ke
   publik di edisi HM mana pun.
4. Bila API shortlink gagal atau limit tercapai, run BERHENTI sebelum
   posting dan laporkan ke user. Jangan posting dengan URL panjang sebagai
   jalan pintas.

Aturan ini berlaku mulai edisi HM berikutnya setelah reaktivasi 2 Nov 2026
(HM sedang jeda 26 Okt-1 Nov) dan seterusnya, kecuali user mengubahnya.
