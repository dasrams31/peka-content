#!/usr/bin/env python3
"""Broadcast konten Peka yang baru rilis ke channel Telegram @peka_aichannel.

Dipanggil sebagai langkah terakhir cron konten, SETELAH semua platform
tayang dan link terverifikasi. Mengirim:
- foto: slide pertama konten (untuk reels: frame/cover pertama),
- caption: judul/hook singkat SAJA (bukan isi penuh postingan),
  link ke postingan di tiap sosmed + blog, ajakan gabung komunitas,
  dan ajakan ke Peka Store.

Catatan aturan: link di sini SENGAJA ada karena ini channel Telegram milik
Peka sendiri (bukan feed sosmed); aturan tanpa-link tetap berlaku penuh
untuk caption Threads/IG/FB/TikTok.

Pengirim: bot @aeternum_premibot (administrator di @peka_aichannel),
token dibaca dari ~/workspace/mc-portal/config/telegram_premibot_token.

Penggunaan:
  python3 telegram_channel.py --type hm --title "Judul" --cover slide1.png \
      --para "Paragraf ringkasan isi edisi ini, 2-4 kalimat." \
      --threads https://www.threads.com/... --instagram https://... \
      --facebook https://... --blog https://blog.peka.ai.id/p/...
  Semua --threads/--instagram/--facebook/--blog opsional (yang tidak ada
  tidak dicetak). --para opsional (bila diisi, dicetak sebagai paragraf setelah judul).
  --dry-run hanya mencetak payload tanpa mengirim.
  --force melewati cek dedupe (hanya untuk re-post yang diperintah user
  secara eksplisit).

ANTI-DOBEL (pelajaran 9 Nov 2026: broadcast Prompt #19 dobel 172/173 dan
Bansos dobel 174/175):
- Satu edisi + satu channel = satu broadcast. Kunci dedupe:
  tanggal WIB | type | title, dicatat di broadcasts.log.
- SEBELUM kirim, cek ledger DAN halaman live channel (t.me/s/peka_aichannel).
  Kalau edisi ini sudah ada di salah satunya, JANGAN kirim, laporkan
  message_id yang sudah ada (baris SKIP) dan exit 0.
- Kalau kirim GAGAL karena koneksi putus, JANGAN langsung anggap gagal:
  pesan bisa saja sudah sampai sebelum koneksi putus. Verifikasi live
  (2x cek halaman channel, jeda 45 detik); kalau ketemu, catat ke ledger
  dan anggap sukses. Hanya bila TIDAK ketemu, exit 1 (aman di-retry nanti).
- JANGAN pernah memutuskan broadcast hilang hanya dari baris chat.
"""

import argparse
import html
import json
import re
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TOKEN_FILE = Path.home() / "workspace/mc-portal/config/telegram_premibot_token"
CHANNEL_ID = "-1001475296402"  # @peka_aichannel
API_BASE = "https://api.telegram.org/bot"
CHANNEL_PAGE = "https://t.me/s/peka_aichannel"
LEDGER = Path.home() / "workspace/peka-content/broadcasts.log"
WIB = ZoneInfo("Asia/Jakarta")

TYPE_LABELS = {
    "hm": "📰 Kabar Harian Peka AI",
    "prompt": "💡 Prompt Harian",
    "gratisan": "🎁 Gratisan AI",
    "spill": "📦 SPILL Repo",
    "katalog": "🛍️ Katalog Peka",
    "blueprint": "📐 BLUEPRINT",
    "log": "📓 LOG PEKA",
    "bansos": "🎟️ Bansos AI",
    "jualan": "💎 Jualan Prompt",
}


def read_token() -> str:
    try:
        return TOKEN_FILE.read_text().strip()
    except FileNotFoundError:
        print(f"Token tidak ditemukan: {TOKEN_FILE}", file=sys.stderr)
        sys.exit(2)


def build_caption(args) -> str:
    label = TYPE_LABELS.get(args.type, "✨ Peka AI")
    lines = [f"{label}", "", f"<b>{args.title}</b>", ""]
    if args.para:
        lines.append(args.para)
        lines.append("")
    links = []
    if args.threads:
        links.append(f"🧵 Threads: {args.threads}")
    if args.instagram:
        links.append(f"📸 Instagram: {args.instagram}")
    if args.facebook:
        links.append(f"📘 Facebook: {args.facebook}")
    if args.blog:
        links.append(f"📝 Blog: {args.blog}")
    if links:
        lines.append("Lengkapnya di sini:")
        lines.extend(links)
        lines.append("")
    lines.append("💬 Gabung komunitas Peka: t.me/peka_aigroup")
    lines.append("📣 Channel Peka: t.me/peka_aichannel")
    lines.append("🤖 Order akun premium: t.me/aeternum_premibot")
    lines.append("🛍️ Belanja produk digital: store.peka.ai.id")
    return "\n".join(lines)


def wib_now() -> datetime:
    return datetime.now(WIB)


def dedupe_key(args) -> str:
    return f"{wib_now().strftime('%Y-%m-%d')}|{args.type}|{args.title}"


def ledger_lookup(key: str):
    """Kembalikan (message_id, url) terakhir untuk kunci ini, atau None."""
    if not LEDGER.is_file():
        return None
    found = None
    try:
        for line in LEDGER.read_text().splitlines():
            parts = line.split("|")
            if len(parts) >= 6 and "|".join(parts[1:4]) == key:
                found = (parts[4], parts[5])
    except OSError:
        return None
    return found


def ledger_append(key: str, message_id: str, source: str) -> None:
    url = f"https://t.me/peka_aichannel/{message_id}"
    line = f"{wib_now().strftime('%Y-%m-%d %H:%M')}|{key}|{message_id}|{url}|{source}\n"
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(line)


def _clean_page_text(raw_html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw_html)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def _markers(args) -> list:
    """Penanda khas edisi ini; dicari di halaman channel. Judul + link-link
    yang disertakan (slug/shortcode), supaya recovery yang judulnya sedikit
    beda tetap ketemu lewat link."""
    out = []
    title = re.sub(r"\s+", " ", args.title).strip()
    if title:
        out.append(title[:60])
    for url in (args.blog, args.threads, args.instagram, args.facebook):
        if not url:
            continue
        slug = url.rstrip("/").rsplit("/", 1)[-1]
        if len(slug) >= 6:
            out.append(slug)
    return out


def find_in_channel(args):
    """Cari edisi ini di halaman live channel. Kembalikan message_id bila
    ketemu, None bila tidak ada / halaman tidak bisa dibaca."""
    markers = _markers(args)
    if not markers:
        return None
    try:
        req = urllib.request.Request(
            CHANNEL_PAGE, headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except Exception as e:
        print(f"Cek live channel gagal dibaca (dianggap belum ada): {e}", file=sys.stderr)
        return None
    # Bagi halaman per pesan (data-post), cek teks tiap segmen.
    segments = re.split(r'data-post="peka_aichannel/(\d+)"', raw)
    found = None
    for i in range(1, len(segments), 2):
        msg_id = segments[i]
        seg_text = _clean_page_text(segments[i + 1]) if i + 1 < len(segments) else ""
        if any(m in seg_text for m in markers):
            found = msg_id  # segmen terakhir yang cocok = yang terbaru
    return found


def verify_live_after_failure(args, attempts: int = 2, wait_secs: int = 45):
    """Setelah kirim gagal, cek live channel beberapa kali (halaman bisa
    telat tampil). Kembalikan message_id bila ketemu."""
    for attempt in range(attempts):
        if attempt:
            time.sleep(wait_secs)
        mid = find_in_channel(args)
        if mid:
            return mid
    return None


def send_photo(token: str, args, caption: str, cover: Path):
    """Kirim sendPhoto. Kembalikan (ok, message_id, error)."""
    boundary = "----peka-channel-boundary"
    photo = cover.read_bytes()
    body = b""
    for name, value in (
        ("chat_id", CHANNEL_ID),
        ("caption", caption),
        ("parse_mode", "HTML"),
    ):
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode("utf-8")
    body += (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; "
        f"filename=\"{cover.name}\"\r\nContent-Type: image/png\r\n\r\n"
    ).encode("utf-8") + photo + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE}{token}/sendPhoto",
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
    ap = argparse.ArgumentParser(description="Broadcast konten Peka ke channel Telegram.")
    ap.add_argument("--type", required=True, choices=list(TYPE_LABELS))
    ap.add_argument("--title", required=True, help="Judul/hook singkat (1-2 baris).")
    ap.add_argument("--para", default="", help="Paragraf ringkasan isi edisi ini, 2-4 kalimat.")
    ap.add_argument("--cover", required=True, help="Path gambar slide pertama.")
    ap.add_argument("--threads", default="")
    ap.add_argument("--instagram", default="")
    ap.add_argument("--facebook", default="")
    ap.add_argument("--blog", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="Lewati cek dedupe (hanya untuk re-post atas perintah user).")
    args = ap.parse_args()

    cover = Path(args.cover)
    if not cover.is_file():
        print(f"Cover tidak ditemukan: {cover}", file=sys.stderr)
        return 2
    caption = build_caption(args)
    if len(caption) > 1024:
        print("Caption >1024 karakter, dipotong.", file=sys.stderr)
        caption = caption[:1020] + "…"
    if args.dry_run:
        print(json.dumps({"chat_id": CHANNEL_ID, "caption": caption, "cover": str(cover)}, indent=2, ensure_ascii=False))
        return 0

    key = dedupe_key(args)

    if not args.force:
        hit = ledger_lookup(key)
        if hit:
            mid, url = hit
            print(f"SKIP already sent channel message_id={mid} type={args.type} title={args.title[:60]} url={url} (ledger)")
            return 0
        live_mid = find_in_channel(args)
        if live_mid:
            ledger_append(key, live_mid, "found-live")
            print(f"SKIP already sent channel message_id={live_mid} type={args.type} title={args.title[:60]} url=https://t.me/peka_aichannel/{live_mid} (live channel)")
            return 0

    token = read_token()
    ok, mid, err = send_photo(token, args, caption, cover)
    if ok:
        ledger_append(key, mid, "sent")
        print(f"OK channel message_id={mid} type={args.type} title={args.title[:60]}")
        return 0

    # Kirim gagal: JANGAN langsung anggap gagal. Pesan bisa sudah sampai
    # sebelum koneksi putus (kasus 9 Nov 2026). Verifikasi live dulu.
    print(f"Gagal kirim ke channel: {err}", file=sys.stderr)
    print("Verifikasi live channel sebelum menyatakan gagal...", file=sys.stderr)
    found_mid = verify_live_after_failure(args)
    if found_mid:
        ledger_append(key, found_mid, "found-after-failure")
        print(f"OK channel message_id={found_mid} type={args.type} title={args.title[:60]} (ditemukan di channel setelah kirim gagal, TIDAK dikirim ulang)")
        return 0
    print("TIDAK ditemukan di channel setelah verifikasi live — aman untuk retry nanti.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
