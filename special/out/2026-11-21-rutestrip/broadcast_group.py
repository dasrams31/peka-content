#!/usr/bin/env python3
"""Broadcast a Peka edition to the Peka Telegram GROUP (@peka_aigroup).

Mirror of telegram_channel.py, but for the group only. Same caption, same
cover, same anti-double discipline:
- Ledger type is "special-group" (or "<type>-group") so channel and group
  PENDING lines in broadcasts.log never cross-talk.
- PENDING line is written BEFORE sendPhoto; a failed send is verified live
  3x (Bot API getUpdates peek, then the t.me/s group page) at 60s intervals;
  if still unverified, NO auto-retry: the PENDING line holds resend until
  a manual check (delete the PENDING line or --force).
- Re-running after a confirmed send SKIP-s via the ledger (no double).
- --dry-run prints the caption + ledger key without sending or writing.

Usage:
  python3 broadcast_group.py --type special --title "..." --para "..." \
      --cover slide-01.png [--threads URL] [--instagram URL] \
      [--facebook URL] [--blog URL] [--dry-run] [--force]
"""
import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, "/home/hatch/workspace/peka-content")
import telegram_channel as tc

GROUP_ID = "-1001167087205"  # @peka_aigroup
GROUP_PAGE = "https://t.me/s/peka_aigroup"


def group_type(base_type: str) -> str:
    return f"{base_type}-group"


def find_in_group(markers):
    try:
        req = urllib.request.Request(GROUP_PAGE, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except Exception as e:
        print(f"Cek live grup gagal dibaca (dianggap belum ada): {e}", file=sys.stderr)
        return None
    segments = re.split(r'data-post="peka_aigroup/(\d+)"', raw)
    found = None
    for i in range(1, len(segments), 2):
        seg_text = tc._clean_page_text(segments[i + 1]) if i + 1 < len(segments) else ""
        if any(m in seg_text for m in markers):
            found = segments[i]
    return found


def verify_live_after_failure(token, args, markers, attempts=3, wait_secs=60):
    for attempt in range(attempts):
        if attempt:
            time.sleep(wait_secs)
        mid = tc.find_in_updates(token, GROUP_ID, markers)
        if mid:
            return mid
        mid = find_in_group(markers)
        if mid:
            return mid
    return None


def send_photo_group(token, caption, cover: Path):
    boundary = "----peka-group-boundary"
    photo = cover.read_bytes()
    body = b""
    for name, value in (
        ("chat_id", GROUP_ID),
        ("caption", caption),
        ("parse_mode", "HTML"),
    ):
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode("utf-8")
    body += (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; "
        f"filename=\"{cover.name}\"\r\nContent-Type: image/png\r\n\r\n"
    ).encode("utf-8") + photo + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        f"{tc.API_BASE}{token}/sendPhoto",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        return False, None, str(e)
    if not data.get("ok"):
        return False, None, f"Telegram menolak: {data}"
    return True, str(data["result"]["message_id"]), ""


def main() -> int:
    ap = argparse.ArgumentParser(description="Broadcast konten Peka ke grup Telegram.")
    ap.add_argument("--type", required=True, help="Tipe edisi (label caption ikut tipe ini).")
    ap.add_argument("--title", required=True)
    ap.add_argument("--para", default="")
    ap.add_argument("--cover", required=True)
    ap.add_argument("--threads", default="")
    ap.add_argument("--instagram", default="")
    ap.add_argument("--facebook", default="")
    ap.add_argument("--blog", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="Lewati cek dedupe (hanya untuk re-post atas perintah user).")
    args = ap.parse_args()

    # DISABLED 21 Nov (user rule): channel Peka ONCE only — the channel post
    # auto-forwards to the Peka group by itself, so a separate group send
    # doubles it (SPILL #31 lesson). This script refuses to send unless
    # --force is passed on the user's explicit order.
    if not args.force and not args.dry_run:
        print("DITOLAK: broadcast grup dimatikan (aturan user 21 Nov). Channel Peka "
              "sekali saja, postingannya auto-forward sendiri ke grup. Jangan "
              "pakai script ini tanpa perintah eksplisit user + --force.",
              file=sys.stderr)
        return 1

    cover = Path(args.cover)
    if not cover.is_file():
        print(f"Cover tidak ditemukan: {cover}", file=sys.stderr)
        return 2
    cap_args = SimpleNamespace(type=args.type, title=args.title, para=args.para,
                               threads=args.threads, instagram=args.instagram,
                               facebook=args.facebook, blog=args.blog)
    caption = tc.build_caption(cap_args)
    if len(caption) > 1024:
        print("Caption >1024 karakter, dipotong.", file=sys.stderr)
        caption = caption[:1020] + "…"

    gtype = group_type(args.type)
    key = f"{tc.wib_now().strftime('%Y-%m-%d')}|{gtype}|{args.title}"
    if args.dry_run:
        print(json.dumps({"chat_id": GROUP_ID, "ledger_key": key,
                          "caption": caption, "cover": str(cover)},
                         indent=2, ensure_ascii=False))
        return 0

    if not args.force:
        hit = tc.ledger_lookup(key)
        if hit:
            mid, url = hit
            print(f"SKIP already sent group message_id={mid} type={gtype} "
                  f"title={args.title[:60]} url={url} (ledger)")
            return 0
        pend = tc.ledger_pending(gtype, args.title)
        if pend:
            print(f"PENDING sejak {pend} WIB: kirim grup '{args.title[:60]}' "
                  "sebelumnya belum terverifikasi. JANGAN kirim ulang otomatis "
                  "- cek live di https://t.me/peka_aigroup dulu. Bila benar belum "
                  "terkirim, hapus baris PENDING di broadcasts.log atau jalankan "
                  "dengan --force.", file=sys.stderr)
            return 1
        markers = tc._markers(cap_args)
        live_mid = find_in_group(markers) if markers else None
        if live_mid:
            tc.ledger_append_raw(key, live_mid,
                                 f"https://t.me/peka_aigroup/{live_mid}", "found-live")
            print(f"SKIP already sent group message_id={live_mid} type={gtype} "
                  f"title={args.title[:60]} url=https://t.me/peka_aigroup/{live_mid} (live group)")
            return 0

    token = tc.read_token()
    tc.ledger_append_pending(key)
    ok, mid, err = send_photo_group(token, caption, cover)
    if ok:
        tc.ledger_append_raw(key, mid, f"https://t.me/peka_aigroup/{mid}", "sent")
        print(f"OK group message_id={mid} type={gtype} title={args.title[:60]}")
        return 0

    print(f"Gagal kirim ke grup: {err}", file=sys.stderr)
    print("Verifikasi live grup sebelum menyatakan gagal...", file=sys.stderr)
    markers = tc._markers(cap_args)
    found_mid = verify_live_after_failure(token, cap_args, markers)
    if found_mid:
        tc.ledger_append_raw(key, found_mid,
                             f"https://t.me/peka_aigroup/{found_mid}", "found-after-failure")
        print(f"OK group message_id={found_mid} type={gtype} title={args.title[:60]} "
              "(ditemukan di grup setelah kirim gagal, TIDAK dikirim ulang)")
        return 0
    print("BELUM TERVERIFIKASI di grup setelah 3x cek (Bot API + halaman "
          "live). JANGAN retry otomatis: pesan bisa saja sudah sampai tapi "
          "belum tampil di halaman. Cek manual di https://t.me/peka_aigroup "
          "- bila sudah ada, catat message_id-nya ke broadcasts.log; bila "
          "benar belum ada, hapus baris PENDING di broadcasts.log lalu retry.",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
