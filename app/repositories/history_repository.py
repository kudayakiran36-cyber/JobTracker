from app.models.history import History
class HistoryRepository:
    def __init__(self, session): self.session = session
    def for_application(self, application_id):
        return self.session.query(History).filter_by(application_id=application_id).order_by(History.event_date.desc()).all()
