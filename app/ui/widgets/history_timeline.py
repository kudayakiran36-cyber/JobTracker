from PySide6.QtWidgets import QListWidget
class HistoryTimeline(QListWidget):
    def load(self, rows):
        self.clear()
        for h in rows:
            self.addItem(f"{h.event_date:%Y-%m-%d %H:%M} — {h.event_description}")
