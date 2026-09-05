from PySide6.QtWidgets import QWidget,QVBoxLayout,QListWidget,QLabel
from app.repositories.job_repository import JobRepository
class FavoritesPage(QWidget):
    def __init__(self,window):
        super().__init__(); self.window=window; l=QVBoxLayout(self); l.addWidget(QLabel("<h2>Favorites</h2>")); self.list=QListWidget(); l.addWidget(self.list); self.list.itemDoubleClicked.connect(self.open); self.refresh()
    def refresh(self):
        self.list.clear(); self.rows=JobRepository(self.window.session).list(favorite=True)
        for j in self.rows:self.list.addItem(f"{j.company_name} — {j.job_title} [{j.application.status}]")
    def open(self,item): self.window.show_detail(self.rows[self.list.row(item)].application_id)
