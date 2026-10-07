"""
UNIT TEST: Validasi Konfigurasi 12-Factor & Logika Billing
Mata Kuliah: Pemrograman Lanjut (SIN442430) - UIN Alauddin Makassar
"""

import os
import sys
from pathlib import Path
import unittest

# Tambahkan src ke path
src_dir = Path(__file__).resolve().parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from siakad_config.settings import AppSettings
from siakad_billing.billing_core import BillingManager


class TestConfigAndBilling(unittest.TestCase):
    def setUp(self):
        # Bersihkan environment sebelum setiap test
        self.original_env = dict(os.environ)

    def tearDown(self):
        # Kembalikan environment semula
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_load_valid_settings(self):
        """Uji pembacaan konfigurasi valid dari environment"""
        os.environ["APP_ENV"] = "production"
        os.environ["APP_PORT"] = "9000"
        os.environ["DEBUG"] = "false"
        os.environ["DATABASE_URL"] = "postgresql://user:pass@localhost/db"
        os.environ["PAYMENT_API_KEY"] = "prod_secret_token_123"

        config = AppSettings.load_from_env()

        self.assertEqual(config.app_env, "production")
        self.assertEqual(config.app_port, 9000)
        self.assertFalse(config.debug)
        self.assertEqual(config.database_url, "postgresql://user:pass@localhost/db")
        self.assertEqual(config.payment_api_key, "prod_secret_token_123")

    def test_fail_fast_on_missing_database_url(self):
        """Uji sifat Fail-Fast jika DATABASE_URL tidak diset"""
        os.environ.pop("DATABASE_URL", None)
        os.environ["PAYMENT_API_KEY"] = "token_abc"

        with self.assertRaises(ValueError) as ctx:
            AppSettings.load_from_env()

        self.assertIn("DATABASE_URL", str(ctx.exception))

    def test_fail_fast_on_invalid_port(self):
        """Uji sifat Fail-Fast jika port bukan integer valid"""
        os.environ["APP_PORT"] = "bukan_angka"
        os.environ["DATABASE_URL"] = "sqlite:///test.db"
        os.environ["PAYMENT_API_KEY"] = "token_abc"

        with self.assertRaises(ValueError) as ctx:
            AppSettings.load_from_env()

        self.assertIn("APP_PORT", str(ctx.exception))

    def test_billing_manager_with_injected_settings(self):
        """Uji BillingManager menggunakan konfigurasi yang diinjeksikan secara agnostik"""
        settings = AppSettings(
            app_env="testing",
            app_port=8080,
            debug=True,
            database_url="sqlite:///:memory:",
            payment_gateway_url="https://mock-bank.local",
            payment_api_key="mock_key",
            wa_auth_token="mock_wa",
        )

        manager = BillingManager(settings=settings)
        transaksi = manager.proses_pembayaran("60200122001", 3500000.0)

        self.assertEqual(transaksi.nim, "60200122001")
        self.assertEqual(transaksi.nominal, 3500000.0)
        self.assertEqual(transaksi.status, "SUCCESS")
        self.assertEqual(transaksi.gateway_url, "https://mock-bank.local/charges")

    def test_billing_manager_rejects_negative_nominal(self):
        """Uji validasi nominal negatif"""
        settings = AppSettings(
            app_env="testing",
            app_port=8080,
            debug=True,
            database_url="sqlite:///:memory:",
            payment_gateway_url="https://mock-bank.local",
            payment_api_key="mock_key",
            wa_auth_token="mock_wa",
        )

        manager = BillingManager(settings=settings)
        with self.assertRaises(ValueError) as ctx:
            manager.proses_pembayaran("60200122001", -50000.0)

        self.assertIn("lebih besar dari 0", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
