from pathlib import Path
from platformdirs import user_data_dir
from app.core.constants import APP_NAME

BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "jobtracker.db"
RESUMES_DIR = DATA_DIR / "Resumes"
BACKUPS_DIR = DATA_DIR / "Backups"

# For a packaged executable, keep data beside the executable when possible.
def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESUMES_DIR.mkdir(parents=True, exist_ok=True)
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
