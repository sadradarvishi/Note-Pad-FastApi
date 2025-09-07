from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers.auth_router import router as auth_router
from app.routers.health_router import router as health_router
from app.routers.note_router import router as note_router
from app.routers.user_router import router as user_router

app = FastAPI(title="Notes API")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(note_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(health_router)
