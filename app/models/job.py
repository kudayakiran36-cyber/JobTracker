from datetime import datetime
from sqlalchemy import String, Text, Date, DateTime, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Job(Base):
    __tablename__ = "jobs"
    job_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_title: Mapped[str] = mapped_column(String(300), nullable=False)
    company_name: Mapped[str] = mapped_column(String(300), nullable=False)
    job_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    location: Mapped[str | None] = mapped_column(String(300))
    work_arrangement: Mapped[str | None] = mapped_column(String(100))
    salary: Mapped[str | None] = mapped_column(String(300))
    job_description: Mapped[str | None] = mapped_column(Text)
    required_skills: Mapped[str | None] = mapped_column(Text)  # JSON array
    preferred_skills: Mapped[str | None] = mapped_column(Text) # JSON array
    experience_required: Mapped[str | None] = mapped_column(String(200))
    job_type: Mapped[str | None] = mapped_column(String(100))
    deadline: Mapped[object | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    application: Mapped["Application | None"] = relationship(back_populates="job", uselist=False, cascade="all, delete-orphan")

Index("ix_jobs_company", Job.company_name)
Index("ix_jobs_title", Job.job_title)
Index("ix_jobs_deadline", Job.deadline)
