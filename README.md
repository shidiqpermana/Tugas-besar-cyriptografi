# Cipher Lab - Aplikasi Kriptografi Interaktif 🔐

Ini adalah tugas besar kriptografi berupa aplikasi web interaktif yang merender visualisasi matematika enkripsi cipher klasik secara edukatif.

## ✨ Fitur Unggulan
- **5 Algoritma Klasik**: Mendukung enkripsi *Caesar*, *Vigenère*, *Affine*, *Hill*, dan *Playfair* Cipher.
- **Tampilan Matematis (Edukatif)**: Algoritma perhitungan matematis di-render secara nyata menggunakan **MathJax** (memvisualisasikan operasi aljabar modular dan perkalian matriks secara step-by-step).
- **Penanganan Dinamis**: Kunci matriks dinamis (2x2 atau 3x3) untuk Hill Cipher, serta generator Matriks 5x5 interaktif untuk Playfair.
- **Kenyamanan UX/UI**: Dibangun dari awal dengan *Custom CSS* yang estetik dan *playful*. Dilengkapi dengan fitur *Dark/Light Mode* *toggle* dan fitur *Session History* berbasis Sidebar khusus yang terintegrasi di Navbar.

## ⚙️ Persyaratan Sistem (Dependencies)
Proyek ini dibangun menggunakan **Python (Flask)** dan modul `numpy`. 
Silakan merujuk pada file `requirements.txt`.

## 🚀 Cara Install & Menjalankan Lokal

1. Buka terminal lalu _clone_ repositori ini:
   ```bash
   git clone https://github.com/[USERNAME]/[NAMA_REPO].git
   cd [NAMA_REPO]
   ```
2. Buat Virtual Environment (Sangat disarankan):
   ```bash
   python -m venv venv
   
   # Untuk pengguna Windows:
   venv\Scripts\activate    
   
   # Untuk pengguna Linux/Mac:
   source venv/bin/activate 
   ```
3. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan aplikasi Flask:
   ```bash
   python app.py
   ```
5. Buka `http://127.0.0.1:5000` di web browser Anda.

## ☁️ Panduan Deployment (Cloud Hosting)
Aplikasi ini diatur menggunakan `gunicorn` sebagai HTTP Server sehingga berstatus *production-ready*. 

**Jika menggunakan Railway / Render / Heroku**:
1. Buat akun dan koneksikan dengan GitHub Repository Anda.
2. Platform akan otomatis mendeteksi file `Procfile` (`web: gunicorn app:app`) dan `requirements.txt`.
3. Aplikasi siap online!

**Jika menggunakan PythonAnywhere**:
1. Buka tab *Web*, *Add a new web app*, pilih framework *Flask* dan versi Python Anda.
2. Upload *source code* ke direktori, dan install *requirements.txt* melalui Bash Console PythonAnywhere.
3. Reload server.

## 📸 Dokumentasi Fitur
*(Tambahkan Screenshot aplikasi yang berjalan dengan baik di sini!)*
- **Dashboard & UI**
  `![Home Screenshot](link_gambar)`
- **Kalkulasi Hill Cipher**
  `![Hill Screenshot](link_gambar)`
- **Aturan Digraphs Playfair**
  `![Playfair Screenshot](link_gambar)`
