"""
AUDIT TOOL: Automated Reproducibility & Secrets Verifier
Mata Kuliah: Pemrograman Lanjut (SIN442430) - UIN Alauddin Makassar

Script ini memvalidasi apakah repositori memenuhi 4 pilar Reproducibility (Sub-CPMK 3.1):
1. Git Hygiene (.gitignore memblokir .env dan .venv)
2. 12-Factor Config (.env.example tersedia & bebas secret asli)
3. Standard Packaging (pyproject.toml terdefinisi)
4. Fresh Test Suite Execution (Unit test lulus 100%)
"""

import os
import sys
from pathlib import Path
import unittest

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def run_audit(root_dir: Path):
    print("=" * 80)
    print(" 🚀 AUDIT REPRODUCIBILITY & KETERLACAKAN REPOSITORI")
    print(f" Target Folder: {root_dir}")
    print("=" * 80)

    score = 0
    checks = []

    # -------------------------------------------------------------
    # 1. PERIKSA .gitignore
    # -------------------------------------------------------------
    gitignore_path = root_dir / ".gitignore"
    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding="utf-8")
        has_env = any(line.strip() == ".env" for line in content.splitlines())
        has_venv = any(".venv" in line for line in content.splitlines())
        if has_env and has_venv:
            checks.append(("PASS", ".gitignore memblokir .env dan .venv secara aman (+25 Poin)"))
            score += 25
        else:
            checks.append(("WARN", ".gitignore ada, tetapi belum lengkap memblokir .env atau .venv (+10 Poin)"))
            score += 10
    else:
        checks.append(("FAIL", "Berkas .gitignore TIDAK DITEMUKAN! (+0 Poin)"))

    # -------------------------------------------------------------
    # 2. PERIKSA .env.example
    # -------------------------------------------------------------
    env_example_path = root_dir / ".env.example"
    if env_example_path.exists():
        content = env_example_path.read_text(encoding="utf-8")
        # Pastikan tidak ada secret asli yang bocor
        dangerous = ["sk-live", "ghp_", "aws_secret_access_key"]
        if any(d in content.lower() for d in dangerous):
            checks.append(("FAIL", ".env.example terdeteksi membocorkan real API key/secret! (+0 Poin)"))
        else:
            checks.append(("PASS", ".env.example tersedia sebagai cetak biru publik tanpa secret (+25 Poin)"))
            score += 25
    else:
        checks.append(("FAIL", "Berkas .env.example TIDAK DITEMUKAN! (+0 Poin)"))

    # -------------------------------------------------------------
    # 3. PERIKSA pyproject.toml
    # -------------------------------------------------------------
    pyproject_path = root_dir / "pyproject.toml"
    if pyproject_path.exists():
        content = pyproject_path.read_text(encoding="utf-8")
        if "[project]" in content and "dependencies" in content:
            checks.append(("PASS", "pyproject.toml standar PEP 621 terdefinisi secara deklaratif (+25 Poin)"))
            score += 25
        else:
            checks.append(("WARN", "pyproject.toml ada tetapi bagian [project] kurang lengkap (+15 Poin)"))
            score += 15
    else:
        checks.append(("FAIL", "Berkas pyproject.toml TIDAK DITEMUKAN! (+0 Poin)"))

    # -------------------------------------------------------------
    # 4. EKSEKUSI TEST SUITE
    # -------------------------------------------------------------
    test_dir = root_dir / "tests"
    sys.path.insert(0, str(root_dir / "src"))
    loader = unittest.TestLoader()
    suite = loader.discover(str(test_dir), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)

    if result.wasSuccessful() and result.testsRun > 0:
        checks.append(("PASS", f"Automated test suite lulus 100% ({result.testsRun} test kasus) (+25 Poin)"))
        score += 25
    else:
        checks.append(("FAIL", f"Test suite gagal dieksekusi ({len(result.failures)} failures) (+0 Poin)"))

    # -------------------------------------------------------------
    # CETAK HASIL SKOR
    # -------------------------------------------------------------
    for status, msg in checks:
        icon = "🟢" if status == "PASS" else ("🟡" if status == "WARN" else "🔴")
        print(f" {icon} [{status}] {msg}")

    print("-" * 80)
    print(f" TOTAL SKOR REPRODUCIBILITY: {score} / 100")
    if score >= 90:
        print(" 🏆 PREDIKAT: SANGAT BAIK (A) - Siap Rilis Produksi & Lulus Audit!")
    elif score >= 75:
        print(" 🟡 PREDIKAT: BAIK (B) - Ada sedikit aspek konfigurasi yang perlu dirapikan.")
    else:
        print(" 🔴 PREDIKAT: KURANG (C/D) - Repositori belum memenuhi standar reproducibility.")
    print("=" * 80)


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    run_audit(project_root)
