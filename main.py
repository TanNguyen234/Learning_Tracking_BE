from fastapi import FastAPI
import models
from database import engine
from routers import users, skills, auth, logs, stats
from config import settings
from fastapi.middleware.cors import CORSMiddleware

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from helpers.limiter import limiter
from slowapi.extension import _rate_limit_exceeded_handler
app = FastAPI(title=settings.APP_NAME)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
print(settings.FRONTEND_URL)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

@app.get('/success')
async def ForEveryone():
    return {"message": 'i can fail but i will win if i do not give up!'}

app.include_router(auth.router)
app.include_router(stats.router)
app.include_router(skills.router)
app.include_router(logs.router)
# app.include_router(admin.router)
app.include_router(users.router)