from datetime import datetime,timedelta,date
from app.reminders.reminder_engine import ReminderEngine
class Job: pass
class App: pass
def make(status="Interested",deadline=None,created=None,checked=None):
    j=Job(); j.company_name="Acme"; j.job_title="Dev"; j.deadline=deadline
    a=App(); a.job=j; a.status=status; a.created_at=created or datetime.now(); a.interested_since=a.created_at; a.last_checked_at=checked
    a.last_application_update_at=None; a.application_date=None; a.deleted_at=None
    return a
class S:
    def get(self,k,d=None): return {"applied_reminder_days":"3","interested_first_reminder_days":"5","interested_second_reminder_days":"8","deadline_reminder_days":"3","deadline_rejection_days":"3"}.get(k,d)
def test_interested_first():
    base=datetime.now()-timedelta(days=5)
    assert ReminderEngine(None,S()).reminders_for(make(created=base))
def test_applied():
    base=datetime.now()-timedelta(days=3)
    assert ReminderEngine(None,S()).reminders_for(make("Applied",created=base,checked=base))
