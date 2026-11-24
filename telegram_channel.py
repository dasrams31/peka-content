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
  (cek update Bot API + halaman channel, 3x, jeda 60 detik); kalau
  ketemu, catat ke ledger dan anggap sukses. Kalau TIDAK ketemu, JANGAN
  nyatakan "aman di-retry": tulis baris PENDING ke ledger dan exit 1.
  Retry otomatis dilarang sampai dicek manual — pelajaran 19 Nov 2026:
  broadcast Figma dobel 272/273 karena halaman t.me/s telat tampil
  (cache), verifikasi 2x45 detik tidak menemukan pesan 272 yang sudah
  terkirim, lalu retry mengirim 273. "Tidak ketemu di halaman" TIDAK
  sama dengan "belum terkirim".
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
PAUSE_FILE = Path.home() / "workspace/peka-content/channel_broadcast_pause_until.txt"
WIB = ZoneInfo("Asia/Jakarta")
PENDING_ID = "PENDING"  # message_id sentinel: kirim sebelumnya belum terverifikasi


def broadcast_paused() -> str | None:
    """Jeda broadcast channel (perintah user 18 Nov 2026, 1 hari).

    Baca PAUSE_FILE (baris pertama non-komentar: 'YYYY-MM-DD HH:MM' WIB).
    Selama waktu WIB sekarang < batas itu, kembalikan batasnya sebagai string;
    bila file tidak ada / sudah kedaluwarsa / tidak bisa dibaca, kembalikan None
    (broadcast jalan normal). File korup tidak pernah memblokir broadcast.
    """
    try:
        lines = PAUSE_FILE.read_text().splitlines()
    except FileNotFoundError:
        return None
    except OSError:
        return None
    until_raw = next((ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")), "")
    if not until_raw:
        return None
    try:
        until = datetime.strptime(until_raw, "%Y-%m-%d %H:%M").replace(tzinfo=WIB)
    except ValueError:
        print(f"Peringatan: format {PAUSE_FILE} tidak dikenal ({until_raw!r}), jeda diabaikan.", file=sys.stderr)
        return None
    if datetime.now(WIB) < until:
        return until_raw
    return None

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
    "special": "✨ Edisi Khusus Peka AI",
    "weekly": "🎬 AI Pekan Ini",
    "tutorial": "📚 Tutorial Peka",
    "tanya-jawab": "❓ Tanya Jawab Nyata",
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
    if args.bansos:
        links.append(f"📄 Detail edisi ini: {args.bansos}")
    if args.type == "bansos":
        links.append("🎟️ Katalog Bansos: bansos.peka.ai.id")
    if links:
        lines.append("Lengkapnya di sini:")
        lines.extend(links)
        lines.append("")
    lines.append("💬 Gabung komunitas Peka: s.peka.ai.id/gabung")
    lines.append("📱 Grup WhatsApp Peka: s.peka.ai.id/k4iKBr")
    lines.append("📣 Channel Peka: t.me/peka_aichannel")
    lines.append("🤖 Order akun premium: t.me/aeternum_premibot")
    lines.append("🛍️ Belanja produk digital: store.peka.ai.id")
    return "\n".join(lines)


def wib_now() -> datetime:
    return datetime.now(WIB)


def dedupe_key(args) -> str:
    return f"{wib_now().strftime('%Y-%m-%d')}|{args.type}|{args.title}"


def ledger_lookup(key: str):
    """Kembalikan (message_id, url) terakhir yang TERKONFIRMASI terkirim
    untuk kunci ini, atau None. Baris PENDING dilewati (bukan bukti kirim)."""
    if not LEDGER.is_file():
        return None
    found = None
    try:
        for line in LEDGER.read_text().splitlines():
            parts = line.split("|")
            if len(parts) >= 6 and "|".join(parts[1:4]) == key and parts[4] != PENDING_ID:
                found = (parts[4], parts[5])
    except OSError:
        return None
    return found


def ledger_append_raw(key: str, message_id: str, url: str, source: str) -> None:
    line = f"{wib_now().strftime('%Y-%m-%d %H:%M')}|{key}|{message_id}|{url}|{source}\n"
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(line)


def ledger_append(key: str, message_id: str, source: str) -> None:
    url = f"https://t.me/peka_aichannel/{message_id}"
    ledger_append_raw(key, message_id, url, source)


def ledger_append_pending(key: str) -> None:
    """Tandai niat kirim SEBELUM sendPhoto dipanggil. Bila proses mati
    atau koneksi putus di tengah kirim, baris ini menahan retry otomatis
    sampai statusnya dicek manual (lihat ledger_pending)."""
    ledger_append_raw(key, PENDING_ID, PENDING_ID, "pending")


def ledger_pending(type_: str, title: str, hours: int = 48):
    """Cari baris PENDING untuk type+title ini dalam `hours` jam terakhir
    (tanggal diabaikan: retry besok tetap tertahan). Kembalikan timestamp
    barisnya, atau None bila tidak ada. Baris PENDING yang sudah
    disusul baris terkirim (message_id asli) untuk kunci yang sama
    dianggap selesai."""
    if not LEDGER.is_file():
        return None
    now = wib_now()
    found = None
    try:
        for line in LEDGER.read_text().splitlines():
            parts = line.split("|")
            if len(parts) < 7 or parts[4] != PENDING_ID:
                continue
            if parts[2] != type_ or parts[3] != title:
                continue
            try:
                ts = datetime.strptime(parts[0], "%Y-%m-%d %H:%M").replace(tzinfo=WIB)
            except ValueError:
                continue
            if (now - ts).total_seconds() > hours * 3600:
                continue
            # PENDING selesai bila ada baris terkirim sesudahnya (kunci sama).
            key = "|".join(parts[1:4])
            superseded = False
            for later in LEDGER.read_text().splitlines():
                lp = later.split("|")
                if len(lp) >= 6 and "|".join(lp[1:4]) == key and lp[4] != PENDING_ID and lp[0] >= parts[0]:
                    superseded = True
                    break
            if not superseded:
                found = parts[0]
    except OSError:
        return None
    return found


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


def find_in_updates(token: str, chat_id: str, markers: list):
    """Cek update Bot API (peek TANPA offset: tidak mengonsumsi update
    polling bot) untuk channel_post yang cocok dengan penanda. Ini sumber
    kebenaran server-side; halaman t.me/s bisa telat karena cache.
    Best-effort saja: selama bot utama long-polling, getUpdates di sini
    biasanya dibalas 409 Conflict. Kembalikan message_id bila ketemu,
    None bila tidak ada / tidak bisa dibaca (polling bot mungkin sudah
    mengonsumsi update-nya — itu normal, bukan bukti belum terkirim)."""
    try:
        req = urllib.request.Request(
            f"{API_BASE}{token}/getUpdates?limit=100",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"Cek getUpdates gagal (dianggap belum ada): {e}", file=sys.stderr)
        return None
    if not data.get("ok"):
        return None
    found = None
    for upd in data.get("result", []):
        post = upd.get("channel_post") or upd.get("message")
        if not post:
            continue
        if str(post.get("chat", {}).get("id")) != str(chat_id):
            continue
        text = post.get("caption") or post.get("text") or ""
        if any(m in text for m in markers if m):
            found = str(post["message_id"])
    return found


def verify_live_after_failure(token: str, args, chat_id: str, attempts: int = 3, wait_secs: int = 60):
    """Setelah kirim gagal, cek live beberapa kali: update Bot API dulu,
    lalu halaman channel. Halaman t.me/s bisa telat tampil (cache) —
    karena itu 3x cek jeda 60 detik. Kembalikan message_id bila ketemu."""
    markers = _markers(args)
    for attempt in range(attempts):
        if attempt:
            time.sleep(wait_secs)
        if str(chat_id) == CHANNEL_ID:
            mid = find_in_updates(token, chat_id, markers)
            if mid:
                return mid
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
    ap.add_argument("--bansos", default="",
                    help="URL halaman detail edisi ini di bansos.peka.ai.id (khusus type bansos).")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="Lewati cek dedupe (hanya untuk re-post atas perintah user).")
    args = ap.parse_args()

    paused_until = broadcast_paused()
    if paused_until:
        print(f"PAUSED broadcast channel ditunda sampai {paused_until} WIB (jeda 1 hari, perintah user 18 Nov 12:48) type={args.type} title={args.title[:60]}")
        return 0

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
        pend = ledger_pending(args.type, args.title)
        if pend:
            print(f"PENDING sejak {pend} WIB: kirim '{args.title[:60]}' sebelumnya "
                  "belum terverifikasi. JANGAN kirim ulang otomatis — cek live di "
                  "https://t.me/peka_aichannel dulu. Bila benar belum terkirim, hapus "
                  "baris PENDING di broadcasts.log atau jalankan dengan --force.",
                  file=sys.stderr)
            return 1
        live_mid = find_in_channel(args)
        if live_mid:
            ledger_append(key, live_mid, "found-live")
            print(f"SKIP already sent channel message_id={live_mid} type={args.type} title={args.title[:60]} url=https://t.me/peka_aichannel/{live_mid} (live channel)")
            return 0

    token = read_token()
    ledger_append_pending(key)
    ok, mid, err = send_photo(token, args, caption, cover)
    if ok:
        ledger_append(key, mid, "sent")
        print(f"OK channel message_id={mid} type={args.type} title={args.title[:60]}")
        return 0

    # Kirim gagal: JANGAN langsung anggap gagal. Pesan bisa sudah sampai
    # sebelum koneksi putus (kasus 9 Nov 2026, dan Figma 19 Nov 2026).
    # Verifikasi live dulu (Bot API + halaman, 3x jeda 60 detik).
    print(f"Gagal kirim ke channel: {err}", file=sys.stderr)
    print("Verifikasi live channel sebelum menyatakan gagal...", file=sys.stderr)
    found_mid = verify_live_after_failure(token, args, CHANNEL_ID)
    if found_mid:
        ledger_append(key, found_mid, "found-after-failure")
        print(f"OK channel message_id={found_mid} type={args.type} title={args.title[:60]} (ditemukan di channel setelah kirim gagal, TIDAK dikirim ulang)")
        return 0
    print("BELUM TERVERIFIKASI di channel setelah 3x cek (Bot API + halaman "
          "live). JANGAN retry otomatis: pesan bisa saja sudah sampai tapi "
          "belum tampil di halaman. Cek manual di https://t.me/peka_aichannel "
          "— bila sudah ada, catat message_id-nya ke broadcasts.log; bila "
          "benar belum ada, hapus baris PENDING di broadcasts.log lalu retry.",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
