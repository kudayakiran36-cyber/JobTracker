from PySide6.QtWidgets import QApplication

class ThemeManager:
    @staticmethod
    def apply(app):
        app.setStyleSheet("""
        QWidget { background: #ffffff; color: #000000; font-size: 13px; }
        QMainWindow { background: #ffffff; }
        QPushButton { border: 1px solid #000000; padding: 8px 12px; background: #ffffff; }
        QPushButton:hover { background: #eeeeee; }
        QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QDateEdit {
            border: 1px solid #000000; padding: 6px; background: #ffffff;
        }
        QTabWidget::pane { border: 1px solid #000000; }
        QTabBar::tab { border: 1px solid #000000; padding: 8px 14px; background: #ffffff; }
        QTabBar::tab:selected { background: #000000; color: #ffffff; }
        QGroupBox { border: 1px solid #000000; margin-top: 12px; padding: 10px; }
        QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 4px; }
        QTableWidget { border: 1px solid #000000; gridline-color: #cccccc; }
        QHeaderView::section { background: #000000; color: #ffffff; padding: 6px; }
        """)
