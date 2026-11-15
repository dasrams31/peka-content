"""Peka katalog sold-out pruner (perintah user 15 Nov 2026).

Every run: fetch the bot's live ready list (same source as the 08:00
digest, via probe_ready_json.py on the old server) and remove from
prices.json any entry whose bot_id is NOT in that ready list — i.e. the
product is sold out, inactive, or deleted. Removed entries go to
pruned.json (full entry + removal date) so a later restock can be
re-added deliberately and manual removals stay respected.

Rules:
- Entries without bot_id are NEVER auto-removed (only counted).
- If the ready fetch fails or returns a suspiciously small list (<5),
  abort with no changes: an empty ready list must never wipe the katalog.
- Only writes prices.json when something was actually pruned (and bumps
  `updated` to today). The peka-katalog-watch rebuilds slides on the
  next tick when prices.json changes.
- Prints PRUNED <names> or NO_CHANGE. --dry-run prints what WOULD be
  pruned and changes nothing.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

KATALOG = "/home/hatch/workspace/peka-content/katalog"
PRICES = os.path.join(KATALOG, "prices.json")
LEDGER = os.path.join(KATALOG, "pruned.json")
PROBE_LOCAL = "/home/hatch/workspace/aeternum/katalog/auto/probe_ready_json.py"

KEY = "/home/hatch/workspace/9router-setup/ssh/tunnel_9router"
KNOWN_HOSTS = "/home/hatch/workspace/9router-setup/ssh/known_hosts"
REMOTE = "ubuntu@43.156.63.114"
REMOTE_PROBE = "/tmp/probe_ready_json.py"
REMOTE_CWD = "/home/ubuntu/aeternum-premiapp-bot"

SSH_ENV = {
    "http_proxy": "",
    "https_proxy": "",
    "HTTP_PROXY": "",
    "HTTPS_PROXY": "",
}
SSH_BASE = [
    "ssh", "-i", KEY, "-o", "IdentitiesOnly=yes",
    "-o", f"UserKnownHostsFile={KNOWN_HOSTS}",
    "-o", "ProxyCommand=none", REMOTE,
]


def fetch_ready_ids():
    subprocess.run(
        ["scp", "-i", KEY, "-o", "IdentitiesOnly=yes",
         "-o", f"UserKnownHostsFile={KNOWN_HOSTS}",
         "-o", "ProxyCommand=none",
         PROBE_LOCAL, f"{REMOTE}:{REMOTE_PROBE}"],
        check=True, env={**os.environ, **SSH_ENV},
        capture_output=True, text=True,
    )
    res = subprocess.run(
        SSH_BASE + [
            f"cd {REMOTE_CWD} && PYTHONPATH={REMOTE_CWD}"
            f" venv/bin/python {REMOTE_PROBE}"
        ],
        check=True, env={**os.environ, **SSH_ENV},
        capture_output=True, text=True, timeout=120,
    )
    return {int(p["id"]) for p in json.loads(res.stdout)}


def main():
    dry_run = "--dry-run" in sys.argv
    try:
        ready = fetch_ready_ids()
    except Exception as exc:  # noqa: BLE001 - probe failure must not prune
        print(f"FAIL: could not fetch ready list: {exc}")
        return 1
    if len(ready) < 5:
        print(f"FAIL: ready list suspiciously small ({len(ready)} ids), aborting")
        return 1

    data = json.loads(open(PRICES, encoding="utf-8").read())
    products = data["products"]
    kept, removed, no_id = [], [], 0
    for p in products:
        bot_id = p.get("bot_id")
        if bot_id is None:
            no_id += 1
            kept.append(p)
        elif int(bot_id) in ready:
            kept.append(p)
        else:
            removed.append(p)

    if not removed:
        print(f"NO_CHANGE: {len(kept)} entries, all in stock"
              + (f", {no_id} without bot_id (skipped)" if no_id else ""))
        return 0

    names = [f"{p['name']} {p['dur']} ({p['price']}, bot {p['bot_id']})"
             for p in removed]
    if dry_run:
        print("DRY-RUN would prune:")
        for n in names:
            print(" -", n)
        return 0

    today = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")
    ledger = []
    if os.path.exists(LEDGER):
        ledger = json.loads(open(LEDGER, encoding="utf-8").read())
    for p in removed:
        ledger.append({**p, "removed_at": today, "reason": "sold out"})
    with open(LEDGER, "w", encoding="utf-8") as fh:
        json.dump(ledger, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    data["products"] = kept
    data["updated"] = today
    with open(PRICES, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    print(f"PRUNED {len(removed)} sold-out entr{'y' if len(removed) == 1 else 'ies'}:")
    for n in names:
        print(" -", n)
    print(f"prices.json now {len(kept)} entries; ledger {LEDGER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
