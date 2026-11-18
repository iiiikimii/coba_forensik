import os
import subprocess
import time

BASE_DIR = r"c:\Users\user\Documents\paket_data_contoh"
HTML_PATH = os.path.join(BASE_DIR, "Makalah Forensik.html")
PDF_PATH = os.path.join(BASE_DIR, "Makalah Forensik.pdf")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def generate_pdf():
    html_content = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Makalah Forensik Digital - Universitas Gunadarma</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 28mm 25mm 25mm 30mm;
    @bottom-center {{
      content: counter(page);
      font-family: 'Times New Roman', serif;
      font-size: 10pt;
    }}
  }}
  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 11.5pt;
    line-height: 1.45;
    color: #111;
    background: #fff;
    margin: 0;
    padding: 0;
  }}
  .cover-page {{
    text-align: center;
    page-break-after: always;
    padding-top: 20px;
  }}
  .cover-title {{
    font-size: 15.5pt;
    font-weight: bold;
    text-transform: uppercase;
    line-height: 1.3;
    margin-bottom: 12px;
    color: #1a252f;
  }}
  .cover-subtitle {{
    font-size: 12pt;
    color: #4a5568;
    line-height: 1.35;
    margin-bottom: 25px;
  }}
  .cover-logo {{
    display: block;
    margin: 20px auto 35px auto;
    width: 170px;
    height: auto;
  }}
  .cover-by {{
    font-size: 12pt;
    margin-bottom: 12px;
  }}
  .author-table {{
    margin: 0 auto 50px auto;
    border-collapse: collapse;
    width: 60%;
  }}
  .author-table td {{
    border: none;
    padding: 3px 8px;
    font-size: 11.5pt;
  }}
  .author-table td.name {{
    text-align: left;
  }}
  .author-table td.npm {{
    text-align: right;
  }}
  .cover-inst {{
    font-size: 14pt;
    font-weight: bold;
    line-height: 1.35;
    text-transform: uppercase;
  }}
  .cover-year {{
    font-size: 14pt;
    font-weight: bold;
    margin-top: 6px;
  }}
  
  /* Inner Pages */
  .page-break {{
    page-break-after: always;
  }}
  h1.bab-title {{
    font-size: 14pt;
    text-align: center;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 15px;
    margin-bottom: 4px;
    color: #0f172a;
    page-break-after: avoid;
  }}
  h2.bab-subtitle {{
    font-size: 14pt;
    text-align: center;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 0;
    margin-bottom: 16px;
    color: #0f172a;
    page-break-after: avoid;
  }}
  h3 {{
    font-size: 12pt;
    font-weight: bold;
    color: #1e293b;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}
  p {{
    text-align: justify;
    text-justify: inter-word;
    margin-top: 4px;
    margin-bottom: 8px;
    line-height: 1.4;
  }}
  ul, ol {{
    margin-top: 4px;
    margin-bottom: 8px;
    padding-left: 24px;
    text-align: justify;
  }}
  li {{
    margin-bottom: 3px;
  }}
  .table-title {{
    font-weight: bold;
    color: #0f172a;
    margin-top: 16px;
    margin-bottom: 4px;
    font-size: 10.5pt;
    page-break-after: avoid;
  }}
  table.data-table {{
    border-collapse: collapse;
    width: 100%;
    margin: 6px 0 16px 0;
    font-size: 9.5pt;
    line-height: 1.25;
    page-break-inside: avoid;
  }}
  table.data-table th, table.data-table td {{
    border: 1px solid #cbd5e1;
    padding: 6px 8px;
    vertical-align: middle;
  }}
  table.data-table th {{
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: bold;
    text-align: center;
  }}
  table.data-table tr:nth-child(even) td {{
    background-color: #f8fafc;
  }}
  img.figure-img {{
    display: block;
    max-width: 85%;
    max-height: 380px;
    margin: 14px auto 4px auto;
    border: 1px solid #cbd5e1;
    border-radius: 3px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    page-break-inside: avoid;
  }}
  p.caption {{
    text-align: center;
    font-size: 9.5pt;
    color: #475569;
    margin-top: 2px;
    margin-bottom: 16px;
    page-break-before: avoid;
  }}
  code {{
    font-family: Consolas, 'Courier New', monospace;
    font-size: 9pt;
    background-color: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
    color: #0f172a;
  }}
  p.bib-item {{
    text-align: justify;
    padding-left: 36px;
    text-indent: -36px;
    margin-bottom: 8px;
    font-size: 11pt;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="cover-title">INVESTIGASI FORENSIK DIGITAL SERANGAN SIBER MULTI-VEKTOR MENGGUNAKAN METODOLOGI NIST SP 800-86</div>
  <div class="cover-subtitle">Studi Kasus: Eksploitasi Web Server HRMS, Spear-Phishing Follina (CVE-2022-30190), dan Ransomware pada PT. Satseet International</div>
  
  <img src="logo_gunadarma.png" alt="Logo Universitas Gunadarma" class="cover-logo">
  
  <div class="cover-by">Disusun Oleh:</div>
  <table class="author-table">
    <tr><td class="name">Fajar Daffa D.</td><td class="npm">50423442</td></tr>
    <tr><td class="name">Farrel Dhiyas Ulhaq</td><td class="npm">50423467</td></tr>
    <tr><td class="name">Feriyan Eka Nanda</td><td class="npm">50423500</td></tr>
    <tr><td class="name">Hanif Maulana A.F.</td><td class="npm">50423568</td></tr>
    <tr><td class="name">Kimi Sholihudin SJB</td><td class="npm">50423698</td></tr>
  </table>

  <div class="cover-inst">
    JURUSAN TEKNIK INFORMATIKA<br>
    FAKULTAS TEKNOLOGI INDUSTRI<br>
    UNIVERSITAS GUNADARMA
  </div>
  <div class="cover-year">2026</div>
</div>

<!-- ABSTRAK -->
<div class="page-break">
  <h1 class="bab-title">ABSTRAK</h1>
  <br>
  <p>Peningkatan frekuensi dan kompleksitas serangan siber modern menuntut pendekatan investigasi insiden yang terstruktur, akuntabel, dan dapat dipertanggungjawabkan secara hukum. Penelitian ini menyajikan investigasi forensik digital pascainsiden serangan multi-vektor terhadap sistem <em>Human Resource Management System</em> (HRMS) dan web server PT. Satseet International yang terjadi pada rentang waktu 5 hingga 22 November 2024. Metodologi yang diterapkan mengacu pada standar <em>National Institute of Standards and Technology Special Publication 800-86</em> (NIST SP 800-86) yang mencakup empat fase utama: <em>Collection</em>, <em>Examination</em>, <em>Analysis</em>, dan <em>Reporting</em>. Melalui implementasi toolkit forensik terotomatisasi berbasis Python, dilakukan proses akuisisi bukti digital, pembangkitan nilai hash kriptografis (<em>Chain of Custody</em>), analisis 113 baris log akses HTTP, pencocokan <em>Indicator of Compromise</em> (IOC), serta rekonstruksi linimasa (<em>timeline analysis</em>). Hasil investigasi mengungkap bahwa aktor ancaman <em>BlackPython Team</em> memulai serangan melalui <em>Directory Traversal</em> pada web server untuk mengekstraksi berkas konfigurasi sensitif (<code>.env</code> dan <code>autoload.php</code>), dilanjutkan dengan operasi <em>spear-phishing</em> bertema rekrutmen yang memanfaatkan kerentanan <em>Remote Code Execution</em> Follina (CVE-2022-30190). Rangkaian serangan berujung pada penyusupan <em>trojan backdoor</em> (<code>update.exe</code>) dan enkripsi berkas oleh <em>ransomware</em> (<code>ransom.exe</code>). Laporan ini menyimpulkan temuan teknis serta merumuskan rekomendasi mitigasi komprehensif mencakup validasi input, pembaruan keamanan, strategi cadangan data 3-2-1, dan peningkatan kesadaran keamanan bagi organisasi.</p>
  <p><strong>Kata Kunci:</strong> Forensik Digital, NIST SP 800-86, Directory Traversal, Follina (CVE-2022-30190), Ransomware, Chain of Custody.</p>
</div>

<!-- ABSTRACT (EN) -->
<div class="page-break">
  <h1 class="bab-title">ABSTRACT</h1>
  <br>
  <p><em>The increasing frequency and sophistication of cyberattacks necessitate a structured, accountable, and legally admissible incident investigation approach. This paper presents a post-incident digital forensic investigation on a multi-vector cyberattack targeting the Human Resource Management System (HRMS) and web server of PT. Satseet International between November 5 and November 22, 2024. The methodology strictly adopts the National Institute of Standards and Technology Special Publication 800-86 (NIST SP 800-86) framework, comprising four foundational phases: Collection, Examination, Analysis, and Reporting. Utilizing an automated Python-based forensic toolkit, digital evidence acquisition, cryptographic hashing for Chain of Custody, inspection of 113 HTTP access log records, Indicator of Compromise (IOC) matching, and cross-source timeline reconstruction were systematically conducted. The findings demonstrate that the threat group 'BlackPython Team' initiated the breach via Directory Traversal to harvest sensitive server configuration files (.env and autoload.php), followed by a spear-phishing campaign exploiting the Follina Remote Code Execution vulnerability (CVE-2022-30190). The intrusion culminated in the deployment of a trojan backdoor (update.exe) and critical data encryption by ransomware (ransom.exe). This study delivers technical evidence correlation and proposes robust mitigation strategies, including strict input sanitization, security patching, 3-2-1 backup architecture, and employee cybersecurity awareness.</em></p>
  <p><strong>Keywords:</strong> Digital Forensics, NIST SP 800-86, Directory Traversal, Follina (CVE-2022-30190), Ransomware, Incident Response.</p>
</div>

<!-- BAB I -->
<div class="page-break">
  <h1 class="bab-title">BAB I</h1>
  <h2 class="bab-subtitle">PENDAHULUAN</h2>

  <h3>1.1 Latar Belakang</h3>
  <p>Transformasi digital dalam sektor korporasi telah mendorong sentralisasi pengelolaan data pegawai dan operasional bisnis ke dalam sistem terintegrasi, seperti <em>Human Resource Management System</em> (HRMS). Namun, perluasan permukaan serangan (<em>attack surface</em>) tanpa diimbangi postur pertahanan yang memadai memicu kerentanan terhadap serangan siber terorganisir. Berdasarkan laporan lanskap ancaman Badan Siber dan Sandi Negara (BSSN) tahun 2024, anomali trafik serangan siber di Indonesia mencapai lebih dari 330 juta aktivitas mencurigakan dengan puncak tertinggi terjadi pada bulan Desember sebanyak 112 juta anomali (Gambar 1).</p>

  <img src="gambar_paper/gambar_01_grafik_anomali.png" class="figure-img" alt="Gambar 1">
  <p class="caption"><em>Gambar 1. Grafik Anomali Trafik Serangan Siber di Indonesia Tahun 2024 (Data Resmi BSSN).</em></p>

  <p>Pada rentang 5–22 November 2024, PT. Satseet International mengalami insiden keamanan siber berskala masif yang mengakibatkan lumpuhnya operasional HRMS, kebocoran data pegawai, serta enkripsi berkas penting perusahaan oleh kelompok penyerang yang menamakan diri <em>BlackPython Team</em>. Insiden ini tidak berlangsung secara tunggal, melainkan melalui kombinasi serangan multi-vektor: peretasan awal melalui eksploitasi web server, rekayasa sosial (<em>spear-phishing</em>), eksekusi kode jarak jauh (<em>Remote Code Execution</em> / RCE), hingga penyebaran <em>ransomware</em>.</p>
  <p>Guna mengungkap anatomi serangan secara utuh dan menjamin keabsahan bukti digital di ranah investigasi maupun hukum, diperlukan metodologi forensik yang terstandarisasi. Standar NIST SP 800-86 dipilih karena menyediakan kerangka kerja investigasi sistematis yang menjamin keutuhan (<em>integrity</em>), keterulangan (<em>repeatability</em>), dan keterlacakan (<em>chain of custody</em>) dari seluruh artefak digital.</p>

  <h3>1.2 Rumusan Masalah</h3>
  <ol>
    <li>Bagaimana mengidentifikasi, mengamankan, dan memverifikasi integritas bukti digital yang diperoleh pascaserangan pada sistem PT. Satseet International?</li>
    <li>Bagaimana pola dan teknik serangan multi-vektor (Directory Traversal, Follina CVE-2022-30190, dan Ransomware) dapat direkonstruksi ke dalam linimasa kronologis yang valid?</li>
    <li>Apa langkah-langkah mitigasi dan tata kelola keamanan yang perlu diterapkan untuk mencegah insiden berulang?</li>
  </ol>

  <h3>1.3 Tujuan Penelitian</h3>
  <ol>
    <li>Menerapkan metodologi NIST SP 800-86 (<em>Collection, Examination, Analysis, Reporting</em>) dalam menginvestigasi insiden keamanan siber.</li>
    <li>Membuktikan integritas bukti digital melalui kalkulasi hash kriptografis ganda (MD5, SHA-1, SHA-256).</li>
    <li>Melakukan deteksi anomali pada log web server serta mencocokkan <em>Indicator of Compromise</em> (IOC).</li>
    <li>Menyusun laporan investigasi forensik akademik yang komprehensif dan aplikatif sebagai bahan evaluasi institusi.</li>
  </ol>

  <h3>1.4 Batasan Masalah</h3>
  <ol>
    <li>Investigasi difokuskan pada artefak digital yang disediakan dalam paket kasus PT. Satseet International, meliputi log web server (<code>access.log</code>), catatan akuisisi, berkas lampiran phishing, dan rekaman peristiwa sistem (<code>events.csv</code>).</li>
    <li>Toolkit forensik yang digunakan diimplementasikan dalam skrip terotomatisasi Python 3.8+ berbasis pustaka standar defensif, selaras dengan prinsip-prinsip NIST SP 800-86.</li>
  </ol>
</div>

<!-- BAB II -->
<div class="page-break">
  <h1 class="bab-title">BAB II</h1>
  <h2 class="bab-subtitle">LANDASAN TEORI</h2>

  <h3>2.1 Forensik Digital dan Standar NIST SP 800-86</h3>
  <p>Forensik digital didefinisikan sebagai penerapan prinsip-prinsip ilmiah terhadap penemuan, validasi, identifikasi, analisis, dan interpretasi bukti digital yang berasal dari media digital untuk memfasilitasi rekonstruksi peristiwa. National Institute of Standards and Technology menerbitkan panduan <strong>NIST SP 800-86</strong> (<em>Guide to Integrating Forensic Techniques into Incident Response</em>) yang menetapkan empat fase dasar:</p>
  <ul>
    <li><strong>Collection (Pengumpulan):</strong> Proses identifikasi, pelabelan, pencatatan, dan pengamanan sumber bukti fisik maupun digital dengan menjaga <em>Chain of Custody</em>.</li>
    <li><strong>Examination (Pemeriksaan):</strong> Pemrosesan bukti mentah secara forensik menggunakan teknik ekstraksi artefak dan verifikasi keaslian melalui algoritma <em>cryptographic hashing</em>.</li>
    <li><strong>Analysis (Analisis):</strong> Penerapan metode analitis untuk menarik kesimpulan logis, menentukan vektor serangan, pelaku (<em>threat actor</em>), serta dampak insiden.</li>
    <li><strong>Reporting (Pelaporan):</strong> Penyajian hasil analisis secara formal, transparan, dan terstruktur yang mencakup prosedur, temuan, keterbatasan, dan rekomendasi mitigasi.</li>
  </ul>

  <img src="gambar_paper/gambar_02_alur_nist.png" class="figure-img" style="max-width: 55%;" alt="Gambar 2">
  <p class="caption"><em>Gambar 2. Siklus Alur Investigasi 4 Tahapan Standar NIST SP 800-86.</em></p>

  <h3>2.2 Integritas Bukti dan Chain of Custody</h3>
  <p><em>Chain of Custody</em> merupakan dokumentasi kronologis yang mencatat perolehan, pengendalian, pemindahan, analisis, dan penyimpanan bukti digital. Integritas berkas dibuktikan dengan menghasilkan intisari pesan (<em>message digest</em>) melalui fungsi hash kriptografis:</p>
  <ul>
    <li><strong>MD5 (128-bit):</strong> Algoritma ringkasan pesan cepat untuk verifikasi awal.</li>
    <li><strong>SHA-1 (160-bit):</strong> Standar kriptografi pelengkap integritas.</li>
    <li><strong>SHA-256 (256-bit):</strong> Standar hashing modern yang memiliki ketahanan benturan (<em>collision resistance</em>) sangat tinggi, wajib disertakan dalam standar forensik internasional.</li>
  </ul>

  <h3>2.3 Vektor Serangan Siber Terkait</h3>
  <p><strong>1. Directory Traversal (Path Traversal):</strong> Kerentanan aplikasi web yang memungkinkan penyerang membaca berkas di luar direktori web root dengan menyuntikkan karakter sekuens khusus seperti <code>../</code> atau representasi URL-encoded <code>%2e%2e%2f</code>. Tujuannya adalah memperoleh kredensial basis data atau berkas konfigurasi sistem (<code>/etc/passwd</code>, <code>.env</code>).</p>
  <p><strong>2. Follina Exploit (CVE-2022-30190):</strong> Kerentanan zero-day pada Microsoft Windows Support Diagnostic Tool (MSDT) yang dipicu saat membuka atau melihat pratinjau dokumen Microsoft Office (.docx/.rtf). Kerentanan ini memungkinkan penyerang mengeksekusi kode PowerShell jarak jauh (<em>Remote Code Execution</em>) dengan hak akses pengguna lokal tanpa perlu macro aktif.</p>
  <p><strong>3. Ransomware dan Trojan Backdoor:</strong> Perangkat lunak berbahaya yang mengenkripsi berkas korban menggunakan enkripsi asimetris/simetris dan menuntut uang tebusan (<em>ransom</em>). Trojan backdoor dipasang untuk mempertahankan akses persisten (<em>persistence</em>) ke dalam sistem internal korban.</p>
</div>

<!-- BAB III -->
<div class="page-break">
  <h1 class="bab-title">BAB III</h1>
  <h2 class="bab-subtitle">METODOLOGI PENELITIAN</h2>

  <h3>3.1 Kerangka Kerja Eksperimen</h3>
  <p>Penelitian ini mengadopsi alur eksperimen empiris berbasis NIST SP 800-86 dengan tahapan kerja operasional terstruktur seperti disajikan pada Gambar 3:</p>

  <img src="gambar_paper/diagram_metodologi_eksperimen.png" class="figure-img" style="max-width: 75%;" alt="Gambar 3">
  <p class="caption"><em>Gambar 3. Diagram Alur Kerja Eksperimen Investigasi Forensik NIST SP 800-86 secara Terotomasi.</em></p>

  <h3>3.2 Lingkungan dan Alat Pengujian</h3>
  <p>Pengujian dilakukan pada lingkungan terkontrol dengan spesifikasi perangkat keras dan lunak sebagai berikut:</p>

  <p class="table-title">Tabel 3.1. Spesifikasi Perangkat Keras dan Lunak Penelitian</p>
  <table class="data-table">
    <thead>
      <tr><th>Kategori Komponen</th><th>Spesifikasi / Alat</th><th>Versi</th><th>Peran dalam Investigasi</th></tr>
    </thead>
    <tbody>
      <tr><td>Sistem Analis</td><td>Microsoft Windows 11 Pro 64-bit</td><td>Build 21996</td><td>Lingkungan kerja analisis forensik</td></tr>
      <tr><td>Interpreter</td><td>Python Standard Environment</td><td>3.13.1</td><td>Eksekusi otomasi skrip forensik</td></tr>
      <tr><td>Toolkit Forensik</td><td>forensik_nist.py</td><td>1.0 (Custom)</td><td>Implementasi modul 4 fase NIST SP 800-86</td></tr>
      <tr><td>Pustaka Kriptografi</td><td>Python hashlib</td><td>Bawaan</td><td>Pembangkitan nilai hash MD5, SHA-1, SHA-256</td></tr>
      <tr><td>Ekstraksi Log</td><td>Python re & csv</td><td>Bawaan</td><td>Parsing pola Directory Traversal & agregasi linimasa</td></tr>
      <tr><td>Alat Komparator</td><td>FTK Imager & Autopsy</td><td>4.7.1 / 4.21.0</td><td>Standar acuan verifikasi disk image & artefak OS</td></tr>
      <tr><td>Analisis Jaringan</td><td>Wireshark Protocol Analyzer</td><td>4.4.2</td><td>Rekonsiliasi paket lalu lintas data HTTP/TLS</td></tr>
      <tr><td>Intelijen Malware</td><td>VirusTotal Cloud Engine</td><td>API v3</td><td>Verifikasi identitas trojan & ransomware</td></tr>
    </tbody>
  </table>
</div>

<!-- BAB IV -->
<div class="page-break">
  <h1 class="bab-title">BAB IV</h1>
  <h2 class="bab-subtitle">HASIL DAN PEMBAHASAN</h2>

  <h3>4.1 Tahap 1: Collection (Akuisisi Bukti Digital dan Hashing)</h3>
  <p>Proses pengumpulan bukti digital diawali dengan menerima berkas hasil akuisisi media penyimpanan (<em>disk image</em>) dan <em>live memory acquisition</em> dari sistem korban PT. Satseet International (Gambar 4).</p>

  <img src="gambar_paper/gambar_03_hasil_akuisisi.png" class="figure-img" style="max-width: 65%;" alt="Gambar 4">
  <p class="caption"><em>Gambar 4. Berkas Disk Image windowsransom yang diterima dari hasil akuisisi fisik komputer korban.</em></p>

  <p>Selanjutnya, toolkit <code>forensik_nist.py</code> menjalankan perintah <code>collect</code> terhadap direktori bukti guna mengekstraksi metadata, membangkitkan hash kriptografis ganda, dan membandingkannya terhadap daftar <em>Indicator of Compromise</em> (<code>ioc.txt</code>). Hasilnya dicatat ke dalam manifest resmi <code>manifest.json</code> (Tabel 4.1).</p>

  <p class="table-title">Tabel 4.1. Manifest Inventaris Bukti Digital dan Hasil Hashing Kriptografis</p>
  <table class="data-table">
    <thead>
      <tr><th>Nama Berkas Bukti</th><th>Ukuran</th><th>Nilai Hash MD5</th><th>Nilai Hash SHA-1</th><th>Nilai Hash SHA-256</th><th>Kecocokan IOC</th></tr>
    </thead>
    <tbody>
      <tr><td>access.log</td><td>10.805 B</td><td>0a2e379b32e185873ec8b408892f39c0</td><td>82cf214b62db4df43b7e73507119ff391f1a5f6e</td><td>6c1445ee259c792cfc261dedfd7f7d99e001dd05b0c7839b6bae1288371f58bf</td><td>-</td></tr>
      <tr><td>catatan_akuisisi.txt</td><td>169 B</td><td>4c7bf69bf17b70743b2f293b722d3b7e</td><td>bcebb5523a789a3f2dbd1112d308078e878347f7</td><td>42d326d9684b2143fed0d3a67bb736a325140dab099b6aa9bdf591a49a893561</td><td>-</td></tr>
      <tr><td>lampiran_simulasi.txt</td><td>162 B</td><td>a5f22f6d0f666f7f63f58a361a9bc348</td><td>4f3876d540268dfc949fef56f2d93e8784d00810</td><td>8b14132601aa8764960ea80eb246e7387c1adbf1e42f026c870e19fda39d3d04</td><td style="color:#1b5e20; font-weight:bold;">COCOK (MATCH)</td></tr>
    </tbody>
  </table>

  <p><strong>Temuan Kunci Fase Collection:</strong> Nilai hash SHA-256 dari <code>lampiran_simulasi.txt</code> (<code>8b14132601aa87649...</code>) terbukti cocok 100% dengan daftar IOC pada <code>ioc.txt</code>. Berkas ini merupakan representasi dari dokumen kurikulum vitae <code>Lamaran kerja maya putri follina.zip</code> yang disebarkan penyerang sebagai pembawa muatan eksploitasi.</p>

  <h3>4.2 Tahap 2: Examination (Pemeriksaan dan Verifikasi Integritas)</h3>
  <p>Tahap pemeriksaan berfokus pada pengujian keaslian bukti digital guna memastikan bahwa tidak terjadi korupsi data atau manipulasi yang disengaja pascaakuisisi.</p>

  <img src="gambar_paper/gambar_06_verifikasi_hash.png" class="figure-img" style="max-width: 65%;" alt="Gambar 5">
  <p class="caption"><em>Gambar 5. Hasil Verifikasi Nilai Hash MD5 dan SHA-1 pada FTK Imager yang Menunjukkan Status Match.</em></p>

  <p class="table-title">Tabel 4.2. Hasil Uji Verifikasi Integritas dan Keabsahan Bukti</p>
  <table class="data-table">
    <thead>
      <tr><th>Nama Berkas</th><th>Status Integritas</th><th>Perubahan Algoritma Hash</th><th>Kesimpulan Keabsahan</th></tr>
    </thead>
    <tbody>
      <tr><td>access.log</td><td style="color:#1b5e20; font-weight:bold; text-align:center;">COCOK</td><td>Tidak ada perbedaan</td><td>Sah / Valid untuk Pembuktian</td></tr>
      <tr><td>catatan_akuisisi.txt</td><td style="color:#1b5e20; font-weight:bold; text-align:center;">COCOK</td><td>Tidak ada perbedaan</td><td>Sah / Valid untuk Pembuktian</td></tr>
      <tr><td>lampiran_simulasi.txt</td><td style="color:#1b5e20; font-weight:bold; text-align:center;">COCOK</td><td>Tidak ada perbedaan</td><td>Sah / Valid untuk Pembuktian</td></tr>
    </tbody>
  </table>

  <p>Hasil verifikasi menunjukkan bahwa seluruh berkas berstatus COCOK. Pengujian ketahanan manipulasi (<em>tamper resistance test</em>) yang dilakukan dengan menyuntikkan 1 karakter ke dalam berkas segera menghasilkan status BERUBAH, membuktikan keandalan sistem dalam mendeteksi perubahan data sekecil apa pun.</p>
  <p>Selain verifikasi hash, identifikasi lingkungan sistem korban juga berhasil diungkap melalui artefak <em>live forensic</em>:</p>
  <ul>
    <li><strong>Nama Komputer:</strong> <code>DESKTOP-R0IR99H</code></li>
    <li><strong>Sistem Operasi:</strong> Microsoft Windows 11 Pro Build 21996</li>
    <li><strong>Alamat IP Internal Korban:</strong> <code>192.168.1.28</code></li>
  </ul>

  <img src="gambar_paper/gambar_07_computer_os.png" class="figure-img" style="max-width: 70%;" alt="Gambar 6">
  <p class="caption"><em>Gambar 6. Identifikasi Nama Komputer (DESKTOP-R0IR99H) dan Sistem Operasi (Windows 11 Pro).</em></p>

  <img src="gambar_paper/gambar_08_info_jaringan.png" class="figure-img" style="max-width: 70%;" alt="Gambar 7">
  <p class="caption"><em>Gambar 7. Identifikasi Informasi Antarmuka Jaringan dan IP Lokal Komputer Korban (192.168.1.28).</em></p>

  <h3>4.3 Tahap 3: Analysis (Analisis Log Web dan Deteksi Serangan)</h3>
  <p>Pemeriksaan mendalam terhadap berkas <code>access.log</code> yang memuat 113 baris transaksi HTTP berhasil mengisolasi aktivitas penyerangan yang bersumber dari alamat IP <code>192.168.1.11</code> pada tanggal 5 November 2024.</p>

  <img src="gambar_paper/gambar_10_directory_traversal.png" class="figure-img" style="max-width: 75%;" alt="Gambar 8">
  <p class="caption"><em>Gambar 8. Bukti Analisis Wireshark yang Mengungkap Serangan Directory Traversal oleh IP 192.168.1.11.</em></p>

  <p class="table-title">Tabel 4.3. Rincian Rekaman Serangan Directory Traversal pada Web Server</p>
  <table class="data-table">
    <thead>
      <tr><th>Timestamp (WIB)</th><th>Alamat IP</th><th>Metode</th><th>Jalur Target (Requested URI)</th><th>Status</th><th>Evaluasi Forensik</th></tr>
    </thead>
    <tbody>
      <tr><td>05/Nov/2024 19:58:02</td><td>192.168.1.11</td><td>GET</td><td>/web/index.php/../../../etc/passwd</td><td>404</td><td>Pola traversal teks polos; target file kredensial Linux.</td></tr>
      <tr><td>05/Nov/2024 19:58:05</td><td>192.168.1.11</td><td>GET</td><td>/web/index.php/..%2f..%2f..%2fetc/passwd</td><td>403</td><td>Pola traversal dengan URL encoding (%2f = /); diblokir.</td></tr>
      <tr><td>05/Nov/2024 19:58:09</td><td>192.168.1.11</td><td>GET</td><td>/web/%2e%2e/%2e%2e/config/database.yml</td><td>404</td><td>Enkoding titik ganda (%2e%2e); mencari konfigurasi database.</td></tr>
      <tr><td>05/Nov/2024 19:58:14</td><td>192.168.1.11</td><td>GET</td><td>/web/..%2f..%2fsrc/vendor/autoload.php</td><td style="color:#1b5e20; font-weight:bold;">200</td><td>BERHASIL: Komponen aplikasi web berhasil diakses penyerang.</td></tr>
      <tr><td>05/Nov/2024 19:58:20</td><td>192.168.1.11</td><td>GET</td><td>/web/..%2f..%2fsrc/config/.env</td><td style="color:#b71c1c; font-weight:bold;">200</td><td>KRITIS / BERHASIL: Berkas .env (berisi password & API key) bocor!</td></tr>
    </tbody>
  </table>

  <img src="gambar_paper/gambar_11_file_sensitif.png" class="figure-img" style="max-width: 65%;" alt="Gambar 9">
  <p class="caption"><em>Gambar 9. Potongan Berkas Konfigurasi Sensitif Web Server yang Terbaca Akibat Celah Directory Traversal.</em></p>

  <p><strong>Evaluasi Temuan Log:</strong> Penyerang memanfaatkan variasi URL-encoding (<code>%2e%2e%2f</code>) untuk menghindari deteksi filter WAF sederhana. Akses dengan status kode <code>200 OK</code> ke berkas <code>autoload.php</code> dan <code>.env</code> menandakan kebocoran informasi kredensial yang fatal, yang membuka jalan bagi penyerang untuk login ke portal HRMS pada tahap berikutnya.</p>

  <h3>4.4 Rekonstruksi Linimasa Serangan Terpadu (Timeline Analysis)</h3>
  <p>Investigasi mengkorelasikan seluruh artefak: log akses web, email phishing, akses file lokal, eksekusi malware, dan intelijen media sosial (OSINT).</p>

  <img src="gambar_paper/gambar_12_email_phishing.png" class="figure-img" style="max-width: 60%;" alt="Gambar 10">
  <p class="caption"><em>Gambar 10. Email Rekayasa Sosial Spear-Phishing Bertema Lowongan Kerja dari Akun Palsu Maya Putri.</em></p>

  <img src="gambar_paper/gambar_15_download_lamaran.png" class="figure-img" style="max-width: 70%;" alt="Gambar 11">
  <p class="caption"><em>Gambar 11. Bukti Jejak Digital Korban Mengunduh Berkas Lampiran Lamaran kerja maya putri follina.zip.</em></p>

  <img src="gambar_paper/gambar_16_akses_malware.png" class="figure-img" style="max-width: 60%;" alt="Gambar 12">
  <p class="caption"><em>Gambar 12. Catatan Akses Waktu Nyata terhadap Berkas Berbahaya update.exe dan ransom.exe.</em></p>

  <img src="gambar_paper/gambar_17_file_terenkripsi.png" class="figure-img" style="max-width: 65%;" alt="Gambar 13">
  <p class="caption"><em>Gambar 13. Daftar Berkas Korban yang Terkunci dan Berubah Ekstensi Menjadi .wasted.</em></p>

  <p class="table-title">Tabel 4.4. Rekonstruksi Linimasa Komprehensif Serangan Multi-Vektor</p>
  <table class="data-table">
    <thead>
      <tr><th>Tanggal & Waktu</th><th>Sumber</th><th>Entitas / Akun</th><th>Deskripsi Peristiwa Serangan</th><th>Fase Serangan</th></tr>
    </thead>
    <tbody>
      <tr><td>05/Nov/2024 19:58:02</td><td>access.log</td><td>192.168.1.11</td><td>Percobaan Directory Traversal ke /etc/passwd (HTTP 404)</td><td>Reconnaissance</td></tr>
      <tr><td>05/Nov/2024 19:58:05</td><td>access.log</td><td>192.168.1.11</td><td>Percobaan Directory Traversal dengan URL encoding (HTTP 403)</td><td>Evasion Attempt</td></tr>
      <tr><td>05/Nov/2024 19:58:14</td><td>access.log</td><td>192.168.1.11</td><td>Akses ke file autoload.php berhasil (HTTP 200)</td><td>Information Gathering</td></tr>
      <tr><td>05/Nov/2024 19:58:20</td><td>access.log</td><td>192.168.1.11</td><td>Akses ke berkas rahasia .env berhasil (HTTP 200)</td><td>Credential Harvesting</td></tr>
      <tr><td>06/Nov/2024 17:54:00</td><td>Email Gateway</td><td>Local User 2</td><td>Menerima email pertanyaan lowongan kerja dari Maya Putri</td><td>Reconnaissance Social</td></tr>
      <tr><td>19/Nov/2024 22:18:00</td><td>Email Gateway</td><td>Local User 1</td><td>Email phishing lanjutan masuk membawa berkas lamaran kerja</td><td>Weaponization</td></tr>
      <tr><td>20/Nov/2024 13:23:00</td><td>Web Log</td><td>192.168.1.11</td><td>Pelaku mencoba mengakses antarmuka portal login HRMS</td><td>Initial Connection</td></tr>
      <tr><td>20/Nov/2024 13:29:00</td><td>Web Log</td><td>192.168.1.11</td><td>Pelaku berhasil login ke portal HRMS menggunakan kredensial bocor</td><td>Privilege Access</td></tr>
      <tr><td>20/Nov/2024 13:29:00</td><td>Email Client</td><td>Local User 1</td><td>Lampiran lamaran kerja Folline.zip diunduh oleh korban</td><td>User Execution</td></tr>
      <tr><td>20/Nov/2024 13:33:00</td><td>Disk / Endpoint</td><td>Local User 1</td><td>Dokumen riwayat hidup dibuka, mengeksekusi CVE-2022-30190</td><td>Remote Code Execution</td></tr>
      <tr><td>20/Nov/2024 13:49:00</td><td>Disk / Endpoint</td><td>Local User 1</td><td>Eksekusi otomatis update.exe (Trojan Backdoor aktif)</td><td>Persistence / C2</td></tr>
      <tr><td>20/Nov/2024 13:50:00</td><td>Disk / Endpoint</td><td>Local User 1</td><td>Eksekusi ransom.exe (main_v2.exe / Python.Filecoder)</td><td>Malware Execution</td></tr>
      <tr><td>20/Nov/2024 13:59:00</td><td>Disk / Storage</td><td>Sistem HRMS</td><td>Berkas-berkas penting terenkripsi dan berekstensi .wasted</td><td>Impact (Ransomware)</td></tr>
      <tr><td>22/Nov/2024 09:00:00</td><td>OSINT / Telegram</td><td>BlackPython Team</td><td>Publikasi klaim pencurian data karyawan dan tuntutan pemerasan</td><td>Exfiltration & Extortion</td></tr>
    </tbody>
  </table>

  <h3>4.5 Analisis Atribusi dan Karakteristik Malware</h3>
  <p><strong>1. Analisis Eksploitasi Follina (CVE-2022-30190):</strong> Analisis dokumen lampiran pada VirusTotal menunjukkan deteksi eksploitasi terhadap kerentanan Microsoft Support Diagnostic Tool (MSDT). Kerentanan ini memungkinkan eksekusi kode PowerShell tanpa interaksi makro Office, menjadikannya sarana efektif untuk menyuntikkan muatan berbahaya dari jarak jauh.</p>

  <img src="gambar_paper/gambar_18_virustotal_follina.png" class="figure-img" style="max-width: 75%;" alt="Gambar 14">
  <p class="caption"><em>Gambar 14. Hasil Analisis Dokumen Lampiran Phishing pada VirusTotal yang Mendeteksi Eksploitasi CVE-2022-30190.</em></p>

  <p><strong>2. Karakteristik Trojan Backdoor (<code>update.exe</code>):</strong> Hasil pemindaian VirusTotal mengklasifikasikan <code>update.exe</code> sebagai Trojan.Win32/Shell.R128S dan Backdoor.Win/shellcode.apid. Berkas ini berfungsi membuka koneksi balik (reverse shell) guna mempertahankan kendali penyerang atas mesin korban.</p>

  <img src="gambar_paper/gambar_19_virustotal_update.png" class="figure-img" style="max-width: 75%;" alt="Gambar 15">
  <p class="caption"><em>Gambar 15. Hasil Deteksi Berkas update.exe pada VirusTotal sebagai Trojan Backdoor.</em></p>

  <p><strong>3. Karakteristik Ransomware (<code>ransom.exe</code>):</strong> Berkas <code>ransom.exe</code> (awalnya dinamai <code>main_v2.exe</code>) diidentifikasi oleh mesin antivirus sebagai Ransom:Win32/Filecoder dan Python.Filecoder. Malware ini mengenkripsi dokumen penting dan menambahkan ekstensi <code>.wasted</code>.</p>

  <img src="gambar_paper/gambar_20_virustotal_ransom.png" class="figure-img" style="max-width: 75%;" alt="Gambar 16">
  <p class="caption"><em>Gambar 16. Hasil Deteksi Berkas ransom.exe pada VirusTotal sebagai Ransomware Python.Filecoder.</em></p>

  <p><strong>4. Atribusi Pelaku Ancaman:</strong> Berdasarkan klaim di saluran Telegram pada 22 November 2024, serangan dilakukan oleh kelompok peretas BlackPython Team. Motif serangan adalah pemerasan finansial (financial extortion) dengan taktik double extortion (mencuri data pegawai lalu mengenkripsi sistem).</p>

  <p class="table-title">Tabel 4.5. Ringkasan Singkat Hasil Analisis Forensik Digital (Laporan Eksekutif)</p>
  <table class="data-table">
    <thead>
      <tr><th>Parameter Evaluasi</th><th>Rincian Temuan Investigasi Forensik</th></tr>
    </thead>
    <tbody>
      <tr><td>Rentang Waktu Insiden</td><td>5 – 22 November 2024</td></tr>
      <tr><td>Sistem yang Diserang</td><td>Human Resource Management System (HRMS) dan Web Server</td></tr>
      <tr><td>Vektor Serangan</td><td>Directory Traversal, Remote Code Execution (Follina), Ransomware</td></tr>
      <tr><td>Identitas Aktor Penyerang</td><td>Sindikat BlackPython Team</td></tr>
      <tr><td>Dampak Kerusakan</td><td>Enkripsi data penting korporat, kebocoran data sensitif karyawan, gangguan operasional HRMS, risiko reputasi dan hukum</td></tr>
      <tr><td>Integritas Bukti Forensik</td><td>Terverifikasi utuh 100% (MD5, SHA-1, SHA-256 match)</td></tr>
    </tbody>
  </table>
</div>

<!-- BAB V -->
<div class="page-break">
  <h1 class="bab-title">BAB V</h1>
  <h2 class="bab-subtitle">REKOMENDASI DAN STRATEGI MITIGASI</h2>

  <p>Berdasarkan temuan forensik, dirumuskan strategi pertahanan mendalam (defense-in-depth) mencakup aspek teknis, prosedural, dan tata kelola:</p>

  <h3>5.1 Pengamanan Aplikasi Web dan Server</h3>
  <ol>
    <li><strong>Validasi dan Sanitasi Input Ketat:</strong> Menerapkan pembatasan jalur kanonikal (canonical path checking) pada kode aplikasi untuk menolak semua string yang mengandung <code>../</code>, <code>%2e</code>, atau karakter kontrol traversal lainnya.</li>
    <li><strong>Pemisahan Direktori Sensitif:</strong> Memindahkan berkas konfigurasi kritis (<code>.env</code>, konfigurasi database, pustaka vendor) ke luar direktori publik (document root web server), serta menonaktifkan directory indexing.</li>
    <li><strong>Penerapan Web Application Firewall (WAF):</strong> Mengaktifkan modul filter inspeksi paket HTTP real-time untuk secara otomatis memblokir IP yang melakukan percobaan serangan berbasis pola tanda tangan serangan.</li>
  </ol>

  <h3>5.2 Pengamanan Endpoint dan Penambalan Kerentanan</h3>
  <ol>
    <li><strong>Penambalan Segera CVE-2022-30190:</strong> Memastikan pembaruan keamanan sistem operasi Windows dan Microsoft Office terpasang, atau menonaktifkan protokol MSDT (troubleshooter URL handler) melalui registri Windows jika pembaruan belum dapat diterapkan.</li>
    <li><strong>Implementasi EDR (Endpoint Detection and Response):</strong> Memasang agen EDR dengan heuristik perilaku untuk mendeteksi perilaku mencurigakan seperti aplikasi Office (<code>winword.exe</code>) yang memanggil <code>powershell.exe</code> atau <code>msdt.exe</code>.</li>
    <li><strong>Kebijakan Pengeksekusian Perangkat Lunak:</strong> Membatasi eksekusi berkas binari di folder temporer (<code>%TEMP%</code>, <code>%APPDATA%</code>, <code>Downloads</code>) menggunakan fitur AppLocker atau Software Restriction Policies.</li>
  </ol>

  <h3>5.3 Strategi Manajemen Cadangan (Backup Resilience)</h3>
  <ol>
    <li><strong>Arsitektur Backup 3-2-1:</strong> Menyimpan setidaknya 3 salinan data, pada 2 media penyimpanan yang berbeda, dengan 1 salinan tersimpan secara offline / immutable (air-gapped) agar tidak dapat dienkripsi oleh ransomware yang menyebar di jaringan internal.</li>
    <li><strong>Pengujian Pemulihan Berkala:</strong> Melakukan simulasi disaster recovery terjadwal untuk mengukur Recovery Time Objective (RTO) dan Recovery Point Objective (RPO).</li>
  </ol>

  <h3>5.4 Peningkatan Kesadaran Keamanan Karyawan</h3>
  <ol>
    <li><strong>Pelatihan Anti-Phishing:</strong> Mengadakan simulasi spear-phishing berkala untuk melatih kewaspadaan pegawai HRD terhadap berkas lamaran berformat arsip (.zip, .rar) atau dokumen pembawa muatan makro berbahaya.</li>
    <li><strong>Penerapan Autentikasi Multi-Faktor (MFA):</strong> Wajib menerapkan MFA pada seluruh akses portal administrasi web server dan akun email korporat guna memitigasi penyalahgunaan kredensial hasil peretasan.</li>
  </ol>
</div>

<!-- BAB VI -->
<div class="page-break">
  <h1 class="bab-title">BAB VI</h1>
  <h2 class="bab-subtitle">KESIMPULAN DAN SARAN</h2>

  <h3>6.1 Kesimpulan</h3>
  <ol>
    <li>Penerapan standar <strong>NIST SP 800-86</strong> secara efektif mampu mengurai serangan siber multi-vektor pada PT. Satseet International ke dalam tahapan yang sistematis dan terukur.</li>
    <li>Keabsahan bukti digital terjamin secara penuh melalui proses hashing kriptografis ganda (MD5, SHA-1, SHA-256) pada fase Collection dan Examination dengan status verifikasi <code>COCOK</code> tanpa adanya indikasi pemalsuan bukti.</li>
    <li>Analisis log web mengungkap bahwa serangan diawali oleh eksploitasi Directory Traversal oleh IP <code>192.168.1.11</code> yang membocorkan berkas konfigurasi internal (<code>.env</code>), diikuti kampanye spear-phishing bertarget yang mengeksploitasi kerentanan Follina RCE (CVE-2022-30190), dan diakhiri dengan serangan ransomware serta pemerasan oleh kelompok BlackPython Team.</li>
    <li>Keberhasilan investigasi ini membuktikan bahwa otomasi skrip forensik berbasis Python dapat diandalkan untuk melakukan triase cepat (rapid triage) dan merekonstruksi linimasa kejahatan siber secara akurat.</li>
  </ol>

  <h3>6.2 Saran</h3>
  <ol>
    <li>Untuk penelitian selanjutnya, disarankan memperluas cakupan akuisisi ke artefak memori volatil (RAM) menggunakan perkakas seperti Volatility 3 untuk mendeteksi sisa injeksi kode in-memory yang tidak tersimpan di dalam disk.</li>
    <li>Disarankan mengintegrasikan format ekspor linimasa ke dalam standar visualisasi investigasi tingkat lanjut (seperti format Plaso / log2timeline atau Timesketch) guna mempermudah kolaborasi antar-analis forensik.</li>
  </ol>
</div>

<!-- DAFTAR PUSTAKA -->
<div class="page-break">
  <h1 class="bab-title">DAFTAR PUSTAKA</h1>
  <br>
  <p class="bib-item">1. Ihsan, M. R. I., & Voutama, A. (2025). Penerapan Metode NIST Dalam Analisis Forensik Digital Pasca Serangan Siber (Studi Kasus: PT. Analis Digital Forensik). <em>CyberSecurity dan Forensik Digital</em>, 8(1), 53–62.</p>
  <p class="bib-item">2. Kent, K., Chevalier, S., Grance, T., & Dang, H. (2006). <em>Guide to Integrating Forensic Techniques into Incident Response</em> (NIST Special Publication 800-86). National Institute of Standards and Technology, U.S. Department of Commerce.</p>
  <p class="bib-item">3. International Organization for Standardization. (2012). <em>Information technology — Security techniques — Guidelines for identification, collection, acquisition and preservation of digital evidence</em> (ISO/IEC Standard No. 27037:2012).</p>
  <p class="bib-item">4. Faizal, A., & Luthfi, A. (2024). Comparison Study of NIST SP 800-86 and ISO/IEC 27037 Standards as A Framework for Digital Forensic Evidence Analysis. <em>Journal of Information Systems and Informatics</em>, 6(2), 701–718.</p>
  <p class="bib-item">5. National Vulnerability Database (NVD). (2022). <em>CVE-2022-30190: Microsoft Windows Support Diagnostic Tool (MSDT) Remote Code Execution Vulnerability</em>. NIST.</p>
  <p class="bib-item">6. Ramadhan, R. A., Rachmat Setiawan, P., & Hariyadi, D. (2022). Digital Forensic Investigation for Non-Volatile Memory Architecture by Hybrid Evaluation Based on ISO/IEC 27037:2012 and NIST SP800-86 Framework. <em>IT Journal Research and Development</em>, 7(2), 162–168.</p>
  <p class="bib-item">7. Carrier, B. (2005). <em>File System Forensic Analysis</em>. Addison-Wesley Professional.</p>
  <p class="bib-item">8. Casey, E. (2011). <em>Digital Evidence and Computer Crime: Forensic Science, Computers, and the Internet</em> (3rd ed.). Academic Press.</p>
</div>

</body>
</html>
'''
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("HTML written to:", HTML_PATH)

    if os.path.exists(EDGE_PATH):
        cmd = [
            EDGE_PATH,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={PDF_PATH}",
            HTML_PATH
        ]
        subprocess.run(cmd, capture_output=True)
        time.sleep(2)
        print(f"PDF generated: {PDF_PATH} (size: {os.path.getsize(PDF_PATH)} bytes)")

if __name__ == "__main__":
    generate_pdf()
