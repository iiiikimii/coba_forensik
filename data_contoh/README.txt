PAKET DATA CONTOH (SIMULASI) - forensik_nist.py
Semua data fiktif, dibuat untuk latihan. Bukan data PT Satseet asli.

Urutan menjalankan (letakkan forensik_nist.py di folder yang sama):
  python forensik_nist.py collect bukti/ --case SIM-01 --examiner "Nama Anda" --ioc ioc.txt -o manifest.json
  python forensik_nist.py verify bukti/ manifest.json
  python forensik_nist.py scan-log bukti/access.log --threshold 3
  python forensik_nist.py timeline events.csv
  python forensik_nist.py report --evidence bukti/ --manifest manifest.json --log bukti/access.log --events events.csv -o laporan.md

Demo deteksi perubahan bukti: ubah isi bukti/catatan_akuisisi.txt lalu jalankan 'verify' lagi (status BERUBAH).
