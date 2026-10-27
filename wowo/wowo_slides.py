"""Kata Wowo project spotlight carousel (Peka paper style, 2048x2048).
All facts observed from https://wowo.peka.ai.id/ homepage (2026-10-27).
No promise percentages are claimed: the site shows labels + sentence counts only.
"""
import os, textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 2048, 2048
PAPER = (246, 241, 230)
INK = (20, 20, 20)
GREY = (110, 105, 95)
YELLOW = (255, 214, 10)
FONTDIR = "/home/hatch/workspace/sertiku-poster/fonts"
DEJAVU = "/home/hatch/workspace/peka-content/spill/animated/assets/DejaVuSansMono-Bold.ttf"
MASCOT = "/home/hatch/workspace/peka-content/spill/animated/assets/mascot-p-dark.png"
OUT = "/home/hatch/workspace/peka-content/wowo/out"

def F(name, size):
    return ImageFont.truetype(os.path.join(FONTDIR, name), size)

def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def base(page, total):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mono = ImageFont.truetype(DEJAVU, 34)
    d.text((110, 92), "KATA WOWO  //  PROJECT PEKA", font=mono, fill=GREY)
    # lockup top-right: dark mascot + peka.ai.id
    mas = Image.open(MASCOT).convert("RGBA")
    mas.thumbnail((72, 72))
    img.paste(mas, (W - 110 - 72 - 300, 70), mas)
    d.text((W - 110 - 290, 84), "peka.ai.id", font=F("Poppins-Bold.ttf", 44), fill=INK)
    # footer hairline + text
    d.line([(110, H - 170), (W - 110, H - 170)], fill=(180, 174, 160), width=3)
    d.text((110, H - 130), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID", font=mono, fill=GREY)
    d.text((W - 110 - 200, H - 130), f"{page:02d} / {total:02d}", font=mono, fill=GREY)
    return img, d

def title_block(d, y, lines, size=150):
    font = F("Poppins-ExtraBold.ttf", size)
    for ln in lines:
        d.text((110, y), ln, font=font, fill=INK)
        y += size + 18
    return y

def body(d, y, text, size=52, lh=76, max_w=W - 220):
    font = F("Poppins-SemiBold.ttf", size)
    for ln in wrap(d, text, font, max_w):
        d.text((110, y), ln, font=font, fill=(51, 51, 51))
        y += lh
    return y

def highlight(d, y, text, size=64):
    font = F("Poppins-ExtraBold.ttf", size)
    w = d.textlength(text, font=font) + 60
    d.rectangle([110, y, 110 + w, y + size + 44], fill=YELLOW)
    d.text((140, y + 16), text, font=font, fill=INK)
    return y + size + 44

def slide1():
    img, d = base(1, 6)
    y = title_block(d, 330, ["KATA", "WOWO"], size=230)
    y = highlight(d, y + 30, "Berapa persen pidato Wowo itu janji?")
    body(d, y + 60, "Bedah pidato Presiden Prabowo, per kalimat. Papan skor pidato yang bisa kamu cek sendiri.", size=56, lh=82)
    d.text((110, 1560), "wowo.peka.ai.id", font=F("Poppins-ExtraBold.ttf", 72), fill=INK)
    img.save(f"{OUT}/wowo-01.png")

def slide2():
    img, d = base(2, 6)
    y = title_block(d, 300, ["Papan skor", "pidato."])
    y = body(d, y + 40, "Kata Wowo membedah pidato Presiden Prabowo kalimat per kalimat. Tiap kalimat diberi label, lalu dipetakan ke detik videonya, jadi kamu bisa cek sendiri ucapan itu muncul di menit ke berapa.", size=54, lh=80)
    y = body(d, y + 50, "Analisis oleh Jev AI dari TypeSafe AI.", size=44, lh=64)
    img.save(f"{OUT}/wowo-02.png")

def slide3():
    img, d = base(3, 6)
    y = title_block(d, 300, ["6 label buat", "tiap kalimat."])
    labels = ["JANJI", "KLAIM DATA", "CERITA", "KRITIK", "AJAKAN", "SEREMONIAL"]
    font = F("Poppins-ExtraBold.ttf", 56)
    y += 50
    for i in range(0, 6, 2):
        for j, lab in enumerate(labels[i:i+2]):
            x = 110 + j * 920
            w = d.textlength(lab, font=font) + 80
            d.rectangle([x, y, x + w, y + 120], fill=INK)
            d.text((x + 40, y + 30), lab, font=font, fill=YELLOW)
        y += 180
    body(d, y + 30, "Satu kalimat, satu label. Tidak ada kalimat yang lolos tanpa kategori.", size=48, lh=72)
    img.save(f"{OUT}/wowo-03.png")

def slide4():
    img, d = base(4, 6)
    y = title_block(d, 300, ["Tempel link,", "langsung dibedah."])
    steps = [
        ("1", "Tempel link YouTube pidato Prabowo."),
        ("2", "Pastikan ada subtitle bahasa Indonesia. Subtitle otomatis pun cukup."),
        ("3", "Tiap kalimat keluar dengan label dan detik videonya."),
    ]
    y += 50
    mono = ImageFont.truetype(DEJAVU, 60)
    for num, txt in steps:
        d.text((110, y), num, font=mono, fill=GREY)
        y = body(d, y, "   " + txt, size=54, lh=80) + 40
    img.save(f"{OUT}/wowo-04.png")

def slide5():
    img, d = base(5, 6)
    y = title_block(d, 300, ["9 pidato sudah", "dianalisis."])
    y = highlight(d, y + 30, "2.709 kalimat.", size=80)
    rows = [
        ("Nota Keuangan dan RAPBN 2027", "893 kalimat"),
        ("Sidang Tahunan MPR 2026", "630 kalimat"),
        ("Hari Buruh Internasional", "234 kalimat"),
    ]
    y += 70
    for name, cnt in rows:
        d.text((110, y), name, font=F("Poppins-Bold.ttf", 52), fill=INK)
        d.text((110, y + 66), cnt, font=F("Poppins-SemiBold.ttf", 44), fill=GREY)
        y += 170
    body(d, y + 10, "Plus 6 pidato lainnya di arsip.", size=48, lh=72)
    img.save(f"{OUT}/wowo-05.png")

def slide6():
    img, d = base(6, 6)
    y = title_block(d, 330, ["Coba", "sendiri."])
    y = body(d, y + 40, "Buka wowo.peka.ai.id, tempel link YouTube pidato, dan lihat sendiri kalimat mana yang janji.", size=56, lh=82)
    y = highlight(d, y + 60, "wowo.peka.ai.id", size=72)
    body(d, y + 60, "Follow @peka.ai.id dan gabung ke komunitas kami di url.peka.ai.id.", size=48, lh=72)
    img.save(f"{OUT}/wowo-06.png")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (slide1, slide2, slide3, slide4, slide5, slide6):
        fn()
    print("slides saved:", sorted(os.listdir(OUT)))
