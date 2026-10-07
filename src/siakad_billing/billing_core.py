"""
MODUL DOMAIN & APLIKASI: SIAKAD Billing Core
Mata Kuliah: Pemrograman Lanjut (SIN442430) - UIN Alauddin Makassar

Menerima injeksi konfigurasi AppSettings sehingga dapat beroperasi di lingkungan
Local, Staging, maupun Production tanpa mengubah satu baris kode pun.
"""

from dataclasses import dataclass
from typing import Dict, Optional
import sys
from pathlib import Path

# Impor konfigurasi
from siakad_config.settings import AppSettings


@dataclass
class PembayaranUKT:
    nim: str
    nominal: float
    status: str
    gateway_url: str


class BillingManager:
    """Manajer billing yang mengandalkan konfigurasi 12-Factor terinjeksi"""

    def __init__(self, settings: AppSettings):
        self.settings = settings

    def proses_pembayaran(self, nim: str, nominal: float) -> PembayaranUKT:
        if nominal <= 0:
            raise ValueError("Nominal pembayaran harus lebih besar dari 0!")

        # Menghubungkan ke gateway pembayaran yang dikonfigurasi via environment
        gateway_endpoint = f"{self.settings.payment_gateway_url}/charges"

        return PembayaranUKT(
            nim=nim,
            nominal=nominal,
            status="SUCCESS",
            gateway_url=gateway_endpoint,
        )

    def status_lingkungan(self) -> str:
        return (
            f"Sistem berjalan di lingkungan [{self.settings.app_env.upper()}] "
            f"pada port {self.settings.app_port} (Debug: {self.settings.debug})"
        )
