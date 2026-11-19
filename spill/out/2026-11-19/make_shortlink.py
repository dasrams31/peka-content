#!/usr/bin/env python3
"""Create admin-owned shortlinks for SPILL #30 (CLAUDE, 2026-11-19).
Direct DB insert into s.peka.ai.id links table, user_id 1 (admin).
NOTE: first batch (ECC, cc-switch, agentic-awesome-skills, gamedev-agent-skills,
awesome-claude-code-toolkit) was created then discarded: those repos were already
in posted.log under other agents. Final batch below is the one used.
"""
import json
import secrets
import sqlite3
import string
from pathlib import Path

DB = "/home/hatch/workspace/peka-shortlink/data/shortlink.db"
OUT = Path("/home/hatch/workspace/peka-content/spill/out/2026-11-19")
TARGETS = [
    "https://github.com/emilkowalski/skills",
    "https://github.com/NVIDIA/SkillSpector",
    "https://github.com/titanwings/distilly",
    "https://github.com/Jeffallan/claude-skills",
    "https://github.com/elementalsouls/Claude-BugHunter",
]
ALPHABET = string.ascii_letters + string.digits

conn = sqlite3.connect(DB)
cur = conn.cursor()

def make_code(target):
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
        (code, target),
    )
    conn.commit()
    return code

data = {}
for t in TARGETS:
    code = make_code(t)
    data[t] = f"https://s.peka.ai.id/{code}"
(OUT / "shortlinks.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
print(json.dumps(data, indent=1, ensure_ascii=False))
