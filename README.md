# 🚀 Lab & Repositori Acuan Pekan 05: Git Workflows & Reproducibility

Selamat datang di materi laboratorium dan contoh implementasi **Pekan 05: Git Workflows, Dependensi, & Reproducibility** untuk mata kuliah **Pemrograman Lanjut (SIN442430)**, Program Studi Sistem Informasi FST UIN Alauddin Makassar.

---

## 📁 Struktur Repositori (Gold Standard Layout)

```text
contoh_kode_pekan_5/
├── .env.example                     # Cetak biru konfigurasi publik (Wajib di-commit)
├── .gitignore                       # Memblokir .env, .venv, *.db, cache (Wajib di-commit)
├── pyproject.toml                   # Manifest deklaratif PEP 621 standar industri
├── src/
│   ├── siakad_config/               # Modul 12-Factor App Settings & Validation
│   │   ├── __init__.py
│   │   └── settings.py
│   └── siakad_billing/              # Modul inti billing agnostik lingkungan
│       ├── __init__.py
│       └── billing_core.py
├── tests/                           # Unit test suite terisolasi
│   └── test_config_and_billing.py
├── scripts/
│   └── verify_reproducibility.py    # Tool audit otomatis 4 pilar reproducibility
└── README.md                        # Panduan ini
```

---

## ⏱️ Protokol Laboratorium: "The Fresh Clone Test" (5 Menit)

Uji apakah repositori Anda dapat direplikasi oleh rekan tim tanpa galat:

### Langkah 1: Siapkan Konfigurasi Lingkungan Lokal
Salin template konfigurasi publik ke berkas `.env` lokal:

```bash
# Di Windows PowerShell:
Copy-Item .env.example .env

# Di Linux / macOS / Git Bash:
cp .env.example .env
```

### Langkah 2: Jalankan Unit Test Suite
Pastikan seluruh pengujian lulus:

```bash
py -m unittest tests/test_config_and_billing.py
```

### Langkah 3: Jalankan Audit Keterlacakan Otomatis
Jalankan skrip audit mandiri untuk mendapatkan skor 100/100:

```bash
py scripts/verify_reproducibility.py
```

---

## 🛠️ Alur Kerja Git Profesional (Git Workflow)

Gunakan standar ini saat mengerjakan tugas mandiri/kelompok:

### 1. Format Conventional Commits
```bash
git commit -m "feat(billing): tambah validasi payment api key fail-fast"
git commit -m "test(config): tambah test case invalid port"
git commit -m "chore(deps): perbarui batasan versi pydantic di pyproject.toml"
```

### 2. Percabangan Fitur (Feature Branch)
```bash
# Buat branch baru untuk fitur diskon
git checkout -b feat/tahfidz-discount

# Setelah selesai & test lulus, push dan buka Pull Request
git push origin feat/tahfidz-discount
```

### 3. Pemberian Tag Rilis (Semantic Versioning)
```bash
# Berikan tag beranotasi pada rilis v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0: Initial reproducible release"
git push origin v1.0.0
```
