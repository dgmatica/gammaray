import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

LOG_PATH = PROJECT_DIR / "data" / "data" / "djangologs" / "access.log"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://gammaray:gammaray@localhost:5432/gammaray",
)
