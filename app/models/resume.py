from datetime import datetime
from sqlalchemy import String, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Resume(Base):
    __tablename__ = "resumes"
    resume_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_name: Mapped[str] = mapped_column(String(300), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    date_added: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    target_role: Mapped[str | None] = mapped_column(String(300))
    skills_emphasized: Mapped[str | None] = mapped_column(Text)
    experience_emphasis: Mapped[str | None] = mapped_column(Text)
    projects_included: Mapped[str | None] = mapped_column(Text)
    applications: Mapped[list["Application"]] = relationship(back_populates="resume")
