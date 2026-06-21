"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-20

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("firebase_uid", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_firebase_uid"), "users", ["firebase_uid"], unique=True)

    habit_frequency = sa.Enum("daily", "weekly", name="habitfrequency")

    op.create_table(
        "habits",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("frequency", habit_frequency, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_habits_user_id"), "habits", ["user_id"], unique=False)

    op.create_table(
        "habit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("habit_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("completed", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["habit_id"], ["habits.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("habit_id", "date", name="uq_habit_log_habit_date"),
    )
    op.create_index(op.f("ix_habit_logs_habit_id"), "habit_logs", ["habit_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_habit_logs_habit_id"), table_name="habit_logs")
    op.drop_table("habit_logs")
    op.drop_index(op.f("ix_habits_user_id"), table_name="habits")
    op.drop_table("habits")
    op.drop_index(op.f("ix_users_firebase_uid"), table_name="users")
    op.drop_table("users")
    sa.Enum(name="habitfrequency").drop(op.get_bind(), checkfirst=True)
