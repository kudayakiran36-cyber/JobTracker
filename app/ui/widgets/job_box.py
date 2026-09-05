from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
class JobBox(QFrame):
    def __init__(self, app):
        super().__init__(); self.app = app
        self.setFrameShape(QFrame.Box)
        l=QVBoxLayout(self); l.addWidget(QLabel(f"{app.job.company_name}"))
        l.addWidget(QLabel(app.job.job_title))
