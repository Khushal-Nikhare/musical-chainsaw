from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class HabitLogCreate(BaseModel):
    date: date
    completed: bool = True
    note: str | None = Field(default=None, max_length=500)


class HabitLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    habit_id: int
    date: date
    completed: bool
    note: str | None
    created_at: datetime


class StreakResponse(BaseModel):
    habit_id: int
    current_streak: int
    frequency: str


class StatsResponse(BaseModel):
    habit_id: int
    weekly_completion_percentage: float
    monthly_completion_percentage: float
