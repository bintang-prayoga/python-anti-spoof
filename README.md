Tentu, berikut adalah terjemahan dari teks tersebut ke dalam bahasa Indonesia.

-----

# Pemindai Metadata File (python-anti-spoof)

Repositori ini berisi aplikasi kecil PyQt5 yang memindai file untuk menentukan tipe aslinya (menggunakan python-magic), mengumpulkan metadata (ukuran, stempel waktu), menghitung hash SHA256, dan dapat membuat laporan PDF.

README ini menjelaskan tiga cara untuk menjalankan aplikasi di Windows (bash shell):

  * Menjalankan *executable* yang sudah dikemas dari `dist/` (jika Anda memiliki *executable* yang sudah di-*build*)
  * Membangun (*build*) *executable* sendiri menggunakan PyInstaller dan `main.spec` yang disediakan
  * Menjalankan aplikasi secara langsung dengan `python main.py`

<!-- end list -->

1)  Menjalankan *executable* yang dikemas (dari `dist/`)

-----

Jika Anda sudah memiliki aplikasi yang dikemas di direktori `dist/` (dibuat oleh PyInstaller), Anda dapat menjalankannya secara langsung.

Catatan:

  * Di Windows, aplikasi yang dikemas biasanya berupa folder yang dibuat oleh PyInstaller jika tidak menggunakan `--onefile`, atau satu file `.exe` jika menggunakan `--onefile`.
  * Proyek ini menggunakan `main.spec` kustom yang menyertakan file data untuk `python-magic` dan `qfluentwidgets`.

Contoh (bash di Windows):

```bash
# Jika `dist/` berisi folder (misalnya `FileScannerApp`), jalankan EXE di dalamnya:
./dist/FileScannerApp/FileScannerApp.exe

# Jika `dist/` berisi satu file exe, jalankan langsung:
./dist/FileScannerApp.exe
```

Jika *executable* gagal dimulai, jalankan dari terminal untuk melihat pesan *error* yang dicetak. Penyebab paling umum adalah *library* atau file data yang hilang.

2)  Membangun *executable* sendiri dengan PyInstaller

-----

### Prasyarat

  * Python 3.8+ (versi yang kompatibel dengan PyQt5 dan paket Anda)
  * pip
  * Lingkungan virtual (venv) direkomendasikan

### Paket Python yang Diperlukan

Instal dependensi *runtime* utama yang digunakan oleh proyek:

```bash
pip install -r requirements.txt
```

Jika Anda tidak memiliki `requirements.txt`, paket terpenting adalah:

```bash
pip install PyQt5 python-magic-bin reportlab pyinstaller
```

Juga install kebutuhan untuk library `qfluentwidgets`

```bash
pip install "PyQt-Fluent-Widgets[full]" -i https://pypi.org/simple/
```
### Catatan tentang python-magic dan qfluentwidgets

  * Di Windows, gunakan `python-magic-bin` yang sudah menyertakan libmagic. Jika Anda mengalami masalah, coba `pip install python-magic-bin`.
  * `qfluentwidgets` berisi file sumber daya (resources) dalam direktori internal `_rc`. File `main.spec` yang disediakan mencoba untuk menyertakan folder tersebut.

### Langkah-langkah Membangun (bash di Windows)

```bash
# 1. Buat/aktifkan lingkungan virtual (opsional tapi disarankan)
python -m venv .venv
source .venv/Scripts/activate

# 2. Instal dependensi
pip install PyQt5 python-magic-bin reportlab pyinstaller

# 3. Instal dependensi qfluentwidgets
pip install "PyQt-Fluent-Widgets[full]" -i https://pypi.org/simple/

# 4. Bangun dengan PyInstaller menggunakan spec yang disertakan
pyinstaller --clean main.spec
```

Setelah selesai, periksa folder `dist/` untuk *executable* atau folder aplikasi yang dihasilkan. Jalankan *executable* seperti yang dijelaskan di bagian (1).

### Pemecahan Masalah (Troubleshooting) saat Membangun

  * Jika PyInstaller tidak dapat menemukan libmagic atau melaporkan file data yang hilang, pastikan `python-magic-bin` terinstal dan path data `main.spec` masih valid. Skrip `main.spec` mencetak informasi debug saat Anda menjalankan PyInstaller sehingga Anda dapat melihat path yang akan coba disertakannya.
  * Jika sumber daya qfluentwidgets hilang, konfirmasikan bahwa `qfluentwidgets` terinstal di lingkungan yang sama dan berisi direktori `_rc`. `main.spec` mencoba menyertakan folder ini sebagai `qfluentwidgets/_rc` di dalam paket.
  * Jika GUI gagal tetapi skrip berjalan dengan `python main.py`, bandingkan paket/versi lingkungan Anda.

<!-- end list -->

3)  Menjalankan aplikasi secara langsung dengan Python

-----

Ini adalah cara tercepat untuk menguji atau mengembangkan aplikasi. Jalankan dari root proyek di bash (Windows):

```bash
python main.py
```

### Catatan penting

  * Pastikan *interpreter* Python yang Anda gunakan telah menginstal paket-paket yang diperlukan.
  * Jika Anda melihat *error* seperti "Missing libraries. Did you 'pip install python-magic-bin qfluentwidgets'?" itu pertanda bahwa modul yang diperlukan tidak ada.
  * Jika `python-magic` memunculkan `ImportError` di Windows, gunakan `python-magic-bin` sebagai gantinya.

### Contoh sesi (bash di Windows)

```bash
# buat dan aktifkan venv
python -m venv .venv
source .venv/Scripts/activate

# Instal dependensi
pip install PyQt5 python-magic-bin reportlab

# Instal dependensi qfluentwidgets
pip install "PyQt-Fluent-Widgets[full]" -i https://pypi.org/simple/

# jalankan aplikasi
python main.py
```

Atau bangun dan jalankan *exe* yang dikemas:

```bash
pyinstaller --clean main.spec
./dist/FileScannerApp/FileScannerApp.exe
```

## Tambahan: Membuat laporan PDF

Aplikasi ini menggunakan `report.py` (ReportLab) untuk membuat laporan PDF. Jika Anda berencana menggunakan fitur "Simpan Laporan", instal ReportLab:

```bash
pip install reportlab
```

## Gerbang kualitas (daftar periksa cepat)

  * [ ] GUI dimulai saat menjalankan `python main.py`.
  * [ ] `verify_file_type` mengembalikan *dict* dengan kunci: `extension`, `detected_mime`, `description`, `hash_sha256`, `size`, `creation_time`, `modified_time`.
  * [ ] Pembuatan PDF melalui `report.py` berhasil ketika `reportlab` diinstal.
