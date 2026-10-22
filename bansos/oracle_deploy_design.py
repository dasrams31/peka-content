#!/usr/bin/env python3
"""Extended carousel for the Oracle Cloud deploy follow-up edition.

Reuses the locked bansos ticket design (bansos_design.py) for the cover and
closing slides, and adds tutorial content slides in the exact same visual
system (black canvas, lockup, big title + yellow underline, cream cards,
same footer) for the in-between steps.

Usage: python3 oracle_deploy_design.py <spec.json>
Output: bansos-01.png .. bansos-07.png in spec["out_dir"].
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bansos_design as bd
from PIL import Image, ImageDraw

S = bd.S


def fit_title(d, text):
    size = 104
    while size > 60 and d.textlength(text, font=bd.f(size)) > 1828:
        size -= 4
    return bd.f(size)


def content_slide(title, cards, sumber):
    img = Image.new("RGB", (S, S), bd.BLACK)
    d = ImageDraw.Draw(img)
    bd.lockup(img, cy=128, mh=104, color=bd.YELLOW)
    d.text((110, 280), title, font=fit_title(d, title), fill=bd.WHITE)
    d.rectangle([110, 420, 640, 438], fill=bd.YELLOW)
    y = 520
    for card_title, rows, numbered in cards:
        y += bd.card(d, 110, y, 1828, card_title, rows, numbered=numbered) + 60
    if y - 60 > S - 210:
        raise SystemExit(f"OVERFLOW: content slide '{title}' too tall (y={y - 60})")
    d.text((110, S - 168), f"Sumber resmi: {sumber}", font=bd.fr(46), fill=bd.GRAY)
    d.text((110, S - 100), "Save biar nggak lupa. Tag teman yang butuh.",
           font=bd.f(50), fill=bd.WHITE)
    return img


def build(spec):
    sumber = spec["fields"]["sumber"]
    slides = [bd.slide1(spec)]

    slides.append(content_slide("1. MASUK CONSOLE", [
        ("PANELNYA DI SINI, BUKAN DI SITUS DEPAN", [
            "Buka cloud.oracle.com, bukan oracle.com (itu situs marketing, isinya chat penjualan)",
            "Kalau diminta Cloud Account Name, isi nama tenancy dari email pendaftaranmu",
            "Login pakai email dan password yang kamu buat pas daftar",
            "Halaman setelah login namanya OCI Console, semua server diatur dari sini",
        ], True),
    ], sumber))

    slides.append(content_slide("2. BIKIN INSTANCE", [
        ("SERVERMU, SEKALI ATUR", [
            "Menu Compute > Instances > Create Instance",
            "Image: Canonical Ubuntu versi terbaru",
            "Shape: A1.Flex Ampere, Always Free Eligible",
            "Mulai 2 OCPU + 12 GB RAM (jatah total 4 OCPU + 24 GB)",
            "Aktifkan public IPv4, generate SSH key, unduh key-nya",
        ], True),
        ("KALAU MENTOK", [
            "Out of capacity? Coba lagi nanti, atau ganti domain",
            "Alternatif mungil: E2.1.Micro, RAM 1 GB, maks 2 instance",
        ], False),
    ], sumber))

    slides.append(content_slide("3. KONEK + BUKA PORT", [
        ("MASUK KE SERVER", [
            "ssh -i namafile.key ubuntu@IP-PUBLIK-kamu",
            "User Oracle Linux: opc, Ubuntu: ubuntu",
            "Nggak mau ribet? Pakai Cloud Shell di console",
        ], True),
        ("PORT WAJIB DUA LAPIS", [
            "Console: instance > Security List > Add Ingress Rules",
            "Sumber 0.0.0.0/0, TCP, port aplikasimu",
            "Server: iptables -I INPUT 6 -p tcp --dport 80 -j ACCEPT",
            "Simpan: sudo netfilter-persistent save",
        ], True),
    ], sumber))

    slides.append(content_slide("4. DEPLOY PAKAI DOCKER", [
        ("DARI KOSONG SAMPAI ONLINE", [
            "Install Docker: curl -fsSL https://get.docker.com | sudo sh",
            "sudo usermod -aG docker ubuntu, lalu login SSH ulang",
            "Tes pertama: docker run -d --name web -p 80:80 nginx",
            "Buka http://IP-PUBLIK-kamu di browser, halaman nginx tampil tandanya online",
            "Proyek sendiri: clone repo kamu, jalanin pakai Docker Compose atau service systemd",
        ], True),
    ], sumber))

    slides.append(content_slide("5. CATATAN PENTING", [
        ("BIAR NGGAK KAGET DI TENGAH JALAN", [
            "Instance nganggur bisa direklamasi Oracle (pemakaian rendah terus 7 hari). Pakai beneran, jangan didiamkan",
            "Home region yang dipilih pas daftar itu permanen, nggak bisa diganti",
            "Private key hilang nggak bisa diunduh ulang. Simpan di tempat aman",
            "Jatah storage blok 200 GB itu gabungan buat semua volume",
            "Panduan lengkap plus FAQ: blog.peka.ai.id",
        ], False),
    ], sumber))

    slides.append(bd.slide3(spec))
    return slides


def main():
    spec = json.load(open(sys.argv[1]))
    out = spec["out_dir"]
    os.makedirs(out, exist_ok=True)
    slides = build(spec)
    for i, img in enumerate(slides, start=1):
        img.save(f"{out}/bansos-{i:02d}.png")
    print("OK", out, len(slides), "slides")


if __name__ == "__main__":
    main()
