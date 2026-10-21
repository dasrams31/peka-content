#!/usr/bin/env python3
"""Peka EDISI KHUSUS: Meta AI Threads "Feature not available" (2026-10-22).

5 slides, 2048x2048. Reuses the buzzer special-edition components.
Two-sided coverage: what Meta AI claimed, and Komdigi's denial.
The user's own screenshot of the @meta.ai profile is the evidence.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import designer as D
import buzzer_design as B
from PIL import Image

X, f = D.X, D.f
W = H = D.W
YEL, WHT = D.YEL, D.WHT

SS = ("/home/hatch/workspace/user/media_library/image/c1/"
      "c1b25e122035a7f8129af3aaa99ff3959484c0f835cb67048b46dcb93138011e.jpg")
OUT = "/home/hatch/workspace/peka-content/edisi-khusus/meta-ai-komdigi"
N = 5


def cover():
    img = Image.new("RGB", (W, H), D.BG)
    d = B.head(img)
    inner = D.browser_window(img, d, (X(70), X(200), X(1010), X(560)),
                             "THREADS")
    vis = D.load_visual(SS)
    if vis:
        d = D.contain_fit(img, vis, inner)
    y = X(596)
    head_lines = [("Biasanya dipake untuk", WHT),
                  ("counter buzzer, kini", WHT),
                  ("Meta AI diblokir!", YEL)]
    for sz in (64, 60, 56, 52):
        if all(d.textlength(t, font=f(sz)) <= W - X(140)
               for t, _ in head_lines):
            break
    for ln, col in head_lines:
        d.text((X(70), y), ln, font=f(sz), fill=col)
        y += X(int(sz * 1.2))
    sub = "Akun @meta.ai tampil Feature not available untuk pengguna Indonesia."
    for s2 in (27, 25, 23):
        if d.textlength(sub, font=f(s2, False)) <= W - X(140):
            break
    d.text((X(70), y + X(14)), sub, font=f(s2, False), fill="#cfcfcf")
    D.swipe_button(d, 918)
    D.footer(d, 1, N)
    return img


def kronologi():
    cards = [
        ("Meta AI buka suara",
         "Di Threads, Meta AI menyebut ada permintaan hukum dari Komdigi "
         "untuk membatasi konten demo, kritik terhadap presiden, sampai "
         "karhutla."),
        ("Mengutip riset resmi",
         "Ia merujuk riset SAFEnet dan Remotivi: 66 dari 73 kasus moderasi "
         "konten kritik warga pada April sampai Agustus 2026 dikaitkan "
         "dengan permintaan Komdigi."),
        ("Andalan warganet",
         "Selama ini @meta.ai memang sering dipakai warganet untuk "
         "mengecek dan membantah narasi buzzer pemerintah. Makanya kabar "
         "ini langsung meledak."),
    ]
    return B.cards_slide(3, "KRONOLOGI", "Kok bisa seheboh ini?", cards)


def bantahan():
    cards = [
        ("Bantahan resmi dua kali",
         "Wakil Menteri Angga Raka Prabowo pada 18 Oktober dan Direktur "
         "Safriansyah Yanwar Rosyadi pada 20 Oktober menegaskan pemerintah "
         "tidak pernah meminta platform membatasi konten karhutla."),
        ("Belum ada bukti",
         "Jawaban chatbot bukan pernyataan resmi Meta. Sampai sekarang "
         "tidak ada bukti fitur ini dimatikan atas permintaan Komdigi "
         "atau pihak mana pun."),
        ("Dugaan lain yang beredar",
         "Sebagian warganet menduga ini filter otomatis Threads untuk "
         "topik politik sensitif, bukan perintah siapa pun. Yang jelas, "
         "warganet kehilangan satu alat bantah andalan."),
    ]
    return B.cards_slide(4, "SISI LAIN", "Kata Komdigi: tidak benar", cards)


def main():
    os.makedirs(OUT, exist_ok=True)
    slides = [
        cover(),
        B.evidence(SS, 1, "PROFIL @META.AI: FEATURE NOT AVAILABLE"),
        kronologi(),
        bantahan(),
        B.closing(),
    ]
    for i, s in enumerate(slides, start=1):
        s.save(f"{OUT}/metaai-{i:02d}.png")
    print(f"[metaai] {len(slides)} slides -> {OUT}")


if __name__ == "__main__":
    main()
