# Proyek UTS Interoperability: Campus Event Registration Platform Politeknik Negeri Bali

Proyek ini adalah implementasi sistem registrasi event kampus untuk Ujian Tengah Semester (UTS) mata kuliah Interoperability.

Sistem ini menunjukkan interoperabilitas antara tiga komponen utama:
* **Backend REST API:** Dibangun menggunakan **FastAPI (Python)**.
* **Database:** Menggunakan **SQLite** (Serverless, berbasis file).
* **Frontend/Client:** Berupa halaman **HTML + Fetch API** yang disajikan langsung oleh FastAPI.

---

## Fitur

* **Publik:**
    * Melihat daftar semua event kampus (`GET /events`).
    * Mendaftar sebagai peserta untuk sebuah event (`POST /register`).
    * Melihat **nama-nama peserta** yang sudah terdaftar di suatu event (`GET /events/{id}/participants`).
* **Admin (Terproteksi API Key):**
    * Membuat, mengubah, dan menghapus event (CRUD).
    * Melihat data lengkap semua peserta.
* **Bonus Autentikasi (+10%):**
    * Endpoint admin diproteksi menggunakan token API Key sederhana via header `X-API-Key`.
* **Bonus Dokumentasi (+10%):**
    * Dokumentasi API interaktif (Swagger UI) otomatis dibuat oleh FastAPI dan tersedia di `/docs`.
* **Fitur Tambahan:**
    * Desain antarmuka (UI) yang modern dan responsif.
    * Database **otomatis terisi** dengan data event default saat server dijalankan pertama kali.

---

## Cara Menjalankan Aplikasi

Berikut adalah langkah-langkah lengkap untuk menjalankan proyek ini, dirancang agar mudah diikuti.

### 1. Prasyarat

* Python 3.7+
* `pip` (Python package installer)
* Git

### 2. Setup Proyek

1.  **Clone Repository:**
    Buka terminal dan jalankan perintah berikut untuk mengunduh proyek:
    ```bash
    git clone [https://github.com/Mangadi-167/Daftar-Event-Kampus.git](https://github.com/Mangadi-167/Daftar-Event-Kampus.git)
    cd Daftar-Event-Kampus
    ```

2.  **Buat & Aktifkan Virtual Environment:**
    Ini akan membuat lingkungan Python yang terisolasi untuk proyek.
    ```bash
    # (Windows)
    python -m venv venv
    .\venv\Scripts\activate
    
    # (macOS/Linux)
    # python3 -m venv venv
    # source venv/bin/activate
    ```
    Terminal Anda akan menampilkan `(venv)` di bagian awal.

3.  **Install Dependensi:**
    Install semua library Python yang dibutuhkan oleh proyek:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Menjalankan Aplikasi

1.  **Jalankan Server API:**
    Pastikan Anda berada di folder *root* proyek (`Daftar-Event-Kampus/`) dan `(venv)` Anda aktif.
    ```bash
    uvicorn backend.main:app --reload
    ```

2.  **Akses Aplikasi:**
    Server sekarang berjalan. Cukup **buka browser** Anda dan kunjungi alamat di bawah ini:
    
    ➡️ **`http://127.0.0.1:8000`**

---

### Catatan untuk Penguji (Dosen)

* **Aplikasi Frontend** (`index.html`) sudah **disajikan secara otomatis** oleh server FastAPI di alamat `http://127.0.0.1:8000`
* **Database Terisi Otomatis:** Saat server dijalankan pertama kali, file `campus_events.db` akan dibuat. Kode di `backend/main.py` akan **otomatis mengisi data event default** (Lomba TRPL, CTF, dll.) ke dalam database.
* **Dokumentasi API** (Swagger UI) tersedia di `http://127.0.0.1:8000/docs` untuk pengujian *endpoint* secara terpisah.

---

## Daftar Endpoint API

Dokumentasi interaktif lengkap tersedia di **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**.

**Admin API Key:** `admin-secret-key-12345` (Masukkan di header `X-API-Key` saat otorisasi di Swagger UI)

| Method | Endpoint | Deskripsi | Proteksi |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Menampilkan frontend `index.html`. | ❌ Publik |
| `GET` | `/events` | Menampilkan semua event. | ❌ Publik |
| `GET`| `/events/{id}/participants`| Melihat nama peserta di event tertentu.| ❌ Publik |
| `POST` | `/register` | Menambahkan peserta baru. | ❌ Publik |
| `POST` | `/events` | Menambah event baru. | ✅ **Admin** |
| `PUT` | `/events/{id}` | Mengubah data event. | ✅ **Admin** |
| `DELETE` | `/events/{id}` | Menghapus event. | ✅ **Admin** |
| `GET` | `/participants`| Menampilkan data lengkap peserta. | ✅ **Admin** |

---

## Screenshot Hasil Uji

*(PENTING: Ganti bagian ini dengan screenshot Anda sendiri)*

**1. Screenshot Frontend (Tampilan Utama)**
![Tampilan Frontend Awal](screenshots/tampilan1.png)

**2. Screenshot Fitur (Daftar Peserta)**
*(Screenshot saat salah satu event di-klik pada *dropdown* dan daftar nama peserta muncul di bawahnya)*

**3. Screenshot Backend (Swagger UI di `/docs`)**
*(Screenshot halaman Swagger UI yang menunjukkan semua *endpoint* yang tersedia)*