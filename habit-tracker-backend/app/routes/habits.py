from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.habit import Habit
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitResponse, HabitUpdate

router = APIRouter(prefix="/habits", tags=["habits"])


def _get_owned_habit(habit_id: int, user: User, db: Session) -> Habit:
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if habit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
    if habit.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this habit",
        )
    return habit


@router.post("", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(
    payload: HabitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    habit = Habit(
        user_id=current_user.id,
        name=payload.name,
        frequency=payload.frequency,
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


@router.get("", response_model=list[HabitResponse])
def list_habits(
    include_inactive: bool = Query(default=False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Habit).filter(Habit.user_id == current_user.id)
    if not include_inactive:
        query = query.filter(Habit.is_active.is_(True))
    return query.order_by(Habit.created_at.desc()).all()


@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _get_owned_habit(habit_id, current_user, db)


@router.put("/{habit_id}", response_model=HabitResponse)
def update_habit(
    habit_id: int,
    payload: HabitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    habit = _get_owned_habit(habit_id, current_user, db)

    if payload.name is None and payload.frequency is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (name or frequency) must be provided",
        )

    if payload.name is not None:
        habit.name = payload.name
    if payload.frequency is not None:
        habit.frequency = payload.frequency

    db.commit()
    db.refresh(habit)
    return habit


@router.delete("/{habit_id}", response_model=HabitResponse)
def delete_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    habit = _get_owned_habit(habit_id, current_user, db)
    habit.is_active = False
    db.commit()
    db.refresh(habit)
    return habit
