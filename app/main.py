from fastapi import FastAPI
from app.core.database import Base, engine
from app.api import users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(partners.router, prefix="/partners", tags=["Partner Universities"])
# app.include_router(applications.router, prefix="/applications", tags=["Applications"])
