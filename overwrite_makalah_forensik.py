import os
import re
import subprocess
import time
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

BASE_DIR = r"c:\Users\user\Documents\paket_data_contoh"
IMG_DIR = os.path.join(BASE_DIR, "gambar_paper")
LOGO_PATH = os.path.join(BASE_DIR, "logo_gunadarma.png")

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_table_borders(table, color="B0BEC5", sz="6", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="4" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def build_makalah_forensik():
    doc = Document()
    
    # Page Setup: A4, Margins: Top 3cm (1.18 in), Bottom 3cm (1.18 in), Left 4cm (1.57 in), Right 3cm (1.18 in)
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.18)
    section.bottom_margin = Inches(1.18)
    section.left_margin = Inches(1.57)
    section.right_margin = Inches(1.18)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
    normal_style.paragraph_format.line_spacing = 1.35
    normal_style.paragraph_format.space_after = Pt(4)

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, size=12, before=0, after=4, line_spacing=1.35, color=None):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)', text)
            for tok in tokens:
                if not tok:
                    continue
                if tok.startswith("**") and tok.endswith("**"):
                    r = p.add_run(tok[2:-2])
                    r.font.bold = True
                elif tok.startswith("*") and tok.endswith("*"):
                    r = p.add_run(tok[1:-1])
                    r.font.italic = True
                elif tok.startswith("`") and tok.endswith("`"):
                    r = p.add_run(tok[1:-1])
                    r.font.name = "Consolas"
                    r.font.size = Pt(size - 1.5)
                else:
                    r = p.add_run(tok)
                    r.font.bold = bold
                    r.font.italic = italic
                r.font.name = 'Times New Roman'
                r.font.size = Pt(size)
                if color:
                    r.font.color.rgb = color
        return p

    def add_img(img_name, caption_text, width_in=5.2):
        img_path = os.path.join(IMG_DIR, img_name)
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run()
            run.add_picture(img_path, width=Inches(width_in))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(1)
            p_cap.paragraph_format.space_after = Pt(12)
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(10)
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    def add_table_data(title, headers, rows):
        p_tt = doc.add_paragraph()
        p_tt.paragraph_format.space_before = Pt(14)
        p_tt.paragraph_format.space_after = Pt(4)
        r_tt = p_tt.add_run(title)
        r_tt.font.name = 'Times New Roman'
        r_tt.font.size = Pt(10.5)
        r_tt.font.bold = True
        r_tt.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

        table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table, color="B0BEC5", sz="6")

        # Header Row
        hdr_row = table.rows[0]
        for c_idx, h_text in enumerate(headers):
            cell = hdr_row.cells[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(h_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            set_cell_background(cell, "1E3A8A")
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)

        # Body Rows
        for r_idx, r_data in enumerate(rows):
            row = table.rows[r_idx + 1]
            bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(r_data):
                cell = row.cells[c_idx]
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.15
                
                # Check alignment
                if c_idx == 0 or len(val) < 15:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
                clean_val = val.replace("**", "").replace("`", "")
                run = p.add_run(clean_val)
                run.font.name = 'Times New Roman'
                run.font.size = Pt(9)
                
                if "COCOK" in val or "MATCH" in val:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
                elif "KRITIS" in val or "BERUBAH" in val:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(0xB7, 0x1C, 0x1C)
                elif val.startswith("`") and val.endswith("`"):
                    run.font.name = "Consolas"
                    run.font.size = Pt(8.5)

                set_cell_background(cell, bg)
                set_cell_margins(cell, top=90, bottom=90, left=120, right=120)

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(4)

    # ==================== COVER PAGE ====================
    add_p("INVESTIGASI FORENSIK DIGITAL SERANGAN SIBER MULTI-VEKTOR MENGGUNAKAN METODOLOGI NIST SP 800-86",
          align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, before=10, after=8, line_spacing=1.2, color=RGBColor(0x1A, 0x25, 0x2F))
    add_p("Studi Kasus: Eksploitasi Web Server HRMS, Spear-Phishing Follina (CVE-2022-30190), dan Ransomware pada PT. Satseet International",
          align=WD_ALIGN_PARAGRAPH.CENTER, size=13, before=0, after=24, line_spacing=1.2, color=RGBColor(0x4A, 0x55, 0x68))

    # Logo Gunadarma
    if os.path.exists(LOGO_PATH):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(8)
        p_logo.paragraph_format.space_after = Pt(28)
        run_logo = p_logo.add_run()
        run_logo.add_picture(LOGO_PATH, width=Inches(2.5))

    add_p("Disusun Oleh:", align=WD_ALIGN_PARAGRAPH.CENTER, size=12, before=0, after=10)

    # Author Table
    authors = [
        ("Fajar Daffa D.", "50423442"),
        ("Farrel Dhiyas Ulhaq", "50423467"),
        ("Feriyan Eka Nanda", "50423500"),
        ("Hanif Maulana A.F.", "50423568"),
        ("Kimi Sholihudin SJB", "50423698")
    ]
    t_auth = doc.add_table(rows=len(authors), cols=2)
    t_auth.alignment = WD_TABLE_ALIGNMENT.CENTER
    # No borders for author table
    tblPr = t_auth._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:bottom w:val="none"/>
            <w:insideH w:val="none"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

    for idx, (nama, npm) in enumerate(authors):
        row = t_auth.rows[idx]
        
        c0 = row.cells[0]
        c0.width = Inches(2.6)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(nama)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(12)

        c1 = row.cells[1]
        c1.width = Inches(1.8)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(npm)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)

    # Space before institution
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(36)

    # Institution Block
    add_p("JURUSAN TEKNIK INFORMATIKA", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, before=0, after=3)
    add_p("FAKULTAS TEKNOLOGI INDUSTRI", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, before=0, after=3)
    add_p("UNIVERSITAS GUNADARMA", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, before=0, after=4)
    add_p("2026", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=0, after=0)

    # Page Break to Abstract
    doc.add_page_break()

    # ==================== ABSTRAK ====================
    add_p("ABSTRAK", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=10, after=12)
    add_p(
        "Peningkatan frekuensi dan kompleksitas serangan siber modern menuntut pendekatan investigasi insiden yang "
        "terstruktur, akuntabel, dan dapat dipertanggungjawabkan secara hukum. Penelitian ini menyajikan investigasi "
        "forensik digital pascainsiden serangan multi-vektor terhadap sistem Human Resource Management System (HRMS) "
        "dan web server PT. Satseet International yang terjadi pada rentang waktu 5 hingga 22 November 2024. "
        "Metodologi yang diterapkan mengacu pada standar National Institute of Standards and Technology Special "
        "Publication 800-86 (NIST SP 800-86) yang mencakup empat fase utama: Collection, Examination, Analysis, dan "
        "Reporting. Melalui implementasi toolkit forensik terotomatisasi berbasis Python, dilakukan proses akuisisi "
        "bukti digital, pembangkitan nilai hash kriptografis (Chain of Custody), analisis 113 baris log akses HTTP, "
        "pencocokan Indicator of Compromise (IOC), serta rekonstruksi linimasa (timeline analysis). Hasil investigasi "
        "mengungkap bahwa aktor ancaman BlackPython Team memulai serangan melalui Directory Traversal pada web server "
        "untuk mengekstraksi berkas konfigurasi sensitif (.env dan autoload.php), dilanjutkan dengan operasi spear-phishing "
        "bertema rekrutmen yang memanfaatkan kerentanan Remote Code Execution Follina (CVE-2022-30190). Rangkaian serangan "
        "berujung pada penyusupan trojan backdoor (update.exe) dan enkripsi berkas oleh ransomware (ransom.exe). Laporan "
        "ini menyimpulkan temuan teknis serta merumuskan rekomendasi mitigasi komprehensif mencakup validasi input, "
        "pembaruan keamanan, strategi cadangan data 3-2-1, dan peningkatan kesadaran keamanan bagi organisasi.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, after=12, line_spacing=1.35
    )
    add_p("**Kata Kunci:** Forensik Digital, NIST SP 800-86, Directory Traversal, Follina (CVE-2022-30190), Ransomware, Chain of Custody.",
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, after=24)

    # Page Break to Abstract EN
    doc.add_page_break()

    # ==================== ABSTRACT (EN) ====================
    add_p("ABSTRACT", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=10, after=12)
    add_p(
        "*The increasing frequency and sophistication of cyberattacks necessitate a structured, accountable, and legally "
        "admissible incident investigation approach. This paper presents a post-incident digital forensic investigation "
        "on a multi-vector cyberattack targeting the Human Resource Management System (HRMS) and web server of PT. Satseet "
        "International between November 5 and November 22, 2024. The methodology strictly adopts the National Institute of "
        "Standards and Technology Special Publication 800-86 (NIST SP 800-86) framework, comprising four foundational phases: "
        "Collection, Examination, Analysis, and Reporting. Utilizing an automated Python-based forensic toolkit, digital "
        "evidence acquisition, cryptographic hashing for Chain of Custody, inspection of 113 HTTP access log records, "
        "Indicator of Compromise (IOC) matching, and cross-source timeline reconstruction were systematically conducted. "
        "The findings demonstrate that the threat group 'BlackPython Team' initiated the breach via Directory Traversal "
        "to harvest sensitive server configuration files (.env and autoload.php), followed by a spear-phishing campaign "
        "exploiting the Follina Remote Code Execution vulnerability (CVE-2022-30190). The intrusion culminated in the deployment "
        "of a trojan backdoor (update.exe) and critical data encryption by ransomware (ransom.exe). This study delivers technical "
        "evidence correlation and proposes robust mitigation strategies, including strict input sanitization, security patching, "
        "3-2-1 backup architecture, and employee cybersecurity awareness.*",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, after=12, line_spacing=1.35
    )
    add_p("**Keywords:** Digital Forensics, NIST SP 800-86, Directory Traversal, Follina (CVE-2022-30190), Ransomware, Incident Response.",
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, after=24)

    doc.add_page_break()

    # ==================== BAB I ====================
    add_p("BAB I", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=10, after=2)
    add_p("PENDAHULUAN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=0, after=14)

    add_p("1.1 Latar Belakang", bold=True, size=12, before=8, after=4)
    add_p(
        "Transformasi digital dalam sektor korporasi telah mendorong sentralisasi pengelolaan data pegawai dan "
        "operasional bisnis ke dalam sistem terintegrasi, seperti Human Resource Management System (HRMS). Namun, "
        "perluasan permukaan serangan (attack surface) tanpa diimbangi postur pertahanan yang memadai memicu kerentanan "
        "terhadap serangan siber terorganisir. Berdasarkan laporan lanskap ancaman Badan Siber dan Sandi Negara (BSSN) "
        "tahun 2024, anomali trafik serangan siber di Indonesia mencapai lebih dari 330 juta aktivitas mencurigakan "
        "dengan puncak tertinggi terjadi pada bulan Desember sebanyak 112 juta anomali (Gambar 1)."
    )

    add_img("gambar_01_grafik_anomali.png", "Gambar 1. Grafik Anomali Trafik Serangan Siber di Indonesia Tahun 2024 (Data Resmi BSSN)", 5.2)

    add_p(
        "Pada rentang 5–22 November 2024, PT. Satseet International mengalami insiden keamanan siber berskala masif yang "
        "mengakibatkan lumpuhnya operasional HRMS, kebocoran data pegawai, serta enkripsi berkas penting perusahaan oleh "
        "kelompok penyerang yang menamakan diri BlackPython Team. Insiden ini tidak berlangsung secara tunggal, melainkan "
        "melalui kombinasi serangan multi-vektor: peretasan awal melalui eksploitasi web server, rekayasa sosial "
        "(spear-phishing), eksekusi kode jarak jauh (Remote Code Execution / RCE), hingga penyebaran ransomware."
    )
    add_p(
        "Guna mengungkap anatomi serangan secara utuh dan menjamin keabsahan bukti digital di ranah investigasi maupun "
        "hukum, diperlukan metodologi forensik yang terstandarisasi. Standar NIST SP 800-86 dipilih karena menyediakan "
        "kerangka kerja investigasi sistematis yang menjamin keutuhan (integrity), keterulangan (repeatability), dan "
        "keterlacakan (chain of custody) dari seluruh artefak digital."
    )

    add_p("1.2 Rumusan Masalah", bold=True, size=12, before=8, after=4)
    add_p("1. Bagaimana mengidentifikasi, mengamankan, dan memverifikasi integritas bukti digital yang diperoleh pascaserangan pada sistem PT. Satseet International?")
    add_p("2. Bagaimana pola dan teknik serangan multi-vektor (Directory Traversal, Follina CVE-2022-30190, dan Ransomware) dapat direkonstruksi ke dalam linimasa kronologis yang valid?")
    add_p("3. Apa langkah-langkah mitigasi dan tata kelola keamanan yang perlu diterapkan untuk mencegah insiden berulang?")

    add_p("1.3 Tujuan Penelitian", bold=True, size=12, before=8, after=4)
    add_p("1. Menerapkan metodologi NIST SP 800-86 (Collection, Examination, Analysis, Reporting) dalam menginvestigasi insiden keamanan siber.")
    add_p("2. Membuktikan integritas bukti digital melalui kalkulasi hash kriptografis ganda (MD5, SHA-1, SHA-256).")
    add_p("3. Melakukan deteksi anomali pada log web server serta mencocokkan Indicator of Compromise (IOC).")
    add_p("4. Menyusun laporan investigasi forensik akademik yang komprehensif dan aplikatif sebagai bahan evaluasi institusi.")

    add_p("1.4 Batasan Masalah", bold=True, size=12, before=8, after=4)
    add_p("1. Investigasi difokuskan pada artefak digital yang disediakan dalam paket kasus PT. Satseet International, meliputi log web server (access.log), catatan akuisisi, berkas lampiran phishing, dan rekaman peristiwa sistem (events.csv).")
    add_p("2. Toolkit forensik yang digunakan diimplementasikan dalam skrip terotomatisasi Python 3.8+ berbasis pustaka standar defensif, selaras dengan prinsip-prinsip NIST SP 800-86.")

    doc.add_page_break()

    # ==================== BAB II ====================
    add_p("BAB II", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=10, after=2)
    add_p("LANDASAN TEORI", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=0, after=14)

    add_p("2.1 Forensik Digital dan Standar NIST SP 800-86", bold=True, size=12, before=8, after=4)
    add_p(
        "Forensik digital didefinisikan sebagai penerapan prinsip-prinsip ilmiah terhadap penemuan, validasi, "
        "identifikasi, analisis, dan interpretasi bukti digital yang berasal dari media digital untuk memfasilitasi "
        "rekonstruksi peristiwa. National Institute of Standards and Technology menerbitkan panduan NIST SP 800-86 "
        "(Guide to Integrating Forensic Techniques into Incident Response) yang menetapkan empat fase dasar:"
    )
    add_p("1. **Collection (Pengumpulan):** Proses identifikasi, pelabelan, pencatatan, dan pengamanan sumber bukti fisik maupun digital dengan menjaga Chain of Custody.")
    add_p("2. **Examination (Pemeriksaan):** Pemrosesan bukti mentah secara forensik menggunakan teknik ekstraksi artefak dan verifikasi keaslian melalui algoritma cryptographic hashing.")
    add_p("3. **Analysis (Analisis):** Penerapan metode analitis untuk menarik kesimpulan logis, menentukan vektor serangan, pelaku (threat actor), serta dampak insiden.")
    add_p("4. **Reporting (Pelaporan):** Penyajian hasil analisis secara formal, transparan, dan terstruktur yang mencakup prosedur, temuan, keterbatasan, dan rekomendasi mitigasi.")

    add_img("gambar_02_alur_nist.png", "Gambar 2. Siklus Alur Investigasi 4 Tahapan Standar NIST SP 800-86", 4.2)

    add_p("2.2 Integritas Bukti dan Chain of Custody", bold=True, size=12, before=8, after=4)
    add_p(
        "Chain of Custody merupakan dokumentasi kronologis yang mencatat perolehan, pengendalian, pemindahan, "
        "analisis, dan penyimpanan bukti digital. Integritas berkas dibuktikan dengan menghasilkan intisari pesan "
        "(message digest) melalui fungsi hash kriptografis:"
    )
    add_p("- **MD5 (128-bit):** Algoritma ringkasan pesan cepat untuk verifikasi awal.")
    add_p("- **SHA-1 (160-bit):** Standar kriptografi pelengkap integritas.")
    add_p("- **SHA-256 (256-bit):** Standar hashing modern yang memiliki ketahanan benturan (collision resistance) sangat tinggi, wajib disertakan dalam standar forensik internasional.")

    add_p("2.3 Vektor Serangan Siber Terkait", bold=True, size=12, before=8, after=4)
    add_p(
        "1. **Directory Traversal (Path Traversal):** Kerentanan aplikasi web yang memungkinkan penyerang membaca berkas "
        "di luar direktori web root dengan menyuntikkan karakter sekuens khusus seperti `../` atau representasi URL-encoded "
        "`%2e%2e%2f`. Tujuannya adalah memperoleh kredensial basis data atau berkas konfigurasi sistem (`/etc/passwd`, `.env`)."
    )
    add_p(
        "2. **Follina Exploit (CVE-2022-30190):** Kerentanan zero-day pada Microsoft Windows Support Diagnostic Tool (MSDT) "
        "yang dipicu saat membuka atau melihat pratinjau dokumen Microsoft Office (.docx/.rtf). Kerentanan ini memungkinkan "
        "penyerang mengeksekusi kode PowerShell jarak jauh (Remote Code Execution) dengan hak akses pengguna lokal tanpa perlu macro aktif."
    )
    add_p(
        "3. **Ransomware dan Trojan Backdoor:** Perangkat lunak berbahaya yang mengenkripsi berkas korban menggunakan "
        "enkripsi asimetris/simetris dan menuntut uang tebusan (ransom). Trojan backdoor dipasang untuk mempertahankan "
        "akses persisten (persistence) ke dalam sistem internal korban."
    )

    doc.add_page_break()

    # ==================== BAB III ====================
    add_p("BAB III", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=10, after=2)
    add_p("METODOLOGI PENELITIAN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=0, after=14)

    add_p("3.1 Kerangka Kerja Eksperimen", bold=True, size=12, before=8, after=4)
    add_p(
        "Penelitian ini mengadopsi alur eksperimen empiris berbasis NIST SP 800-86 dengan tahapan kerja operasional "
        "terstruktur seperti disajikan pada Gambar 3:"
    )

    add_img("diagram_metodologi_eksperimen.png", "Gambar 3. Diagram Alur Kerja Eksperimen Investigasi Forensik NIST SP 800-86 secara Terotomasi", 5.2)

    add_p("3.2 Lingkungan dan Alat Pengujian", bold=True, size=12, before=8, after=4)
    add_p("Pengujian dilakukan pada lingkungan terkontrol dengan spesifikasi perangkat keras dan lunak sebagai berikut:")

    t3_headers = ["Kategori Komponen", "Spesifikasi / Alat", "Versi", "Peran dalam Investigasi"]
    t3_rows = [
        ["Sistem Analis", "Microsoft Windows 11 Pro 64-bit", "Build 21996", "Lingkungan kerja analisis forensik"],
        ["Interpreter", "Python Standard Environment", "3.13.1", "Eksekusi otomasi skrip forensik"],
        ["Toolkit Forensik", "forensik_nist.py", "1.0 (Custom)", "Implementasi modul 4 fase NIST SP 800-86"],
        ["Pustaka Kriptografi", "Python hashlib", "Bawaan", "Pembangkitan nilai hash MD5, SHA-1, SHA-256"],
        ["Ekstraksi Log", "Python re & csv", "Bawaan", "Parsing pola Directory Traversal & agregasi linimasa"],
        ["Alat Komparator", "FTK Imager & Autopsy", "4.7.1 / 4.21.0", "Standar acuan verifikasi disk image & artefak OS"],
        ["Analisis Jaringan", "Wireshark Protocol Analyzer", "4.4.2", "Rekonsiliasi paket lalu lintas data HTTP/TLS"],
        ["Intelijen Malware", "VirusTotal Cloud Engine", "API v3", "Verifikasi identitas trojan & ransomware"]
    ]
    add_table_data("Tabel 3.1. Spesifikasi Perangkat Keras dan Lunak Penelitian", t3_headers, t3_rows)

    doc.add_page_break()

    # ==================== BAB IV ====================
    add_p("BAB IV", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=10, after=2)
    add_p("HASIL DAN PEMBAHASAN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=0, after=14)

    add_p("4.1 Tahap 1: Collection (Akuisisi Bukti Digital dan Hashing)", bold=True, size=12, before=8, after=4)
    add_p(
        "Proses pengumpulan bukti digital diawali dengan menerima berkas hasil akuisisi media penyimpanan (disk image) "
        "dan live memory acquisition dari sistem korban PT. Satseet International (Gambar 4)."
    )

    add_img("gambar_03_hasil_akuisisi.png", "Gambar 4. Berkas Disk Image windowsransom yang diterima dari hasil akuisisi fisik komputer korban", 4.8)

    add_p(
        "Selanjutnya, toolkit forensik_nist.py menjalankan perintah collect terhadap direktori bukti guna mengekstraksi "
        "metadata, membangkitkan hash kriptografis ganda, dan membandingkannya terhadap daftar Indicator of Compromise "
        "(ioc.txt). Hasilnya dicatat ke dalam manifest resmi manifest.json (Tabel 4.1)."
    )

    t41_headers = ["Nama Berkas Bukti", "Ukuran", "Nilai Hash MD5", "Nilai Hash SHA-1", "Nilai Hash SHA-256", "Kecocokan IOC"]
    t41_rows = [
        ["access.log", "10.805 B", "0a2e379b32e185873ec8b408892f39c0", "82cf214b62db4df43b7e73507119ff391f1a5f6e", "6c1445ee259c792cfc261dedfd7f7d99e001dd05b0c7839b6bae1288371f58bf", "-"],
        ["catatan_akuisisi.txt", "169 B", "4c7bf69bf17b70743b2f293b722d3b7e", "bcebb5523a789a3f2dbd1112d308078e878347f7", "42d326d9684b2143fed0d3a67bb736a325140dab099b6aa9bdf591a49a893561", "-"],
        ["lampiran_simulasi.txt", "162 B", "a5f22f6d0f666f7f63f58a361a9bc348", "4f3876d540268dfc949fef56f2d93e8784d00810", "8b14132601aa8764960ea80eb246e7387c1adbf1e42f026c870e19fda39d3d04", "COCOK (MATCH)"]
    ]
    add_table_data("Tabel 4.1. Manifest Inventaris Bukti Digital dan Hasil Hashing Kriptografis", t41_headers, t41_rows)

    add_p(
        "**Temuan Kunci Fase Collection:** Nilai hash SHA-256 dari `lampiran_simulasi.txt` (`8b14132601aa87649...`) "
        "terbukti cocok 100% dengan daftar IOC pada `ioc.txt`. Berkas ini merupakan representasi dari dokumen kurikulum vitae "
        "`Lamaran kerja maya putri follina.zip` yang disebarkan penyerang sebagai pembawa muatan eksploitasi."
    )

    add_p("4.2 Tahap 2: Examination (Pemeriksaan dan Verifikasi Integritas)", bold=True, size=12, before=8, after=4)
    add_p(
        "Tahap pemeriksaan berfokus pada pengujian keaslian bukti digital guna memastikan bahwa tidak terjadi "
        "korupsi data atau manipulasi yang disengaja pascaakuisisi."
    )

    add_img("gambar_06_verifikasi_hash.png", "Gambar 5. Hasil Verifikasi Nilai Hash MD5 dan SHA-1 pada FTK Imager yang Menunjukkan Status Match", 4.6)

    t42_headers = ["Nama Berkas", "Status Integritas", "Perubahan Algoritma Hash", "Kesimpulan Keabsahan"]
    t42_rows = [
        ["access.log", "COCOK", "Tidak ada perbedaan", "Sah / Valid untuk Pembuktian"],
        ["catatan_akuisisi.txt", "COCOK", "Tidak ada perbedaan", "Sah / Valid untuk Pembuktian"],
        ["lampiran_simulasi.txt", "COCOK", "Tidak ada perbedaan", "Sah / Valid untuk Pembuktian"]
    ]
    add_table_data("Tabel 4.2. Hasil Uji Verifikasi Integritas dan Keabsahan Bukti", t42_headers, t42_rows)

    add_p(
        "Hasil verifikasi menunjukkan bahwa seluruh berkas berstatus COCOK. Pengujian ketahanan manipulasi (tamper resistance "
        "test) yang dilakukan dengan menyuntikkan 1 karakter ke dalam berkas segera menghasilkan status BERUBAH, membuktikan "
        "keandalan sistem dalam mendeteksi perubahan data sekecil apa pun."
    )
    add_p(
        "Selain verifikasi hash, identifikasi lingkungan sistem korban juga berhasil diungkap melalui artefak live forensic:"
    )
    add_p("- **Nama Komputer:** `DESKTOP-R0IR99H`")
    add_p("- **Sistem Operasi:** Microsoft Windows 11 Pro Build 21996")
    add_p("- **Alamat IP Internal Korban:** `192.168.1.28`")

    add_img("gambar_07_computer_os.png", "Gambar 6. Identifikasi Nama Komputer (DESKTOP-R0IR99H) dan Sistem Operasi (Windows 11 Pro)", 4.8)
    add_img("gambar_08_info_jaringan.png", "Gambar 7. Identifikasi Informasi Antarmuka Jaringan dan IP Lokal Komputer Korban (192.168.1.28)", 4.8)

    add_p("4.3 Tahap 3: Analysis (Analisis Log Web dan Deteksi Serangan)", bold=True, size=12, before=8, after=4)
    add_p(
        "Pemeriksaan mendalam terhadap berkas `access.log` yang memuat 113 baris transaksi HTTP berhasil mengisolasi "
        "aktivitas penyerangan yang bersumber dari alamat IP `192.168.1.11` pada tanggal 5 November 2024."
    )

    add_img("gambar_10_directory_traversal.png", "Gambar 8. Bukti Analisis Wireshark yang Mengungkap Serangan Directory Traversal oleh IP 192.168.1.11", 5.2)

    t43_headers = ["Timestamp (WIB)", "Alamat IP", "Metode", "Jalur Target (Requested URI)", "Status", "Evaluasi Forensik"]
    t43_rows = [
        ["05/Nov/2024 19:58:02", "192.168.1.11", "GET", "/web/index.php/../../../etc/passwd", "404", "Pola traversal teks polos; target file kredensial Linux."],
        ["05/Nov/2024 19:58:05", "192.168.1.11", "GET", "/web/index.php/..%2f..%2f..%2fetc/passwd", "403", "Pola traversal dengan URL encoding (%2f = /); diblokir."],
        ["05/Nov/2024 19:58:09", "192.168.1.11", "GET", "/web/%2e%2e/%2e%2e/config/database.yml", "404", "Enkoding titik ganda (%2e%2e); mencari konfigurasi database."],
        ["05/Nov/2024 19:58:14", "192.168.1.11", "GET", "/web/..%2f..%2fsrc/vendor/autoload.php", "200", "BERHASIL: Komponen aplikasi web berhasil diakses penyerang."],
        ["05/Nov/2024 19:58:20", "192.168.1.11", "GET", "/web/..%2f..%2fsrc/config/.env", "200", "KRITIS / BERHASIL: Berkas .env (berisi password & API key) bocor!"]
    ]
    add_table_data("Tabel 4.3. Rincian Rekaman Serangan Directory Traversal pada Web Server", t43_headers, t43_rows)

    add_img("gambar_11_file_sensitif.png", "Gambar 9. Potongan Berkas Konfigurasi Sensitif Web Server yang Terbaca Akibat Celah Directory Traversal", 4.8)

    add_p(
        "**Evaluasi Temuan Log:** Penyerang memanfaatkan variasi URL-encoding (`%2e%2e%2f`) untuk menghindari deteksi filter "
        "WAF sederhana. Akses dengan status kode `200 OK` ke berkas `autoload.php` dan `.env` menandakan kebocoran informasi "
        "kredensial yang fatal, yang membuka jalan bagi penyerang untuk login ke portal HRMS pada tahap berikutnya."
    )

    add_p("4.4 Rekonstruksi Linimasa Serangan Terpadu (Timeline Analysis)", bold=True, size=12, before=8, after=4)
    add_p(
        "Investigasi mengkorelasikan seluruh artefak: log akses web, email phishing, akses file lokal, eksekusi malware, "
        "dan intelijen media sosial (OSINT)."
    )

    add_img("gambar_12_email_phishing.png", "Gambar 10. Email Rekayasa Sosial Spear-Phishing Bertema Lowongan Kerja dari Akun Palsu Maya Putri", 4.6)
    add_img("gambar_15_download_lamaran.png", "Gambar 11. Bukti Jejak Digital Korban Mengunduh Berkas Lampiran Lamaran kerja maya putri follina.zip", 5.0)
    add_img("gambar_16_akses_malware.png", "Gambar 12. Catatan Akses Waktu Nyata terhadap Berkas Berbahaya update.exe dan ransom.exe", 4.5)
    add_img("gambar_17_file_terenkripsi.png", "Gambar 13. Daftar Berkas Korban yang Terkunci dan Berubah Ekstensi Menjadi .wasted", 4.8)

    t44_headers = ["Tanggal & Waktu", "Sumber", "Entitas / Akun", "Deskripsi Peristiwa Serangan", "Fase Serangan"]
    t44_rows = [
        ["05/Nov/2024 19:58:02", "access.log", "192.168.1.11", "Percobaan Directory Traversal ke /etc/passwd (HTTP 404)", "Reconnaissance"],
        ["05/Nov/2024 19:58:05", "access.log", "192.168.1.11", "Percobaan Directory Traversal dengan URL encoding (HTTP 403)", "Evasion Attempt"],
        ["05/Nov/2024 19:58:14", "access.log", "192.168.1.11", "Akses ke file autoload.php berhasil (HTTP 200)", "Information Gathering"],
        ["05/Nov/2024 19:58:20", "access.log", "192.168.1.11", "Akses ke berkas rahasia .env berhasil (HTTP 200)", "Credential Harvesting"],
        ["06/Nov/2024 17:54:00", "Email Gateway", "Local User 2", "Menerima email pertanyaan lowongan kerja dari Maya Putri", "Reconnaissance Social"],
        ["19/Nov/2024 22:18:00", "Email Gateway", "Local User 1", "Email phishing lanjutan masuk membawa berkas lamaran kerja", "Weaponization"],
        ["20/Nov/2024 13:23:00", "Web Log", "192.168.1.11", "Pelaku mencoba mengakses antarmuka portal login HRMS", "Initial Connection"],
        ["20/Nov/2024 13:29:00", "Web Log", "192.168.1.11", "Pelaku berhasil login ke portal HRMS menggunakan kredensial bocor", "Privilege Access"],
        ["20/Nov/2024 13:29:00", "Email Client", "Local User 1", "Lampiran lamaran kerja Folline.zip diunduh oleh korban", "User Execution"],
        ["20/Nov/2024 13:33:00", "Disk / Endpoint", "Local User 1", "Dokumen riwayat hidup dibuka, mengeksekusi CVE-2022-30190", "Remote Code Execution"],
        ["20/Nov/2024 13:49:00", "Disk / Endpoint", "Local User 1", "Eksekusi otomatis update.exe (Trojan Backdoor aktif)", "Persistence / C2"],
        ["20/Nov/2024 13:50:00", "Disk / Endpoint", "Local User 1", "Eksekusi ransom.exe (main_v2.exe / Python.Filecoder)", "Malware Execution"],
        ["20/Nov/2024 13:59:00", "Disk / Storage", "Sistem HRMS", "Berkas-berkas penting terenkripsi dan berekstensi .wasted", "Impact (Ransomware)"],
        ["22/Nov/2024 09:00:00", "OSINT / Telegram", "BlackPython Team", "Publikasi klaim pencurian data karyawan dan tuntutan pemerasan", "Exfiltration & Extortion"]
    ]
    add_table_data("Tabel 4.4. Rekonstruksi Linimasa Komprehensif Serangan Multi-Vektor", t44_headers, t44_rows)

    add_p("4.5 Analisis Atribusi dan Karakteristik Malware", bold=True, size=12, before=8, after=4)
    add_p(
        "1. **Analisis Eksploitasi Follina (CVE-2022-30190):** Analisis dokumen lampiran pada VirusTotal menunjukkan "
        "deteksi eksploitasi terhadap kerentanan Microsoft Support Diagnostic Tool (MSDT). Kerentanan ini memungkinkan "
        "eksekusi kode PowerShell tanpa interaksi makro Office, menjadikannya sarana efektif untuk menyuntikkan muatan berbahaya dari jarak jauh."
    )

    add_img("gambar_18_virustotal_follina.png", "Gambar 14. Hasil Analisis Dokumen Lampiran Phishing pada VirusTotal yang Mendeteksi Eksploitasi CVE-2022-30190", 5.2)

    add_p(
        "2. **Karakteristik Trojan Backdoor (`update.exe`):** Hasil pemindaian VirusTotal mengklasifikasikan `update.exe` "
        "sebagai Trojan.Win32/Shell.R128S dan Backdoor.Win/shellcode.apid. Berkas ini berfungsi membuka koneksi balik (reverse shell) "
        "guna mempertahankan kendali penyerang atas mesin korban."
    )

    add_img("gambar_19_virustotal_update.png", "Gambar 15. Hasil Deteksi Berkas update.exe pada VirusTotal sebagai Trojan Backdoor", 5.2)

    add_p(
        "3. **Karakteristik Ransomware (`ransom.exe`):** Berkas `ransom.exe` (awalnya dinamai `main_v2.exe`) diidentifikasi "
        "oleh mesin antivirus sebagai Ransom:Win32/Filecoder dan Python.Filecoder. Malware ini mengenkripsi dokumen penting dan menambahkan ekstensi `.wasted`."
    )

    add_img("gambar_20_virustotal_ransom.png", "Gambar 16. Hasil Deteksi Berkas ransom.exe pada VirusTotal sebagai Ransomware Python.Filecoder", 5.2)

    add_p(
        "4. **Atribusi Pelaku Ancaman:** Berdasarkan klaim di saluran Telegram pada 22 November 2024, serangan dilakukan oleh kelompok "
        "peretas BlackPython Team. Motif serangan adalah pemerasan finansial (financial extortion) dengan taktik double extortion (mencuri data pegawai lalu mengenkripsi sistem)."
    )

    t45_headers = ["Parameter Evaluasi", "Rincian Temuan Investigasi Forensik"]
    t45_rows = [
        ["Rentang Waktu Insiden", "5 – 22 November 2024"],
        ["Sistem yang Diserang", "Human Resource Management System (HRMS) dan Web Server"],
        ["Vektor Serangan", "Directory Traversal, Remote Code Execution (Follina), Ransomware"],
        ["Identitas Aktor Penyerang", "Sindikat BlackPython Team"],
        ["Dampak Kerusakan", "Enkripsi data penting korporat, kebocoran data sensitif karyawan, gangguan operasional HRMS, risiko reputasi dan hukum"],
        ["Integritas Bukti Forensik", "Terverifikasi utuh 100% (MD5, SHA-1, SHA-256 match)"]
    ]
    add_table_data("Tabel 4.5. Ringkasan Singkat Hasil Analisis Forensik Digital (Laporan Eksekutif)", t45_headers, t45_rows)

    doc.add_page_break()

    # ==================== BAB V ====================
    add_p("BAB V", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=10, after=2)
    add_p("REKOMENDASI DAN STRATEGI MITIGASI", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=0, after=14)

    add_p("Berdasarkan temuan forensik, dirumuskan strategi pertahanan mendalam (defense-in-depth) mencakup aspek teknis, prosedural, dan tata kelola:")

    add_p("5.1 Pengamanan Aplikasi Web dan Server", bold=True, size=12, before=8, after=4)
    add_p("1. **Validasi dan Sanitasi Input Ketat:** Menerapkan pembatasan jalur kanonikal (canonical path checking) pada kode aplikasi untuk menolak semua string yang mengandung `../`, `%2e`, atau karakter kontrol traversal lainnya.")
    add_p("2. **Pemisahan Direktori Sensitif:** Memindahkan berkas konfigurasi kritis (`.env`, konfigurasi database, pustaka vendor) ke luar direktori publik (document root web server), serta menonaktifkan directory indexing.")
    add_p("3. **Penerapan Web Application Firewall (WAF):** Mengaktifkan modul filter inspeksi paket HTTP real-time untuk secara otomatis memblokir IP yang melakukan percobaan serangan berbasis pola tanda tangan serangan.")

    add_p("5.2 Pengamanan Endpoint dan Penambalan Kerentanan", bold=True, size=12, before=8, after=4)
    add_p("1. **Penambalan Segera CVE-2022-30190:** Memastikan pembaruan keamanan sistem operasi Windows dan Microsoft Office terpasang, atau menonaktifkan protokol MSDT (troubleshooter URL handler) melalui registri Windows jika pembaruan belum dapat diterapkan.")
    add_p("2. **Implementasi EDR (Endpoint Detection and Response):** Memasang agen EDR dengan heuristik perilaku untuk mendeteksi perilaku mencurigakan seperti aplikasi Office (`winword.exe`) yang memanggil `powershell.exe` atau `msdt.exe`.")
    add_p("3. **Kebijakan Pengeksekusian Perangkat Lunak:** Membatasi eksekusi berkas binari di folder temporer (`%TEMP%`, `%APPDATA%`, `Downloads`) menggunakan fitur AppLocker atau Software Restriction Policies.")

    add_p("5.3 Strategi Manajemen Cadangan (Backup Resilience)", bold=True, size=12, before=8, after=4)
    add_p("1. **Arsitektur Backup 3-2-1:** Menyimpan setidaknya 3 salinan data, pada 2 media penyimpanan yang berbeda, dengan 1 salinan tersimpan secara offline / immutable (air-gapped) agar tidak dapat dienkripsi oleh ransomware yang menyebar di jaringan internal.")
    add_p("2. **Pengujian Pemulihan Berkala:** Melakukan simulasi disaster recovery terjadwal untuk mengukur Recovery Time Objective (RTO) dan Recovery Point Objective (RPO).")

    add_p("5.4 Peningkatan Kesadaran Keamanan Karyawan", bold=True, size=12, before=8, after=4)
    add_p("1. **Pelatihan Anti-Phishing:** Mengadakan simulasi spear-phishing berkala untuk melatih kewaspadaan pegawai HRD terhadap berkas lamaran berformat arsip (.zip, .rar) atau dokumen pembawa muatan makro berbahaya.")
    add_p("2. **Penerapan Autentikasi Multi-Faktor (MFA):** Wajib menerapkan MFA pada seluruh akses portal administrasi web server dan akun email korporat guna memitigasi penyalahgunaan kredensial hasil peretasan.")

    doc.add_page_break()

    # ==================== BAB VI ====================
    add_p("BAB VI", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=10, after=2)
    add_p("KESIMPULAN DAN SARAN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=0, after=14)

    add_p("6.1 Kesimpulan", bold=True, size=12, before=8, after=4)
    add_p("1. Penerapan standar **NIST SP 800-86** secara efektif mampu mengurai serangan siber multi-vektor pada PT. Satseet International ke dalam tahapan yang sistematis dan terukur.")
    add_p("2. Keabsahan bukti digital terjamin secara penuh melalui proses hashing kriptografis ganda (MD5, SHA-1, SHA-256) pada fase Collection dan Examination dengan status verifikasi `COCOK` tanpa adanya indikasi pemalsuan bukti.")
    add_p("3. Analisis log web mengungkap bahwa serangan diawali oleh eksploitasi Directory Traversal oleh IP `192.168.1.11` yang membocorkan berkas konfigurasi internal (`.env`), diikuti kampanye spear-phishing bertarget yang mengeksploitasi kerentanan Follina RCE (CVE-2022-30190), dan diakhiri dengan serangan ransomware serta pemerasan oleh kelompok BlackPython Team.")
    add_p("4. Keberhasilan investigasi ini membuktikan bahwa otomasi skrip forensik berbasis Python dapat diandalkan untuk melakukan triase cepat (rapid triage) dan merekonstruksi linimasa kejahatan siber secara akurat.")

    add_p("6.2 Saran", bold=True, size=12, before=8, after=4)
    add_p("1. Untuk penelitian selanjutnya, disarankan memperluas cakupan akuisisi ke artefak memori volatil (RAM) menggunakan perkakas seperti Volatility 3 untuk mendeteksi sisa injeksi kode in-memory yang tidak tersimpan di dalam disk.")
    add_p("2. Disarankan mengintegrasikan format ekspor linimasa ke dalam standar visualisasi investigasi tingkat lanjut (seperti format Plaso / log2timeline atau Timesketch) guna mempermudah kolaborasi antar-analis forensik.")

    doc.add_page_break()

    # ==================== DAFTAR PUSTAKA ====================
    add_p("DAFTAR PUSTAKA", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=10, after=14)

    citations = [
        "Ihsan, M. R. I., & Voutama, A. (2025). Penerapan Metode NIST Dalam Analisis Forensik Digital Pasca Serangan Siber (Studi Kasus: PT. Analis Digital Forensik). *CyberSecurity dan Forensik Digital*, 8(1), 53–62.",
        "Kent, K., Chevalier, S., Grance, T., & Dang, H. (2006). *Guide to Integrating Forensic Techniques into Incident Response* (NIST Special Publication 800-86). National Institute of Standards and Technology, U.S. Department of Commerce.",
        "International Organization for Standardization. (2012). *Information technology — Security techniques — Guidelines for identification, collection, acquisition and preservation of digital evidence* (ISO/IEC Standard No. 27037:2012).",
        "Faizal, A., & Luthfi, A. (2024). Comparison Study of NIST SP 800-86 and ISO/IEC 27037 Standards as A Framework for Digital Forensic Evidence Analysis. *Journal of Information Systems and Informatics*, 6(2), 701–718.",
        "National Vulnerability Database (NVD). (2022). *CVE-2022-30190: Microsoft Windows Support Diagnostic Tool (MSDT) Remote Code Execution Vulnerability*. NIST.",
        "Ramadhan, R. A., Rachmat Setiawan, P., & Hariyadi, D. (2022). Digital Forensic Investigation for Non-Volatile Memory Architecture by Hybrid Evaluation Based on ISO/IEC 27037:2012 and NIST SP800-86 Framework. *IT Journal Research and Development*, 7(2), 162–168.",
        "Carrier, B. (2005). *File System Forensic Analysis*. Addison-Wesley Professional.",
        "Casey, E. (2011). *Digital Evidence and Computer Crime: Forensic Science, Computers, and the Internet* (3rd ed.). Academic Press."
    ]

    for c in citations:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.left_indent = Inches(0.5)
        p_c.paragraph_format.first_line_indent = Inches(-0.5)
        p_c.paragraph_format.space_after = Pt(6)
        p_c.paragraph_format.line_spacing = 1.3
        p_c.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        tokens = re.split(r'(\*.*?\*)', c)
        for tok in tokens:
            if tok.startswith("*") and tok.endswith("*"):
                r = p_c.add_run(tok[1:-1])
                r.font.italic = True
            else:
                r = p_c.add_run(tok)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)

    # Save to Makalah Forensik.docx
    target_docx = os.path.join(BASE_DIR, "Makalah Forensik.docx")
    doc.save(target_docx)
    print(f"SUCCESS: {target_docx} has been updated with the Gunadarma template!")

if __name__ == "__main__":
    build_makalah_forensik()
