# Proyek UTS Interoperability: Campus Event Registration Platform

Sistem ini menunjukkan interoperabilitas antara:
* **Backend REST API:** **FastAPI (Python)**
* **Database:** **SQLite** (Serverless, berbasis file)
* **Frontend/Client:** **HTML + Fetch API**

---

## Fitur

* **Publik:** Melihat event (`GET /events`), mendaftar event (`POST /register`).
* **Admin (Terproteksi API Key):** CRUD Event (`POST`, `PUT`, `DELETE /events`), melihat peserta (`GET /participants`).
* **Bonus Autentikasi (+10%):** Endpoint admin diproteksi via header `X-API-Key`.
* **Bonus Dokumentasi (+10%):** Dokumentasi API (Swagger UI) otomatis tersedia di `/docs`.

---

## Cara Menjalankan Aplikasi

### 1. Prasyarat

* Python 3.7+
* `pip` (Python package installer)

### 2. Setup

1.  **Clone Repository:**
    ```bash
    git clone [https://github.com/username/interoperability-final-](https://github.com/username/interoperability-final-)[namamahasiswa].git
    cd interoperability-final-[namamahasiswa]
    ```

2.  **Buat & Aktifkan Virtual Environment:**
    ```bash
    # (Windows)
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Menjalankan Aplikasi

1.  **Jalankan Server API:**
    Pastikan Anda berada di folder *root* (`interoperability-final-budi-sentana/`) dan `(venv)` Anda aktif.
    ```bash
    uvicorn backend.main:app --reload
    ```

2.  **Database Terbuat:**
    Saat server berjalan pertama kali, sebuah file baru bernama `campus_events.db` akan otomatis muncul di folder *root* proyek Anda. **Inilah database Anda.**

3.  **Akses API:**
    * Server berjalan di: `http://127.0.0.1:8000`
    * Dokumentasi API (Swagger): `http://127.0.0.1:8000/docs`

4.  **Jalankan Frontend (Client):**
    * **Buka file `index.html`** langsung di browser Anda (klik dua kali).
    * Frontend akan otomatis terhubung ke API.

---

## Daftar Endpoint API

Dokumentasi interaktif lengkap tersedia di **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**.

**Admin API Key:** `admin-secret-key-12345` (Masukkan di header `X-API-Key`)

| Method | Endpoint | Deskripsi | Proteksi |
| :--- | :--- | :--- | :--- |
| `GET` | `/events` | Menampilkan semua event. | ❌ Publik |
| `POST` | `/register` | Menambahkan peserta baru. | ❌ Publik |
| `POST` | `/events` | Menambah event baru. | ✅ **Admin** |
| `PUT` | `/events/{id}` | Mengubah data event. | ✅ **Admin** |
| `DELETE` | `/events/{id}` | Menghapus event. | ✅ **Admin** |
| `GET` | `/participants`| Menampilkan daftar peserta. | ✅ **Admin** |

---

## Screenshot Hasil Uji

*(Ganti dengan screenshot Anda sendiri)*

**1. Screenshot Frontend (`index.html`)**


**2. Screenshot Backend (Swagger UI di `/docs`)**


**3. Screenshot Database (Menggunakan DB Browser for SQLite)**