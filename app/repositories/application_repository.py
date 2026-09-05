from datetime import datetime
from app.models.application import Application

class ApplicationRepository:
    def __init__(self, session): self.session = session
    def get(self, application_id): return self.session.get(Application, application_id)
    def active(self): return self.session.query(Application).filter(Application.deleted_at.is_(None)).all()
    def due_update_candidates(self): return [a for a in self.active() if a.status == "Applied"]
    def recently_visited(self, cutoff):
        return self.session.query(Application).filter(
            Application.deleted_at.is_(None),
            Application.last_visited_at.is_not(None),
            Application.last_visited_at >= cutoff
        ).order_by(Application.last_visited_at.desc()).limit(5).all()
    def deleted(self):
        return self.session.query(Application).filter(Application.deleted_at.is_not(None)).order_by(Application.delete_expires_at).all()
