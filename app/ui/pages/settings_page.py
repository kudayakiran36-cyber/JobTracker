from PySide6.QtWidgets import QWidget,QVBoxLayout,QFormLayout,QSpinBox,QPushButton,QLabel,QFileDialog,QMessageBox,QListWidget
from app.repositories.settings_repository import SettingsRepository
from app.services.backup_service import BackupService
from app.services.resume_service import ResumeService
from app.core.config import BACKUPS_DIR
class SettingsPage(QWidget):
    def __init__(self,window):
        super().__init__(); self.window=window
        l=QVBoxLayout(self); l.addWidget(QLabel("<h2>Settings</h2>"))
        form=QFormLayout(); self.spins={}
        labels=[("applied_reminder_days","Applied update reminder (days)"),
                ("interested_first_reminder_days","Interested first reminder (days)"),
                ("interested_second_reminder_days","Interested second reminder (days)"),
                ("deadline_reminder_days","Deadline reminder (days before)"),
                ("deadline_rejection_days","Deadline auto-reject (days after)")]
        repo=SettingsRepository(window.session)
        for k,label in labels:
            s=QSpinBox(); s.setRange(0,3650); s.setValue(int(repo.get(k,3))); self.spins[k]=s; form.addRow(label,s)
        save=QPushButton("Save Reminder Settings"); save.clicked.connect(self.save); l.addLayout(form); l.addWidget(save)
        backup=QPushButton("Create Backup (.jtb)"); backup.clicked.connect(self.backup); l.addWidget(backup)
        restore=QPushButton("Restore Backup"); restore.clicked.connect(self.restore); l.addWidget(restore)
        resumes=QPushButton("Resume Library"); resumes.clicked.connect(window.show_resumes); l.addWidget(resumes)
        l.addWidget(QLabel("Fixed lifecycle values: Recently Visited = 72 hours; Recycle Bin = 24 hours."))
    def save(self):
        repo=SettingsRepository(self.window.session)
        for k,s in self.spins.items(): repo.set(k,s.value())
        self.window.session.commit(); QMessageBox.information(self,"Saved","Settings updated.")
        self.window.home.refresh()
    def backup(self):
        p=QFileDialog.getSaveFileName(self,"Create Backup",str(BACKUPS_DIR/"JobTracker.jtb"),"Job Tracker Backup (*.jtb)")[0]
        if p:
            try: BackupService().create(p); QMessageBox.information(self,"Backup created",p)
            except Exception as e: QMessageBox.critical(self,"Backup error",str(e))
    def restore(self):
        p=QFileDialog.getOpenFileName(self,"Restore Backup","","Job Tracker Backup (*.jtb)")[0]
        if p:
            try: BackupService().restore(p); QMessageBox.information(self,"Restored","Backup restored. Restart the application.")
            except Exception as e: QMessageBox.critical(self,"Restore error",str(e))
