from fastapi import FastAPI
from app.authentication.repositories.authentication_repository import (
    AuthenticationRepository,
)
from app.authentication.services.authentication_service import AuthenticationService

from app.health.controllers import health_controller
from app.health.services.health_service import HealthService
from app.authentication.controllers import authentication_controller


class Initializer:
    def __init__(self, app: FastAPI):
        self.app = app

    def setup(self):
        self.init_health_module()
        self.init_authentication_module()

    def init_health_module(self):
        print("Initializing health module")
        health_service = HealthService()
        health_controller.initialize(health_service)
        self.app.include_router(health_controller.router)
        print("Health module initialized successfully")

    def init_authentication_module(self):
        print("Initializing authentication module")
        authentication_repository = AuthenticationRepository()
        authentication_service = AuthenticationService(authentication_repository)
        authentication_controller.initialize(authentication_service)
        self.app.include_router(authentication_controller.router)
        print("Authentication module initialized successfully")
