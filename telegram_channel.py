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
      --threads https://www.threads.com/... --instagram https://... \
      --facebook https://... --blog https://blog.peka.ai.id/p/...
  Semua --threads/--instagram/--facebook/--blog opsional (yang tidak ada
  tidak dicetak). --dry-run hanya mencetak payload tanpa mengirim.
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path

TOKEN_FILE = Path.home() / "workspace/mc-portal/config/telegram_premibot_token"
CHANNEL_ID = "-1001475296402"  # @peka_aichannel
API_BASE = "https://api.telegram.org/bot"

TYPE_LABELS = {
    "hm": "📰 Homeless Media",
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
    lines.append("🛍️ Belanja produk digital: store.peka.ai.id")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Broadcast konten Peka ke channel Telegram.")
    ap.add_argument("--type", required=True, choices=list(TYPE_LABELS))
    ap.add_argument("--title", required=True, help="Judul/hook singkat (1-2 baris).")
    ap.add_argument("--cover", required=True, help="Path gambar slide pertama.")
    ap.add_argument("--threads", default="")
    ap.add_argument("--instagram", default="")
    ap.add_argument("--facebook", default="")
    ap.add_argument("--blog", default="")
    ap.add_argument("--dry-run", action="store_true")
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

    token = read_token()
    # Multipart manual (tanpa dependensi): kirim foto + caption.
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
        print(f"Gagal kirim ke channel: {e}", file=sys.stderr)
        return 1
    if not data.get("ok"):
        print(f"Telegram menolak: {data}", file=sys.stderr)
        return 1
    msg = data["result"]
    print(f"OK channel message_id={msg['message_id']} type={args.type} title={args.title[:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
