from datetime import datetime
from app.models.history import History

class HistoryService:
    def __init__(self, session): self.session = session
    def record(self, application_id, event_type, description, old_value=None, new_value=None, event_date=None):
        self.session.add(History(
            application_id=application_id, event_type=event_type,
            event_description=description, old_value=old_value,
            new_value=new_value, event_date=event_date or datetime.now()
        ))
