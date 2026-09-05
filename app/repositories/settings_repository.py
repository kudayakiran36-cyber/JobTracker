from app.models.setting import Setting
from app.core.constants import DEFAULT_SETTINGS

class SettingsRepository:
    def __init__(self, session): self.session = session
    def initialize_defaults(self):
        for key, value in DEFAULT_SETTINGS.items():
            if not self.session.query(Setting).filter_by(setting_key=key).first():
                self.session.add(Setting(setting_key=key, setting_value=value))
    def get(self, key, default=None):
        row = self.session.query(Setting).filter_by(setting_key=key).first()
        return row.setting_value if row else default
    def set(self, key, value):
        row = self.session.query(Setting).filter_by(setting_key=key).first()
        if row: row.setting_value = str(value)
        else: self.session.add(Setting(setting_key=key, setting_value=str(value)))
