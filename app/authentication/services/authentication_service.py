import jwt
from typing import TYPE_CHECKING
from fastapi import HTTPException
from app.commons.settings import settings

from app.commons.schemas import UserCredentials

if TYPE_CHECKING:
    from app.authentication.repositories.authentication_repository import (
        AuthenticationRepository,
    )


class AuthenticationService:
    def __init__(self, authentication_repository: "AuthenticationRepository"):
        self.authentication_repository = authentication_repository

    async def get_auth_token(self, credentials: UserCredentials):
        try:
            user = await self.authentication_repository.get_user_by_credentials(
                credentials
            )
            token = jwt.encode(
                {"role_id": user["role_id"], "email": user["email"]},
                settings.secret_key,
                settings.algorithm,
            )

            return {"token": token, "role_id": user["role_id"], "email": user["email"]}
        except HTTPException as e:
            print("Http exception: ", e.detail)
            raise e
        except Exception as e:
            print("Internal error: ", e)
            raise e