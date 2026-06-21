from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import habit_logs, habits

app = FastAPI(
    title="Habit Tracker API",
    description="Backend API for the Habit Tracker app with Firebase Authentication",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(habits.router)
app.include_router(habit_logs.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
