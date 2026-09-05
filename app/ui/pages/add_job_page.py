from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPlainTextEdit,QPushButton,QMessageBox
class AddJobPage(QWidget):
    MASTER_PROMPT = '''Return ONLY valid JSON for the job posting. Required keys: job_title, company_name, job_url. Optional keys: location, work_arrangement, salary, job_description, required_skills, preferred_skills, experience_required, job_type, deadline. Use null when unavailable. deadline must be YYYY-MM-DD or null. required_skills and preferred_skills must be arrays of strings. Include schema_version: "1.0". Do not add extra keys.'''
    def __init__(self, window):
        super().__init__(); self.window=window
        l=QVBoxLayout(self); l.addWidget(QLabel("<h2>Add New Job</h2>"))
        l.addWidget(QLabel("Paste JSON from your external AI/tool:"))
        self.text=QPlainTextEdit(); l.addWidget(self.text)
        row=QHBoxLayout(); copy=QPushButton("Copy Master Prompt"); copy.clicked.connect(lambda: self.window.clipboard().setText(self.MASTER_PROMPT))
        review=QPushButton("Validate & Review"); review.clicked.connect(self.review); row.addWidget(copy); row.addWidget(review); l.addLayout(row)
    def review(self):
        from app.json_import.importer import parse
        from app.core.exceptions import ValidationError
        try: data=parse(self.text.toPlainText())
        except Exception as e: QMessageBox.critical(self,"Invalid JSON",str(e)); return
        self.window.show_review(data)
