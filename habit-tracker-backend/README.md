# Habit Tracker Backend

FastAPI backend for a Habit Tracker app with Firebase Authentication, PostgreSQL, and SQLAlchemy.

## Tech Stack

- Python + FastAPI
- PostgreSQL (SQLAlchemy ORM)
- Firebase Admin SDK (token verification)
- Alembic (database migrations)
- Pydantic (request/response schemas)

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- A Firebase project with Authentication enabled
- Firebase service account JSON key file

## Setup

### 1. Clone and enter the project

```bash
cd habit-tracker-backend
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Edit `.env` in the project root:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/habit_tracker
FIREBASE_CREDENTIALS_PATH=./firebase-service-account.json
```

- Update `DATABASE_URL` with your PostgreSQL credentials.
- Place your Firebase service account JSON at the path specified by `FIREBASE_CREDENTIALS_PATH`.

### 5. Create the database

```bash
createdb habit_tracker
```

Or create the database using your preferred PostgreSQL client.

### 6. Run migrations

```bash
alembic upgrade head
```

### 7. Start the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs: `http://localhost:8000/docs`.

## Authentication

All routes except `/health` require a Firebase ID token in the `Authorization` header:

```
Authorization: Bearer <firebase_id_token>
```

On first authenticated request, the user is automatically created in the database using their Firebase UID, email, and name.

## API Endpoints

### Health

| Method | Path     | Auth | Description        |
|--------|----------|------|--------------------|
| GET    | `/health`| No   | Server health check |

### Habits

| Method | Path            | Description                          |
|--------|-----------------|--------------------------------------|
| POST   | `/habits`       | Create a new habit                   |
| GET    | `/habits`       | List habits for the current user     |
| GET    | `/habits/{id}`  | Get a single habit                   |
| PUT    | `/habits/{id}`  | Update habit name or frequency       |
| DELETE | `/habits/{id}`  | Soft delete (sets `is_active=false`) |

### Habit Logs

| Method | Path                              | Description                              |
|--------|-----------------------------------|------------------------------------------|
| POST   | `/habits/{id}/logs`               | Log completion for a date (past allowed) |
| GET    | `/habits/{id}/logs`               | List logs (optional `start_date`, `end_date`) |
| DELETE | `/habits/{id}/logs/{log_id}`      | Delete a log entry                       |
| GET    | `/habits/{id}/streak`             | Current completion streak                |
| GET    | `/habits/{id}/stats`              | Weekly and monthly completion %          |

## Example Requests

### Create a habit

```bash
curl -X POST http://localhost:8000/habits \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Morning run", "frequency": "daily"}'
```

### Log a habit (backfill a past date)

```bash
curl -X POST http://localhost:8000/habits/1/logs \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-06-15", "completed": true, "note": "5km run"}'
```

### Get streak

```bash
curl http://localhost:8000/habits/1/streak \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Project Structure

```
habit-tracker-backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # SQLAlchemy engine and session
│   ├── firebase.py          # Firebase Admin SDK setup
│   ├── dependencies.py      # Auth dependency (get_current_user)
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   └── routes/              # API route handlers
├── alembic/                 # Database migrations
├── .env                     # Environment variables
├── requirements.txt
└── README.md
```

## HTTP Status Codes

| Code | When                                      |
|------|-------------------------------------------|
| 401  | Missing or invalid Firebase token         |
| 403  | Habit belongs to another user             |
| 404  | Habit or log not found                    |
| 409  | Duplicate log for the same habit and date |

## Development

Generate a new migration after model changes:

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```
