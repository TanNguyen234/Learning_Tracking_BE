from fastapi import FastAPI
import models
from database import engine
from routers import users, skills, auth, logs, stats
from config import settings
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(stats.router)
app.include_router(skills.router)
app.include_router(logs.router)
# app.include_router(admin.router)
app.include_router(users.router)