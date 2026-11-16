#!/usr/bin/env python3
"""
forensik_nist.py - Toolkit forensik digital sederhana berbasis NIST SP 800-86.

Tahap NIST -> perintah:
  1. Collection   : collect   (hash bukti + manifest chain of custody)
  2. Examination  : verify    (verifikasi integritas bukti terhadap manifest)
  3. Analysis     : scan-log  (deteksi directory traversal pada access log)
                    timeline  (gabungkan peristiwa menjadi kronologi)
  4. Reporting    : report    (laporan Markdown dari semua tahap)

Hanya memakai pustaka standar Python 3.8+. Alat ini hanya untuk ANALISIS
bukti milik sendiri / yang diizinkan (defensif), bukan untuk menyerang.

Contoh:
  python forensik_nist.py collect  bukti/ --case KASUS-01 --examiner "Nama" -o manifest.json
  python forensik_nist.py verify   bukti/ manifest.json
  python forensik_nist.py scan-log access.log
  python forensik_nist.py timeline events.csv
  python forensik_nist.py report --evidence bukti/ --manifest manifest.json \
        --log access.log --events events.csv -o laporan.md
"""
import argparse
import csv
import hashlib
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ALGOS = ("md5", "sha1", "sha256")

# ---------------------------------------------------------------- utilitas

def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def hash_file(path, chunk=1 << 20):
    hashers = {a: hashlib.new(a) for a in ALGOS}
    with open(path, "rb") as f:
        while True:
            data = f.read(chunk)
            if not data:
                break
            for h in hashers.values():
                h.update(data)
    return {a: h.hexdigest() for a, h in hashers.items()}


def load_hash_set(path):
    """Baca daftar hash IOC (satu per baris, '#' = komentar)."""
    out = set()
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.split("#")[0].strip().lower()
        if line:
            out.add(line)
    return out

# ------------------------------------------------- 1. COLLECTION (hashing)

def collect(evidence_dir, case="", examiner="", ioc_file=None):
    root = Path(evidence_dir)
    if not root.is_dir():
        sys.exit(f"Folder bukti tidak ditemukan: {root}")
    iocs = load_hash_set(ioc_file) if ioc_file else set()
    files = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        st = p.stat()
        entry = {
            "path": p.relative_to(root).as_posix(),
            "size": st.st_size,
            "modified_utc": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat(timespec="seconds"),
            **hash_file(p),
        }
        entry["ioc_match"] = any(entry[a] in iocs for a in ALGOS)
        files.append(entry)
    return {
        "case": case,
        "examiner": examiner,
        "collected_at_utc": now_iso(),
        "evidence_root": str(root.resolve()),
        "files": files,
    }

# ------------------------------------------- 2. EXAMINATION (verifikasi)

def verify(evidence_dir, manifest):
    root = Path(evidence_dir)
    recorded = {f["path"]: f for f in manifest["files"]}
    results = []
    seen = set()
    for rel, rec in recorded.items():
        p = root / rel
        if not p.is_file():
            results.append((rel, "HILANG", ""))
            continue
        seen.add(rel)
        cur = hash_file(p)
        diff = [a for a in ALGOS if cur[a] != rec[a]]
        results.append((rel, "COCOK" if not diff else "BERUBAH", ",".join(diff)))
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).as_posix()
        if p.is_file() and rel not in recorded:
            results.append((rel, "BARU", "tidak ada di manifest"))
    return results

# ------------------------------------------------- 3a. ANALYSIS (log web)

LOG_RE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<ts>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+)[^"]*" (?P<status>\d{3}) (?P<size>\S+)'
)
TRAVERSAL_RE = re.compile(
    r"(\.\./|\.\.\\|%2e%2e(%2f|%5c|/)|%252e%252e|\.\.%2f|%c0%ae|%c1%9c)", re.I
)
SENSITIVE_RE = re.compile(
    r"(/etc/passwd|/etc/shadow|win\.ini|boot\.ini|\.env\b|\.git/|"
    r"autoload\.php|wp-config|web\.config|id_rsa|\.htpasswd)", re.I
)


def parse_ts(raw):
    for fmt in ("%d/%b/%Y:%H:%M:%S %z", "%d/%b/%Y:%H:%M:%S"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def scan_log(log_path, scan_threshold=5):
    hits, per_ip, errors_by_ip = [], defaultdict(int), defaultdict(int)
    total = 0
    with open(log_path, encoding="utf-8", errors="replace") as f:
        for n, line in enumerate(f, 1):
            m = LOG_RE.match(line)
            if not m:
                continue
            total += 1
            d = m.groupdict()
            if d["status"] in ("403", "404"):
                errors_by_ip[d["ip"]] += 1
            reasons = []
            if TRAVERSAL_RE.search(d["path"]):
                reasons.append("pola path traversal")
            if SENSITIVE_RE.search(d["path"]):
                reasons.append("target file sensitif")
            if reasons:
                per_ip[d["ip"]] += 1
                ts = parse_ts(d["ts"])
                hits.append({
                    "line": n, "ip": d["ip"], "time": ts.isoformat() if ts else d["ts"],
                    "method": d["method"], "path": d["path"], "status": d["status"],
                    "reasons": reasons,
                    # 200 pada permintaan traversal = kemungkinan BERHASIL
                    "possible_success": d["status"].startswith("2"),
                })
    scanners = {ip: c for ip, c in errors_by_ip.items() if c >= scan_threshold}
    return {"total_lines": total, "hits": hits, "per_ip": dict(per_ip), "scanners": scanners}

# --------------------------------------------------- 3b. ANALYSIS (timeline)

def load_events(csv_path):
    """CSV: timestamp,source,description  (timestamp ISO 8601 / 'YYYY-MM-DD HH:MM')."""
    events = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ts = row["timestamp"].strip()
            try:
                dt = datetime.fromisoformat(ts)
            except ValueError:
                sys.exit(f"Format waktu tidak valid: {ts!r}")
            events.append((dt, row.get("source", "").strip(), row.get("description", "").strip()))
    return events


def build_timeline(events, log_findings=None):
    items = list(events)
    if log_findings:
        for h in log_findings["hits"]:
            dt = parse_ts(h["time"]) if isinstance(h["time"], str) and "T" not in h["time"] else datetime.fromisoformat(h["time"])
            tag = "BERHASIL?" if h["possible_success"] else f"status {h['status']}"
            items.append((dt, "access.log", f"{h['ip']} {h['method']} {h['path']} [{tag}]"))
    # samakan zona waktu agar bisa diurutkan
    norm = [(dt.replace(tzinfo=None) if dt.tzinfo is None else dt.astimezone(timezone.utc).replace(tzinfo=None), s, d)
            for dt, s, d in items]
    return sorted(norm)

# ------------------------------------------------------- 4. REPORTING

def build_report(manifest, verification, log_findings, timeline):
    L = []
    a = L.append
    a("# Laporan Forensik Digital (NIST SP 800-86)\n")
    if manifest:
        a(f"- **Kasus:** {manifest.get('case') or '-'}")
        a(f"- **Pemeriksa:** {manifest.get('examiner') or '-'}")
        a(f"- **Waktu akuisisi (UTC):** {manifest['collected_at_utc']}")
        a(f"- **Laporan dibuat (UTC):** {now_iso()}\n")

    a("## 1. Collection\n")
    if manifest:
        a("| File | Ukuran (B) | SHA-256 | IOC |")
        a("|---|---|---|---|")
        for f in manifest["files"]:
            a(f"| {f['path']} | {f['size']} | `{f['sha256']}` | {'**COCOK**' if f['ioc_match'] else '-'} |")
        a("")
    else:
        a("_Manifest tidak diberikan._\n")

    a("## 2. Examination (verifikasi integritas)\n")
    if verification:
        a("| File | Status | Keterangan |")
        a("|---|---|---|")
        for rel, st, note in verification:
            a(f"| {rel} | {st} | {note} |")
        bad = [r for r in verification if r[1] != "COCOK"]
        a(f"\n**Kesimpulan:** {'Ada ketidaksesuaian, integritas bukti dipertanyakan.' if bad else 'Semua hash cocok; bukti tidak berubah.'}\n")
    else:
        a("_Verifikasi tidak dijalankan._\n")

    a("## 3. Analysis\n")
    if log_findings:
        a("### 3.1 Temuan access log\n")
        a(f"Baris log dianalisis: {log_findings['total_lines']}; permintaan mencurigakan: {len(log_findings['hits'])}.\n")
        if log_findings["hits"]:
            a("| Waktu | IP | Permintaan | Status | Catatan |")
            a("|---|---|---|---|---|")
            for h in log_findings["hits"]:
                note = "; ".join(h["reasons"]) + ("; **kemungkinan berhasil (2xx)**" if h["possible_success"] else "")
                a(f"| {h['time']} | {h['ip']} | {h['method']} `{h['path']}` | {h['status']} | {note} |")
            a("")
        if log_findings["scanners"]:
            a("IP dengan banyak respons 403/404 (indikasi pemindaian): " +
              ", ".join(f"{ip} ({c}x)" for ip, c in log_findings["scanners"].items()) + "\n")
    if timeline:
        a("### 3.2 Kronologi\n")
        a("| Waktu | Sumber | Peristiwa |")
        a("|---|---|---|")
        for dt, src, desc in timeline:
            a(f"| {dt:%Y-%m-%d %H:%M:%S} | {src} | {desc} |")
        a("")

    a("## 4. Reporting - Keterbatasan & Rekomendasi\n")
    a("- Temuan berbasis log yang tersedia; aktivitas yang tidak terekam tidak terdeteksi.")
    a("- Atribusi pelaku (IP/kelompok) bersifat indikatif dan perlu bukti tambahan.")
    a("- Rekomendasi umum: validasi input path, batasi akses di luar web root, patch Office/OS, "
      "email filtering, pelatihan karyawan, serta backup offline dan uji pemulihan.")
    return "\n".join(L)

# ------------------------------------------------------------------ CLI

def main():
    ap = argparse.ArgumentParser(description="Toolkit forensik digital berbasis NIST SP 800-86")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("collect", help="Hash semua file bukti dan buat manifest")
    p.add_argument("evidence")
    p.add_argument("--case", default="")
    p.add_argument("--examiner", default="")
    p.add_argument("--ioc", help="File daftar hash IOC (MD5/SHA1/SHA256)")
    p.add_argument("-o", "--output", default="manifest.json")

    p = sub.add_parser("verify", help="Verifikasi bukti terhadap manifest")
    p.add_argument("evidence")
    p.add_argument("manifest")

    p = sub.add_parser("scan-log", help="Deteksi directory traversal di access log")
    p.add_argument("log")
    p.add_argument("--threshold", type=int, default=5, help="Batas 403/404 per IP")

    p = sub.add_parser("timeline", help="Urutkan peristiwa dari CSV")
    p.add_argument("events")

    p = sub.add_parser("report", help="Buat laporan Markdown")
    p.add_argument("--evidence")
    p.add_argument("--manifest")
    p.add_argument("--log")
    p.add_argument("--events")
    p.add_argument("-o", "--output", default="laporan.md")

    args = ap.parse_args()

    if args.cmd == "collect":
        m = collect(args.evidence, args.case, args.examiner, args.ioc)
        Path(args.output).write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"{len(m['files'])} file di-hash -> {args.output}")
        for f in m["files"]:
            print(f"  {f['sha256']}  {f['path']}" + ("  <-- COCOK IOC" if f["ioc_match"] else ""))

    elif args.cmd == "verify":
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        res = verify(args.evidence, manifest)
        for rel, st, note in res:
            print(f"[{st:7}] {rel} {note}")
        sys.exit(0 if all(r[1] == "COCOK" for r in res) else 1)

    elif args.cmd == "scan-log":
        r = scan_log(args.log, args.threshold)
        print(f"Baris dianalisis: {r['total_lines']}, mencurigakan: {len(r['hits'])}")
        for h in r["hits"]:
            flag = "  <-- kemungkinan BERHASIL" if h["possible_success"] else ""
            print(f"  {h['time']} {h['ip']} {h['method']} {h['path']} -> {h['status']}{flag}")
        for ip, c in r["scanners"].items():
            print(f"  Indikasi pemindaian: {ip} ({c}x 403/404)")

    elif args.cmd == "timeline":
        for dt, src, desc in build_timeline(load_events(args.events)):
            print(f"{dt:%Y-%m-%d %H:%M:%S}  [{src}]  {desc}")

    elif args.cmd == "report":
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8")) if args.manifest else None
        verification = verify(args.evidence, manifest) if (args.evidence and manifest) else None
        findings = scan_log(args.log) if args.log else None
        events = load_events(args.events) if args.events else []
        tl = build_timeline(events, findings) if (events or findings) else None
        Path(args.output).write_text(build_report(manifest, verification, findings, tl), encoding="utf-8")
        print(f"Laporan ditulis ke {args.output}")


if __name__ == "__main__":
    main()
