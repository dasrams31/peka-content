#!/usr/bin/env python3
"""Weekly Facebook strategy analyzer for Peka.

Reads performance.log (last 28 days) plus a live read of the newest
Facebook Page posts, computes median views/shares per (pillar, format),
compares against the previous state, writes fb-state.json, and appends
a dated verdict to learnings.md ONLY when a verdict changes
(new format winner, kill rule triggered, or format deviation found).

FB score definition (2026-11-17): FB is judged by views + shares.
Reactions are recorded but are NOT the target and NOT a verdict.
"""
import json
import os
import re
import statistics
import subprocess
from collections import defaultdict
from datetime import date, timedelta

BASE = os.path.dirname(os.path.abspath(__file__))
PERF_LOG = os.path.join(BASE, "performance.log")
STATE_PATH = os.path.join(BASE, "fb-state.json")
LEARNINGS_PATH = os.path.join(BASE, "learnings.md")
BLOG_DIR = os.path.join(BASE, "blog")
FB_PAGE_ID = "1399217353266190"

# Expected FB format per pillar (locked by fb-strategy.md).
FB_FORMAT_MAP = {
    "spill-repo": "carousel",
    "hm": "carousel",
    "prompt-harian": "reel",
    "gratisan-ai": "reel",
    "katalog": "carousel",
    "blueprint": "reel",
    "tutorial-mirror": "reel",
    "weekly-ai": "reel",
    "agent-tutorial": "reel",
    # bansos: either format allowed (photo proof -> carousel, else reel)
}

# Pillars whose FB format is locked by a user order (HM: 6 Nov carousel +
# benchmark reel extra; katalog: 6 Nov carousel). The analyzer never
# proposes a format change for them; their lever is hook/CTA, not format.
LOCKED_FORMAT_PILLARS = {"hm", "katalog"}

# Pillars that no longer air. Never a verdict target.
DEAD_PILLARS = {"pancingan"}
SLUG_PILLAR = [
    ("spill-repo", "spill-repo"),
    ("prompt-harian", "prompt-harian"),
    ("gratisan", "gratisan-ai"),
    ("katalog", "katalog"),
    ("blueprint", "blueprint"),
    ("ai-pekan-ini", "weekly-ai"),
    ("tutorial-agent", "agent-tutorial"),
    ("membuat-chatbot", "tutorial-mirror"),
    ("query-agregat", "tutorial-mirror"),
]


def parse_perf_log(days=28):
    """Return {(pillar, format): [(views, shares, likes), ...]} for FB rows."""
    cutoff = date.today() - timedelta(days=days)
    rows = defaultdict(list)
    if not os.path.exists(PERF_LOG):
        return rows
    with open(PERF_LOG, encoding="utf-8", errors="replace") as f:
        for line in f:
            p = line.strip().split("|")
            if len(p) < 7 or p[3] != "facebook":
                continue
            try:
                d = date.fromisoformat(p[0])
            except ValueError:
                continue
            if d < cutoff:
                continue
            lain = p[6]
            note = p[7] if len(p) > 7 else ""
            m = re.search(r"views=(\d+)", lain)
            s = re.search(r"shares=(\d+)", lain)
            lk = re.search(r"likes=(\d+)", p[4])
            txt = (note + " " + lain).lower()
            if "reel" in txt:
                fmt = "reel"
            elif "carousel" in txt or "foto" in txt:
                fmt = "carousel"
            else:
                fmt = "unknown"
            rows[(p[2], fmt)].append((
                int(m.group(1)) if m else 0,
                int(s.group(1)) if s else 0,
                int(lk.group(1)) if lk else 0,
            ))
    return rows


def summarize(rows):
    stats = {}
    for (pillar, fmt), vals in sorted(rows.items()):
        views = [v[0] for v in vals]
        shares = [v[1] for v in vals]
        stats[f"{pillar}|{fmt}"] = {
            "pillar": pillar,
            "format": fmt,
            "n": len(vals),
            "views_median": statistics.median(views),
            "views_max": max(views),
            "shares_median": statistics.median(shares),
            "shares_max": max(shares),
            "likes_total": sum(v[2] for v in vals),
        }
    return stats


def live_fb_check():
    """Best-effort live read of the 10 newest FB posts. Never fatal."""
    try:
        out = subprocess.run(
            ["/opt/hatch/bin/facebook-cli", "pages", "posts", "list",
             "--page-id", FB_PAGE_ID, "--limit", "10"],
            capture_output=True, text=True, timeout=90,
        )
        text = out.stdout or ""
        reactions = text.count("reactions: 0") + text.count("reactions:0")
        return {"ok": out.returncode == 0, "raw_chars": len(text),
                "zero_reaction_mentions": reactions}
    except Exception as e:  # noqa: BLE001 - live check must never kill the run
        return {"ok": False, "error": str(e)}


def format_guard():
    """Check recent blog JSONs: does the FB link type match the map?

    A facebook.com/reel/ link means a reel was posted; any other FB
    post URL means a carousel/photo post. Returns deviation strings.
    """
    deviations = []
    cutoff = date.today() - timedelta(days=7)
    if not os.path.isdir(BLOG_DIR):
        return deviations
    for name in os.listdir(BLOG_DIR):
        if not name.endswith(".json"):
            continue
        path = os.path.join(BLOG_DIR, name)
        try:
            if date.fromtimestamp(os.path.getmtime(path)) < cutoff:
                continue
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:  # noqa: BLE001 - one bad file must not stop the guard
            continue
        slug = data.get("slug", "")
        fb = (data.get("links") or {}).get("facebook", "")
        if not fb:
            continue
        pillar = None
        for prefix, p in SLUG_PILLAR:
            if slug.startswith(prefix):
                pillar = p
                break
        if pillar is None or pillar not in FB_FORMAT_MAP:
            continue
        # Only a /reel/ URL proves a reel was posted. Bare-ID FB URLs
        # (https://www.facebook.com/<id>) are used for BOTH reels and
        # carousel posts (Prompt reels are stored that way), so they prove
        # nothing. Only flag a proven deviation: a reel posted where the
        # map says carousel.
        expected = FB_FORMAT_MAP[pillar]
        if expected == "carousel" and "/reel/" in fb:
            deviations.append(
                f"{slug} ({pillar}): FB posted as reel, map says {expected}")
    return deviations


def append_learning(lines):
    """Append a dated FB verdict block to learnings.md."""
    block = "\n## FACEBOOK (otomatis, fb_analyzer.py) - %s\n%s\n" % (
        date.today().isoformat(),
        "\n".join("- " + line for line in lines),
    )
    with open(LEARNINGS_PATH, "a", encoding="utf-8") as f:
        f.write(block)


def main():
    rows28 = parse_perf_log(28)
    rows7 = parse_perf_log(7)
    stats28 = summarize(rows28)
    stats7 = summarize(rows7)
    prev = {}
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH, encoding="utf-8") as f:
                prev = json.load(f)
        except Exception:  # noqa: BLE001 - corrupt state restarts clean
            prev = {}
    prev_verdicts = set(prev.get("verdicts", []))
    prev_kill_streak = prev.get("kill_streak", {})

    verdicts = []
    kill_streak = {}

    # Promote rule: one format's median views >= 2x the pillar's other
    # format, n >= 3 for the winner.
    by_pillar = defaultdict(dict)
    for key, st in stats28.items():
        by_pillar[st["pillar"]][st["format"]] = st
    for pillar, fmts in by_pillar.items():
        if pillar in LOCKED_FORMAT_PILLARS:
            continue
        if "reel" in fmts and "carousel" in fmts:
            r, c = fmts["reel"], fmts["carousel"]
            if r["n"] >= 3 and r["views_median"] >= 2 * max(c["views_median"], 1):
                verdicts.append(
                    f"PROMOTE {pillar}: reel median {r['views_median']:.0f} views "
                    f"(n={r['n']}) >= 2x carousel {c['views_median']:.0f}; "
                    f"reel jadi format FB default {pillar}")
            if c["n"] >= 3 and c["views_median"] >= 2 * max(r["views_median"], 1):
                verdicts.append(
                    f"PROMOTE {pillar}: carousel median {c['views_median']:.0f} views "
                    f"(n={c['n']}) >= 2x reel {r['views_median']:.0f}; "
                    f"carousel jadi format FB default {pillar}")

    # Kill rule: a format is killed only when it is the LOSER of its
    # pillar: another format of the same pillar beats it by >= 2x on
    # median views, and the loser sits below 10 median views in 2
    # consecutive weekly reads (streak tracked in state). This mirrors
    # the promote rule, so the winner is never killed. "unknown" format
    # rows (old log lines without a format note) and dead pillars are
    # never killed.
    for key, st in stats28.items():
        if st["pillar"] in LOCKED_FORMAT_PILLARS or st["pillar"] in DEAD_PILLARS:
            continue
        if st["format"] == "unknown":
            kill_streak[key] = 0
            continue
        beaten = False
        for other in by_pillar.get(st["pillar"], {}).values():
            if other["format"] == st["format"] or other["format"] == "unknown":
                continue
            if other["n"] >= 2 and other["views_median"] >= 2 * max(st["views_median"], 1):
                beaten = True
        if st["n"] >= 3 and st["views_median"] < 10 and beaten:
            streak = prev_kill_streak.get(key, 0) + 1
            kill_streak[key] = streak
            if streak >= 2:
                verdicts.append(
                    f"KILL {key}: median views {st['views_median']:.0f} "
                    f"(n={st['n']}) kalah >= 2x dari format lain pilar yang sama "
                    f"dan di bawah 10 dua minggu berturut-turut; "
                    f"hentikan format ini di FB {st['pillar']}")
        else:
            kill_streak[key] = 0

    # Format guard deviations.
    for dev in format_guard():
        verdicts.append(f"DEVIASI FORMAT: {dev}")

    live = live_fb_check()
    state = {
        "date": date.today().isoformat(),
        "stats_28d": stats28,
        "stats_7d": stats7,
        "verdicts": verdicts,
        "kill_streak": kill_streak,
        "live_fb": live,
    }
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    new_verdicts = [v for v in verdicts if v not in prev_verdicts]
    if new_verdicts:
        append_learning(new_verdicts)

    print(f"FB analyzer {date.today().isoformat()}: "
          f"{len(stats28)} (pilar, format) 28 hari, "
          f"{len(verdicts)} vonis ({len(new_verdicts)} baru), "
          f"live FB ok={live.get('ok')}")
    for key in sorted(stats28):
        st = stats28[key]
        print(f"  {key}: n={st['n']} views med={st['views_median']:.0f} "
              f"max={st['views_max']} shares med={st['shares_median']:.0f} "
              f"max={st['shares_max']} likes tot={st['likes_total']}")
    for v in verdicts:
        print(f"  VONIS: {v}")
    if not verdicts:
        print("  Tidak ada vonis baru minggu ini.")


if __name__ == "__main__":
    main()
