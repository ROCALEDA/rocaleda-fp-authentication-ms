import jwt
import pytest
from fastapi import HTTPException
from app.commons.schemas import UserCredentials
from unittest.mock import Mock, AsyncMock, patch


class TestAuthenticationService:
    @pytest.mark.asyncio
    @patch("app.commons.settings.get_settings")
    async def test_get_auth_token(self, mock_get_settings):
        mock_get_settings.return_value = Mock(secret_key="secret", algorithm="HS256")

        mock_repository = Mock()
        mock_repository.get_user_by_credentials = AsyncMock()
        mock_repository.get_user_by_credentials.return_value = {
            "role_id": 1,
            "email": "user@example.com",
            "id": 1,
        }

        from app.authentication.services.authentication_service import (
            AuthenticationService,
        )

        auth_data = {"email": "test@example.com", "password": "testpassword"}

        credentials = UserCredentials(**auth_data)

        service = AuthenticationService(mock_repository)
        token_response = await service.get_auth_token(credentials)

        assert "token" in token_response
        assert "role_id" in token_response
        assert "email" in token_response

    @pytest.mark.asyncio
    @patch("app.commons.settings.get_settings")
    async def test_get_auth_token_http_exception(self, mock_get_settings):
        mock_get_settings.return_value = Mock(secret_key="secret", algorithm="HS256")

        mock_repository = Mock()
        mock_repository.get_user_by_credentials = AsyncMock()
        mock_repository.get_user_by_credentials.side_effect = HTTPException(
            400, "Some Error"
        )

        from app.authentication.services.authentication_service import (
            AuthenticationService,
        )

        auth_data = {"email": "test@example.com", "password": "testpassword"}

        credentials = UserCredentials(**auth_data)

        service = AuthenticationService(mock_repository)

        with pytest.raises(HTTPException):
            await service.get_auth_token(credentials)

    @pytest.mark.asyncio
    @patch("app.commons.settings.get_settings")
    async def test_get_auth_token_general_exception(self, mock_get_settings):
        mock_get_settings.return_value = Mock(secret_key="secret", algorithm="HS256")

        mock_repository = Mock()
        mock_repository.get_user_by_credentials = AsyncMock()
        mock_repository.get_user_by_credentials.side_effect = Exception("Some error")

        from app.authentication.services.authentication_service import (
            AuthenticationService,
        )

        auth_data = {"email": "test@example.com", "password": "testpassword"}

        credentials = UserCredentials(**auth_data)

        service = AuthenticationService(mock_repository)

        with pytest.raises(Exception):
            await service.get_auth_token(credentials)

    @pytest.mark.asyncio
    @patch("app.commons.settings.get_settings")
    async def test_validate_jwt(self, mock_get_settings):
        mock_get_settings.return_value = Mock(secret_key="secret", algorithm="HS256")

        mock_repository = Mock()

        from app.authentication.services.authentication_service import (
            AuthenticationService,
        )

        token = jwt.encode(
            {"role_id": 1, "email": "user@example.com"},
            "secret",
            "HS256",
        )

        service = AuthenticationService(mock_repository)
        token_response = await service.validate_jwt(token)

        assert "valid" in token_response
        assert "data" in token_response

    @pytest.mark.asyncio
    @patch("app.commons.settings.get_settings")
    async def test_validate_jwt_with_invalid_token(self, mock_get_settings):
        mock_get_settings.return_value = Mock(secret_key="secret", algorithm="HS256")

        mock_repository = Mock()

        from app.authentication.services.authentication_service import (
            AuthenticationService,
        )

        invalid_token = "invalid_token"

        service = AuthenticationService(mock_repository)

        with pytest.raises(HTTPException):
            await service.validate_jwt(invalid_token)
