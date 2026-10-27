# Project Spotlight Template

Carousel template gaya Peka (kertas #f6f1e6, 2048x2048) untuk menampilkan
project apa pun, tanpa menulis script baru tiap kali. Dibuat dari slide
Kata Wowo yang tayang 27 Okt 2026; template ini me-render ulang keenam
slide itu sampai piksel-identik (terverifikasi).

## Cara pakai

1. Salin `specs/wowo.json` jadi `specs/<project-baru>.json`.
2. Isi dengan fakta yang SUDAH diobservasi dari situs live project itu.
   Template tidak pernah mengarang angka, persentase, atau klaim.
3. Render:

```bash
python3 project_spotlight.py specs/<project-baru>.json out/
```

4. Cek visual tiap slide (tidak ada teks luber/tabrak) sebelum posting.
5. Posting ke IG + Threads + FB seperti spotlight biasa; caption ditulis
   per platform di folder out (lihat `wowo/out/caption-*.txt` sebagai contoh).

## Skema spec

```json
{
  "project": "KATA WOWO",
  "domain": "wowo.peka.ai.id",
  "slug": "wowo",
  "slides": [ ... ]
}
```

- `project`: kicker header, huruf besar.
- `domain`: tampil di cover dan slide CTA. Kosongkan bila tidak ada.
- `slug`: nama file output (`<slug>-01.png`, dst). Default: nama project
  huruf kecil tanpa spasi.

## Tipe slide

| Tipe | Isi |
| ---- | --- |
| `cover` | `title` (array baris), `highlight` (blok kuning), `body`, domain otomatis di bawah |
| `text` | `title`, `body` (array paragraf; paragraf bisa string, atau `{"text","size","lh"}`) |
| `chips` | `title`, `items` (array label, grid 2 kolom), `footnote` opsional |
| `steps` | `title`, `items` (array langkah bernomor) |
| `stats` | `title`, `highlight`, `rows` (array `[nama, jumlah]`), `footnote` opsional |
| `cta` | `title`, `body`, domain otomatis sebagai blok kuning, `follow` opsional |

Header (kicker + lockup peka.ai.id) dan footer
("GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID" + nomor halaman) otomatis
di semua slide.

## Contoh yang sudah tayang

- `specs/wowo.json` = Kata Wowo (wowo.peka.ai.id), 6 slide, tayang
  IG + Threads + FB 27 Okt 2026.
