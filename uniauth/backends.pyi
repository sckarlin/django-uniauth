from django.contrib.auth.backends import ModelBackend
from django.http.request import HttpRequest
from typing import Any
from django.contrib.auth.base_user import AbstractBaseUser

from uniauth.models import Institution


class CASBackend(ModelBackend):
    def authenticate(
            self,
            request: HttpRequest | None,
            institution: Institution | None = None,
            ticket: str | None = None,
            service: str | None = None,
            **kwargs: Any,
    ) -> AbstractBaseUser | None: ...

class LinkedEmailBackend(ModelBackend):
    def authenticate(
            self,
            request: HttpRequest | None,
            username: str | None = None,
            password: str | None = None,
            email: str | None = None,
            **kwargs: Any,
    ) -> AbstractBaseUser | None: ...

class UsernameOrLinkedEmailBackend(LinkedEmailBackend): ...
