# Lembar Jawab TOEFL Interaktif (PKN STAN) — Generator PDF (Python)

Repository/skrip ini menghasilkan **lembar jawab ujian TOEFL berbentuk PDF interaktif** (AcroForm) untuk kebutuhan ujian di **Politeknik Keuangan Negara STAN**. PDF yang dihasilkan memiliki:

- **Halaman identitas peserta** dengan kolom isian (textfield) seperti Program Studi, Semester, Tanggal, Mata Kuliah, No. Urut, Kelas, NPM, Nama, dan Nama Dosen. 
- **Halaman jawaban pilihan ganda** per section, dengan opsi **A–D** untuk setiap nomor, menggunakan **radio button** (satu jawaban per nomor).
- Struktur section default:
  - Listening Comprehension (50 soal)
  - Structure and Written Expressions (40 soal)
  - Reading Comprehension (50 soal)

Output default bernama: **`Lembar Jawab Ujian Kotak.pdf`**.


---

## Fitur Utama

- **PDF interaktif (fillable)**: peserta bisa mengetik identitas dan memilih jawaban langsung di PDF.
- **Tampilan “kotak” pilihan**: skrip menggambar kotak visual di setiap opsi, sementara inputnya memakai radio button untuk stabilitas (buttonStyle/shape `circle`).
- **Paging otomatis**: jika baris sudah melebihi batas per halaman atau posisi terlalu bawah, skrip otomatis membuat halaman lanjutan (Continued). 
- **Spasi ekstra tiap 5 nomor**: membantu keterbacaan dan mengurangi salah isi.  

---

## Prasyarat

- Python 3.9+ (disarankan)
- Library:
  - `reportlab`

Install dependensi:

```bash
pip install reportlab
```

---

## Cara Menjalankan

1. Simpan skrip Python (misalnya `generate_toefl_answer_sheet.py`).
2. Jalankan:

```bash
python generate_toefl_answer_sheet.py
```

3. File PDF akan muncul di folder yang sama dengan nama:

- `Lembar Jawab Ujian Kotak.pdf`  

---

## Kustomisasi Cepat

### 1) Ubah nama file output
Di bagian akhir skrip, ubah parameter `file_path`:

```python
generate_answer_sheet("Lembar Jawab Ujian Kotak.pdf")
```

Menjadi misalnya:

```python
generate_answer_sheet("LJK_TOEFL_STAN.pdf")
```

### 2) Ubah jumlah soal per section / tambah section
Edit daftar `sections`:

```python
sections = [
    ("Listening Comprehension", 50),
    ("Structure and Written Expressions", 40),
    ("Reading Comprehension", 50),
]
```

Contoh menambah section “Vocabulary” 30 soal:

```python
sections = [
    ("Listening Comprehension", 50),
    ("Structure and Written Expressions", 40),
    ("Reading Comprehension", 50),
    ("Vocabulary", 30),
]
```

### 3) Ubah opsi jawaban (default A–D)
Default pilihan:

```python
choices = ['A', 'B', 'C', 'D']
```

Jika ingin A–E (misalnya untuk format lain), ubah menjadi:

```python
choices = ['A', 'B', 'C', 'D', 'E']
```

> Catatan: jika menambah opsi, pertimbangkan juga penyesuaian `spacing_x` agar tidak terlalu rapat.

### 4) Ubah tampilan jarak/kerapatan baris
Parameter yang umum diutak-atik:

- `spacing_y` (jarak antar baris)
- `extra_spacing_factor` (tambahan spasi tiap 5 nomor)
- `max_rows_per_page` (batas baris per halaman)
- `square_visual_size` (ukuran kotak visual)
- `radio_button_interactive_size` (ukuran radio button)

---

## Struktur Logika Skrip

- `draw_first_page(...)`: membuat halaman identitas dengan beberapa `acroForm.textfield(...)`. 
- `draw_section(...)`: menggambar daftar nomor dan pilihan A–D dengan `acroForm.radio(...)` per nomor.
- `generate_answer_sheet(file_path)`: orkestrasi pembuatan halaman identitas, membuat halaman section, lalu menyimpan PDF.

---

## Troubleshooting

### PDF tidak bisa diisi / radio button tidak bisa dipilih
- Pastikan Anda membukanya di PDF viewer yang mendukung **AcroForm** (mis. Adobe Acrobat Reader).
- Beberapa browser PDF viewer kadang tidak mendukung semua field interaktif.

### Error terkait bentuk tombol (KeyError)
Skrip menggunakan `buttonStyle='circle'` dan `shape='circle'` untuk menghindari error bentuk tombol. 

---

## Catatan Implementasi & Kepatuhan

- Skrip ini **tidak melakukan scoring** dan **tidak membaca hasil** dari PDF; fokusnya hanya menghasilkan template LJK yang interaktif.
- Jika LJK perlu distandarisasi (mis. penomoran, field wajib, watermark, kode ujian), lakukan penyesuaian pada fungsi gambar (layout) sebelum dipakai secara operasional.

---
