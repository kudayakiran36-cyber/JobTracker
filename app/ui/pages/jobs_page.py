from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLineEdit,QComboBox,QTableWidget,QTableWidgetItem,QPushButton,QHeaderView
class JobsPage(QWidget):
    def __init__(self,window):
        super().__init__(); self.window=window
        l=QVBoxLayout(self); row=QHBoxLayout()
        self.search=QLineEdit(); self.search.setPlaceholderText("Search jobs..."); self.search.textChanged.connect(self.refresh)
        self.status=QComboBox(); self.status.addItems(["All","Interested","Applied","Not Interested","Rejected"]); self.status.currentTextChanged.connect(self.refresh)
        row.addWidget(self.search); row.addWidget(self.status); l.addLayout(row)
        self.table=QTableWidget(0,6); self.table.setHorizontalHeaderLabels(["Company","Job Title","Status","Location","Deadline","Favorite"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch); self.table.cellDoubleClicked.connect(self.open_row); l.addWidget(self.table)
        self.refresh()
    def refresh(self):
        from app.repositories.job_repository import JobRepository
        rows=JobRepository(self.window.session).list(self.search.text(),self.status.currentText())
        self.rows=rows; self.table.setRowCount(len(rows))
        for i,j in enumerate(rows):
            a=j.application
            vals=[j.company_name,j.job_title,a.status,j.location or "",str(j.deadline or ""), "Yes" if a.is_favorite else ""]
            for c,v in enumerate(vals): self.table.setItem(i,c,QTableWidgetItem(v))
    def open_row(self,r,c): self.window.show_detail(self.rows[r].application_id)
