#!/usr/bin/env python3
"""Create admin-owned shortlink for the Coba Dulu 2026-11-25 edition (Cleanup.pictures).
Direct DB insert into s.peka.ai.id links table, user_id 1 (admin)."""
import json
import secrets
import sqlite3
import string
from pathlib import Path

DB = "/home/hatch/workspace/peka-shortlink/data/shortlink.db"
OUT = Path("/home/hatch/workspace/peka-content/coba-dulu/out/2026-11-25-cleanup-pictures-hapus-objek-foto")
BLOG_LONG = "https://blog.peka.ai.id/p/cleanup-pictures-hapus-objek-foto"
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

blog_code = make_code(BLOG_LONG)
data = {
    "blog": {"code": blog_code, "short": f"https://s.peka.ai.id/{blog_code}", "target_url": BLOG_LONG}
}
(OUT / "shortlinks.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
print(json.dumps(data, indent=1, ensure_ascii=False))
