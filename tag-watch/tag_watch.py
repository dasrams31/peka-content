#!/usr/bin/env python3
"""Daily tag + FYP caption learner for Peka (user order 2026-10-30).

Collects a small daily sample of top Threads posts per candidate tag
(threads-cli search returns only a couple of posts per query, so the
signal is the 7-day rolling aggregate, never one day alone), stores
samples in samples.jsonl, and rewrites tag-watch.md + fyp-learning.md.

Rules:
- Read-only: never posts, never edits captions. The CURRENT CLOSING TAG
  in tag-watch.md is applied by content crons automatically under the
  user's full-autonomy grant (2026-10-30); it only moves off #AI on
  7-day evidence (another tag >= 2x #AI average likes, n>=10 both).
- Tolerant: a failed search or empty trends result is recorded as
  such; the script never fails the cron run over missing data.
"""
import json
import os
import re
import statistics
import subprocess
import sys
from datetime import datetime, timedelta, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
SAMPLES = os.path.join(BASE, "samples.jsonl")
WATCH_MD = os.path.join(BASE, "tag-watch.md")
FYP_MD = os.path.join(BASE, "fyp-learning.md")
ACCOUNT_ID = "17841417164011141"
TAGS = ["AI", "Teknologi", "BelajarAI", "Mahasiswa", "Coding",
        "ChatGPT", "Belajar", "Kuliah", "Gemini", "Python"]
WIB = timezone(timedelta(hours=7))

DAY_RE = re.compile(r"\bday\s*\d+", re.IGNORECASE)
STORY_WORDS = ("gue ", "gua ", "saya ", "aku ", "cerita", "pengalaman")


def run_search(tag):
    cmd = ["/opt/hatch/bin/threads-cli", "search",
           "--account-id", ACCOUNT_ID, "--query", f"#{tag}", "--first", "20"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        data = json.loads(out.stdout)
    except Exception:
        return []
    posts = []
    edges = data.get("data", {}).get("searchResults", {}).get("edges", [])
    for edge in edges:
        for item in edge.get("node", {}).get("thread", {}).get("thread_items", []):
            post = item.get("post") or {}
            if post.get("pk"):
                posts.append(post)
    return posts


def run_trends():
    cmd = ["/opt/hatch/bin/threads-cli", "trends", "--account-id", ACCOUNT_ID]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        data = json.loads(out.stdout)
        edges = data.get("data", {}).get("trends", {}).get("edges", [])
        return [e for e in edges if e]
    except Exception:
        return []


def load_samples():
    rows = []
    if os.path.exists(SAMPLES):
        with open(SAMPLES, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    return rows


def caption_features(caption):
    text = caption or ""
    lower = text.lower()
    tags = re.findall(r"#\w+", text)
    return {
        "day_counter": bool(DAY_RE.search(text)),
        "has_question": "?" in text,
        "ends_question": text.strip().endswith("?"),
        "story": any(w in lower for w in STORY_WORDS),
        "breaking": lower.lstrip().startswith("breaking"),
        "hashtags": len(tags),
        "words": len(text.split()),
        "chars": len(text),
    }


def main():
    today = datetime.now(WIB).date().isoformat()
    existing = load_samples()
    seen = {(r["tag"], r["post_id"]) for r in existing}
    new_rows = []
    per_tag_today = {}
    for tag in TAGS:
        posts = run_search(tag)
        per_tag_today[tag] = len(posts)
        for post in posts:
            key = (tag, str(post.get("pk")))
            if key in seen:
                continue
            seen.add(key)
            info = post.get("text_post_app_info", {}) or {}
            caption = (post.get("caption") or {}).get("text", "")
            new_rows.append({
                "date": today,
                "tag": tag,
                "post_id": str(post.get("pk")),
                "username": (post.get("user") or {}).get("username", ""),
                "likes": int(post.get("like_count") or 0),
                "reposts": int(info.get("repost_count") or 0),
                "replies": int(info.get("direct_reply_count") or 0),
                "taken_at": int(post.get("taken_at") or 0),
                "caption": caption,
            })
    if new_rows:
        with open(SAMPLES, "a", encoding="utf-8") as fh:
            for row in new_rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        existing.extend(new_rows)
    trends = run_trends()

    # Rolling 7-day stats per tag.
    cutoff = (datetime.now(WIB).date() - timedelta(days=6)).isoformat()
    recent = [r for r in existing if r["date"] >= cutoff]
    stats = []
    for tag in TAGS:
        rows = [r for r in recent if r["tag"] == tag]
        if not rows:
            stats.append((tag, 0, 0.0, 0, 0.0, 0.0, 0))
            continue
        likes = [r["likes"] for r in rows]
        stats.append((tag, len(rows), statistics.mean(likes),
                      statistics.median(likes),
                      statistics.mean([r["reposts"] for r in rows]),
                      statistics.mean([r["replies"] for r in rows]),
                      max(likes)))
    stats.sort(key=lambda s: (-s[2], -s[1]))

    # CURRENT CLOSING TAG (autonomous, user grant 2026-10-30): #AI stays
    # unless another tag beats it by 2x on 7-day average likes with n>=10
    # samples on both sides. The script owns this decision; content crons
    # read it from tag-watch.md. Every change is logged in tag-changes.log.
    by_tag = {s[0]: s for s in stats}
    ai_stat = by_tag.get("AI")
    current_tag, current_reason = "AI", "default: not enough samples yet (need n>=10 per tag)"
    if ai_stat and ai_stat[1] >= 10:
        contenders = [s for s in stats if s[0] != "AI" and s[1] >= 10]
        best = max(contenders, key=lambda s: s[2], default=None)
        if best and best[2] >= 2 * ai_stat[2]:
            current_tag = best[0]
            current_reason = (f"7-day avg likes {best[2]:.1f} (n={best[1]}) >= 2x "
                              f"#AI {ai_stat[2]:.1f} (n={ai_stat[1]})")
        elif best:
            current_reason = (f"no tag beats #AI by 2x yet (best #{best[0]} "
                              f"{best[2]:.1f} vs #AI {ai_stat[2]:.1f})")
        else:
            current_reason = "no other tag has n>=10 yet"
    tag_state_file = os.path.join(BASE, "current_tag.txt")
    prev_tag = ""
    if os.path.exists(tag_state_file):
        prev_tag = open(tag_state_file, encoding="utf-8").read().strip()
    with open(tag_state_file, "w", encoding="utf-8") as fh:
        fh.write(current_tag + "\n")
    if prev_tag and prev_tag != current_tag:
        with open(os.path.join(BASE, "tag-changes.log"), "a", encoding="utf-8") as fh:
            fh.write(f"{today}: #{prev_tag} -> #{current_tag} ({current_reason})\n")

    # FYP caption patterns: top quartile by likes vs the rest (7-day pool).
    pool = sorted(recent, key=lambda r: -r["likes"])
    top_n = max(1, len(pool) // 4)
    top, rest = pool[:top_n], pool[top_n:]
    feats = []
    for label, group in (("TOP", top), ("REST", rest)):
        if not group:
            feats.append((label, 0, {}))
            continue
        f = [caption_features(r["caption"]) for r in group]
        feats.append((label, len(group), {
            "day_counter": sum(x["day_counter"] for x in f) / len(f),
            "has_question": sum(x["has_question"] for x in f) / len(f),
            "story": sum(x["story"] for x in f) / len(f),
            "hashtags_avg": statistics.mean([x["hashtags"] for x in f]),
            "words_avg": statistics.mean([x["words"] for x in f]),
        }))
    top_examples = [(r["tag"], r["likes"], r["username"],
                     r["caption"][:120].replace("\n", " ")) for r in top[:5]]

    def pct(x):
        return f"{x * 100:.0f}%"

    with open(WATCH_MD, "w", encoding="utf-8") as fh:
        fh.write("# Tag watch (Threads, rolling 7 days)\n\n")
        fh.write(f"Updated: {today} WIB. Sample: {len(recent)} posts in 7 days, "
                 f"{len(new_rows)} new today. Search returns only a few posts "
                 "per tag per day, so one day never ranks a tag alone.\n\n")
        fh.write(f"CURRENT CLOSING TAG: #{current_tag} ({current_reason}).\n")
        fh.write("Content crons apply this tag automatically (user granted full "
                 "autonomy 2026-10-30). Changes are logged in tag-changes.log.\n\n")
        fh.write("| Tag | n | avg likes | median | avg reposts | avg replies | max |\n")
        fh.write("|---|---|---|---|---|---|---|\n")
        for tag, n, avg, med, rep, rpl, mx in stats:
            fh.write(f"| #{tag} | {n} | {avg:.1f} | {med} | {rep:.1f} | {rpl:.1f} | {mx} |\n")
        fh.write("\n## Today\n\n")
        fh.write(", ".join(f"#{t}: {per_tag_today.get(t, 0)} posts" for t in TAGS) + ".\n\n")
        fh.write("## Trends endpoint\n\n")
        fh.write(f"{len(trends)} trending topics returned.\n")
        ranked = [s for s in stats if s[1] >= 10]
        if current_tag != "AI":
            fh.write(f"\nClosing tag is now #{current_tag}: {current_reason}.\n")
        elif ranked:
            fh.write(f"\nClosing tag stays #AI: {current_reason}.\n")
        else:
            fh.write("\nClosing tag stays #AI: not enough samples yet (need n>=10 per tag); "
                     "keep collecting daily.\n")

    section = [f"## {today}\n"]
    for label, n, f in feats:
        if n:
            section.append(
                f"- {label} (n={n}): day-counter {pct(f['day_counter'])}, "
                f"question {pct(f['has_question'])}, story {pct(f['story'])}, "
                f"hashtags avg {f['hashtags_avg']:.1f}, words avg {f['words_avg']:.0f}.")
    section.append("- Top posts today:")
    for tag, likes, user, cap in top_examples:
        section.append(f"  - #{tag} @{user} ({likes} likes): {cap}")
    section_text = "\n".join(section) + "\n"
    old = ""
    if os.path.exists(FYP_MD):
        old = open(FYP_MD, encoding="utf-8").read()
    header = ("# FYP caption learning (Threads top posts, rolling)\n\n"
              "Daily dated findings from the tag-watch collector. Patterns "
              "here are OBSERVED from sampled top posts, not rules. "
              "Caption decisions stay with the playbook + user approval.\n")
    old_sections = []
    if os.path.exists(FYP_MD):
        old = open(FYP_MD, encoding="utf-8").read()
        if old.startswith("# FYP"):
            old = old[len(header):]
        old_sections = [s for s in old.split("\n## ") if s.strip()]
    all_sections = [section_text.strip()] + ["## " + s.strip() for s in old_sections]
    # Drop a stale duplicate of today's section if the script reruns.
    deduped = []
    for s in all_sections:
        if s.startswith(f"## {today}") and deduped and deduped[0].startswith(f"## {today}"):
            continue
        deduped.append(s)
    with open(FYP_MD, "w", encoding="utf-8") as fh:
        fh.write(header + "\n" + "\n\n".join(deduped[:14]).strip() + "\n")
    print(f"done: {len(new_rows)} new samples, {len(recent)} in 7-day pool, "
          f"trends={len(trends)}")


if __name__ == "__main__":
    main()
