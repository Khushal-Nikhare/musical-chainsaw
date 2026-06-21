from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.habit import HabitFrequency


class HabitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    frequency: HabitFrequency


class HabitUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    frequency: HabitFrequency | None = None


class HabitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    frequency: HabitFrequency
    created_at: datetime
    is_active: bool
