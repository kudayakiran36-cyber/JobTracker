from datetime import datetime
from sqlalchemy import String, Text, DateTime, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class GmailEmail(Base):
    __tablename__ = "gmail_emails"
    email_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gmail_message_id: Mapped[str] = mapped_column(String(300), unique=True, nullable=False)
    thread_id: Mapped[str | None] = mapped_column(String(300))
    sender: Mapped[str | None] = mapped_column(String(500))
    subject: Mapped[str | None] = mapped_column(String(1000))
    received_at: Mapped[datetime | None] = mapped_column(DateTime)
    snippet: Mapped[str | None] = mapped_column(Text)
    gmail_link: Mapped[str | None] = mapped_column(String(1000))
    first_seen_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    links: Mapped[list["ApplicationEmailLink"]] = relationship(back_populates="email", cascade="all, delete-orphan")

Index("ix_gmail_received", GmailEmail.received_at)
