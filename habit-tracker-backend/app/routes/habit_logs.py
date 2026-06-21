from calendar import monthrange
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.habit import Habit, HabitFrequency
from app.models.habit_log import HabitLog
from app.models.user import User
from app.routes.habits import _get_owned_habit
from app.schemas.habit_log import (
    HabitLogCreate,
    HabitLogResponse,
    StatsResponse,
    StreakResponse,
)

router = APIRouter(prefix="/habits", tags=["habit logs"])


def _week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())


def _calculate_daily_streak(logs_by_date: dict[date, bool], today: date) -> int:
    streak = 0
    current = today

    if current not in logs_by_date or not logs_by_date[current]:
        current -= timedelta(days=1)

    while current in logs_by_date and logs_by_date[current]:
        streak += 1
        current -= timedelta(days=1)

    return streak


def _calculate_weekly_streak(logs_by_date: dict[date, bool], today: date) -> int:
    completed_weeks: set[date] = set()
    for log_date, completed in logs_by_date.items():
        if completed:
            completed_weeks.add(_week_start(log_date))

    streak = 0
    current_week = _week_start(today)

    if current_week not in completed_weeks:
        current_week -= timedelta(weeks=1)

    while current_week in completed_weeks:
        streak += 1
        current_week -= timedelta(weeks=1)

    return streak


def _weekly_completion(habit: Habit, logs: list[HabitLog], today: date) -> float:
    week_start = _week_start(today)
    week_end = week_start + timedelta(days=6)

    completed_logs = [
        log for log in logs if log.completed and week_start <= log.date <= week_end
    ]

    if habit.frequency == HabitFrequency.daily:
        expected = 7
        actual = len({log.date for log in completed_logs})
    else:
        expected = 1
        actual = 1 if completed_logs else 0

    return round((actual / expected) * 100, 2) if expected else 0.0


def _monthly_completion(habit: Habit, logs: list[HabitLog], today: date) -> float:
    month_start = today.replace(day=1)
    days_in_month = monthrange(today.year, today.month)[1]
    month_end = month_start.replace(day=days_in_month)

    completed_logs = [
        log for log in logs if log.completed and month_start <= log.date <= month_end
    ]

    if habit.frequency == HabitFrequency.daily:
        expected = days_in_month
        actual = len({log.date for log in completed_logs})
    else:
        weeks_in_month = len(
            {_week_start(d) for d in (month_start + timedelta(days=i) for i in range(days_in_month))}
        )
        expected = weeks_in_month
        actual = len({_week_start(log.date) for log in completed_logs})

    return round((actual / expected) * 100, 2) if expected else 0.0


@router.post("/{habit_id}/logs", response_model=HabitLogResponse, status_code=status.HTTP_201_CREATED)
def create_habit_log(
    habit_id: int,
    payload: HabitLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    habit = _get_owned_habit(habit_id, current_user, db)

    if payload.date > date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot log habits for future dates",
        )

    log = HabitLog(
        habit_id=habit.id,
        date=payload.date,
        completed=payload.completed,
        note=payload.note,
    )
    db.add(log)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A log already exists for this habit on the given date",
        )
    db.refresh(log)
    return log


@router.get("/{habit_id}/logs", response_model=list[HabitLogResponse])
def list_habit_logs(
    habit_id: int,
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    habit = _get_owned_habit(habit_id, current_user, db)

    query = db.query(HabitLog).filter(HabitLog.habit_id == habit.id)
    if start_date is not None:
        query = query.filter(HabitLog.date >= start_date)
    if end_date is not None:
        query = query.filter(HabitLog.date <= end_date)

    return query.order_by(HabitLog.date.desc()).all()


@router.delete("/{habit_id}/logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit_log(
    habit_id: int,
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    habit = _get_owned_habit(habit_id, current_user, db)

    log = db.query(HabitLog).filter(HabitLog.id == log_id, HabitLog.habit_id == habit.id).first()
    if log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")

    db.delete(log)
    db.commit()


@router.get("/{habit_id}/streak", response_model=StreakResponse)
def get_habit_streak(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    habit = _get_owned_habit(habit_id, current_user, db)

    logs = db.query(HabitLog).filter(HabitLog.habit_id == habit.id).all()
    logs_by_date = {log.date: log.completed for log in logs}
    today = date.today()

    if habit.frequency == HabitFrequency.daily:
        streak = _calculate_daily_streak(logs_by_date, today)
    else:
        streak = _calculate_weekly_streak(logs_by_date, today)

    return StreakResponse(
        habit_id=habit.id,
        current_streak=streak,
        frequency=habit.frequency.value,
    )


@router.get("/{habit_id}/stats", response_model=StatsResponse)
def get_habit_stats(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    habit = _get_owned_habit(habit_id, current_user, db)

    logs = db.query(HabitLog).filter(HabitLog.habit_id == habit.id).all()
    today = date.today()

    return StatsResponse(
        habit_id=habit.id,
        weekly_completion_percentage=_weekly_completion(habit, logs, today),
        monthly_completion_percentage=_monthly_completion(habit, logs, today),
    )
