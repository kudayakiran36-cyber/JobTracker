from PySide6.QtWidgets import QListWidgetItem
class EmailCardItem(QListWidgetItem):
    def __init__(self, email):
        super().__init__(f"{email.received_at or ''} | {email.sender or ''} | {email.subject or '(no subject)'}")
        self.email = email
