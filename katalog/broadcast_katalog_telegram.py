#!/usr/bin/env python3
"""Broadcast Katalog Peka (format baru, perintah user 19 Nov 2026) ke channel
Telegram @peka_aichannel DAN grup @peka_aigroup — SATU-SATUNYA tempat
katalog tayang.

Perintah user 19 Nov 2026, 08:11: hanya katalog Peka yang di-share ke
channel + grup Peka. Katalog Aeternum tetap build-only, tidak di-broadcast
ke mana pun.

Alasan format baru: katalog #6 (17 Nov 2026) kena removed Meta 18 Nov di
Facebook (404) dan Instagram (carousel hilang dari daftar post); Threads
ikut restricted (visibility private). Mulai 19 Nov: katalog TIDAK POSTING
ke Threads/IG/FB, TIDAK ada IG Story, TIDAK ada reel TikTok. Katalog hanya
muncul sebagai broadcast Telegram 2x seminggu (Selasa + Jumat 13:00).

Isi broadcast (4 pesan, 2 per tujuan):
  Channel @peka_aichannel:
    1. Album foto: semua slide katalog (4096x4096) + caption singkat
       (hook + rentang harga + cara order + gabung komunitas).
    2. Pesan teks: daftar harga lengkap dari prices.json (sumber tunggal)
       + cara order + gabung komunitas + store.
  Grup @peka_aigroup: sama persis, album + daftar harga (kunci dedupe
  sendiri, isi sama).

Pengirim: bot @aeternum_premibot (administrator di @peka_aichannel dan
@peka_aigroup), token dibaca dari
~/workspace/mc-portal/config/telegram_premibot_token.

Penggunaan:
  python3 broadcast_katalog_telegram.py --folder <folder edisi auto-*> \
      --title "22 akun premium, mulai 2,2K aja." \
      --para "Ringkasan 2-4 kalimat: rentang harga + produk andalan edisi ini."
  --dry-run hanya mencetak payload tanpa mengirim.
  --force melewati cek dedupe (hanya untuk re-post atas perintah user).

ANTI-DOBEL (pelajaran 9 Nov 2026: broadcast dobel di channel):
- Album dan pesan daftar harga punya kunci dedupe sendiri-sendiri, PER
  TUJUAN: tanggal WIB | katalog-album | title (channel),
  tanggal WIB | katalog-album-group | title (grup), dan begitu pula
  untuk daftar harga.
- SEBELUM kirim tiap pesan, cek ledger; untuk channel, cek JUGA halaman
  live channel. Kalau sudah ada di salah satunya, JANGAN kirim, laporkan
  message_id yang sudah ada (baris SKIP) dan exit 0.
- Grup TIDAK punya halaman publik (t.me/s/peka_aigroup kosong), jadi
  dedupe grup hanya via ledger. Kalau kirim ke grup GAGAL, JANGAN
  langsung retry: cek manual di grup dulu, pesan bisa saja sudah sampai
  sebelum koneksi putus. Baris PENDING di ledger menahan retry otomatis
  sampai dicek manual.
- Kalau kirim ke channel GAGAL karena koneksi putus, JANGAN langsung
  anggap gagal: pesan bisa saja sudah sampai sebelum koneksi putus.
  Verifikasi live (Bot API + halaman, 3x jeda 60 detik); kalau ketemu,
  catat ke ledger dan anggap sukses. Kalau TIDAK ketemu, JANGAN nyatakan
  "aman di-retry": tulis baris PENDING dan exit 1 — pelajaran 19 Nov
  2026, broadcast Figma dobel 272/273 karena halaman t.me/s telat
  tampil (cache) dan retry mengirim salinan kedua.
- Urutan kirim: channel dulu, baru grup. Bila channel gagal, grup TIDAK
  dikirim (hindari tayang grup-only). Retry nanti akan SKIP channel
  (sudah di ledger) dan hanya mengirim yang belum.
"""

import argparse
import html
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path.home() / "workspace/peka-content"))
from telegram_channel import (  # noqa: E402
    API_BASE,
    CHANNEL_ID,
    LEDGER,
    PENDING_ID,
    WIB,
    broadcast_paused,
    find_in_channel,
    ledger_append_raw,
    ledger_lookup,
    ledger_pending,
    read_token,
    verify_live_after_failure,
)

GROUP_ID = "-1001167087205"  # @peka_aigroup

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


def send_media_group(token: str, photos: list, caption: str, chat_id: str):
    """Kirim album foto ke satu chat. Kembalikan (ok, message_id pertama, error)."""
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
             f"name=\"chat_id\"\r\n\r\n{chat_id}\r\n").encode("utf-8")
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


def send_text(token: str, text: str, chat_id: str):
    """Kirim pesan teks ke satu chat. Kembalikan (ok, message_id, error)."""
    try:
        data = _post_json(token, "sendMessage", {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
        })
    except Exception as e:
        return False, None, str(e)
    if not data.get("ok"):
        return False, None, f"Telegram menolak: {data}"
    return True, str(data["result"]["message_id"]), ""


def ledger_append_dest(key: str, message_id: str, source: str, dest: str) -> None:
    """Catat ke ledger dengan URL sesuai tujuan (channel / grup)."""
    handle = "peka_aichannel" if dest == "channel" else "peka_aigroup"
    url = f"https://t.me/{handle}/{message_id}"
    line = (f"{wib_now().strftime('%Y-%m-%d %H:%M')}|{key}|{message_id}|"
            f"{url}|{source}\n")
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(line)


def already_sent(key: str, marker_title: str, dest: str):
    """Cek ledger (+ live channel bila dest=channel) untuk satu kunci.
    Kembalikan message_id bila sudah terkirim, PENDING_ID bila kirim
    sebelumnya belum terverifikasi (retry otomatis dilarang), None bila
    belum."""
    hit = ledger_lookup(key)
    if hit:
        return hit[0]
    try:
        _, ktype, ktitle = key.split("|", 2)
    except ValueError:
        ktype, ktitle = "", ""
    if ledger_pending(ktype, ktitle):
        return PENDING_ID
    if dest != "channel":
        return None
    ns = SimpleNamespace(title=marker_title, blog="", threads="",
                         instagram="", facebook="")
    live_mid = find_in_channel(ns)
    if live_mid:
        ledger_append_dest(key, live_mid, f"{LEDGER_NOTE}-found-live", dest)
        return live_mid
    return None


def send_one(token: str, dest: str, chat_id: str, kind: str,
             slides, caption: str, list_text: str, key: str,
             marker_title: str, force: bool):
    """Kirim satu pesan (album atau daftar harga) ke satu tujuan.
    Kembalikan message_id, atau None bila gagal / tertahan PENDING
    (pesan error sudah dicetak)."""
    if not force:
        mid = already_sent(key, marker_title, dest)
        if mid == PENDING_ID:
            print(f"PENDING {kind} {dest} title={marker_title[:60]}: kirim "
                  "sebelumnya belum terverifikasi. JANGAN kirim ulang "
                  "otomatis — cek manual dulu di "
                  + ("https://t.me/peka_aichannel" if dest == "channel"
                     else "grup @peka_aigroup")
                  + ". Bila benar belum terkirim, hapus baris PENDING di "
                  "broadcasts.log atau jalankan dengan --force.",
                  file=sys.stderr)
            return None
        if mid:
            print(f"SKIP {kind} already sent {dest} message_id={mid} "
                  f"title={marker_title[:60]}")
            return mid
    ledger_append_raw(key, PENDING_ID, PENDING_ID, f"{LEDGER_NOTE}-pending")
    if kind == "album":
        ok, mid, err = send_media_group(token, slides, caption, chat_id)
    else:
        ok, mid, err = send_text(token, list_text, chat_id)
    if not ok:
        print(f"Gagal kirim {kind} ke {dest}: {err}", file=sys.stderr)
        if dest == "channel":
            ns = SimpleNamespace(title=marker_title, blog="", threads="",
                                 instagram="", facebook="")
            found = verify_live_after_failure(token, ns, chat_id)
            if found:
                ledger_append_dest(key, found, f"{LEDGER_NOTE}-found-after-failure", dest)
                print(f"OK {kind} {dest} message_id={found} (ditemukan di "
                      "channel setelah kirim gagal, TIDAK dikirim ulang)")
                return found
            print(f"{kind} BELUM TERVERIFIKASI di channel setelah 3x cek "
                  "(Bot API + halaman live). JANGAN retry otomatis: pesan "
                  "bisa saja sudah sampai tapi belum tampil di halaman. "
                  "Cek manual di https://t.me/peka_aichannel — bila sudah "
                  "ada, catat message_id-nya ke ledger; bila benar belum "
                  "ada, hapus baris PENDING di broadcasts.log lalu retry.",
                  file=sys.stderr)
        else:
            print(f"{kind} ke grup TIDAK bisa diverifikasi live (grup tidak "
                  "punya halaman publik) — cek manual di grup sebelum retry. "
                  "Baris PENDING di ledger menahan retry otomatis.",
                  file=sys.stderr)
        return None
    ledger_append_dest(key, mid, LEDGER_NOTE, dest)
    handle = "peka_aichannel" if dest == "channel" else "peka_aigroup"
    print(f"OK {kind} {dest} message_id={mid} title={marker_title[:60]} "
          f"url=https://t.me/{handle}/{mid}")
    return mid


def main() -> int:
    ap = argparse.ArgumentParser(description="Broadcast Katalog Peka ke channel + grup Telegram.")
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
    list_marker = f"Daftar harga \u2014 Katalog Peka {date_label}"
    keys = {
        "channel": (f"{date_key}|katalog-album|{args.title}",
                    f"{date_key}|katalog-list|{args.title}"),
        "group": (f"{date_key}|katalog-album-group|{args.title}",
                  f"{date_key}|katalog-list-group|{args.title}"),
    }

    if args.dry_run:
        print(json.dumps({
            "album_caption": caption,
            "album_photos": [str(s) for s in slides],
            "list_text": list_text,
            "channel": {"album_key": keys["channel"][0],
                        "list_key": keys["channel"][1]},
            "group": {"album_key": keys["group"][0],
                      "list_key": keys["group"][1]},
        }, indent=2, ensure_ascii=False))
        return 0

    token = read_token()
    sent = {}
    # Urutan: channel dulu, baru grup. Bila channel gagal, grup tidak dikirim.
    for dest, chat_id in (("channel", CHANNEL_ID), ("group", GROUP_ID)):
        album_key, list_key = keys[dest]
        album_mid = send_one(token, dest, chat_id, "album", slides, caption,
                             list_text, album_key, args.title, args.force)
        if album_mid is None:
            return 1
        list_mid = send_one(token, dest, chat_id, "list", slides, caption,
                            list_text, list_key, list_marker, args.force)
        if list_mid is None:
            return 1
        sent[dest] = (album_mid, list_mid)

    print(f"ALBUM channel https://t.me/peka_aichannel/{sent['channel'][0]}")
    print(f"LIST channel https://t.me/peka_aichannel/{sent['channel'][1]}")
    print(f"ALBUM group https://t.me/peka_aigroup/{sent['group'][0]}")
    print(f"LIST group https://t.me/peka_aigroup/{sent['group'][1]}")
    print("BROADCAST KATALOG SELESAI")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
