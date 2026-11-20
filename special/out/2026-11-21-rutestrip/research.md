# RuteStrip Special — Research (tested live 21 Nov 2026, ~00:05 WIB)

User correction: the site is rutestrip.ai.id (NOT airutestrip.web.id) and the
chatbot is chat.rutestrip.ai.id. All facts below are from rutestrip.ai.id /
chat.rutestrip.ai.id / rutestrip.ai.id/arsitektur, plus live chatbot tests.

## Brand
- Theme color #059669 (emerald-600), dark #064e3b, light #ecfdf5. Green palette
  confirmed from the live site CSS.
- Tagline (chat meta): "Asisten pintar berbasis AI untuk pendakian gunung
  Indonesia. Dapatkan rekomendasi jalur, cuaca realtime, itinerary, estimasi
  biaya, dan panduan survival."
- Links: rutestrip.ai.id (shortlink s.peka.ai.id/TknXVJ),
  chat.rutestrip.ai.id (shortlink s.peka.ai.id/gXbVzB), Telegram t.me/rutestrip
  and t.me/rutestrip_bot.

## Recommendation system (from /arsitektur)
- Content-Based Filtering with SBERT + Cosine Similarity.
- Flow: File GPX input -> Preprocessing (cleaning, lowercase, selective
  stopword removal, no stemming) -> SBERT Embedding 384 dimensi ->
  Cosine Similarity Sim(Q,D) = (Q.D)/(||Q||x||D||) -> Top-N Ranking.
- Model: paraphrase-multilingual-MiniLM-L12-v2, supports Bahasa Indonesia.
- GPX features extracted: jarak, elevasi, grade, durasi Naismith.
  Plus manual descriptions (vegetasi, sumber air, panorama) and coordinates.
- Stack: Laravel 11, Python 3.11, SBERT, Leaflet.js map.
- Features: rekomendasi AI SBERT, analisis file GPX otomatis, peta interaktif,
  kalkulasi Naismith Time, rating & review rute.

## Chatbot — live tests via POST https://chat.rutestrip.ai.id/api/chat
Body: {"message": ..., "history": [], "stream": false}. No auth needed (guest).
Model reported in timing: gemini-3.1-flash-lite.

### Test 1 — "rekomendasi gunung untuk pemula di Jawa Barat"
- Top pick: Gunung Papandayan (Garut). Table returned:
  Papandayan 1.79 km, elev gain 341 m, durasi Naismith 1.5 jam, Mudah, 65%;
  Patuha 1.24 km, 247 m, 1.1 jam, Mudah, 65%;
  Lembu 1.92 km, 336 m, 1.5 jam, Mudah, 65%;
  Kerenceng 2.86 km, 535 m, 2.3 jam, Sedang, 66%.
- retrieved_routes similarity: Sikendil 0.6586, Kerenceng 0.6561, Lembu 0.6517,
  Papandayan 0.6506, Patuha via Kawah Putih 0.6487.
- Timing: retrieval 190 ms, generation ~18.5 s, total ~18.8 s, type rekomendasi.
- Papandayan pitch: jalur bersahabat, kawah + Hutan Mati ikonik, cocok buat
  foto-foto. Tips: manajemen air, Leave No Trace, cek cuaca.

### Test 2 — "perlengkapan wajib buat mendaki Gunung Papandayan untuk pemula"
- Gear checklist (3 orang, 2 hari): air bersih 18.0 liter total (6L/orang),
  tenda dome 1 unit (kapasitas 4), gas kaleng 4 + 1 kompor portable,
  logistik 18 porsi utama + snack energi, personal gear wajib (jaket gunung,
  sleeping bag, matras, headlamp, raincoat, sepatu trekking), safety & medical
  (P3K, obat pribadi, oxycan, thermal blanket, povidone, trash bag x3).
- Tips: layering quick-dry, sepatu trekking grip kasar + 1 nomor lebih besar,
  sumber air melimpah di Pondok Saladah, headlamp wajib.
- Timing: retrieval 58 ms, total ~3.9 s, type logistik.

### Test 3 — "itinerary 2 hari 1 malam Papandayan dan estimasi biayanya"
- Itinerary 2D1N via Cisurupan: basecamp 08:00, parkiran atas/kawah 09:00
  (ojek ~60 mnt), Pondok Saladah 11:00 (~120 mnt), summit Tegal Alun 06:30
  (start 05:00, ~90 mnt), turun ke basecamp 12:00 (~180 mnt).
- Biaya per orang: simaksi Rp30.000 weekday / Rp45.000 weekend, parkir motor
  Rp10.000 / mobil Rp35.000, ojek Rp25.000-50.000 (opsional), logistik
  +-Rp150.000, tak terduga Rp50.000. Total +-Rp250.000-300.000 (bawa alat sendiri).
- Timing: retrieval 52 ms, total ~4.5 s, type itinerary.

## Update 21 Nov ~02:50 — fakta homepage buat reel v3 (user: "lebih berisi")
- Skala (homepage rutestrip.ai.id, live): **143 jalur** dengan data GPX, **50 gunung**, **4 provinsi** di Pulau Jawa, **1.202 km** total panjang jalur.
- Contoh hasil homepage: Watupayon Muria 2,2 km / puncak 1.488 m / 1 j 15 mnt; Ungaran via Perantunan 3,1 km / 2.020 m / 1 j 51 mnt; Telomoyo via Arsal 2,2 km / 1.757 m / 1 j 15 mnt.
- Fitur chat (homepage): cuaca live (suhu, angin, hujan basecamp + puncak), itinerary, info porter, peta satelit, rekomendasi jalur.
- Contoh percakapan homepage (Merbabu via Selo 2D1N): cuaca basecamp berawan, angin ringan, sore peluang hujan, bawa jas hujan; Hari 1 basecamp ke pos camp ~5 jam; Hari 2 summit pagi, turun ke basecamp; porter opsional, berguna kalau bawa tenda + logistik berat.
- Cara kerja (homepage): 1 SBERT ubah kalimat jadi vektor makna; 2 content-based filtering vs data GPX (jarak, tanjakan, kemiringan), cosine similarity; 3 Naismith: 1 jam per 5 km + 1 jam per 600 m tanjakan; plus peta, profil elevasi, cuaca Open-Meteo.
- **Riset terbit di Jurnal Sistemasi (SINTA 3)**: R. D. P. Wijaya & A. N. Rahman (2026), "Mountain Hiking Route Recommendation System using Content-based Filtering with SBERT and Cosine Similarity".
- Fitur lain: upload GPX (single + batch), suka & ulasan, profil elevasi, rating & review rute.
- Catatan: halaman /arsitektur tulis stack **Laravel 12** (research awal + blog tulis Laravel 11).

## Content plan (6 slides, 4096x4096, green RuteStrip theme)
1. Cover: RUTESTRIP, "AI yang ngerti gunung", coba sekarang: buka chat.rutestrip.ai.id
2. Masalah: milih gunung itu susah (info berserakan, tiap jalur beda jarak/elevasi/durasi)
3. Cara kerja: GPX -> SBERT 384 dimensi -> Cosine Similarity -> Top-N
4. Bukti test nyata: Papandayan top pick (1,79 km, 341 m, 1,5 jam, Mudah)
5. Chatbot bisa apa: rekomendasi, checklist logistik, itinerary + biaya, cuaca, survival
6. Penutup: coba di rutestrip.ai.id + chat link, pertanyaan penutup

## Posting
- 21 Nov 2026 18:00 WIB via runonce cron (posting script in this out dir).
- Threads carousel + IG carousel + FB carousel + blog + channel broadcast
  (telegram_channel.py --type special).
- Shortlinks in visuals only (TknXVJ for site, gXbVzB for chat).
