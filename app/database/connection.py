from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from app.core.config import DB_PATH, ensure_dirs

ensure_dirs()
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
    future=True,
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

def init_db():
    from app.models import (
        job, application, history, resume, gmail_email, email_link, setting
    )
    from app.database.base import Base
    Base.metadata.create_all(bind=engine)
    from app.repositories.settings_repository import SettingsRepository
    with SessionLocal() as session:
        SettingsRepository(session).initialize_defaults()
        session.commit()
