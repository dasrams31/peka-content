#!/usr/bin/env python3
"""Create an admin-owned shortlink for a Tutorial Agent Peka edition.

Direct DB insert into s.peka.ai.id links table, user_id 1 (admin).
Usage: python3 make_shortlink.py <out_dir> <target_url> [--key blog]
Writes/updates <out_dir>/shortlinks.json and verifies the redirect
with a bot user-agent (bots get a 307, browsers get the interstitial).
"""
import json
import os
import secrets
import sqlite3
import string
import subprocess
import sys

DB = "/home/hatch/workspace/peka-shortlink/data/shortlink.db"
ALPHABET = string.ascii_letters + string.digits


def make_code(cur, conn, target):
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


def main():
    out_dir, target = sys.argv[1], sys.argv[2]
    key = "blog"
    if "--key" in sys.argv:
        key = sys.argv[sys.argv.index("--key") + 1]
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    code = make_code(cur, conn, target)
    conn.close()
    short = f"https://s.peka.ai.id/{code}"
    path = os.path.join(out_dir, "shortlinks.json")
    data = {}
    if os.path.exists(path):
        data = json.load(open(path, encoding="utf-8"))
    data[key] = short
    data[key + "_long"] = target
    data["code"] = code
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    # verify redirect (bot UA gets 307 + Location)
    r = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code} %{redirect_url}",
         "-A", "TelegramBot (like TwitterBot)", short],
        capture_output=True, text=True)
    print(f"shortlink: {short} -> {target}")
    print(f"redirect check: {r.stdout.strip()}")
    assert r.stdout.strip().startswith("307"), "redirect bukan 307"
    assert target in r.stdout, "redirect tidak mengarah ke target"


if __name__ == "__main__":
    main()
