from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_class import Base


class Session(Base):
    id: Mapped[str] = mapped_column(primary_key=True)
    attempts = relationship("Attempt", back_populates="session")
