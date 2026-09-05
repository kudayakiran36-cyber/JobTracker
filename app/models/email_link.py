from datetime import datetime
from sqlalchemy import Integer, ForeignKey, DateTime, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class ApplicationEmailLink(Base):
    __tablename__ = "application_email_links"
    link_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.application_id", ondelete="CASCADE"), nullable=False)
    email_id: Mapped[int] = mapped_column(ForeignKey("gmail_emails.email_id", ondelete="CASCADE"), nullable=False)
    linked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    link_type: Mapped[str | None] = mapped_column(String(100))
    application: Mapped["Application"] = relationship(back_populates="email_links")
    email: Mapped["GmailEmail"] = relationship(back_populates="links")
    __table_args__ = (UniqueConstraint("application_id", "email_id", name="uq_application_email"),)
