#!/usr/bin/env python3
"""Peka Homeless Media - Scout: ingest AI news from RSS feeds into SQLite.

Usage:
    venv/bin/python scout.py            # fetch all feeds, store new items
    venv/bin/python scout.py --test     # report which feeds return entries
"""
import feedparser
import hashlib
import sqlite3
import sys
import time
from datetime import datetime, timezone

DB = "/home/hatch/workspace/peka-content/hm/news.db"

FEEDS = [
    # English - AI/tech
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
    ("MIT Tech Review", "https://www.technologyreview.com/feed/"),
    ("Google Blog", "https://blog.google/rss/"),
    ("OpenAI Blog", "https://openai.com/news/rss.xml"),
    # Indonesian - tech
    ("CNN Indonesia Tech", "https://www.cnnindonesia.com/teknologi/rss"),
    ("Antara Tekno", "https://www.antaranews.com/rss/tekno.xml"),
]


def init_db():
    con = sqlite3.connect(DB)
    con.execute(
        """CREATE TABLE IF NOT EXISTS items(
            id INTEGER PRIMARY KEY,
            url TEXT UNIQUE,
            url_hash TEXT,
            title TEXT,
            summary TEXT,
            source TEXT,
            published TEXT,
            fetched_at TEXT,
            used INTEGER DEFAULT 0,
            score REAL DEFAULT 0
        )"""
    )
    con.commit()
    return con


def fetch():
    con = init_db()
    now = datetime.now(timezone.utc).isoformat()
    total_new = 0
    for name, url in FEEDS:
        try:
            d = feedparser.parse(url, agent="PekaHM/1.0")
            added = 0
            for e in d.entries:
                link = (e.get("link") or "").strip()
                title = (e.get("title") or "").strip()
                if not link or not title:
                    continue
                h = hashlib.sha256(link.encode()).hexdigest()[:16]
                summary = (e.get("summary") or e.get("description") or "")[:500]
                pub = e.get("published") or e.get("updated") or ""
                try:
                    con.execute(
                        "INSERT OR IGNORE INTO items(url,url_hash,title,summary,source,published,fetched_at)"
                        " VALUES(?,?,?,?,?,?,?)",
                        (link, h, title, summary, name, pub, now),
                    )
                    if con.total_changes:
                        added += 1
                except sqlite3.IntegrityError:
                    pass
            con.commit()
            total_new += added
            print(f"[scout] {name}: {len(d.entries)} entries, {added} new")
        except Exception as ex:  # noqa: BLE001 - keep scout resilient per-feed
            print(f"[scout] {name}: ERROR {ex}")
        time.sleep(1)
    con.close()
    print(f"[scout] done, {total_new} new items total")


def test():
    for name, url in FEEDS:
        try:
            d = feedparser.parse(url, agent="PekaHM/1.0")
            n = len(d.entries)
            flag = "OK " if n else "EMPTY"
            print(f"[{flag}] {name}: {n} entries")
        except Exception as ex:  # noqa: BLE001
            print(f"[FAIL] {name}: {ex}")
        time.sleep(1)


if __name__ == "__main__":
    if "--test" in sys.argv:
        test()
    else:
        fetch()
