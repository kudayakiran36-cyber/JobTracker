import json
from datetime import datetime
from app.models.job import Job
from app.models.application import Application
from app.services.history_service import HistoryService

JOB_FIELDS = [
    "job_title","company_name","job_url","location","work_arrangement","salary",
    "job_description","required_skills","preferred_skills","experience_required",
    "job_type","deadline"
]

class JobService:
    def __init__(self, session): self.session = session
    def duplicates(self, company, title):
        from app.repositories.job_repository import JobRepository
        return JobRepository(self.session).duplicate_candidates(company, title)
    def create(self, data, status="Interested", application_date=None, application_date_type=None, resume_id=None):
        job = Job()
        for f in JOB_FIELDS:
            value = data.get(f)
            if f in ("required_skills","preferred_skills") and isinstance(value, list):
                value = json.dumps(value, ensure_ascii=False)
            setattr(job, f, value)
        self.session.add(job)
        self.session.flush()
        now = datetime.now()
        app = Application(
            job_id=job.job_id, status=status,
            application_date=application_date if status == "Applied" else None,
            application_date_type=application_date_type if status == "Applied" else None,
            resume_id=resume_id, interested_since=now if status == "Interested" else None
        )
        self.session.add(app)
        self.session.flush()
        HistoryService(self.session).record(app.application_id, "CREATED", "Job/application created.", new_value=status)
        self.session.commit()
        return app
    def update_job(self, job, data, app):
        changes = []
        for f in JOB_FIELDS:
            if f not in data:
                continue
            new = data.get(f)
            if f in ("required_skills","preferred_skills") and isinstance(new, list):
                new = json.dumps(new, ensure_ascii=False)
            old = getattr(job, f)
            if old != new:
                setattr(job, f, new)
                changes.append((f, old, new))
        if changes:
            for f, old, new in changes:
                HistoryService(self.session).record(
                    app.application_id, "JOB_UPDATED", f"Job field changed: {f}.",
                    None if old is None else str(old), None if new is None else str(new)
                )
            self.session.commit()
        return changes
