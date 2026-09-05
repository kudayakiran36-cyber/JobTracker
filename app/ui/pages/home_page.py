from datetime import datetime, timedelta
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QLabel,QGroupBox,QScrollArea
from app.reminders.reminder_engine import ReminderEngine
from app.repositories.settings_repository import SettingsRepository
from app.repositories.application_repository import ApplicationRepository

class HomePage(QWidget):
    def __init__(self, window):
        super().__init__(); self.window=window
        self.layout=QVBoxLayout(self)
        title=QLabel("<h1>Job Tracker</h1>"); self.layout.addWidget(title)
        row=QHBoxLayout()
        for text, fn in [("Add New Job", window.show_add),("View / Search Jobs", window.show_jobs),("Update Center", window.show_update)]:
            b=QPushButton(text); b.setMinimumHeight(55); b.clicked.connect(fn); row.addWidget(b)
        self.layout.addLayout(row)
        self.reminders_box=QGroupBox("Reminders"); self.reminders_layout=QVBoxLayout(self.reminders_box); self.layout.addWidget(self.reminders_box)
        self.recent_box=QGroupBox("Recently Visited"); self.recent_layout=QVBoxLayout(self.recent_box); self.layout.addWidget(self.recent_box)
        self.refresh()
    def refresh(self):
        while self.reminders_layout.count(): self.reminders_layout.takeAt(0).widget().deleteLater()
        while self.recent_layout.count(): self.recent_layout.takeAt(0).widget().deleteLater()
        engine=ReminderEngine(self.window.session, SettingsRepository(self.window.session))
        reminders=engine.all_reminders()
        for r in reminders[:8]:
            b=QPushButton(r.message); b.clicked.connect(lambda _,a=r.app:self.window.show_detail(a.application_id)); self.reminders_layout.addWidget(b)
        if not reminders: self.reminders_layout.addWidget(QLabel("No reminders due."))
        cutoff=datetime.now()-timedelta(hours=72)
        recent=ApplicationRepository(self.window.session).recently_visited(cutoff)
        for a in recent:
            b=QPushButton(f"{a.job.company_name} — {a.job.job_title}"); b.clicked.connect(lambda _,x=a:self.window.show_detail(x.application_id)); self.recent_layout.addWidget(b)
        if not recent: self.recent_layout.addWidget(QLabel("No recently visited jobs."))
