from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
class ReminderCard(QFrame):
    def __init__(self, reminder):
        super().__init__(); self.setFrameShape(QFrame.Box)
        l=QVBoxLayout(self); l.addWidget(QLabel(reminder.message))
