#!/usr/bin/env python3
"""Create admin-owned shortlinks for the Coba Dulu 2026-11-27 edition (Pollinations).
Direct DB insert into s.peka.ai.id links table, user_id 1 (admin)."""
import json
import secrets
import sqlite3
import string
from pathlib import Path

DB = "/home/hatch/workspace/peka-shortlink/data/shortlink.db"
OUT = Path("/home/hatch/workspace/peka-content/coba-dulu/out/2026-11-27-pollinations-bikin-ilustrasi-dari-teks")

TARGETS = {
    "blog": "https://blog.peka.ai.id/p/pollinations-bikin-ilustrasi-dari-teks",
    "tool": "https://pollinations.ai/",
    "contoh_robot": "https://image.pollinations.ai/prompt/a%20cute%20yellow%20robot%20mascot%20watering%20a%20small%20green%20plant%2C%20flat%20vector%20illustration%2C%20plain%20dark%20background?width=1024&height=1024&seed=7&nologo=true",
    "contoh_kedai": "https://image.pollinations.ai/prompt/a%20cozy%20Indonesian%20coffee%20shop%20at%20sunrise%2C%20warm%20morning%20light%2C%20flat%20vector%20illustration%2C%20clean%20simple%20shapes?width=1024&height=1024&seed=7&nologo=true",
}
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
for key, target in TARGETS.items():
    code = make_code(target)
    data[key] = {"code": code, "short": f"https://s.peka.ai.id/{code}", "target_url": target}

(OUT / "shortlinks.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
print(json.dumps(data, indent=1, ensure_ascii=False))
