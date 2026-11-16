# Laporan Forensik Digital (NIST SP 800-86)

- **Kasus:** SIM-01
- **Pemeriksa:** Peneliti Forensik
- **Waktu akuisisi (UTC):** 2026-11-16T05:55:13+00:00
- **Laporan dibuat (UTC):** 2026-11-16T05:55:32+00:00

## 1. Collection

| File | Ukuran (B) | SHA-256 | IOC |
|---|---|---|---|
| access.log | 10805 | `6c1445ee259c792cfc261dedfd7f7d99e001dd05b0c7839b6bae1288371f58bf` | - |
| catatan_akuisisi.txt | 169 | `42d326d9684b2143fed0d3a67bb736a325140dab099b6aa9bdf591a49a893561` | - |
| lampiran_simulasi.txt | 162 | `8b14132601aa8764960ea80eb246e7387c1adbf1e42f026c870e19fda39d3d04` | **COCOK** |

## 2. Examination (verifikasi integritas)

| File | Status | Keterangan |
|---|---|---|
| access.log | COCOK |  |
| catatan_akuisisi.txt | COCOK |  |
| lampiran_simulasi.txt | COCOK |  |

**Kesimpulan:** Semua hash cocok; bukti tidak berubah.

## 3. Analysis

### 3.1 Temuan access log

Baris log dianalisis: 113; permintaan mencurigakan: 5.

| Waktu | IP | Permintaan | Status | Catatan |
|---|---|---|---|---|
| 2024-11-05T19:58:02+07:00 | 192.168.1.11 | GET `/web/index.php/../../../etc/passwd` | 404 | pola path traversal; target file sensitif |
| 2024-11-05T19:58:05+07:00 | 192.168.1.11 | GET `/web/index.php/..%2f..%2f..%2fetc/passwd` | 403 | pola path traversal |
| 2024-11-05T19:58:09+07:00 | 192.168.1.11 | GET `/web/%2e%2e/%2e%2e/config/database.yml` | 404 | pola path traversal |
| 2024-11-05T19:58:14+07:00 | 192.168.1.11 | GET `/web/..%2f..%2fsrc/vendor/autoload.php` | 200 | pola path traversal; target file sensitif; **kemungkinan berhasil (2xx)** |
| 2024-11-05T19:58:20+07:00 | 192.168.1.11 | GET `/web/..%2f..%2fsrc/config/.env` | 200 | pola path traversal; target file sensitif; **kemungkinan berhasil (2xx)** |

IP dengan banyak respons 403/404 (indikasi pemindaian): 192.168.1.11 (8x)

### 3.2 Kronologi

| Waktu | Sumber | Peristiwa |
|---|---|---|
| 2024-11-05 12:58:02 | access.log | 192.168.1.11 GET /web/index.php/../../../etc/passwd [status 404] |
| 2024-11-05 12:58:05 | access.log | 192.168.1.11 GET /web/index.php/..%2f..%2f..%2fetc/passwd [status 403] |
| 2024-11-05 12:58:09 | access.log | 192.168.1.11 GET /web/%2e%2e/%2e%2e/config/database.yml [status 404] |
| 2024-11-05 12:58:14 | access.log | 192.168.1.11 GET /web/..%2f..%2fsrc/vendor/autoload.php [BERHASIL?] |
| 2024-11-05 12:58:20 | access.log | 192.168.1.11 GET /web/..%2f..%2fsrc/config/.env [BERHASIL?] |
| 2024-11-06 17:54:00 | email | Local User 2 menerima email lowongan kerja dari pengirim "Maya Putri" |
| 2024-11-19 22:18:00 | email | Email mencurigakan dari pengirim yang sama masuk ke akun Local User 1 |
| 2024-11-20 13:29:00 | email | Lampiran lamaran diunduh oleh Local User 1 |
| 2024-11-20 13:33:00 | disk | Dokumen riwayat hidup (lampiran) dibuka |
| 2024-11-20 13:49:00 | disk | Akses file update.exe (diduga backdoor) |
| 2024-11-20 13:50:00 | disk | Akses file ransom.exe (diduga ransomware) |
| 2024-11-20 13:59:00 | disk | Beberapa file terenkripsi/terkunci |
| 2024-11-22 09:00:00 | osint | Kelompok BlackPython Team mengklaim pencurian data di Telegram |

## 4. Reporting - Keterbatasan & Rekomendasi

- Temuan berbasis log yang tersedia; aktivitas yang tidak terekam tidak terdeteksi.
- Atribusi pelaku (IP/kelompok) bersifat indikatif dan perlu bukti tambahan.
- Rekomendasi umum: validasi input path, batasi akses di luar web root, patch Office/OS, email filtering, pelatihan karyawan, serta backup offline dan uji pemulihan.