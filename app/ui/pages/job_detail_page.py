import json
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QFormLayout,QLabel,QLineEdit,QPlainTextEdit,QPushButton,QComboBox,QMessageBox,QCheckBox
from app.repositories.history_repository import HistoryRepository
from app.services.application_service import ApplicationService
from app.services.job_service import JobService
from app.ui.widgets.history_timeline import HistoryTimeline
class JobDetailPage(QWidget):
    def __init__(self,window):
        super().__init__(); self.window=window; self.app=None
        self.layout=QVBoxLayout(self); self.form=QFormLayout(); self.fields={}
        for key,label in [("job_title","Job Title"),("company_name","Company"),("job_url","URL"),("location","Location"),("work_arrangement","Work Arrangement"),("salary","Salary"),("experience_required","Experience"),("job_type","Job Type"),("deadline","Deadline")]:
            w=QLineEdit(); self.fields[key]=w; self.form.addRow(label,w)
        self.desc=QPlainTextEdit(); self.form.addRow("Description",self.desc)
        self.notes=QPlainTextEdit(); self.form.addRow("Personal Notes",self.notes)
        self.status=QComboBox(); self.status.addItems(["Interested","Applied","Not Interested","Rejected"]); self.form.addRow("Status",self.status)
        self.favorite=QCheckBox("Favorite"); self.form.addRow("",self.favorite)
        self.layout.addLayout(self.form)
        row=QHBoxLayout()
        for text,fn in [("Save Changes",self.save),("Open Job URL",self.open_url),("Check Gmail",self.check_gmail),("Add to Update Center",self.add_update),("Delete",self.delete)]:
            b=QPushButton(text); b.clicked.connect(fn); row.addWidget(b)
        self.layout.addLayout(row)
        self.history=HistoryTimeline(); self.layout.addWidget(QLabel("<b>History</b>")); self.layout.addWidget(self.history)
    def load(self,app):
        self.app=app; job=app.job
        for k,w in self.fields.items(): w.setText("" if getattr(job,k) is None else str(getattr(job,k)))
        self.desc.setPlainText(job.job_description or ""); self.notes.setPlainText(app.personal_notes or "")
        self.status.setCurrentText(app.status); self.favorite.setChecked(app.is_favorite)
        self.history.load(HistoryRepository(self.window.session).for_application(app.application_id))
        from app.services.application_service import ApplicationService
        ApplicationService(self.window.session).mark_visited(app)
    def save(self):
        job=self.app.job
        data={k:w.text().strip() or None for k,w in self.fields.items()}
        if not data["job_title"] or not data["company_name"] or not data["job_url"]:
            QMessageBox.warning(self,"Missing required fields","Job title, company name and URL are required."); return
        from datetime import date
        try: data["deadline"]=date.fromisoformat(data["deadline"]) if data["deadline"] else None
        except ValueError: QMessageBox.warning(self,"Invalid deadline","Use YYYY-MM-DD."); return
        data["job_description"]=self.desc.toPlainText().strip() or None
        data["required_skills"] = job.required_skills
        data["preferred_skills"] = job.preferred_skills
        JobService(self.window.session).update_job(job,data,self.app)
        ApplicationService(self.window.session).update_notes(self.app,self.notes.toPlainText().strip() or None)
        if self.status.currentText()!=self.app.status:
            ApplicationService(self.window.session).change_status(self.app,self.status.currentText())
        ApplicationService(self.window.session).set_favorite(self.app,self.favorite.isChecked())
        self.load(self.app)
    def open_url(self):
        import webbrowser; webbrowser.open(self.app.job.job_url)
    def check_gmail(self):
        self.window.show_update(self.app.application_id)
    def add_update(self):
        self.window.update_center.add_application(self.app)
        self.window.show_update()
    def delete(self):
        if QMessageBox.question(self,"Delete","Move this application to Recycle Bin?",QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes:
            ApplicationService(self.window.session).soft_delete(self.app); self.window.show_jobs()
