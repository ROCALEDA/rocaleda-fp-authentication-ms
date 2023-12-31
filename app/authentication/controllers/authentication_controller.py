from fastapi import APIRouter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.authentication.services.authentication_service import AuthenticationService
from app.commons.schemas import UserCredentials


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


def initialize(authentication_service: "AuthenticationService"):
    @router.post("")
    async def get_auth_token(credentials: UserCredentials):
        return await authentication_service.get_auth_token(credentials)

    @router.get("/validate/{token}")
    async def validate_jwt(token: str):
        return await authentication_service.validate_jwt(token)

    return {"get_auth_token": get_auth_token, "validate_jwt": validate_jwt}
