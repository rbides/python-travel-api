from fastapi import FastAPI
from sqladmin import Admin
from app.api.routers import travel, user, health_check, auth
from app.database.session import engine
from app.admin.auth_backend import authentication_backend
from app.admin.views import TravelAdmin

app = FastAPI()

app.include_router(health_check.router)
app.include_router(user.router)
app.include_router(travel.router)
app.include_router(auth.router)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(TravelAdmin)