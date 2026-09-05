from PySide6.QtWidgets import QWidget,QVBoxLayout,QListWidget,QPushButton,QMessageBox,QHBoxLayout,QLabel
from app.services.recycle_bin_service import RecycleBinService
class RecycleBinPage(QWidget):
    def __init__(self,window):
        super().__init__(); self.window=window; l=QVBoxLayout(self)
        l.addWidget(QLabel("<h2>Recycle Bin</h2>")); self.list=QListWidget(); l.addWidget(self.list)
        row=QHBoxLayout(); r=QPushButton("Restore Selected"); r.clicked.connect(self.restore); p=QPushButton("Purge Expired"); p.clicked.connect(self.purge); row.addWidget(r); row.addWidget(p); l.addLayout(row); self.refresh()
    def refresh(self):
        self.list.clear(); self.rows=RecycleBinService(self.window.session).items()
        for a in self.rows:self.list.addItem(f"{a.job.company_name} — {a.job.job_title} | expires {a.delete_expires_at:%Y-%m-%d %H:%M}")
    def restore(self):
        i=self.list.currentRow()
        if i>=0: RecycleBinService(self.window.session).restore(self.rows[i]); self.refresh()
    def purge(self):
        n=RecycleBinService(self.window.session).purge(); QMessageBox.information(self,"Recycle Bin",f"Purged {n} expired item(s)."); self.refresh()
