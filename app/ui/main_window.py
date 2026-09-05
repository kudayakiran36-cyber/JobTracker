import sys
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QApplication,QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QPushButton,QStackedWidget,QLabel,QProgressBar,QMessageBox
from app.database.connection import init_db, SessionLocal
from app.services.application_service import ApplicationService
from app.reminders.reminder_engine import ReminderEngine
from app.repositories.settings_repository import SettingsRepository
from app.ui.themes.theme_manager import ThemeManager

class Loading(QWidget):
    def __init__(self,done):
        super().__init__(); l=QVBoxLayout(self); l.setAlignment(Qt.AlignCenter)
        l.addWidget(QLabel("<h1>Job Tracker</h1>")); l.addWidget(QLabel("Loading..."))
        bar=QProgressBar(); bar.setRange(0,0); l.addWidget(bar)
        QTimer.singleShot(500,done)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle("Job Tracker"); self.resize(1200,800)
        self.session=SessionLocal()
        ApplicationService(self.session).purge_expired()
        ReminderEngine(self.session,SettingsRepository(self.session)).auto_reject_expired()
        self.stack=QStackedWidget()
        self.sidebar=QVBoxLayout(); self.sidebar_widget=QWidget(); self.sidebar_widget.setLayout(self.sidebar)
        container=QWidget(); lay=QHBoxLayout(container); lay.addWidget(self.sidebar_widget,1); lay.addWidget(self.stack,5); self.setCentralWidget(container)
        from app.ui.pages.home_page import HomePage
        from app.ui.pages.add_job_page import AddJobPage
        from app.ui.pages.review_job_page import ReviewJobPage
        from app.ui.pages.jobs_page import JobsPage
        from app.ui.pages.job_detail_page import JobDetailPage
        from app.ui.pages.update_center_page import UpdateCenterPage
        from app.ui.pages.settings_page import SettingsPage
        from app.ui.pages.recycle_bin_page import RecycleBinPage
        from app.ui.pages.favorites_page import FavoritesPage
        from app.ui.pages.resumes_page import ResumesPage
        self.home=HomePage(self); self.add=AddJobPage(self); self.review=ReviewJobPage(self); self.jobs=JobsPage(self)
        self.detail=JobDetailPage(self); self.update_center=UpdateCenterPage(self); self.settings=SettingsPage(self)
        self.recycle=RecycleBinPage(self); self.favorites=FavoritesPage(self); self.resumes=ResumesPage(self)
        for name,w in [("Home",self.home),("Add Job",self.add),("Jobs",self.jobs),("Update Center",self.update_center),("Favorites",self.favorites),("Recycle Bin",self.recycle),("Resumes",self.resumes),("Settings",self.settings)]:
            b=QPushButton(name); b.clicked.connect(lambda _,x=w:self.stack.setCurrentWidget(x)); self.sidebar.addWidget(b)
        self.sidebar.addStretch()
        for w in [self.home,self.add,self.review,self.jobs,self.detail,self.update_center,self.settings,self.recycle,self.favorites,self.resumes]: self.stack.addWidget(w)
        self.stack.setCurrentWidget(self.home)
    def clipboard(self): return QApplication.clipboard()
    def show_add(self): self.stack.setCurrentWidget(self.add)
    def show_review(self,data): self.review.load(data); self.stack.setCurrentWidget(self.review)
    def show_jobs(self): self.jobs.refresh(); self.stack.setCurrentWidget(self.jobs)
    def show_detail(self,application_id):
        app=self.session.get(__import__("app.models.application",fromlist=["Application"]).Application,application_id)
        if app: self.detail.load(app); self.stack.setCurrentWidget(self.detail)
    def show_update(self,application_id=None):
        if application_id:
            app=self.session.get(__import__("app.models.application",fromlist=["Application"]).Application,application_id)
            if app:self.update_center.add_application(app)
        self.update_center.load_jobs(); self.stack.setCurrentWidget(self.update_center)
    def show_resumes(self): self.resumes.refresh(); self.stack.setCurrentWidget(self.resumes)
    def closeEvent(self,e):
        self.session.close(); e.accept()

def run():
    app=QApplication(sys.argv); ThemeManager.apply(app)
    init_db()
    win=None
    def launch():
        nonlocal win
        win=MainWindow(); win.show()
    loading=Loading(launch); loading.show()
    sys.exit(app.exec())
