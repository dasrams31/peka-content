#!/usr/bin/env python3
"""Build the long-form blog JSON for the SPILL skill-agent edition."""
import json
import os

BLOG_DIR = "/home/hatch/workspace/peka-content/blog"
IMG_DIR = "/home/hatch/workspace/peka-content/images"
SLUG = "spill-skill-agent-claude-hermes"

BODY = """
<p>Kalau kamu sudah pernah pakai agent AI buat ngoding atau ngerjain tugas harian, kamu pasti sadar satu hal: model yang sama bisa terasa jauh lebih pintar di tangan orang yang workflow-nya rapi. Bedanya sering bukan di modelnya, tapi di <strong>skill</strong> yang dipasang ke agent itu.</p>
<p>Artikel ini adalah versi lengkap dari seri SPILL di akun Peka. Kita bedah apa itu skill, skill apa saja yang kepakai beneran di Claude dan Hermes, dan repo GitHub mana saja yang layak kamu buka kalau mau ambil skill siap pakai. Semua repo di bawah ini sudah diverifikasi satu per satu ke GitHub, termasuk jumlah star-nya per Oktober 2026.</p>

<h2>Skill Itu Apa?</h2>
<p>Skill adalah folder berisi file bernama <strong>SKILL.md</strong>. Isinya instruksi langkah demi langkah yang ditulis dalam bahasa manusia, kadang ditemani script, template, atau file pendukung lain. Begini cara kerjanya:</p>
<ul>
<li><strong>Agent membaca skill hanya saat topiknya relevan.</strong> Nama dan deskripsi skill selalu terlihat oleh agent, tapi isi lengkapnya baru dimuat ketika tugasmu cocok. Teknik ini disebut progressive disclosure, dan gunanya besar: konteks agent tidak kepenuhan hal yang tidak perlu.</li>
<li><strong>Sekali bikin, dipakai berkali-kali.</strong> Workflow yang berulang, misalnya format laporan mingguan atau standar review kode tim kamu, cukup ditulis sekali. Setelah itu agent menjalankannya sendiri tanpa perlu kamu jelaskan dari awal.</li>
<li><strong>Formatnya standar terbuka.</strong> Spesifikasi skill diterbitkan di agentskills.io, jadi skill yang sama bisa berjalan di Claude, Hermes, dan agent lain yang mendukung standar ini.</li>
<li><strong>Tidak harus menulis sendiri.</strong> Ada banyak skill bikinan komunitas yang dibagikan lewat GitHub. Tinggal clone, baca isinya, pasang yang cocok.</li>
</ul>

<h2>Claude: Paling Matang buat Ngoding dan Dokumen</h2>
<p>Claude dari Anthropic mendukung Agent Skills di Claude.ai, Claude Code, dan API. Buat urusan programming dan kerja kantoran, ekosistem skill Claude saat ini yang paling rapi. Skill yang paling kepakai:</p>
<ul>
<li><strong>Skill dokumen Office.</strong> Skill resmi untuk membuat dan mengedit file Word, Excel, PowerPoint, dan PDF langsung dari percakapan, lengkap dengan tabel, rumus, dan format yang rapi.</li>
<li><strong>Code review dan debugging.</strong> Di Claude Code, skill dan perintah bawaan membantu meninjau perubahan kode, mencari bug, dan memberi usulan perbaikan sebelum kode di-merge.</li>
<li><strong>Frontend design.</strong> Skill desain yang bikin antarmuka web tidak terasa generik: tipografi, layout, dan detail visualnya lebih niat daripada hasil template pasaran.</li>
<li><strong>Testing aplikasi web.</strong> Skill testing menjalankan aplikasi web secara otomatis: klik, isi form, ambil screenshot, lalu melaporkan bug. Berguna sebelum rilis.</li>
<li><strong>Skill kustom untuk tim.</strong> Kamu bisa menulis SKILL.md sendiri berisi standar commit, cara deploy, atau format laporan tim. Sekali tulis, hasilnya konsisten seterusnya.</li>
</ul>

<h3>Repo Skill Claude yang Kepakai Beneran</h3>
<p><a href="https://github.com/anthropics/skills"><strong>anthropics/skills</strong></a> (182 ribu star). Repo resmi milik Anthropic. Isinya skill dokumen Office dan contoh skill standar yang aman dijadikan titik awal sekaligus referensi kalau kamu mau menulis skill sendiri.</p>
<p><a href="https://github.com/obra/superpowers"><strong>obra/superpowers</strong></a> (302 ribu star). Framework skill plus metodologi software development untuk Claude Code. Skill di dalamnya mengajarkan agent cara brainstorming fitur, menulis test sebelum ngoding, debugging sistematis, dan review kode.</p>
<p><a href="https://github.com/alirezarezvani/claude-skills"><strong>alirezarezvani/claude-skills</strong></a> (28 ribu star). Satu repo berisi 380+ skill dan plugin Claude Code, dari engineering, marketing, product, sampai operasi bisnis. Cocok buat yang mau stok banyak dalam sekali ambil.</p>
<p><a href="https://github.com/kepano/obsidian-skills"><strong>kepano/obsidian-skills</strong></a> (49 ribu star). Skill yang mengajarkan agent memakai Obsidian dengan benar: Markdown, Bases, JSON Canvas, dan Obsidian CLI. Vault catatanmu bisa dirapikan dan dikelola agent.</p>
<p><a href="https://github.com/wshobson/agents"><strong>wshobson/agents</strong></a> (41 ribu star). Marketplace plugin dan skill untuk Claude Code dan beberapa agent lain. Isinya terkurasi per kategori, enak buat berburu kemampuan baru.</p>
<p><a href="https://github.com/ComposioHQ/awesome-claude-skills"><strong>ComposioHQ/awesome-claude-skills</strong></a> (77 ribu star). Daftar kurasi bergaya awesome list berisi link skill, resource, dan tools Claude. Simpan sebagai bookmark; dari sini kamu bisa loncat ke ratusan repo lain.</p>

<h2>Hermes: Agent Otonom yang Belajar dari Pengalaman</h2>
<p>Hermes adalah agent open source dari Nous Research. Kalau Claude unggul sebagai partner kerja yang kamu ajak ngobrol, Hermes unggul sebagai pekerja latar yang jalan terus. Kelebihan utamanya:</p>
<ul>
<li><strong>Skill yang menulis dirinya sendiri.</strong> Setelah menyelesaikan tugas yang berat, Hermes menuliskan pengalamannya menjadi SKILL.md baru. Tugas serupa berikutnya dikerjakan lebih cepat karena prosedurnya sudah terdokumentasi.</li>
<li><strong>Memory persisten.</strong> Hermes mengingat preferensi, proyek, dan pelajaran dari sesi sebelumnya. Kamu tidak mulai dari nol setiap kali membuka chat.</li>
<li><strong>Jalan 24/7 di server.</strong> Hermes enak ditinggal di VPS: cron, monitoring, backup, dan laporan otomatis berjalan sendiri tanpa kamu tunggu.</li>
<li><strong>Satu otak di banyak aplikasi.</strong> Gateway yang sama melayani Telegram, WhatsApp, Discord, Slack, sampai email. Ganti aplikasi, ingatannya tetap nyambung.</li>
<li><strong>Model bebas.</strong> Hermes tidak terikat satu provider. Claude, GPT, Gemini, sampai model lokal bisa dipakai dan diganti tanpa mengganti agent-nya.</li>
</ul>

<h3>Repo Skill Hermes yang Kepakai Beneran</h3>
<p><a href="https://github.com/NousResearch/hermes-agent"><strong>NousResearch/hermes-agent</strong></a> (255 ribu star). Repo utama Hermes. Skill bawaannya ada di sini, termasuk mekanisme penulisan skill otomatis dari pengalaman.</p>
<p><a href="https://github.com/0xNyk/awesome-hermes-agent"><strong>0xNyk/awesome-hermes-agent</strong></a> (5,8 ribu star). Direktori independen berisi skill, plugin, penyedia memory, dan tools pilihan untuk Hermes. Titik awal yang bagus buat menjelajah ekosistemnya.</p>
<p><a href="https://github.com/NousResearch/hermes-agent-self-evolution"><strong>NousResearch/hermes-agent-self-evolution</strong></a> (5,5 ribu star). Proyek resmi Nous Research untuk mengoptimasi skill dan prompt Hermes secara otomatis memakai DSPy dan GEPA. Ini dapurnya fitur belajar sendiri Hermes.</p>
<p><a href="https://github.com/kerpopule/hermes-jev-skills"><strong>kerpopule/hermes-jev-skills</strong></a> (1,1 ribu star). Kumpulan skill praktis: routing model, memory, compaction, pemilihan skill, sampai computer use dan browser use untuk Hermes.</p>
<p><a href="https://github.com/ksimback/hermes-ecosystem"><strong>ksimback/hermes-ecosystem</strong></a> (1,3 ribu star). Hermes Atlas: panduan memilih mode dan skill yang cocok untuk kebutuhanmu, lengkap dengan panduan install. Enak dibaca sebelum mulai utak-atik.</p>

<h2>Jadi, Pilih yang Mana?</h2>
<ul>
<li><strong>Ngoding dan dokumen serius:</strong> Claude. Ekosistem skill-nya paling matang dan repo resminya paling aman buat pemula.</li>
<li><strong>Asisten 24/7 yang belajar sendiri:</strong> Hermes. Dia tinggal di server, ingatannya awet, dan skill-nya bertambah seiring pemakaian.</li>
<li><strong>Keduanya sekaligus:</strong> bisa. Format skill-nya mirip karena sama-sama mengikuti standar terbuka, jadi investasi belajar nulis skill tidak terbuang.</li>
</ul>

<h2>Tips Aman Sebelum Memasang Skill</h2>
<ul>
<li><strong>Baca dulu isi SKILL.md-nya.</strong> Skill pada dasarnya adalah instruksi yang akan diikuti agent kamu, kadang ditemani script yang akan dijalankan. Luangkan dua menit untuk membaca sebelum memasang.</li>
<li><strong>Utamakan sumber tepercaya.</strong> Mulai dari repo resmi dan repo dengan star besar serta maintainer jelas. Ekosistem skill pernah kecolongan skill berbahaya yang menyusup di marketplace, jadi jangan asal install.</li>
<li><strong>Mulai dari satu skill.</strong> Pasang, coba di tugas beneran, rasakan bedanya. Menumpuk puluhan skill sekaligus justru bikin perilaku agent susah ditebak.</li>
</ul>

<h2>Penutup</h2>
<p>Produktivitas agent AI tidak ditentukan oleh modelnya saja. Skill yang terpasang di dalamnya yang membedakan agent yang sekadar bisa menjawab dan agent yang benar-benar bisa bekerja dengan caramu.</p>
<p>Seri SPILL repo skill tayang tiap hari jam 21.30 WIB di akun Peka, bergantian antara Claude dan Hermes, satu slide per repo. Follow @peka.ai.id biar tidak ketinggalan, dan simpan artikel ini sebagai contekan jangka panjang.</p>
""".strip()

post = {
    "slug": SLUG,
    "title": "Spill Skill Agent AI: Claude dan Hermes, Lengkap dengan Repo GitHub-nya",
    "date": "2026-10-20",
    "datetime": "2026-10-20 21:05",
    "excerpt": "Versi lengkap seri SPILL Peka: apa itu skill agent AI, skill Claude dan Hermes yang kepakai beneran buat ngoding dan produktivitas, plus daftar repo GitHub terverifikasi buat ambil skill siap pakai.",
    "image": SLUG + ".png",
    "body_html": BODY,
    "tags": ["AI Agent", "Claude", "Hermes"],
    "links": {
        "threads": "https://www.threads.net/t/18387105736224802",
        "facebook": "https://facebook.com/61594934228841/posts/pfbid06yWNPtZqioZGy5ntbSQi6KKNyryvyc6hpQRryDUac2x4HobunZz6w2yad9Garyq6l/",
    },
}

# hard guard: no em-dash / en-dash anywhere
blob = json.dumps(post, ensure_ascii=False)
assert "\u2014" not in blob and "\u2013" not in blob, "dash terlarang ditemukan"

with open(os.path.join(BLOG_DIR, SLUG + ".json"), "w") as fh:
    json.dump(post, fh, ensure_ascii=False, indent=2)

import shutil
shutil.copy(
    "/home/hatch/workspace/peka-content/spill/out/2026-10-20/carousel-claude/repo-01.png",
    os.path.join(IMG_DIR, SLUG + ".png"),
)
words = len(BODY.split())
print("blog written:", SLUG, "| body words ~", words)
