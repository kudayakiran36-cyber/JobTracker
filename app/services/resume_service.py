from pathlib import Path
import shutil
from app.core.config import RESUMES_DIR
from app.models.resume import Resume

class ResumeService:
    def __init__(self, session): self.session = session
    def add(self, source_path, target_role=None, skills=None, experience=None, projects=None):
        src = Path(source_path)
        if not src.exists(): raise FileNotFoundError(src)
        RESUMES_DIR.mkdir(parents=True, exist_ok=True)
        dest = RESUMES_DIR / src.name
        if dest.exists():
            stem, suffix = src.stem, src.suffix
            i = 2
            while (RESUMES_DIR / f"{stem}_{i}{suffix}").exists(): i += 1
            dest = RESUMES_DIR / f"{stem}_{i}{suffix}"
        shutil.copy2(src, dest)
        rel = dest.relative_to(RESUMES_DIR.parent.parent).as_posix()
        row = Resume(file_name=dest.name, file_path=rel, target_role=target_role,
                     skills_emphasized=skills, experience_emphasis=experience, projects_included=projects)
        self.session.add(row); self.session.commit()
        return row
    def all(self): return self.session.query(Resume).order_by(Resume.date_added.desc()).all()
