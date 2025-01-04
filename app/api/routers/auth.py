from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status

from app.service import auth
from app.api.models import Token


router = APIRouter(
    prefix="/auth",
)


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        access_token = auth.login_for_access_token(form_data.username, form_data.password)
    except: # TODO: fix exception handling
        # if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=access_token, token_type="bearer")
