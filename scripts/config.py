from pathlib import Path

# ==========================
# Project Paths
# ==========================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
LOG_DIR = DATA_DIR / "logs"

for folder in [RAW_DIR, PROCESSED_DIR, LOG_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# ==========================
# Download Configuration
# ==========================

START_DATE = "2026-06-25"
END_DATE = "2026-07-01"

CONNECT_TIMEOUT = 5
READ_TIMEOUT = 15

MAX_RETRIES = 3

REQUEST_DELAY = 0.5