import json, shutil, zipfile, tempfile
from datetime import datetime
from pathlib import Path
from app.core.config import DB_PATH, RESUMES_DIR, BACKUPS_DIR
from app.core.constants import APP_VERSION, SCHEMA_VERSION
from app.core.exceptions import BackupError

class BackupService:
    def create(self, destination=None):
        BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
        destination = Path(destination) if destination else BACKUPS_DIR / f"JobTracker_{datetime.now():%Y%m%d_%H%M%S}.jtb"
        with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as z:
            if DB_PATH.exists(): z.write(DB_PATH, "jobtracker.db")
            for p in RESUMES_DIR.rglob("*"):
                if p.is_file(): z.write(p, str(Path("Resumes") / p.relative_to(RESUMES_DIR)))
            z.writestr("metadata.json", json.dumps({
                "application_version": APP_VERSION,
                "schema_version": SCHEMA_VERSION,
                "created_at": datetime.now().isoformat()
            }, indent=2))
        return destination
    def restore(self, backup_path):
        backup_path = Path(backup_path)
        if not zipfile.is_zipfile(backup_path): raise BackupError("Invalid .jtb backup.")
        with zipfile.ZipFile(backup_path) as z:
            names = set(z.namelist())
            if "jobtracker.db" not in names or "metadata.json" not in names:
                raise BackupError("Backup is missing required files.")
            temp = Path(tempfile.mkdtemp(prefix="jobtracker_restore_"))
            z.extractall(temp)
        safety = self.create()
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(temp / "jobtracker.db", DB_PATH)
        if RESUMES_DIR.exists(): shutil.rmtree(RESUMES_DIR)
        shutil.copytree(temp / "Resumes", RESUMES_DIR, dirs_exist_ok=True) if (temp / "Resumes").exists() else RESUMES_DIR.mkdir(parents=True)
        shutil.rmtree(temp, ignore_errors=True)
        return safety
