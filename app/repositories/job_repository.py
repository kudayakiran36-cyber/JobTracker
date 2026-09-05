from sqlalchemy import or_
from app.models.job import Job
from app.models.application import Application

class JobRepository:
    def __init__(self, session): self.session = session
    def get(self, job_id): return self.session.get(Job, job_id)
    def list(self, search=None, status=None, favorite=None, include_deleted=False):
        q = self.session.query(Job).join(Application)
        if not include_deleted: q = q.filter(Application.deleted_at.is_(None))
        if status and status != "All": q = q.filter(Application.status == status)
        if favorite is True: q = q.filter(Application.is_favorite.is_(True))
        if search:
            s = f"%{search.strip()}%"
            q = q.filter(or_(Job.job_title.ilike(s), Job.company_name.ilike(s),
                             Job.location.ilike(s), Job.required_skills.ilike(s),
                             Job.preferred_skills.ilike(s), Job.job_type.ilike(s)))
        return q.order_by(Job.updated_at.desc()).all()
    def duplicate_candidates(self, company, title):
        return self.session.query(Job).filter(
            Job.company_name.ilike(company.strip()),
            Job.job_title.ilike(title.strip())
        ).all()
