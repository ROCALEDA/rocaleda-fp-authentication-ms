import jwt
from typing import TYPE_CHECKING
from fastapi import HTTPException
from app.commons.settings import get_settings

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
                {
                    "role_id": user["role_id"],
                    "email": user["email"],
                    "user_id": user["id"],
                },
                get_settings().secret_key,
                get_settings().algorithm,
            )

            return {"token": token, "role_id": user["role_id"], "email": user["email"]}
        except HTTPException as e:
            print("Http exception: ", e.detail)
            raise e
        except Exception as e:
            print("Internal error: ", e)
            raise e

    async def validate_jwt(self, token: str):
        try:
            decoded_payload = jwt.decode(
                token, get_settings().secret_key, algorithms=[get_settings().algorithm]
            )
            return {"valid": True, "data": decoded_payload}
        except jwt.InvalidTokenError:
            raise HTTPException(400, "Invalid token")
