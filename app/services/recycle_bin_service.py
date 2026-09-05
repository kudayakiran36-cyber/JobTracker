from app.services.application_service import ApplicationService
class RecycleBinService:
    def __init__(self, session): self.session = session
    def items(self):
        from app.repositories.application_repository import ApplicationRepository
        return ApplicationRepository(self.session).deleted()
    def restore(self, app): return ApplicationService(self.session).restore(app)
    def purge(self):
        return ApplicationService(self.session).purge_expired()
