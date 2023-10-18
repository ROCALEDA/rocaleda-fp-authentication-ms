import pytest
from unittest.mock import Mock, AsyncMock
from app.commons.schemas import UserCredentials
from app.authentication.controllers import authentication_controller

class TestAuthenticationController:
  @pytest.mark.asyncio
  async def test_get_auth_token(self):
    mocked_service = Mock()
    mocked_service.get_auth_token = AsyncMock()
    
    get_auth_token_func = authentication_controller.initialize(mocked_service)["get_auth_token"]
    
    auth_data = {
      "email": "test@example.com",
      "password": "testpassword"
    }
    
    credentials = UserCredentials(**auth_data)
    
    await get_auth_token_func(credentials)
    assert mocked_service.get_auth_token.call_count == 1
    mocked_service.get_auth_token.assert_called_once_with(credentials)

  @pytest.mark.asyncio
  async def test_validate_jwt(self):
    mocked_service = Mock()
    mocked_service.validate_jwt = AsyncMock()
    
    validate_jwt_func = authentication_controller.initialize(mocked_service)["validate_jwt"]
    
    token = "mock-jwt"
    await validate_jwt_func(token)
    assert mocked_service.validate_jwt.call_count == 1
    mocked_service.validate_jwt.assert_called_once_with(token)
