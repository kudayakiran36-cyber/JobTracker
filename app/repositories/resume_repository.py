from app.models.resume import Resume
class ResumeRepository:
    def __init__(self, session): self.session = session
    def all(self): return self.session.query(Resume).order_by(Resume.date_added.desc()).all()
    def get(self, resume_id): return self.session.get(Resume, resume_id)
