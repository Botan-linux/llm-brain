"""
LLM-Brain Logging Module

Merkezi log yapılandırması. Tüm core modülleri bu modülü kullanmalıdır.
Kullanım:
    from core.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Bilgi mesajı")
    logger.warning("Uyarı mesajı")
    logger.error("Hata mesajı")
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler


# ANSI renk kodları
class ColorFormatter(logging.Formatter):
    """Renkli konsol çıktısı için formatter."""

    COLORS = {
        logging.DEBUG: "\033[90m",       # Gri
        logging.INFO: "\033[92m",         # Yeşil
        logging.WARNING: "\033[93m",      # Sarı
        logging.ERROR: "\033[91m",        # Kırmızı
        logging.CRITICAL: "\033[91m\033[1m",  # Kalın kırmızı
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        record.levelname = f"{color}{record.levelname:<8}{self.RESET}"
        return super().format(record)


# Log dizini
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOG_DIR = os.path.join(_PROJECT_ROOT, "storage", "logs")

# Global flag: logger zaten başlatıldı mı?
_initialized = False


def _ensure_log_dir():
    """Log dizinini oluştur."""
    if not os.path.exists(_LOG_DIR):
        os.makedirs(_LOG_DIR, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """
    Yapılandırılmış logger döndür.

    Args:
        name: Modül adı (genellikle __name__)

    Returns:
        logging.Logger: Yapılandırılmış logger
    """
    global _initialized

    logger = logging.getLogger(name)

    # Root logger'ı sadece bir kere yapılandır
    if not _initialized:
        _ensure_log_dir()

        root = logging.getLogger("core")
        root.setLevel(logging.DEBUG)

        # Konsol handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_fmt = ColorFormatter(
            fmt="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_fmt)
        root.addHandler(console_handler)

        # Dosya handler (rotating)
        file_handler = RotatingFileHandler(
            os.path.join(_LOG_DIR, "ilk.log"),
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=3,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_fmt = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)-8s %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_fmt)
        root.addHandler(file_handler)

        _initialized = True

    return logger
