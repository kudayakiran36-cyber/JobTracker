from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QListWidget,QPushButton,QMessageBox,QGroupBox
from app.repositories.application_repository import ApplicationRepository
from app.services.gmail_service import GmailService
from app.services.application_service import ApplicationService
from app.ui.widgets.email_card import EmailCardItem
class UpdateCenterPage(QWidget):
    def __init__(self,window):
        super().__init__(); self.window=window; self.selected=[]; self.gmail_rows=[]
        l=QVBoxLayout(self); l.addWidget(QLabel("<h2>Update Center</h2>"))
        l.addWidget(QLabel("Select Applied jobs to process. Gmail matching is manual."))
        self.jobs=QListWidget(); self.jobs.setSelectionMode(QListWidget.MultiSelection); l.addWidget(self.jobs)
        row=QHBoxLayout()
        for t,fn in [("Load Applied",self.load_jobs),("Check Gmail",self.check_gmail),("Mark No Update",self.no_update),("Link Selected Email",self.link_selected)]:
            b=QPushButton(t); b.clicked.connect(fn); row.addWidget(b)
        l.addLayout(row)
        self.emails=QListWidget(); l.addWidget(self.emails)
        self.load_jobs()
    def add_application(self,app):
        if app.application_id not in [a.application_id for a in self.selected]: self.selected.append(app)
        self.load_jobs()
    def load_jobs(self):
        self.jobs.clear()
        due=ApplicationRepository(self.window.session).due_update_candidates()
        seen=set()
        for a in self.selected+due:
            if a.application_id not in seen:
                seen.add(a.application_id); item=__import__("PySide6.QtWidgets",fromlist=["QListWidgetItem"]).QListWidgetItem(f"{a.job.company_name} — {a.job.job_title}")
                item.app=a; self.jobs.addItem(item)
    def check_gmail(self):
        from pathlib import Path
        cred=Path("credentials.json"); token=Path("token.json")
        if not cred.exists():
            QMessageBox.information(self,"Gmail setup","Place your Gmail OAuth desktop credentials as credentials.json beside the application, then run Check Gmail again."); return
        try:
            from app.gmail.authentication import authorize
            from app.gmail.client import GmailClient
            rows=GmailClient(authorize(cred,token)).list_messages()
            self.gmail_rows=GmailService(self.window.session).import_messages(rows)
            self.emails.clear()
            for e in GmailService(self.window.session).emails()[:200]: self.emails.addItem(EmailCardItem(e))
            QMessageBox.information(self,"Gmail","Gmail messages loaded. Select a job and an email, then Link Selected Email.")
        except Exception as e: QMessageBox.critical(self,"Gmail error",str(e))
    def current_app(self):
        item=self.jobs.currentItem(); return getattr(item,"app",None) if item else None
    def link_selected(self):
        app=self.current_app(); item=self.emails.currentItem()
        if not app or not item: QMessageBox.warning(self,"Select","Select one job and one email."); return
        GmailService(self.window.session).link(app,item.email)
        ApplicationService(self.window.session).mark_gmail_checked(app,1)
        self.load_jobs(); self.emails.takeItem(self.emails.row(item))
    def no_update(self):
        app=self.current_app()
        if not app: return
        ApplicationService(self.window.session).mark_gmail_checked(app,0)
        self.jobs.takeItem(self.jobs.currentRow())
