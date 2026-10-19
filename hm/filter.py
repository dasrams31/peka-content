#!/usr/bin/env python3
"""Peka Homeless Media - Filter: score unused news items for viral potential.

Scoring (0-100):
  recency      0-30  (fresher = higher)
  ai_relevance 0-35  (AI keyword hits, title weighted 2x)
  source       0-15  (source authority tier)
  hook         0-20  (click-worthy title signals)

Usage:
    venv/bin/python filter.py           # score all unused, print top 10
    venv/bin/python filter.py --top 3   # print top 3 as JSON
"""
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone

DB = "/home/hatch/workspace/peka-content/hm/news.db"

AI_KEYWORDS = [
    "artificial intelligence", "kecerdasan buatan", "machine learning",
    "ai agent", "agentic", "chatgpt", "gpt-", "gemini", "claude", "copilot",
    "deepseek", "llama", "mistral", "openai", "anthropic", "deepmind",
    "neural", "llm", "chatbot", "deepfake", "generative ai", "gen ai",
    "diffusion", "transformer", "robot", "humanoid", "automation",
    "otomatisasi", "prompt", "rag", "vector database", "tiktok ai",
]

SOURCE_TIER = {
    "TechCrunch AI": 15,
    "The Verge": 13,
    "MIT Tech Review": 13,
    "Ars Technica": 12,
    "Google Blog": 11,
    "OpenAI Blog": 11,
    "CNN Indonesia Tech": 10,
    "Antara Tekno": 9,
}

HOOK_SIGNALS = [
    (r"\d+(\.\d+)?\s*(x|kali|persen|%|juta|miliar|triliun)", 5),  # numbers
    (r"\b(gratis|free|tanpa bayar)\b", 5),
    (r"\b(baru|new|perdana|pertama kali|launch|rilis)\b", 4),
    (r"\?", 4),
    (r"\b(vs|versus|melawan|dibanding)\b", 4),
    (r"\b(cara|how to|panduan|tips|tutorial)\b", 4),
    (r"\b(terbesar|tercepat|termurah|terbaik|rekor|pecah)\b", 4),
    (r"\b(bocor|leak|rahasia|terungkap)\b", 5),
    (r"\b(phk|layoff|tutup|bangkrut|skandal)\b", 5),
]


def parse_dt(s):
    if not s:
        return None
    for fmt in (
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(s.strip()[:31], fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


def recency_score(pub):
    dt = parse_dt(pub)
    if not dt:
        return 10
    age_h = (datetime.now(timezone.utc) - dt).total_seconds() / 3600
    if age_h < 0:
        return 25  # future-dated, treat as fresh
    if age_h <= 6:
        return 30
    if age_h <= 12:
        return 22
    if age_h <= 24:
        return 15
    if age_h <= 48:
        return 8
    return 3


def ai_score(title, summary):
    t, s = title.lower(), (summary or "").lower()
    hits = sum(1 for k in AI_KEYWORDS if k in t)
    hits += sum(0.5 for k in AI_KEYWORDS if k in s and k not in t)
    return min(35, hits * 7)


def hook_score(title):
    t = title.lower()
    pts = sum(w for pat, w in HOOK_SIGNALS if re.search(pat, t))
    return min(20, pts)


def score_item(row):
    _id, title, summary, source, pub = row
    total = (
        recency_score(pub)
        + ai_score(title, summary)
        + SOURCE_TIER.get(source, 8)
        + hook_score(title)
    )
    return round(total, 1)


def main():
    con = sqlite3.connect(DB)
    rows = con.execute(
        "SELECT id,title,summary,source,published FROM items WHERE used=0"
    ).fetchall()
    scored = []
    for r in rows:
        sc = score_item(r)
        scored.append((sc,) + r)
    con.executemany("UPDATE items SET score=? WHERE id=?", [(s, i) for s, i, *_ in scored])
    con.commit()
    scored.sort(reverse=True)
    top_n = 10
    if "--top" in sys.argv:
        top_n = int(sys.argv[sys.argv.index("--top") + 1])
    out = [
        {"id": i, "score": s, "source": src, "title": t, "url": None, "published": p}
        for s, i, t, _sm, src, p in scored[:top_n]
    ]
    # attach urls
    ids = [o["id"] for o in out]
    if ids:
        urls = dict(
            con.execute(
                f"SELECT id,url FROM items WHERE id IN ({','.join('?'*len(ids))})", ids
            ).fetchall()
        )
        for o in out:
            o["url"] = urls.get(o["id"])
    con.close()
    if "--top" in sys.argv:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        print(f"[filter] scored {len(scored)} unused items")
        for o in out:
            print(f"  {o['score']:5.1f} [{o['source']}] {o['title'][:80]}")


if __name__ == "__main__":
    main()
