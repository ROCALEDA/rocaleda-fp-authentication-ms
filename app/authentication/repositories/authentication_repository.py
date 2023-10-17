from fastapi import HTTPException
import httpx
import json

from app.commons.settings import settings
from app.commons.schemas import UserCredentials


class AuthenticationRepository:
    async def get_user_by_credentials(self, credentials: UserCredentials):
        async with httpx.AsyncClient() as client:
            params = json.dumps(credentials.model_dump())
            uri = self.__build_request_uri(settings.users_ms, "user/by-credentials")
            print(f"Sending {params} to {uri}")
            response = await client.get(
                uri, params=credentials.model_dump(), timeout=60
            )

            if 400 <= response.status_code < 600:
                error_detail = response.json().get("detail", response.text)
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )
            return response.json()

    def __build_request_uri(self, host: str, endpoint: str) -> str:
        # TODO: Change to https
        return f"http://{host}/{endpoint}"
