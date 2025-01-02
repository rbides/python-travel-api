from datetime import datetime, timedelta, timezone
import json
import uuid
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import logging
from app.api.routers import travel, user, health_check, auth


app = FastAPI()

app.include_router(health_check.router)
app.include_router(user.router)
app.include_router(travel.router)
app.include_router(auth.router)

