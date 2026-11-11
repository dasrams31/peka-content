#!/usr/bin/env python3
"""Create one admin-owned shortlink for the Claude Fable 5.2 special edition (2026-11-12).

Direct DB insert into s.peka.ai.id links table, user_id 1 (admin).
Verifies the code is unique, then prints the code + short URL.
"""
import secrets
import sqlite3
import string

DB = "/home/hatch/workspace/peka-shortlink/data/shortlink.db"
TARGET = "https://www.anthropic.com/claude-fable-and-mythos-5-2"
ALPHABET = string.ascii_letters + string.digits

conn = sqlite3.connect(DB)
cur = conn.cursor()
for _ in range(20):
    code = "".join(secrets.choice(ALPHABET) for _ in range(6))
    cur.execute("SELECT 1 FROM links WHERE code = ?", (code,))
    if cur.fetchone() is None:
        break
else:
    raise SystemExit("could not find a unique code")

cur.execute(
    "INSERT INTO links (user_id, ip_hash, code, target_url, is_active, clicks)"
    " VALUES (1, '12ca17b49af2289436f303e0166030a2', ?, ?, 1, 0)",
    (code, TARGET),
)
conn.commit()
print(f"code={code}")
print(f"shortlink=https://s.peka.ai.id/{code}")
print(f"target={TARGET}")
