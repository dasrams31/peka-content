#!/usr/bin/env python3
"""Create admin-owned shortlink for AI Pekan Ini #01 (Bikin Skill Claude).
Direct DB insert into s.peka.ai.id links table, user_id 1 (admin).
Destination: official Anthropic skills repo (template + 19 example skills).
"""
import json
import secrets
import sqlite3
import string
from pathlib import Path

DB = "/home/hatch/workspace/peka-shortlink/data/shortlink.db"
OUT = Path("/home/hatch/workspace/peka-content/weekly-ai/out/2026-11-15-bikin-skill-claude-sendiri")
TARGET = "https://github.com/anthropics/skills"
ALPHABET = string.ascii_letters + string.digits

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Reuse an existing verified admin-owned link for the same destination.
cur.execute(
    "SELECT code FROM links WHERE target_url = ? AND user_id = 1 AND is_active = 1",
    (TARGET,),
)
row = cur.fetchone()
if row:
    code = row[0]
    print("reused existing code:", code)
else:
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
    print("created new code:", code)

data = {
    "repo": f"https://s.peka.ai.id/{code}",
    "repo_long": TARGET,
}
(OUT / "shortlinks.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
print(json.dumps(data, indent=1, ensure_ascii=False))
