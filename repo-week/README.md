# Repo of the Week

Seri premium satu repo per edisi, tayang 1x seminggu (bukan harian).
Gaya sengaja beda dari SPILL: kanvas hitam pekat, aksen emas, tipografi
serif display, ruang kosong lega, hanya 4 slide.

## Cara pakai

1. Buat `specs/<repo>.json` dari contoh `specs/sample-browser-use.json`.
2. Isi dengan fakta dari GitHub + PyPI/README live (stars, forks, issues,
   perintah install). Jangan karang angka.
3. Render:

```bash
python3 repo_week.py specs/<repo>.json out/
```

4. Cek visual, posting IG + Threads + FB.

## Slide

1. Cover: nama repo serif raksasa + hook + stats + URL GitHub.
2. Kenapa repo ini: screenshot repo dalam bingkai jendela browser (titik exit/minimize/maximize + URL) + penjelasan singkat. Tanpa `image` di spec, slide ini jadi 2 paragraf teks saja.
3. Install: panel terminal + COCOK BUAT.
4. Closing: edisi + follow + komunitas.
