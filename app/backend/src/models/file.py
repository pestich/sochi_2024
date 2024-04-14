from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_class import Base


class File(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    content: Mapped[str] = mapped_column(nullable=True)
    minio_id: Mapped[str] = mapped_column(nullable=True)
    category: Mapped[str] = mapped_column(default=None)

    attempt_id: Mapped[int] = mapped_column(ForeignKey("attempts.id"))
    attempt = relationship("Attempt", back_populates="files")
