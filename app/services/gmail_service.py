from datetime import datetime
from app.models.gmail_email import GmailEmail
from app.models.email_link import ApplicationEmailLink
from app.services.history_service import HistoryService

class GmailService:
    def __init__(self, session): self.session = session
    def import_messages(self, messages):
        new = []
        for m in messages:
            row = self.session.query(GmailEmail).filter_by(gmail_message_id=m["gmail_message_id"]).first()
            if not row:
                row = GmailEmail(**m, first_seen_at=datetime.now())
                self.session.add(row); self.session.flush(); new.append(row)
        self.session.commit()
        return new
    def link(self, app, email, link_type="Manual"):
        exists = self.session.query(ApplicationEmailLink).filter_by(application_id=app.application_id, email_id=email.email_id).first()
        if not exists:
            self.session.add(ApplicationEmailLink(application_id=app.application_id, email_id=email.email_id, link_type=link_type))
            HistoryService(self.session).record(app.application_id, "EMAIL_LINKED",
                f"Linked Gmail email: {email.subject or '(no subject)'}.",
                new_value=str(email.email_id), event_date=email.received_at or datetime.now())
            self.session.commit()
    def emails(self):
        return self.session.query(GmailEmail).order_by(GmailEmail.received_at.desc()).all()
