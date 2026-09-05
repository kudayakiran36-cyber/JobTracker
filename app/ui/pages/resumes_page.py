from PySide6.QtWidgets import QWidget,QVBoxLayout,QListWidget,QPushButton,QFileDialog,QMessageBox,QLabel
from app.services.resume_service import ResumeService
class ResumesPage(QWidget):
    def __init__(self,window):
        super().__init__(); self.window=window; l=QVBoxLayout(self); l.addWidget(QLabel("<h2>Resume Library</h2>")); self.list=QListWidget(); l.addWidget(self.list)
        b=QPushButton("Add Resume"); b.clicked.connect(self.add); l.addWidget(b); self.refresh()
    def refresh(self):
        self.list.clear(); self.rows=ResumeService(self.window.session).all()
        for r in self.rows:self.list.addItem(f"{r.file_name} | {r.target_role or 'No target role'}")
    def add(self):
        p,_=QFileDialog.getOpenFileName(self,"Add Resume","","PDF/DOCX (*.pdf *.docx);;All files (*)")
        if p:
            try: ResumeService(self.window.session).add(p); self.refresh()
            except Exception as e: QMessageBox.critical(self,"Resume error",str(e))
