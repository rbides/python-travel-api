from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from app.api.models.auth import TokenData
from app.config import settings
from app.repository import user as repo
from app.service.models.user import User
from app.utils.auth import verify_password  # TODO: bring it here?

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(username: str, password: str) -> User:
    print(username, password)
    user = repo.get_by_username(username)
    if not user or not verify_password(password, user.password):
        return

    user.password = (
        None  # Workaround for removing password. TODO: find a better way
    )
    return User.model_validate(user)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def login_for_access_token(username: str, password: str):
    user = authenticate_user(username, password)
    if not user:
        raise  # TODO:
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    permissions = [] if not user.role else user.role.permissions
    access_token = create_access_token(
        data={"sub": user.username, "scopes": permissions},
        expires_delta=access_token_expires,
    )
    return access_token


def get_token_data(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        scopes: list[str] = payload.get("scopes", [])
        if username is None:
            raise credentials_exception
        return TokenData(username=username, scopes=scopes)
    # Is it safe to warn for expired token?
    except jwt.InvalidTokenError:
        raise credentials_exception


# TODO: Create a decorator for this maybe.
# Edit: don't need a decorator. Security and SecurityScopes
# already solve our needs
def verify_permissions(
    security_scopes: SecurityScopes,
    token_data: Annotated[TokenData, Depends(get_token_data)],
):
    print(token_data, security_scopes.scopes)
    for p in security_scopes.scopes:
        if p not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                # headers={"WWW-Authenticate": },
            )
