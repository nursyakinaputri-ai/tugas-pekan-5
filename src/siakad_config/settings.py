"""
MODUL KONFIGURASI: 12-Factor App Configuration & Validation
Mata Kuliah: Pemrograman Lanjut (SIN442430) - UIN Alauddin Makassar

Menerapkan prinsip The Twelve-Factor App (Faktor III: Config in Environment).
Memvalidasi tipe data secara ketat dan memberikan jaminan Fail-Fast.
"""

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Optional


def load_env_file(filepath: str = ".env") -> None:
    """Helper sederhana untuk memuat berkas .env ke os.environ jika belum diset"""
    env_path = Path(filepath)
    if not env_path.exists():
        return

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip("'\"")
            # Hanya isi jika belum ada di environment sistem
            if key not in os.environ:
                os.environ[key] = val


@dataclass(frozen=True)
class AppSettings:
    """
    Kelas konfigurasi type-safe.
    Memvalidasi tipe data dan memastikan kredensial wajib tersedia (Fail-Fast).
    """

    app_env: str
    app_port: int
    debug: bool
    database_url: str
    payment_gateway_url: str
    payment_api_key: str
    wa_auth_token: str

    @classmethod
    def load_from_env(cls, env_file: str = ".env") -> "AppSettings":
        # 1. Muat berkas .env jika ada
        load_env_file(env_file)

        # 2. Ambil nilai dengan validasi tipe & fail-fast
        app_env = os.environ.get("APP_ENV", "development").lower()
        if app_env not in ["development", "staging", "production", "testing"]:
            raise ValueError(f"APP_ENV tidak valid: '{app_env}'. Harus development/staging/production/testing.")

        raw_port = os.environ.get("APP_PORT", "8000")
        try:
            app_port = int(raw_port)
            if not (1 <= app_port <= 65535):
                raise ValueError
        except ValueError:
            raise ValueError(f"APP_PORT harus berupa integer antara 1-65535, didapat: '{raw_port}'")

        raw_debug = os.environ.get("DEBUG", "true").lower()
        debug = raw_debug in ["true", "1", "yes"]

        # 3. Kredensial wajib (Fail-Fast: langsung crash jika kosong!)
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            raise ValueError("Konfigurasi Wajib Hilang: 'DATABASE_URL' belum diset di environment / .env!")

        payment_gateway_url = os.environ.get("PAYMENT_GATEWAY_URL", "https://sandbox.bank.uinam.ac.id/api/v1")

        payment_api_key = os.environ.get("PAYMENT_API_KEY")
        if not payment_api_key:
            raise ValueError("Konfigurasi Wajib Hilang: 'PAYMENT_API_KEY' belum diset di environment / .env!")

        wa_auth_token = os.environ.get("WA_AUTH_TOKEN", "default_dummy_token")

        return cls(
            app_env=app_env,
            app_port=app_port,
            debug=debug,
            database_url=database_url,
            payment_gateway_url=payment_gateway_url,
            payment_api_key=payment_api_key,
            wa_auth_token=wa_auth_token,
        )
