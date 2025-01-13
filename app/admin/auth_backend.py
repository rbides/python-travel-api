from fastapi.security import SecurityScopes
from sqladmin.authentication import AuthenticationBackend
from fastapi import HTTPException, Request # Starlette
from app.service import auth
from app.utils.enums import Permissions
from app.config import settings


class AdminAuth(AuthenticationBackend):
    # TODO: is there a way for binding permission checking to table/operation?
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        
        # Validate username/password credentials
        # And update session
        token = auth.login_for_access_token(username, password)
        request.session.update({"token": token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        
        if not token:
            return False

        # Check the token in depth
        token_data = auth.get_token_data(token)
        try:
            # TODO: Would be better to check for role instead, but it's not being passed to the token currently.
            auth.verify_permissions(
                security_scopes=SecurityScopes([Permissions.TRAVEL_WRITE.value, Permissions.TRAVEL_DELETE.value]),
                token_data=token_data
            )
        except HTTPException:
            return False
        
        return True
    
authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY) # Is it ok to use the same key we used for Oauth?