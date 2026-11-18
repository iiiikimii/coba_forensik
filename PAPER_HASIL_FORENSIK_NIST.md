# INVESTIGASI FORENSIK DIGITAL SERANGAN SIBER MULTI-VEKTOR MENGGUNAKAN METODOLOGI NIST SP 800-86
**Studi Kasus: Eksploitasi Web Server HRMS, Spear-Phishing Follina (CVE-2022-30190), dan Ransomware pada PT. Satseet International**

---

**Disusun Oleh:**  
- **Nama:** [Nama Lengkap Mahasiswa]  
- **NIM:** [Nomor Induk Mahasiswa]  
- **Program Studi:** [Sistem Informasi / Teknik Informatika]  
- **Fakultas / Universitas:** [Nama Fakultas & Universitas]  
- **Mata Kuliah:** [Forensik Digital / Keamanan Siber]  
- **Tahun Akademik:** 2024/2025  

---

## ABSTRAK

Peningkatan frekuensi dan kompleksitas serangan siber modern menuntut pendekatan investigasi insiden yang terstruktur, akuntabel, dan dapat dipertanggungjawabkan secara hukum. Penelitian ini menyajikan investigasi forensik digital pascainsiden serangan multi-vektor terhadap sistem *Human Resource Management System* (HRMS) dan web server PT. Satseet International yang terjadi pada rentang waktu 5 hingga 22 November 2024. Metodologi yang diterapkan mengacu pada standar *National Institute of Standards and Technology Special Publication 800-86* (NIST SP 800-86) yang mencakup empat fase utama: *Collection*, *Examination*, *Analysis*, dan *Reporting*. Melalui implementasi toolkit forensik terotomatisasi berbasis Python, dilakukan proses akuisisi bukti digital, pembangkitan nilai hash kriptografis (*Chain of Custody*), analisis 113 baris log akses HTTP, pencocokan *Indicator of Compromise* (IOC), serta rekonstruksi linimasa (*timeline analysis*). Hasil investigasi mengungkap bahwa aktor ancaman *BlackPython Team* memulai serangan melalui *Directory Traversal* pada web server untuk mengekstraksi berkas konfigurasi sensitif (`.env` dan `autoload.php`), dilanjutkan dengan operasi *spear-phishing* bertema rekrutmen yang memanfaatkan kerentanan *Remote Code Execution* Follina (CVE-2022-30190). Rangkaian serangan berujung pada penyusupan *trojan backdoor* (`update.exe`) dan enkripsi berkas oleh *ransomware* (`ransom.exe`). Laporan ini menyimpulkan temuan teknis serta merumuskan rekomendasi mitigasi komprehensif mencakup validasi input, pembaruan keamanan, strategi cadangan data 3-2-1, dan peningkatan kesadaran keamanan bagi organisasi.

**Kata Kunci:** *Forensik Digital, NIST SP 800-86, Directory Traversal, Follina (CVE-2022-30190), Ransomware, Chain of Custody.*

---

## ABSTRACT

*The increasing frequency and sophistication of cyberattacks necessitate a structured, accountable, and legally admissible incident investigation approach. This paper presents a post-incident digital forensic investigation on a multi-vector cyberattack targeting the Human Resource Management System (HRMS) and web server of PT. Satseet International between November 5 and November 22, 2024. The methodology strictly adopts the National Institute of Standards and Technology Special Publication 800-86 (NIST SP 800-86) framework, comprising four foundational phases: Collection, Examination, Analysis, and Reporting. Utilizing an automated Python-based forensic toolkit, digital evidence acquisition, cryptographic hashing for Chain of Custody, inspection of 113 HTTP access log records, Indicator of Compromise (IOC) matching, and cross-source timeline reconstruction were systematically conducted. The findings demonstrate that the threat group 'BlackPython Team' initiated the breach via Directory Traversal to harvest sensitive server configuration files (.env and autoload.php), followed by a spear-phishing campaign exploiting the Follina Remote Code Execution vulnerability (CVE-2022-30190). The intrusion culminated in the deployment of a trojan backdoor (update.exe) and critical data encryption by ransomware (ransom.exe). This study delivers technical evidence correlation and proposes robust mitigation strategies, including strict input sanitization, security patching, 3-2-1 backup architecture, and employee cybersecurity awareness.*

**Keywords:** *Digital Forensics, NIST SP 800-86, Directory Traversal, Follina (CVE-2022-30190), Ransomware, Incident Response.*

---

## BAB I: PENDAHULUAN

### 1.1 Latar Belakang
Transformasi digital dalam sektor korporasi telah mendorong sentralisasi pengelolaan data pegawai dan operasional bisnis ke dalam sistem terintegrasi, seperti *Human Resource Management System* (HRMS). Namun, perluasan permukaan serangan (*attack surface*) tanpa diimbangi postur pertahanan yang memadai memicu kerentanan terhadap serangan siber terorganisir. Berdasarkan laporan lanskap ancaman Badan Siber dan Sandi Negara (BSSN), anomali trafik dan insiden siber terus menunjukkan tren eskalasi dengan ratusan juta anomali tercatat setiap tahunnya.

Pada rentang 5–22 November 2024, PT. Satseet International mengalami insiden keamanan siber berskala masif yang mengakibatkan lumpuhnya operasional HRMS, kebocoran data pegawai, serta enkripsi berkas penting perusahaan oleh kelompok penyerang yang menamakan diri *BlackPython Team*. Insiden ini tidak berlangsung secara tunggal, melainkan melalui kombinasi serangan multi-vektor: peretasan awal melalui eksploitasi web server, rekayasa sosial (*spear-phishing*), eksekusi kode jarak jauh (*Remote Code Execution* / RCE), hingga penyebaran *ransomware*.

Guna mengungkap anatomi serangan secara utuh dan menjamin keabsahan bukti digital di ranah investigasi maupun hukum, diperlukan metodologi forensik yang terstandarisasi. Standar NIST SP 800-86 dipilih karena menyediakan kerangka kerja investigasi sistematis yang menjamin keutuhan (*integrity*), keterulangan (*repeatability*), dan keterlacakan (*chain of custody*) dari seluruh artefak digital.

### 1.2 Rumusan Masalah
1. Bagaimana mengidentifikasi, mengamankan, dan memverifikasi integritas bukti digital yang diperoleh pascaserangan pada sistem PT. Satseet International?
2. Bagaimana pola dan teknik serangan multi-vektor (Directory Traversal, Follina CVE-2022-30190, dan Ransomware) dapat direkonstruksi ke dalam linimasa kronologis yang valid?
3. Apa langkah-langkah mitigasi dan tata kelola keamanan yang perlu diterapkan untuk mencegah insiden berulang?

### 1.3 Tujuan Penelitian
1. Menerapkan metodologi NIST SP 800-86 (*Collection, Examination, Analysis, Reporting*) dalam menginvestigasi insiden keamanan siber.
2. Membuktikan integritas bukti digital melalui kalkulasi hash kriptografis ganda (MD5, SHA-1, SHA-256).
3. Melakukan deteksi anomali pada log web server serta mencocokkan *Indicator of Compromise* (IOC).
4. Menyusun laporan investigasi forensik akademik yang komprehensif dan aplikatif sebagai bahan evaluasi institusi.

### 1.4 Batasan Masalah
1. Investigasi difokuskan pada artefak digital yang disediakan dalam paket simulasi kasus PT. Satseet International, meliputi log web server (`access.log`), catatan akuisisi, berkas lampiran phishing simulasi, dan rekaman peristiwa sistem (`events.csv`).
2. Toolkit forensik yang digunakan diimplementasikan dalam skrip terotomatisasi Python 3.8+ berbasis pustaka standar defensif, selaras dengan prinsip-prinsip NIST SP 800-86.

---

## BAB II: LANDASAN TEORI

### 2.1 Forensik Digital dan Standar NIST SP 800-86
Forensik digital didefinisikan sebagai penerapan prinsip-prinsip ilmiah terhadap penemuan, validasi, identifikasi, analisis, dan interpretasi bukti digital yang berasal dari media digital untuk memfasilitasi rekonstruksi peristiwa. National Institute of Standards and Technology menerbitkan panduan **NIST SP 800-86** (*Guide to Integrating Forensic Techniques into Incident Response*) yang menetapkan empat fase dasar:
1. **Collection (Pengumpulan):** Proses identifikasi, pelabelan, pencatatan, dan pengamanan sumber bukti fisik maupun digital dengan menjaga *Chain of Custody*.
2. **Examination (Pemeriksaan):** Pemrosesan bukti mentah secara forensik menggunakan teknik ekstraksi artefak dan verifikasi keaslian melalui algoritma *cryptographic hashing*.
3. **Analysis (Analisis):** Penerapan metode analitis untuk menarik kesimpulan logis, menentukan vektor serangan, pelaku (*threat actor*), serta dampak insiden.
4. **Reporting (Pelaporan):** Penyajian hasil analisis secara formal, transparan, dan terstruktur yang mencakup prosedur, temuan, keterbatasan, dan rekomendasi mitigasi.

```
+------------------+      +--------------------+      +------------------+      +-------------------+
|  1. COLLECTION   | ---> |   2. EXAMINATION   | ---> |   3. ANALYSIS    | ---> |   4. REPORTING    |
| (Hash & Manifest)|      | (Integrity Verify) |      | (Log & Timeline) |      | (Formal Report)   |
+------------------+      +--------------------+      +------------------+      +-------------------+
```

### 2.2 Integritas Bukti dan Chain of Custody
*Chain of Custody* merupakan dokumentasi kronologis yang mencatat perolehan, pengendalian, pemindahan, analisis, dan penyimpanan bukti digital. Integritas berkas dibuktikan dengan menghasilkan intisari pesan (*message digest*) melalui fungsi hash kriptografis:
- **MD5 (128-bit):** Algoritma ringkasan pesan cepat untuk verifikasi awal.
- **SHA-1 (160-bit):** Standar kriptografi pelengkap integritas.
- **SHA-256 (256-bit):** Standar hashing modern yang memiliki ketahanan benturan (*collision resistance*) sangat tinggi, wajib disertakan dalam standar forensik internasional.

### 2.3 Vektor Serangan Siber Terkait
1. **Directory Traversal (Path Traversal):** Kerentanan aplikasi web yang memungkinkan penyerang membaca berkas di luar direktori *web root* dengan menyuntikkan karakter sekuens khusus seperti `../` atau representasi URL-encoded `%2e%2e%2f`. Tujuannya adalah memperoleh kredensial basis data atau berkas konfigurasi sistem (`/etc/passwd`, `.env`).
2. **Follina Exploit (CVE-2022-30190):** Kerentanan zero-day pada Microsoft Windows Support Diagnostic Tool (MSDT) yang dipicu saat membuka atau melihat pratinjau dokumen Microsoft Office (.docx/.rtf). Kerentanan ini memungkinkan penyerang mengeksekusi kode PowerShell jarak jauh (*Remote Code Execution*) dengan hak akses pengguna lokal tanpa perlu macro aktif.
3. **Ransomware dan Trojan Backdoor:** Perangkat lunak berbahaya yang mengenkripsi berkas korban menggunakan enkripsi asimetris/simetris dan menuntut uang tebusan (*ransom*). Trojan backdoor dipasang untuk mempertahankan akses persisten (*persistence*) ke dalam sistem internal korban.

---

## BAB III: METODOLOGI PENELITIAN

### 3.1 Kerangka Kerja Eksperimen
Penelitian ini mengadopsi alur eksperimen empiris berbasis NIST SP 800-86 dengan tahapan kerja operasional sebagai berikut:

```
[Mulai]
   │
   ▼
[1. Fase Collection]
   ├─ Pindaian rekursif direktori bukti (bukti/)
   ├─ Ekstraksi metadata berkas (nama, ukuran, st_mtime)
   ├─ Komputasi hash MD5, SHA-1, SHA-256
   ├─ Pencocokan otomatis terhadap basis data IOC (ioc.txt)
   └─ Ekspor manifest Chain of Custody (manifest.json)
   │
   ▼
[2. Fase Examination]
   ├─ Pemuatan manifest.json
   ├─ Komputasi ulang hash berkas fisik saat ini
   ├─ Komparasi hash (Deteksi status: COCOK, BERUBAH, HILANG, BARU)
   └─ Validasi tamper resistance
   │
   ▼
[3. Fase Analysis]
   ├─ Parsing log web server HTTP (bukti/access.log)
   ├─ Regex matching pola traversal (../, %2e%2e, %252e%252e)
   ├─ Deteksi akses berkas sensitif (/etc/passwd, autoload.php, .env)
   ├─ Evaluasi HTTP status code (200 OK vs 403/404)
   ├─ Ingest data peristiwa insiden (events.csv)
   └─ Normalisasi zona waktu (UTC/WIB) & agregasi linimasa terpadu
   │
   ▼
[4. Fase Reporting]
   ├─ Kompilasi seluruh matriks temuan
   ├─ Sintesis dampak dan atribusi aktor (BlackPython Team)
   └─ Penyusunan laporan resmi (laporan.md)
   │
   ▼
[Selesai]
```

### 3.2 Lingkungan dan Alat Pengujian
Pengujian dilakukan pada lingkungan terkontrol dengan spesifikasi sebagai berikut:
- **Sistem Operasi Analis:** Microsoft Windows 11 Pro 64-bit
- **Lingkungan Eksekusi:** Python 3.13.1 (Standard Library: `hashlib`, `pathlib`, `re`, `csv`, `datetime`, `argparse`, `json`)
- **Toolkit Utama:** `forensik_nist.py`
- **Data Uji:** Paket simulasi kasus PT. Satseet International (`bukti/access.log`, `catatan_akuisisi.txt`, `lampiran_simulasi.txt`, `events.csv`, `ioc.txt`)
- **Komparator Teoritis:** Wireshark v4.4.2, FTK Imager v4.7.1.2, Autopsy v4.21.0, dan VirusTotal Intelligence

---

## BAB IV: HASIL DAN PEMBAHASAN

### 4.1 Tahap 1: Collection (Akuisisi Bukti dan Hashing)
Proses pengumpulan bukti dijalankan terhadap direktori `bukti/` dengan parameter kasus `SIM-01` dan pencocokan terhadap `ioc.txt`. Pembangkitan tanda tangan digital menghasilkan berkas `manifest.json`.

**Tabel 4.1. Manifest Inventaris Bukti Digital dan Hasil Hashing**
| Nama Berkas Bukti | Ukuran (Bytes) | Hash MD5 | Hash SHA-1 | Hash SHA-256 | Kecocokan IOC |
| :--- | :---: | :--- | :--- | :--- | :---: |
| `access.log` | 10.805 | `0a2e379b32e185873ec8b408892f39c0` | `82cf214b62db4df43b7e73507119ff391f1a5f6e` | `6c1445ee259c792cfc261dedfd7f7d99e001dd05b0c7839b6bae1288371f58bf` | - |
| `catatan_akuisisi.txt` | 169 | `4c7bf69bf17b70743b2f293b722d3b7e` | `bcebb5523a789a3f2dbd1112d308078e878347f7` | `42d326d9684b2143fed0d3a67bb736a325140dab099b6aa9bdf591a49a893561` | - |
| `lampiran_simulasi.txt`| 162 | `a5f22f6d0f666f7f63f58a361a9bc348` | `4f3876d540268dfc949fef56f2d93e8784d00810` | `8b14132601aa8764960ea80eb246e7387c1adbf1e42f026c870e19fda39d3d04` | **COCOK (MATCH)** |

**Temuan Kunci:**
Berkas `lampiran_simulasi.txt` memiliki nilai hash SHA-256 yang identik dengan entri dalam `ioc.txt`. Hal ini membuktikan secara ilmiah bahwa berkas lampiran yang diunduh korban pada skenario insiden merupakan sampel dokumen berbahaya (*malicious document*) Follina yang disebarkan penyerang.

---

### 4.2 Tahap 2: Examination (Verifikasi Integritas Data)
Pada tahap pemeriksaan, dilakukan verifikasi integritas dengan membandingkan kondisi riil seluruh berkas di media penyimpanan terhadap tanda tangan digital yang tercatat di dalam `manifest.json`.

**Tabel 4.2. Hasil Uji Verifikasi Integritas Bukti**
| Nama Berkas | Status Integritas | Keterangan Hash | Validasi Keabsahan |
| :--- | :---: | :---: | :---: |
| `access.log` | **COCOK** | Tidak ada perbedaan hash | Sah / Valid |
| `catatan_akuisisi.txt` | **COCOK** | Tidak ada perbedaan hash | Sah / Valid |
| `lampiran_simulasi.txt` | **COCOK** | Tidak ada perbedaan hash | Sah / Valid |

**Analisis Verifikasi:**  
Semua berkas bukti berstatus `COCOK`. Tidak ada indikasi modifikasi, penambahan, maupun penghapusan data pascaakuisisi. Bukti dinyatakan memenuhi prinsip *admissibility* dalam standar hukum forensik. Pengujian *tamper resistance* yang dilakukan dengan memanipulasi 1 bita isi berkas langsung memicu status `BERUBAH`, membuktikan keandalan sistem deteksi.

---

### 4.3 Tahap 3: Analysis (Analisis Log Web dan Deteksi Anomali)
Pemeriksaan terhadap berkas `access.log` (total 113 baris transaksi HTTP) berhasil mendeteksi aktivitas pemindaian dan eksploitasi oleh alamat IP eksternal `192.168.1.11`.

**Tabel 4.3. Rincian Rekaman Serangan Directory Traversal pada Web Server**
| Timestamp (WIB) | Alamat IP Penyerang | Metode | Jalur Target (*Requested URI*) | Status HTTP | Evaluasi Forensik |
| :---: | :---: | :---: | :--- | :---: | :--- |
| `05/Nov/2024 19:58:02` | `192.168.1.11` | GET | `/web/index.php/../../../etc/passwd` | 404 | Pola traversal teks polos; target file kredensial sistem Linux. |
| `05/Nov/2024 19:58:05` | `192.168.1.11` | GET | `/web/index.php/..%2f..%2f..%2fetc/passwd` | 403 | Pola traversal dengan enkoding URL (`%2f` = `/`); diblokir server. |
| `05/Nov/2024 19:58:09` | `192.168.1.11` | GET | `/web/%2e%2e/%2e%2e/config/database.yml` | 404 | Enkoding titik ganda (`%2e%2e`); mencari konfigurasi basis data. |
| `05/Nov/2024 19:58:14` | `192.168.1.11` | GET | `/web/..%2f..%2fsrc/vendor/autoload.php` | **200** | **BERHASIL:** File loader komponen aplikasi web berhasil diakses. |
| `05/Nov/2024 19:58:20` | `192.168.1.11` | GET | `/web/..%2f..%2fsrc/config/.env` | **200** | **KRITIS / BERHASIL:** Berkas `.env` (berisi password, API key, konfigurasi internal) bocor. |

**Evaluasi Teknis:**  
Pelaku melakukan teknik *fuzzing/scanning* dengan variasi URL encoding untuk mengelabui filter *Web Application Firewall* (WAF). Keberhasilan respons status `200 OK` pada permintaan berkas `.env` menjadi titik balik kritis insiden, di mana penyerang berhasil memperoleh kredensial administratif internal yang kemudian dipakai untuk menembus portal HRMS pada tahap serangan berikutnya.

---

### 4.4 Rekonstruksi Linimasa Serangan Terpadu (*Integrated Timeline Analysis*)
Dengan menggabungkan artefak log akses web, data rekayasa sosial, dan rekaman peristiwa endpoint (`events.csv`), berhasil disusun linimasa komprehensif dari awal hingga akhir insiden.

**Tabel 4.4. Linimasa Komprehensif Serangan Multi-Vektor**
| Tanggal & Waktu (WIB) | Sumber Artefak | Entitas / Akun | Deskripsi Peristiwa Serangan | Fase Serangan |
| :---: | :---: | :---: | :--- | :--- |
| `05/Nov/2024 19:58:02` | `access.log` | `192.168.1.11` | Percobaan Directory Traversal ke `/etc/passwd` (HTTP 404) | *Reconnaissance* |
| `05/Nov/2024 19:58:05` | `access.log` | `192.168.1.11` | Percobaan Directory Traversal dengan URL encoding (HTTP 403) | *Evasion Attempt* |
| `05/Nov/2024 19:58:14` | `access.log` | `192.168.1.11` | Akses ke `autoload.php` berhasil (HTTP 200) | *Information Gathering* |
| `05/Nov/2024 19:58:20` | `access.log` | `192.168.1.11` | Akses ke konfigurasi rahasia `.env` berhasil (HTTP 200) | *Credential Leakage* |
| `06/Nov/2024 17:54:00` | Email Gateway | Local User 2 | Menerima email pertanyaan lowongan kerja dari "Maya Putri" | *Reconnaissance Social* |
| `19/Nov/2024 22:18:00` | Email Gateway | Local User 1 ("Ahmad Habibie") | Email phishing lanjutan masuk membawa tautan/lampiran lamaran kerja | *Initial Access Weaponization* |
| `20/Nov/2024 13:23:00` | Web Log | `192.168.1.11` | Pelaku mencoba mengakses antarmuka portal login HRMS | *Initial Connection* |
| `20/Nov/2024 13:29:00` | Web Log | `192.168.1.11` | Pelaku berhasil login ke portal HRMS menggunakan kredensial bocor | *Privilege Access* |
| `20/Nov/2024 13:29:00` | Email Client | Local User 1 | Lampiran lamaran kerja `Folline.zip` diunduh oleh korban | *Delivery / User Execution* |
| `20/Nov/2024 13:33:00` | Disk / Endpoint | Local User 1 | Dokumen kurikulum vitae dibuka, memicu eksploitasi CVE-2022-30190 | *Remote Code Execution* |
| `20/Nov/2024 13:49:00` | Disk / Endpoint | Local User 1 | Eksekusi otomatis `update.exe` (Trojan Backdoor aktif) | *Persistence / C2* |
| `20/Nov/2024 13:50:00` | Disk / Endpoint | Local User 1 | Eksekusi `ransom.exe` (`main_v2.exe` / *Python.Filecoder*) | *Malware Execution* |
| `20/Nov/2024 13:59:00` | Disk / Storage | Sistem HRMS | Berkas-berkas penting terenkripsi dan ekstensi berganti `.wasted` | *Impact (Ransomware)* |
| `22/Nov/2024 09:00:00` | OSINT / Telegram | BlackPython Team | Publikasi klaim pencurian data karyawan dan tuntutan pemerasan | *Exfiltration & Extortion* |

---

### 4.5 Analisis Atribusi dan Karakteristik Malware
1. **Atribusi Aktor Ancaman:**  
   Klaim publik pada saluran Telegram tanggal 22 November 2024 mengonfirmasi keterlibatan sindikat **BlackPython Team**. Pola serangan mencerminkan model *double extortion* (pemerasan ganda), di mana data sensitif pegawai diunduh terlebih dahulu sebelum sistem dienkripsi secara total.
2. **Karakteristik Trojan Backdoor (`update.exe`):**  
   Berdasarkan intelijen VirusTotal dan telemetri endpoint, berkas ini dikenali sebagai keluarga *Trojan.Win32/Shell.R128S* dan *Backdoor.Win/shellcode.apid*. Berkas ini berfungsi menjaga koneksi balik (*reverse shell*) guna memfasilitasi injeksi muatan sekunder.
3. **Karakteristik Ransomware (`ransom.exe`):**  
   Malware ini merupakan varian *Python.Filecoder* yang memanfaatkan algoritma kriptografi hibrida untuk mengunci struktur file korporat tanpa kemungkinan dekripsi tanpa kunci privat penyerang.

---

## BAB V: REKOMENDASI DAN STRATEGI MITIGASI

Berdasarkan temuan forensik, dirumuskan strategi pertahanan mendalam (*defense-in-depth*) mencakup aspek teknis, prosedural, dan sumber daya manusia:

### 5.1 Pengamanan Aplikasi Web dan Server
1. **Validasi dan Sanitasi Input Ketat:** Menerapkan pembatasan jalur kanonikal (*canonical path checking*) pada kode PHP untuk menolak semua string yang mengandung `../`, `%2e`, atau karakter kontrol traversal lainnya.
2. **Pemisahan Direktori Sensitif:** Memindahkan berkas konfigurasi kritis (`.env`, konfigurasi database, pustaka vendor) ke luar direktori publik (*document root* web server), serta menonaktifkan *directory indexing*.
3. **Penerapan Web Application Firewall (WAF):** Mengaktifkan modul filter inspeksi paket HTTP real-time untuk secara otomatis memblokir IP yang melakukan percobaan serangan berbasis pola tanda tangan serangan.

### 5.2 Pengamanan Endpoint dan Penambalan Kerentanan
1. **Penambalan Segera CVE-2022-30190:** Memastikan pembaruan keamanan sistem operasi Windows dan Microsoft Office terpasang, atau menonaktifkan protokol MSDT (*troubleshooter URL handler*) melalui registri Windows jika pembaruan belum dapat diterapkan.
2. **Implementasi EDR (*Endpoint Detection and Response*):** Memasang agen EDR dengan heuristik perilaku untuk mendeteksi perilaku mencurigakan seperti aplikasi Office (`winword.exe`) yang memanggil `powershell.exe` atau `msdt.exe`.
3. **Kebijakan Pengeksekusian Perangkat Lunak:** Membatasi eksekusi berkas binari di folder temporer (`%TEMP%`, `%APPDATA%`, `Downloads`) menggunakan fitur *AppLocker* atau *Software Restriction Policies*.

### 5.3 Strategi Manajemen Cadangan (*Backup Resilience*)
1. **Arsitektur Backup 3-2-1:** Menyimpan setidaknya 3 salinan data, pada 2 media penyimpanan yang berbeda, dengan 1 salinan tersimpan secara *offline / immutable* (air-gapped) agar tidak dapat dienkripsi oleh ransomware yang menyebar di jaringan internal.
2. **Pengujian Pemulihan Berkala:** Melakukan simulasi *disaster recovery* terjadwal untuk mengukur *Recovery Time Objective* (RTO) dan *Recovery Point Objective* (RPO).

### 5.4 Peningkatan Kesadaran Keamanan Karyawan
1. **Pelatihan Anti-Phishing:** Mengadakan simulasi *spear-phishing* berkala untuk melatih kewaspadaan pegawai HRD terhadap berkas lamaran berformat arsip (.zip, .rar) atau dokumen pembawa muatan makro berbahaya.
2. **Penerapan Autentikasi Multi-Faktor (MFA):** Wajib menerapkan MFA pada seluruh akses portal administrasi web server dan akun email korporat guna memitigasi penyalahgunaan kredensial hasil peretasan.

---

## BAB VI: KESIMPULAN DAN SARAN

### 6.1 Kesimpulan
1. Penerapan standar **NIST SP 800-86** secara efektif mampu mengurai serangan siber multi-vektor pada PT. Satseet International ke dalam tahapan yang sistematis dan terukur.
2. Keabsahan bukti digital terjamin secara penuh melalui proses hashing kriptografis ganda (MD5, SHA-1, SHA-256) pada fase *Collection* dan *Examination* dengan status verifikasi `COCOK` tanpa adanya indikasi pemalsuan bukti.
3. Analisis log web mengungkap bahwa serangan diawali oleh eksploitasi *Directory Traversal* oleh IP `192.168.1.11` yang membocorkan berkas konfigurasi internal (`.env`), diikuti kampanye *spear-phishing* bertarget yang mengeksploitasi kerentanan *Follina RCE* (CVE-2022-30190), dan diakhiri dengan serangan *ransomware* serta pemerasan oleh kelompok *BlackPython Team*.
4. Keberhasilan investigasi ini membuktikan bahwa otomasi skrip forensik berbasis Python dapat diandalkan untuk melakukan triase cepat (*rapid triage*) dan merekonstruksi linimasa kejahatan siber secara akurat.

### 6.2 Saran
1. Untuk penelitian selanjutnya, disarankan memperluas cakupan akuisisi ke artefak memori volatil (RAM) menggunakan perkakas seperti *Volatility 3* untuk mendeteksi sisa injeksi kode *in-memory* yang tidak tersimpan di dalam disk.
2. Disarankan mengintegrasikan format ekspor linimasa ke dalam standar visualisasi investigasi tingkat lanjut (seperti format *Plaso / log2timeline* atau *Timesketch*) guna mempermudah kolaborasi antar-analis forensik.

---

## DAFTAR PUSTAKA

1. Ihsan, M. R. I., & Voutama, A. (2025). Penerapan Metode NIST Dalam Analisis Forensik Digital Pasca Serangan Siber (Studi Kasus: PT. Analis Digital Forensik). *CyberSecurity dan Forensik Digital*, 8(1), 53–62.
2. Kent, K., Chevalier, S., Grance, T., & Dang, H. (2006). *Guide to Integrating Forensic Techniques into Incident Response* (NIST Special Publication 800-86). National Institute of Standards and Technology, U.S. Department of Commerce.
3. International Organization for Standardization. (2012). *Information technology — Security techniques — Guidelines for identification, collection, acquisition and preservation of digital evidence* (ISO/IEC Standard No. 27037:2012).
4. Faizal, A., & Luthfi, A. (2024). Comparison Study of NIST SP 800-86 and ISO/IEC 27037 Standards as A Framework for Digital Forensic Evidence Analysis. *Journal of Information Systems and Informatics*, 6(2), 701–718.
5. National Vulnerability Database (NVD). (2022). *CVE-2022-30190: Microsoft Windows Support Diagnostic Tool (MSDT) Remote Code Execution Vulnerability*. NIST.
6. Ramadhan, R. A., Rachmat Setiawan, P., & Hariyadi, D. (2022). Digital Forensic Investigation for Non-Volatile Memory Architecture by Hybrid Evaluation Based on ISO/IEC 27037:2012 and NIST SP800-86 Framework. *IT Journal Research and Development*, 7(2), 162–168.
7. Carrier, B. (2005). *File System Forensic Analysis*. Addison-Wesley Professional.
8. Casey, E. (2011). *Digital Evidence and Computer Crime: Forensic Science, Computers, and the Internet* (3rd ed.). Academic Press.
