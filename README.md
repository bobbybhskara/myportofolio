Nama : Muhammad Eshan Bobby Bhaskara

NPM : 2506546333

Kelas : PBP C

Status : Ganteng

## AI Disclosure
Berikut workflow AI saya:

Yang saya lakukan sendiri:
- Seluruh konten (deskripsi tiap project, role tag, pemilihan project
  dan pengalaman organisasi mana yang ditampilkan) berdasarkan data dan
  pengalaman saya sendiri
- Color palette (navy, blue, and white) —
  saya melakukan berbagai revisi serta brainstorming dengan Claude hingga sesuai preferensi saya
- Rencana layouting dan susunan/tata letak dari website ini sendiri. Dari layout about me, headers, projects, experience, dan education.
- Setiap perubahan kode direview satu per satu (mode
  approval manual di codex) sebelum diterapkan. Tidak ada
  perubahan yang diaccept tanpa saya pahami dulu apa yang diubah

Yang dibantu AI
- Menyusun struktur code awal per section (CSS Grid untuk Projects,
  positioning untuk timeline Experience/Education, hover-reveal pada card) sesuai instruksi saya
- Membantu debugging (misal header yang tidak berubah warna setelah migrasi palet ternyata karena cache browser, bukan bug di kode, dan ditemukan dengan cross-check
  incognito mode)
- Merapikan kalimat commit message dan draft deskripsi project

Strategi saya yaitu dengan menggunakan ai untuk mempercepat bagian teknis (nulis css/html yang mengulang), sementara keputusan desain, konten, dan struktur akhir tetap saya validasi dan tentukan sendiri. Banyak kali saya meminta revisi karena hasil awal belum sesuai yang saya inginkan

## Refleksi

### 1. Penggunaan Elemen Semantik HTML5

Saya pakai `<section>` untuk misahin profile, projects, experience, dan education, masing masing juga punya `id` sendiri agar bisa jadi target anchor link di navbar. Selain itu section juga bikin styling & spacing tiap bagian lebih gampang diatur lewat CSS dibanding kalau semuanya numpuk jadi `<div>` doang.

Untuk project card dan education card saya pakai `<article>`, karena isinya masing-masing bisa berdiri sendiri. Menurut saya ini bikin struktur kode lebih jelas fungsinya, dan browser/screen reader juga lebih ngerti hierarki kontennya.

`<aside>` belum saya pakai karena memang belum ada konten sampingan (sidebar, catatan tambahan, dll) di website ini.

### 2. Tantangan dalam Menerapkan Responsive Design

Saat mengatur grid projects biar seimbang di berbagai ukuran layar. Awalnya pakai `repeat(auto-fit, minmax(...))`, tapi 3 card-nya jadi nggak ngisi container full, nyisa ruang kosong di kanan. Karena jumlah card di baris pertama sudah pasti 3, saya ganti ke `grid-template-columns: repeat(3, 1fr)` biar rata. Di layar di bawah `600px`, grid-nya jadi 1 kolom aja.

Selain itu ada juga masalah untuk menjaga rasio gambar project tetap 16:9 tanpa gepeng/distorsi — solusinya pakai `aspect-ratio: 16 / 9` di container gambar plus `object-fit: cover` di elemen `<img>`-nya.

### 3. Batasan Static Web dan Rencana Pengembangan Fitur Dinamis

Kontennya sekarang masih full statis, semua data data yang ada ditulis langsung di HTML. Jadi saat ingin nambah project baru, saya harus membuka template, copy struktur card yang ada, terus edit manual satu satu. Card yang coming soon juga masih placeholder, belum kesambung ke data apapun.

Ke depannya saya ingin manfaatin sisi dinamis Django biar kontennya bisa diedit langsung dari browser tanpa buka kode. Selain itu pengen nambahin form kontak dan status project otomatis, jadi placeholder coming soon di project bisa berubah sendiri begitu ada project baru yang dipublish.
