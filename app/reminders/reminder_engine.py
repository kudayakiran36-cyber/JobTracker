from datetime import datetime, timedelta

class Reminder:
    def __init__(self, app, kind, message, priority=1):
        self.app = app; self.kind = kind; self.message = message; self.priority = priority

class ReminderEngine:
    def __init__(self, session, settings):
        self.session = session
        self.settings = settings
    def _int(self, key, default):
        try: return max(0, int(self.settings.get(key, default)))
        except (TypeError, ValueError): return default
    def reminders_for(self, app, now=None):
        now = now or datetime.now()
        job = app.job
        out = []
        if app.deleted_at: return out
        if app.status == "Applied":
            days = self._int("applied_reminder_days", 3)
            base = app.last_checked_at or app.last_application_update_at or (
                datetime.combine(app.application_date, datetime.min.time()) if app.application_date else app.created_at
            )
            if now >= base + timedelta(days=days):
                out.append(Reminder(app, "APPLIED_UPDATE", f"{job.company_name} — {job.job_title}: application update check is due."))
        elif app.status == "Interested":
            if job.deadline:
                deadline = datetime.combine(job.deadline, datetime.min.time())
                days_before = self._int("deadline_reminder_days", 3)
                if deadline - timedelta(days=days_before) <= now <= deadline + timedelta(days=self._int("deadline_rejection_days", 3)):
                    if now <= deadline:
                        out.append(Reminder(app, "DEADLINE", f"{job.company_name} — {job.job_title}: deadline is approaching ({job.deadline})."))
                    else:
                        elapsed = (now.date() - job.deadline).days
                        if elapsed >= self._int("deadline_rejection_days", 3):
                            out.append(Reminder(app, "OVERDUE", f"{job.company_name} — {job.job_title}: deadline passed; automatic rejection is due."))
            else:
                base = app.interested_since or app.created_at
                first = self._int("interested_first_reminder_days", 5)
                second = self._int("interested_second_reminder_days", 8)
                age = (now - base).days
                if age >= second:
                    out.append(Reminder(app, "INTERESTED_SECOND", f"{job.company_name} — {job.job_title}: still Interested after {second} days."))
                elif age >= first:
                    out.append(Reminder(app, "INTERESTED_FIRST", f"{job.company_name} — {job.job_title}: still Interested after {first} days."))
        return out
    def all_reminders(self):
        result = []
        from app.models.application import Application
        apps = self.session.query(Application).filter(Application.deleted_at.is_(None)).all()
        for app in apps: result.extend(self.reminders_for(app))
        return sorted(result, key=lambda x: x.priority)
    def auto_reject_expired(self):
        from app.models.application import Application
        from app.services.application_service import ApplicationService
        now = datetime.now()
        changed = 0
        apps = self.session.query(Application).filter(Application.deleted_at.is_(None), Application.status == "Interested").all()
        days = self._int("deadline_rejection_days", 3)
        for app in apps:
            if app.job.deadline and (now.date() - app.job.deadline).days >= days:
                ApplicationService(self.session).change_status(app, "Rejected")
                changed += 1
        return changed
