from datetime import datetime
from sqlalchemy import String, Date, DateTime, Boolean, Integer, ForeignKey, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Application(Base):
    __tablename__ = "applications"
    application_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.job_id", ondelete="CASCADE"), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="Interested")
    application_date: Mapped[object | None] = mapped_column(Date)
    application_date_type: Mapped[str | None] = mapped_column(String(30))
    resume_id: Mapped[int | None] = mapped_column(ForeignKey("resumes.resume_id", ondelete="SET NULL"))
    personal_notes: Mapped[str | None] = mapped_column(Text)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime)
    last_application_update_at: Mapped[datetime | None] = mapped_column(DateTime)
    last_visited_at: Mapped[datetime | None] = mapped_column(DateTime)
    interested_since: Mapped[datetime | None] = mapped_column(DateTime)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime)
    delete_expires_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    job: Mapped["Job"] = relationship(back_populates="application")
    resume: Mapped["Resume | None"] = relationship(back_populates="applications")
    history: Mapped[list["History"]] = relationship(back_populates="application", cascade="all, delete-orphan")
    email_links: Mapped[list["ApplicationEmailLink"]] = relationship(back_populates="application", cascade="all, delete-orphan")

Index("ix_app_status", Application.status)
Index("ix_app_checked", Application.last_checked_at)
Index("ix_app_visited", Application.last_visited_at)
Index("ix_app_deleted", Application.deleted_at, Application.delete_expires_at)
