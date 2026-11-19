#!/usr/bin/env python3
"""Broadcast Katalog Peka (format baru, perintah user 19 Nov 2026) ke channel
Telegram @peka_aichannel — SATU-SATUNYA tempat katalog tayang.

Alasan format baru: katalog #6 (17 Nov 2026) kena removed Meta 18 Nov di
Facebook (404) dan Instagram (carousel hilang dari daftar post); Threads
ikut restricted (visibility private). Mulai 19 Nov: katalog TIDAK POSTING
ke Threads/IG/FB, TIDAK ada IG Story, TIDAK ada reel TikTok. Katalog hanya
muncul sebagai broadcast channel Telegram 2x seminggu (Selasa + Jumat 13:00).

Isi broadcast (2 pesan):
  1. Album foto: semua slide katalog (4096x4096) + caption singkat
     (hook + rentang harga + cara order + gabung komunitas).
  2. Pesan teks: daftar harga lengkap dari prices.json (sumber tunggal)
     + cara order + gabung komunitas + store.

Pengirim: bot @aeternum_premibot (administrator di @peka_aichannel),
token dibaca dari ~/workspace/mc-portal/config/telegram_premibot_token.

Penggunaan:
  python3 broadcast_katalog_telegram.py --folder <folder edisi auto-*> \
      --title "22 akun premium, mulai 2,2K aja." \
      --para "Ringkasan 2-4 kalimat: rentang harga + produk andalan edisi ini."
  --dry-run hanya mencetak payload tanpa mengirim.
  --force melewati cek dedupe (hanya untuk re-post atas perintah user).

ANTI-DOBEL (pelajaran 9 Nov 2026: broadcast dobel di channel):
- Album dan pesan daftar harga punya kunci dedupe sendiri-sendiri:
  tanggal WIB | katalog-album | title  dan  tanggal WIB | katalog-list | title.
- SEBELUM kirim tiap pesan, cek ledger DAN halaman live channel.
  Kalau sudah ada di salah satunya, JANGAN kirim, laporkan message_id
  yang sudah ada (baris SKIP) dan exit 0.
- Kalau kirim GAGAL karena koneksi putus, JANGAN langsung anggap gagal:
  pesan bisa saja sudah sampai sebelum koneksi putus. Verifikasi live
  1x; kalau ketemu, catat ke ledger dan anggap sukses. Hanya bila TIDAK
  ketemu, exit 1 (aman di-retry nanti, idempotent).
"""

import argparse
import html
import json
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path.home() / "workspace/peka-content"))
from telegram_channel import (  # noqa: E402
    API_BASE,
    CHANNEL_ID,
    WIB,
    broadcast_paused,
    find_in_channel,
    ledger_append,
    ledger_lookup,
    read_token,
)

PRICES = Path.home() / "workspace/peka-content/katalog/prices.json"
LEDGER_NOTE = "broadcast_katalog_telegram"


def wib_now() -> datetime:
    return datetime.now(WIB)


def load_prices() -> dict:
    return json.loads(PRICES.read_text())


def fmt_price_line(p: dict) -> str:
    return f"{p['name']} · {p['dur']} {p['price']}"


def build_list_text(products: list, date_label: str) -> str:
    """Daftar harga lengkap, dikelompokkan per seksi (urutan kemunculan
    pertama di prices.json)."""
    sections: dict[str, list] = {}
    for p in products:
        sections.setdefault(p["sec"], []).append(p)
    lines = [f"Daftar harga \u2014 Katalog Peka {date_label}", ""]
    for sec, items in sections.items():
        lines.append(f"<b>{html.escape(sec)}</b>")
        for p in items:
            lines.append(html.escape(fmt_price_line(p)))
        lines.append("")
    lines.append("Cara order: DM @aeternum_premibot, ketik MAU [nama produk].")
    lines.append("Gabung komunitas: s.peka.ai.id/gabung")
    lines.append("Store: store.peka.ai.id")
    return "\n".join(lines).strip()


def build_album_caption(title: str, para: str, n: int,
                        lo: float, hi: float) -> str:
    def rp(v: float) -> str:
        s = f"{v:g}".replace(".", ",")
        return f"{s}K"
    lines = ["\U0001f6cd\ufe0f Katalog Peka", "", f"<b>{html.escape(title)}</b>", ""]
    if para:
        lines.append(html.escape(para))
        lines.append("")
    lines.append(f"{n} akun premium, harga {rp(lo)} sampai {rp(hi)}. "
                 "Daftar lengkap ada di pesan berikut.")
    lines.append("")
    lines.append("Cara order: DM @aeternum_premibot, ketik MAU [nama produk].")
    lines.append("Gabung komunitas: s.peka.ai.id/gabung")
    return "\n".join(lines)


def _post_json(token: str, method: str, payload: dict):
    req = urllib.request.Request(
        f"{API_BASE}{token}/{method}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def send_media_group(token: str, photos: list, caption: str):
    """Kirim album foto. Kembalikan (ok, message_id pertama, error)."""
    boundary = "----peka-katalog-boundary"
    media = []
    body = b""
    for i, photo in enumerate(photos):
        name = f"slide{i + 1}"
        item = {"type": "photo", "media": f"attach://{name}"}
        if i == 0:
            item["caption"] = caption
            item["parse_mode"] = "HTML"
        media.append(item)
    body += (f"--{boundary}\r\nContent-Disposition: form-data; "
             f"name=\"chat_id\"\r\n\r\n{CHANNEL_ID}\r\n").encode("utf-8")
    body += (f"--{boundary}\r\nContent-Disposition: form-data; "
             f"name=\"media\"\r\n\r\n{json.dumps(media, ensure_ascii=False)}\r\n"
             ).encode("utf-8")
    for i, photo in enumerate(photos):
        name = f"slide{i + 1}"
        body += (f"--{boundary}\r\nContent-Disposition: form-data; "
                 f"name=\"{name}\"; filename=\"{photo.name}\"\r\n"
                 f"Content-Type: image/png\r\n\r\n").encode("utf-8")
        body += photo.read_bytes()
        body += b"\r\n"
    body += f"--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE}{token}/sendMediaGroup",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        return False, None, str(e)
    if not data.get("ok"):
        return False, None, f"Telegram menolak: {data}"
    msgs = data["result"]
    return True, str(msgs[0]["message_id"]), ""


def send_text(token: str, text: str):
    """Kirim pesan teks. Kembalikan (ok, message_id, error)."""
    try:
        data = _post_json(token, "sendMessage", {
            "chat_id": CHANNEL_ID,
            "text": text,
            "parse_mode": "HTML",
        })
    except Exception as e:
        return False, None, str(e)
    if not data.get("ok"):
        return False, None, f"Telegram menolak: {data}"
    return True, str(data["result"]["message_id"]), ""


def already_sent(key: str, marker_title: str):
    """Cek ledger + live channel untuk satu kunci. Kembalikan message_id
    bila sudah terkirim, None bila belum."""
    hit = ledger_lookup(key)
    if hit:
        return hit[0]
    ns = SimpleNamespace(title=marker_title, blog="", threads="",
                         instagram="", facebook="")
    live_mid = find_in_channel(ns)
    if live_mid:
        ledger_append(key, live_mid, f"{LEDGER_NOTE}-found-live")
        return live_mid
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Broadcast Katalog Peka ke channel Telegram.")
    ap.add_argument("--folder", required=True, help="Folder edisi (auto-*) berisi slide peka-katalog-*.png.")
    ap.add_argument("--title", required=True, help="Judul/hook singkat edisi ini.")
    ap.add_argument("--para", default="", help="Ringkasan 2-4 kalimat: rentang harga + produk andalan.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="Lewati cek dedupe (hanya untuk re-post atas perintah user).")
    args = ap.parse_args()

    paused_until = broadcast_paused()
    if paused_until:
        print(f"PAUSED broadcast channel ditunda sampai {paused_until} WIB "
              f"type=katalog title={args.title[:60]}")
        return 0

    folder = Path(args.folder)
    slides = sorted(folder.glob("peka-katalog-*.png"))
    if not slides:
        print(f"Tidak ada slide di {folder}", file=sys.stderr)
        return 2
    if len(slides) > 10:
        print(f"Album Telegram maks 10 foto, folder ini punya {len(slides)} slide",
              file=sys.stderr)
        return 2

    prices = load_prices()
    products = prices["products"]
    date_label = prices.get("date_label", wib_now().strftime("%d %B %Y"))
    nums = [p["price_num"] for p in products]
    caption = build_album_caption(args.title, args.para, len(products),
                                  min(nums), max(nums))
    if len(caption) > 1024:
        print("Caption album >1024 karakter, dipotong.", file=sys.stderr)
        caption = caption[:1020] + "…"
    list_text = build_list_text(products, date_label)
    if len(list_text) > 4096:
        print("Pesan daftar harga >4096 karakter.", file=sys.stderr)
        return 2

    date_key = wib_now().strftime("%Y-%m-%d")
    album_key = f"{date_key}|katalog-album|{args.title}"
    list_key = f"{date_key}|katalog-list|{args.title}"
    list_marker = f"Daftar harga \u2014 Katalog Peka {date_label}"

    if args.dry_run:
        print(json.dumps({
            "album_caption": caption,
            "album_photos": [str(s) for s in slides],
            "list_text": list_text,
            "album_key": album_key,
            "list_key": list_key,
        }, indent=2, ensure_ascii=False))
        return 0

    # --- Pesan 1: album slide ---
    album_mid = None
    if not args.force:
        album_mid = already_sent(album_key, args.title)
    if album_mid:
        print(f"SKIP album already sent channel message_id={album_mid} "
              f"title={args.title[:60]}")
    else:
        token = read_token()
        ok, album_mid, err = send_media_group(token, slides, caption)
        if not ok:
            print(f"Gagal kirim album: {err}", file=sys.stderr)
            time.sleep(5)
            found = already_sent(album_key, args.title)
            if found:
                album_mid = found
                print(f"OK album message_id={album_mid} (ditemukan di channel "
                      "setelah kirim gagal, TIDAK dikirim ulang)")
            else:
                print("Album TIDAK ditemukan di channel setelah verifikasi "
                      "live — aman untuk retry nanti.", file=sys.stderr)
                return 1
        else:
            ledger_append(album_key, album_mid, LEDGER_NOTE)
            print(f"OK album channel message_id={album_mid} "
                  f"title={args.title[:60]} "
                  f"url=https://t.me/peka_aichannel/{album_mid}")

    # --- Pesan 2: daftar harga lengkap ---
    list_mid = None
    if not args.force:
        list_mid = already_sent(list_key, list_marker)
    if list_mid:
        print(f"SKIP daftar harga already sent channel message_id={list_mid} "
              f"title={args.title[:60]}")
    else:
        token = read_token()
        ok, list_mid, err = send_text(token, list_text)
        if not ok:
            print(f"Gagal kirim daftar harga: {err}", file=sys.stderr)
            time.sleep(5)
            found = already_sent(list_key, list_marker)
            if found:
                list_mid = found
                print(f"OK daftar harga message_id={list_mid} (ditemukan di "
                      "channel setelah kirim gagal, TIDAK dikirim ulang)")
            else:
                print("Daftar harga TIDAK ditemukan di channel setelah "
                      "verifikasi live — aman untuk retry nanti.", file=sys.stderr)
                return 1
        else:
            ledger_append(list_key, list_mid, LEDGER_NOTE)
            print(f"OK daftar harga channel message_id={list_mid} "
                  f"title={args.title[:60]} "
                  f"url=https://t.me/peka_aichannel/{list_mid}")

    print(f"ALBUM https://t.me/peka_aichannel/{album_mid}")
    print(f"LIST https://t.me/peka_aichannel/{list_mid}")
    print("BROADCAST KATALOG SELESAI")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
