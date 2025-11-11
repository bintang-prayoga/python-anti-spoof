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

### Screenshot Aplikasi

Berikut beberapa tangkapan layar aplikasi. Klik gambar untuk melihat versi ukuran penuh.

<p align="center">
  <a href="https://media.discordapp.net/attachments/819910038155952172/1437641111760797726/image.png?ex=6913fb1f&is=6912a99f&hm=723d68c56ae1fdc0c6b8138218eae9833ee7f991c0090f49d75c45aeb8b910e7&=&format=webp&quality=lossless&width=816&height=750">
    <img alt="Tampilan utama aplikasi" src="https://media.discordapp.net/attachments/819910038155952172/1437641111760797726/image.png?ex=6913fb1f&is=6912a99f&hm=723d68c56ae1fdc0c6b8138218eae9833ee7f991c0090f49d75c45aeb8b910e7&=&format=webp&quality=lossless&width=816&height=750" width="640" />
  </a>
  <br/>
  <em>Tampilan utama aplikasi</em>
</p>

<p align="center">
  <a href="https://media.discordapp.net/attachments/819910038155952172/1437641112255729744/image.png?ex=6913fb1f&is=6912a99f&hm=24bb64ace3f0cb1f8e352fb3b68b64cade158ad960dde53ce03c532bf8b02404&=&format=webp&quality=lossless&width=803&height=743">
    <img alt="Tampilan saat file di-scan" src="https://media.discordapp.net/attachments/819910038155952172/1437641112255729744/image.png?ex=6913fb1f&is=6912a99f&hm=24bb64ace3f0cb1f8e352fb3b68b64cade158ad960dde53ce03c532bf8b02404&=&format=webp&quality=lossless&width=803&height=743" width="640" />
  </a>
  <br/>
  <em>Tampilan ketika file di-scan</em>
</p>

<p align="center">
  <a href="https://media.discordapp.net/attachments/819910038155952172/1437641112746721363/image.png?ex=6913fb1f&is=6912a99f&hm=3689bcce37f3a2f5d263550b9e46448f537029f9b3d362c1f24487a579020be8&=&format=webp&quality=lossless&width=1058&height=747">
    <img alt="Contoh laporan PDF" src="https://media.discordapp.net/attachments/819910038155952172/1437641112746721363/image.png?ex=6913fb1f&is=6912a99f&hm=3689bcce37f3a2f5d263550b9e46448f537029f9b3d362c1f24487a579020be8&=&format=webp&quality=lossless&width=1058&height=747" width="720" />
  </a>
  <br/>
  <em>Contoh hasil laporan file (PDF)</em>
</p>