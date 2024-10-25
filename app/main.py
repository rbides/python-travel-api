from fastapi import FastAPI

from app.api.routers import travel, user, health_check


app = FastAPI()

app.include_router(health_check.router)
app.include_router(user.router)
app.include_router(travel.router)

