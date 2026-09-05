import json
from datetime import date
from PySide6.QtWidgets import QWidget,QFormLayout,QVBoxLayout,QHBoxLayout,QLineEdit,QPlainTextEdit,QPushButton,QMessageBox,QDateEdit,QComboBox,QFileDialog
from app.core.constants import STATUSES, APPLICATION_DATE_TYPES

class ReviewJobPage(QWidget):
    def __init__(self, window):
        super().__init__(); self.window=window; self.data={}
        self.form=QFormLayout(); self.fields={}
        for key,label in [("job_title","Job Title"),("company_name","Company"),("job_url","Job URL"),("location","Location"),("work_arrangement","Work Arrangement"),("salary","Salary"),("experience_required","Experience"),("job_type","Job Type")]:
            w=QLineEdit(); self.fields[key]=w; self.form.addRow(label,w)
        self.desc=QPlainTextEdit(); self.form.addRow("Description",self.desc)
        self.skills=QLineEdit(); self.form.addRow("Required Skills (comma-separated)",self.skills)
        self.pref=QLineEdit(); self.form.addRow("Preferred Skills (comma-separated)",self.pref)
        self.deadline=QLineEdit(); self.form.addRow("Deadline (YYYY-MM-DD)",self.deadline)
        self.status=QComboBox(); self.status.addItems(["Interested","Already Applied"]); self.form.addRow("Initial State",self.status)
        self.app_date=QLineEdit(); self.form.addRow("Application Date",self.app_date)
        self.date_type=QComboBox(); self.date_type.addItems(APPLICATION_DATE_TYPES); self.form.addRow("Date Type",self.date_type)
        self.resume=QLineEdit(); rb=QPushButton("Choose Resume"); rb.clicked.connect(self.choose_resume)
        rr=QHBoxLayout(); rr.addWidget(self.resume); rr.addWidget(rb); self.form.addRow("Resume (optional)",rr)
        save=QPushButton("Confirm & Save"); save.clicked.connect(self.save)
        l=QVBoxLayout(self); l.addLayout(self.form); l.addWidget(save)
    def load(self,data):
        self.data=data
        for k,w in self.fields.items(): w.setText("" if data.get(k) is None else str(data.get(k)))
        self.desc.setPlainText(data.get("job_description") or "")
        self.skills.setText(", ".join(data.get("required_skills") or []))
        self.pref.setText(", ".join(data.get("preferred_skills") or []))
        self.deadline.setText("" if not data.get("deadline") else data["deadline"].isoformat())
        self.status.setCurrentIndex(0); self.app_date.clear(); self.resume.clear()
    def choose_resume(self):
        p,_=QFileDialog.getOpenFileName(self,"Choose Resume","","PDF/DOCX (*.pdf *.docx);;All files (*)")
        if p:self.resume.setText(p)
    def save(self):
        from datetime import date
        from app.services.job_service import JobService
        data={k:w.text().strip() or None for k,w in self.fields.items()}
        data["job_description"]=self.desc.toPlainText().strip() or None
        data["required_skills"]=[x.strip() for x in self.skills.text().split(",") if x.strip()]
        data["preferred_skills"]=[x.strip() for x in self.pref.text().split(",") if x.strip()]
        try:
            data["deadline"]=date.fromisoformat(self.deadline.text()) if self.deadline.text().strip() else None
        except ValueError:
            QMessageBox.warning(self,"Invalid deadline","Use YYYY-MM-DD."); return
        if not data["job_title"] or not data["company_name"] or not data["job_url"]:
            QMessageBox.warning(self,"Missing required fields","Job title, company name and job URL are required."); return
        dup=JobService(self.window.session).duplicates(data["company_name"],data["job_title"])
        if dup and QMessageBox.question(self,"Possible duplicate","A job with the same company and title already exists. Create anyway?",QMessageBox.Yes|QMessageBox.No)!=QMessageBox.Yes:return
        status="Applied" if self.status.currentText()=="Already Applied" else "Interested"
        ad=None; dt=None
        if status=="Applied":
            if not self.app_date.text().strip():
                QMessageBox.warning(self,"Application date required","Enter the application date."); return
            try: ad=date.fromisoformat(self.app_date.text().strip())
            except ValueError: QMessageBox.warning(self,"Invalid date","Use YYYY-MM-DD."); return
            dt=self.date_type.currentText()
        resume_id=None
        if self.resume.text().strip():
            from app.services.resume_service import ResumeService
            resume=ResumeService(self.window.session).add(self.resume.text().strip())
            resume_id=resume.resume_id
        JobService(self.window.session).create(data,status,ad,dt,resume_id)
        QMessageBox.information(self,"Saved","Job saved successfully.")
        self.window.show_jobs()
