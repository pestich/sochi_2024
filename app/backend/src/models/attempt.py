from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_class import Base


class Attempt(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("sessions.id"))
    status: Mapped[bool] = mapped_column(default=False)

    files = relationship("File", back_populates="attempt")
    session = relationship("Session", back_populates="attempts")
