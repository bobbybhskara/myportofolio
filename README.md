Nama : Muhammad Eshan Bobby Bhaskara

NPM : 2506546333

Kelas : PBP C

Status : Ganteng

## AI Disclosure

Selama mengerjakan project ini saya menggunakan Claude dan Codex. Saya memakai AI untuk berdiskusi, memahami tugas, membantu menulis bagian kode yang berulang, dan mencari penyebab error. Walaupun dibantu AI, saya tetap membaca kembali kode yang dibuat dan menentukan sendiri hasil akhir yang dimasukkan ke repository.

Yang saya lakukan sendiri:

- Menentukan isi, deskripsi, dan pengalaman pribadi yang ditampilkan.
- Menentukan susunan halaman profile, projects, experience, dan education.
- Memilih warna navy, blue, dan white yang dipakai pada website.
- Mengecek hasil website melalui browser dan memastikan tampilannya sesuai dengan yang saya inginkan.
- Membaca kembali perubahan kode dan hasil test sebelum menyelesaikan tugas.

Yang dibantu AI:

- Claude membantu saya berdiskusi tentang pilihan warna dan tampilan website.
- AI membantu membuat struktur awal CSS Grid, timeline, dan efek hover pada card.
- Codex membantu saya membaca Tutorial 3 dan Tugas 3 lalu membaginya menjadi beberapa langkah pengerjaan.
- Codex membantu membuat form, view, URL, template, modal, dan test berdasarkan model yang sudah saya punya.
- AI membantu menjelaskan cara kerja JSON, CSRF, create, update, dan delete.
- AI membantu mencari error, mengecek Git, dan merapikan commit message.

Strategi saya adalah memakai AI untuk membantu bagian teknis dan bagian kode yang berulang. Saya memberikan konteks tentang model dan kode yang sudah ada, lalu meminta pengerjaannya dibagi per langkah agar lebih mudah dicek. Hasil dari AI tidak langsung saya gunakan semuanya karena tetap perlu disesuaikan dengan model, desain, dan kebutuhan project saya. Setelah itu saya mengecek kembali melalui browser, `python manage.py check`, dan `python manage.py test`.

## Refleksi

### Tugas 1

1. Penggunaan Elemen Semantik HTML5

Saya pakai `<section>` untuk misahin profile, projects, experience, dan education, masing masing juga punya `id` sendiri agar bisa jadi target anchor link di navbar. Selain itu section juga bikin styling & spacing tiap bagian lebih gampang diatur lewat CSS dibanding kalau semuanya numpuk jadi `<div>` doang.

Untuk project card dan education card saya pakai `<article>`, karena isinya masing-masing bisa berdiri sendiri. Menurut saya ini bikin struktur kode lebih jelas fungsinya, dan browser/screen reader juga lebih ngerti hierarki kontennya.

`<aside>` belum saya pakai karena memang belum ada konten sampingan (sidebar, catatan tambahan, dll) di website ini.

2. Tantangan dalam Menerapkan Responsive Design

Saat mengatur grid projects biar seimbang di berbagai ukuran layar. Awalnya pakai `repeat(auto-fit, minmax(...))`, tapi 3 card-nya jadi nggak ngisi container full, nyisa ruang kosong di kanan. Karena jumlah card di baris pertama sudah pasti 3, saya ganti ke `grid-template-columns: repeat(3, 1fr)` biar rata. Di layar di bawah `600px`, grid-nya jadi 1 kolom aja.

Selain itu ada juga masalah untuk menjaga rasio gambar project tetap 16:9 tanpa gepeng atau distorsi. Solusinya pakai `aspect-ratio: 16 / 9` di container gambar plus `object-fit: cover` di elemen `<img>`-nya.

3. Batasan Static Web dan Rencana Pengembangan Fitur Dinamis

Kontennya sekarang masih full statis, semua data data yang ada ditulis langsung di HTML. Jadi saat ingin nambah project baru, saya harus membuka template, copy struktur card yang ada, terus edit manual satu satu. Card yang coming soon juga masih placeholder, belum kesambung ke data apapun.

Ke depannya saya ingin manfaatin sisi dinamis Django biar kontennya bisa diedit langsung dari browser tanpa buka kode. Selain itu pengen nambahin form kontak dan status project otomatis, jadi placeholder coming soon di project bisa berubah sendiri begitu ada project baru yang dipublish.

### Tugas 2

1. Alur projek dan peran urls.py proyek, urls.py aplikasi, view, model, dan template.

Jadi di browser membuka proyek lalu di balik layar browser akan request URL projects dan akan diterima urls.py proyek. Kemudian dari situ urls.py aplikasi akan memilih view dari request URL tersebut, dalam hal ini adalah "show_projects". Kemudian view akan mengambil data dari model yang terhubung langsung dengan database. Lalu view akan mengirim data melalui context, dan data data tersebut akan diloop oleh template. Setelah itu html akan dikirimkan langsung ke browser untuk ditampilkan ke user.

2. Karena jika suatu waktu bagian tersebut ingin dihapus, diubah, diupdate, atau ditambah, akan sangat sulit untuk men-trace kembali satu persatu baris kodenya apalagi jika project sudah terlalu banyak. Maka dari itu, diperlukan sebuah sistem baru yang tidak perlu hard-coded untuk menambahkan/mengedit section di dalamnya. Dengan sistem ini juga tampilan semua kartu akan tetap konsisten karena sudah diloop. Data data dari section tersebut juga bisa dikelola melalui django admin sehingga akan lebih mudah.

3. Makemigrations dijalankan ketika ada perubahan pada struktur data atau model. Ini dilakukan untuk memberikan instruksi perubahan database kepada django sehingga data akan sinkron dengan tampilan. Migrate berfungsi untuk menerapkan hasil instruksi yang dihasilkan makemigration ke dalam database agar database tersebut aktif dan bisa secara real-time update. Contoh: Ketika menambahkan model Project, makemigrations menghasilkan 0002_project.py. Setelah itu, migrate membuat tabel Project di database.

### Tugas 3

1. Saya menggunakan `ModelForm` karena formnya bisa langsung mengikuti field yang ada di model. Contohnya, `ExperienceForm` mengambil field `title`, `description`, `category`, dan `thumbnail` dari model `Experience`. Saya jadi tidak perlu menulis input dan aturan pengecekannya satu per satu secara manual. Django juga bisa langsung mengecek isi form dengan `form.is_valid()` dan menyimpan datanya dengan `form.save()`. Kalau membuat form HTML biasa, saya harus mengambil setiap input sendiri, mengecek datanya sendiri, lalu menyimpannya ke model secara manual.

`{% csrf_token %}` digunakan untuk memastikan bahwa request POST berasal dari form website kita. Django akan memberikan token pada form dan mengeceknya kembali saat form dikirim. Jika tokennya tidak ada atau tidak sesuai, request akan ditolak. Hal ini mencegah website lain mengirim request tambah, ubah, atau hapus data tanpa izin melalui browser pengguna. Namun, CSRF bukan login, jadi orang lain masih bisa membuka form saya selama belum ada fitur autentikasi.

2. JSON lebih sering digunakan pada website modern karena penulisannya lebih singkat dan lebih mudah dibaca dibandingkan XML. JSON juga mudah dipakai oleh JavaScript karena bentuknya mirip dengan object dan array. Sementara itu, XML memakai tag pembuka dan penutup sehingga isinya menjadi lebih panjang. Karena itu JSON lebih praktis untuk mengirim data dari backend ke frontend. XML masih bisa digunakan, tetapi biasanya ditemukan pada sistem lama atau sistem yang memang membutuhkan format XML.

3. Saat `/api/experiences/` dibuka, URL tersebut akan menjalankan fungsi `get_experiences_json`. Fungsi ini mengambil data Experience dari database menggunakan `Experience.objects.order_by(...)`. Hasilnya masih berbentuk QuerySet dan berisi object model Django. Setelah itu `serializers.serialize("json", experiences)` mengubah data tersebut menjadi teks JSON. Teks JSON kemudian dikirim sebagai response menggunakan `HttpResponse` dengan tipe `application/json`.

Proses serialization diperlukan karena object model Django tidak bisa langsung dikirim melalui HTTP dan dibaca oleh browser sebagai JSON. Object tersebut harus diubah dulu menjadi format teks yang berisi model, id, dan fields. Pada halaman Experience, JSON itu diubah kembali menggunakan `serializers.deserialize`, lalu object hasilnya dikirim ke template melalui context. Pada tugas ini proses tersebut memang terasa berulang, tetapi tujuannya untuk memahami proses pengiriman data antara server dan client.
