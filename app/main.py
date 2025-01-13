from fastapi import FastAPI
from sqladmin import Admin

from app.admin.auth_backend import authentication_backend
from app.admin.views import TravelAdmin
from app.api.routers import auth, health_check, travel, user
from app.database.session import engine

app = FastAPI()

app.include_router(health_check.router)
app.include_router(user.router)
app.include_router(travel.router)
app.include_router(auth.router)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(TravelAdmin)
