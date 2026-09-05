from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
class JobCard(QFrame):
    def __init__(self, app, on_open):
        super().__init__()
        self.setFrameShape(QFrame.Box)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"<b>{app.job.job_title}</b>"))
        layout.addWidget(QLabel(app.job.company_name))
        layout.addWidget(QLabel(f"Status: {app.status}"))
        b = QPushButton("Open")
        b.clicked.connect(lambda: on_open(app))
        layout.addWidget(b)
