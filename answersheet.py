from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.colors import black, lightgrey

def draw_first_page(c, width, height):
    """
    Menggambar halaman pertama dengan kolom isian untuk Nama, NPM, dan Kelas.
    """
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2.0, height - 80, "Politeknik Keuangan Negara STAN")

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2.0, height - 100, "Lembar Jawab Ujian")

    # Posisi awal untuk label (baseline teks)
    x_label_start = 100
    y_current = height - 150 # Posisi Y awal untuk label pertama

    # Posisi X untuk awal semua kotak isian, agar rata kiri satu sama lain
    # Ini adalah koordinat X tetap untuk sisi kiri semua kotak isian
    x_field_align = 100 # Mengatur posisi X untuk semua kotak isian agar rata kiri satu sama lain

    field_height = 25 # Tinggi kotak isian
    field_width = 400
    
    # Spasi vertikal antara baseline label dan bagian atas kotak isian
    vertical_gap_label_to_field = 5 
    # Spasi vertikal total antara satu set label/kolom dengan set berikutnya
    vertical_spacing_between_pairs = 50 # Meningkatkan spasi vertikal antar pasangan

    c.setFont("Helvetica", 12)

    # Fungsi pembantu untuk menggambar label dan kolom isian
    def draw_input_field(label_text, field_name, tooltip_text, current_label_y):
        # Gambar teks label
        c.drawString(x_label_start, current_label_y, label_text)

        # Hitung posisi Y untuk bagian bawah kotak isian
        # current_label_y adalah baseline teks label.
        # Bagian atas kotak isian akan berada di current_label_y - vertical_gap_label_to_field.
        # Karena parameter 'y' untuk textfield adalah bagian bawah, maka:
        y_input_field_bottom = current_label_y - vertical_gap_label_to_field - field_height

        # Gambar kotak visual untuk kolom isian
        c.rect(x_field_align, y_input_field_bottom, field_width, field_height, stroke=1, fill=0) 
        
        # Buat kolom isian interaktif
        c.acroForm.textfield(
            name=field_name,
            tooltip=tooltip_text,
            x=x_field_align, # Menggunakan posisi X yang sejajar
            y=y_input_field_bottom,
            width=field_width,
            height=field_height,
            borderStyle='solid',
            borderColor=black,
            fillColor=None,
            textColor=black,
            fontName='Helvetica',
            fontSize=12,
            forceBorder=True
        )
        
        # Kembalikan posisi Y baru untuk baseline label berikutnya
        return current_label_y - vertical_spacing_between_pairs

    y_current = draw_input_field("Program Studi:", 'A. Prodi', 'Program Studi', y_current)
    y_current = draw_input_field("Semester:", 'B. Semester', 'Semester', y_current)
    y_current = draw_input_field("Tanggal/bulan/tahun:", 'C. Tanggal', 'Tanggal', y_current)
    y_current = draw_input_field("Judul Mata Kuliah:", 'D. Mata Kuliah', 'Mata Kuliah', y_current)
    y_current = draw_input_field("No. Urut:", 'E. Nomor Urut', 'Nomor Urut', y_current)
    y_current = draw_input_field("Kelas:", 'F. Kelas', 'Kelas', y_current)
    y_current = draw_input_field("NPM:", 'G. NPM', 'Nomor Pokok Mahasiswa', y_current)
    y_current = draw_input_field("Nama:", 'H. Nama', 'Nama', y_current)
    draw_input_field("Nama Dosen:", 'I. Dosen', 'Dosen', y_current)

def draw_section(c, section_title, num_questions, x_start, y_start, section_number):
    """
    Menggambar bagian soal dengan pilihan ganda.
    """
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x_start, y_start, f"Section {section_number}: {section_title}")
    y_current = y_start - 30
    c.setFont("Helvetica", 12)

    choices = ['A', 'B', 'C', 'D']
    spacing_y = 25  # Spasi vertikal dasar
    extra_spacing_factor = 0.5 # 50% spasi tambahan
    extra_spacing = spacing_y * extra_spacing_factor # Spasi tambahan
    spacing_x_base = 80
    
    # Spasi horizontal disesuaikan untuk mengakomodasi kotak dan teks
    spacing_x = spacing_x_base * 1.05 
    
    line_width = 0.5
    border_color = lightgrey
    row_height = 23      # Tinggi baris yang disesuaikan
    rows_on_page = 0
    max_rows_per_page = 25

    # Ukuran untuk visual kotak dan tombol radio interaktif
    square_visual_size = 16 # Ukuran sisi kotak yang digambar
    radio_button_interactive_size = 14 # Ukuran radio button interaktif (akan berbentuk lingkaran)

    for i in range(num_questions):
        q_num = i + 1
        
        # Periksa apakah perlu pindah halaman
        if rows_on_page >= max_rows_per_page or y_current < 50:
            c.showPage()
            y_current = A4[1] - 50
            rows_on_page = 0
            c.setFont("Helvetica", 12)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(x_start, y_current + 20, f"Section {section_number}: {section_title} (Continued)")
            y_current -= 30
            c.setFont("Helvetica", 12)

        row_y_top = y_current + row_height / 2
        row_y_bottom = y_current - row_height / 2

        # Gambar garis batas baris
        c.setStrokeColor(border_color)
        c.setLineWidth(line_width)
        c.line(x_start - 5, row_y_top, A4[0] - 50, row_y_top)
        c.line(x_start - 5, row_y_bottom, A4[0] - 50, row_y_bottom)
        c.setStrokeColor(black) # Kembalikan warna stroke ke hitam

        c.drawString(x_start, y_current, f"{q_num:>2}") # Nomor pertanyaan
        for j, choice in enumerate(choices):
            label = f"{section_title.replace(' ', '')}_{q_num}_{choice}"
            
            # Hitung posisi tengah untuk visual kotak dan tombol radio
            visual_center_x = x_start + 30 + j * spacing_x
            
            # Gambar kotak visual
            square_x = visual_center_x - square_visual_size / 2
            square_y = y_current + 2 - square_visual_size / 2 # Menyesuaikan dengan baseline teks
            c.rect(square_x, square_y, square_visual_size, square_visual_size, stroke=1, fill=0)

            # Posisikan radio button interaktif (berbentuk lingkaran) di tengah kotak visual
            radio_x_centered = square_x + (square_visual_size - radio_button_interactive_size) / 2
            radio_y_centered = square_y + (square_visual_size - radio_button_interactive_size) / 2
            
            c.acroForm.radio(
                name=f"{section_title}_{q_num}", # Nama grup radio button
                value=choice, # Nilai pilihan
                tooltip=label,
                x=radio_x_centered,
                y=radio_y_centered,
                buttonStyle='circle', # Kembali ke 'circle' untuk menghindari KeyError
                borderStyle='solid',
                shape='circle',       # Kembali ke 'circle' untuk menghindari KeyError
                size=radio_button_interactive_size,
            )
            # Posisikan teks pilihan (A, B, C, D) di sebelah kanan kotak
            c.drawString(square_x + square_visual_size + 4, y_current, choice)
        
        # Terapkan spasi tambahan setiap 5 nomor isian
        if q_num % 5 == 0:
            y_current -= (spacing_y + extra_spacing) # Pindah ke baris berikutnya dengan spasi tambahan
        else:
            y_current -= spacing_y # Pindah ke baris berikutnya dengan spasi biasa
        
        rows_on_page += 1

    # Gambar garis batas bawah bagian
    c.setStrokeColor(border_color)
    c.setLineWidth(line_width)
    # Sesuaikan perhitungan y untuk garis batas bawah agar sesuai dengan spasi terakhir
    # Ini sedikit rumit karena spasi bisa berbeda di akhir. Pendekatan yang lebih aman adalah dengan menggunakannya
    # y_current setelah loop.
    last_y_spacing_applied = (spacing_y + extra_spacing) if (num_questions % 5 == 0 and num_questions > 0) else spacing_y
    c.line(x_start - 5, y_current + last_y_spacing_applied + row_height / 2, A4[0] - 50, y_current + last_y_spacing_applied + row_height / 2)
    c.setStrokeColor(black)


def generate_answer_sheet(file_path):
    """
    Menghasilkan lembar jawaban PDF interaktif.
    """
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    x_start = 50
    y_start = height - 50

    # Gambar halaman pertama dengan informasi peserta
    draw_first_page(c, width, height)
    c.showPage() # Pindah ke halaman baru untuk bagian soal

    sections = [
        ("Listening Comprehension", 50),
        ("Structure and Written Expressions", 40),
        ("Reading Comprehension", 50),
    ]

    for idx, (title, num_questions) in enumerate(sections, start=1):
        # Untuk bagian kedua dan seterusnya, mulai di halaman baru
        if idx > 1:
            c.showPage()
            y_start = height - 50 # Reset posisi y_start untuk halaman baru
        draw_section(c, title, num_questions, x_start, y_start, idx)

    c.save() # Simpan PDF

# Panggil fungsi untuk menghasilkan PDF
generate_answer_sheet("Lembar Jawab Ujian Kotak.pdf")
