from datetime import datetime, timedelta
from app.core.constants import STATUSES, ALLOWED_TRANSITIONS, APPLICATION_DATE_TYPES, RECYCLE_BIN_HOURS
from app.core.exceptions import TransitionError
from app.services.history_service import HistoryService

class ApplicationService:
    def __init__(self, session): self.session = session
    def change_status(self, app, new_status, application_date=None, application_date_type=None):
        if new_status not in STATUSES: raise TransitionError("Invalid status.")
        if new_status != app.status and new_status not in ALLOWED_TRANSITIONS.get(app.status, set()):
            raise TransitionError(f"{app.status} → {new_status} is not allowed.")
        old = app.status
        now = datetime.now()
        app.status = new_status
        if new_status == "Applied":
            app.application_date = application_date or now.date()
            app.application_date_type = application_date_type or "Exact"
            app.last_application_update_at = now
            app.interested_since = None
        elif old == "Applied" and new_status == "Interested":
            app.application_date = None
            app.application_date_type = None
            app.interested_since = now
        elif new_status == "Interested":
            app.interested_since = now
        else:
            app.interested_since = None
        HistoryService(self.session).record(app.application_id, "STATUS_CHANGED",
            f"Status changed from {old} to {new_status}.", old, new_status)
        self.session.commit()
    def set_favorite(self, app, value):
        old = app.is_favorite
        app.is_favorite = bool(value)
        if old != app.is_favorite:
            HistoryService(self.session).record(app.application_id, "FAVORITE_CHANGED",
                f"Favorite {'enabled' if value else 'disabled'}.", str(old), str(value))
        self.session.commit()
    def mark_visited(self, app):
        app.last_visited_at = datetime.now()
        self.session.commit()
    def mark_gmail_checked(self, app, found_count=0):
        now = datetime.now()
        app.last_checked_at = now
        if found_count:
            app.last_application_update_at = now
        HistoryService(self.session).record(
            app.application_id, "GMAIL_CHECKED",
            f"Gmail checked; {found_count} relevant email(s) linked." if found_count else "Gmail checked; no update marked.",
            event_date=now
        )
        self.session.commit()
    def update_notes(self, app, notes):
        old = app.personal_notes
        app.personal_notes = notes
        if old != notes:
            HistoryService(self.session).record(app.application_id, "NOTES_UPDATED", "Personal notes updated.", old, notes)
        self.session.commit()
    def soft_delete(self, app):
        now = datetime.now()
        app.deleted_at = now
        app.delete_expires_at = now + timedelta(hours=RECYCLE_BIN_HOURS)
        HistoryService(self.session).record(app.application_id, "DELETED", "Application moved to Recycle Bin.")
        self.session.commit()
    def restore(self, app):
        app.deleted_at = None
        app.delete_expires_at = None
        HistoryService(self.session).record(app.application_id, "RESTORED", "Application restored from Recycle Bin.")
        self.session.commit()
    def purge_expired(self):
        now = datetime.now()
        rows = self.session.query(type(self.session.query)).all() if False else []
        from app.models.application import Application
        expired = self.session.query(Application).filter(Application.delete_expires_at.is_not(None), Application.delete_expires_at <= now).all()
        for app in expired: self.session.delete(app)
        if expired: self.session.commit()
        return len(expired)
