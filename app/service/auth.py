from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.api.models.auth import TokenData
from app.repository import user as repo
from app.service.models.user import User
from app.utils.auth import verify_password # TODO: bring it here?
from app.config import settings

import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username: str, password: str) -> User:
    user = repo.get_by_username(username)
    if not user or not verify_password(password, user.password):
        return

    user.password = None # Workaround for removing password. TODO: find a better way
    return User.model_validate(user)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def login_for_access_token(username: str, password: str):
    user = authenticate_user(username, password)
    print(user)
    if not user:
        raise # TODO:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    print(user.role)
    permissions = [] if not user.role else user.role.permissions
    access_token = create_access_token(
        data={"sub": user.username, "scopes": permissions},
        expires_delta=access_token_expires
    )
    return access_token

def get_token_data(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return TokenData(username=username)
    # Is it safe to warn for expired token?
    except jwt.InvalidTokenError:
        raise credentials_exception