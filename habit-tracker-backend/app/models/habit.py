import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class HabitFrequency(str, enum.Enum):
    daily = "daily"
    weekly = "weekly"


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    frequency: Mapped[HabitFrequency] = mapped_column(Enum(HabitFrequency))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")

    user: Mapped["User"] = relationship("User", back_populates="habits")  # noqa: F821
    logs: Mapped[list["HabitLog"]] = relationship(  # noqa: F821
        "HabitLog", back_populates="habit", cascade="all, delete-orphan"
    )
