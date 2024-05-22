from _typeshed import Incomplete
from django.contrib.auth.backends import ModelBackend
from django.http.request import HttpRequest
from typing import Any
from django.contrib.auth.base_user import AbstractBaseUser

class CASBackend(ModelBackend):
    # FIXME
    def authenticate(
            self,
            request: HttpRequest | None,
            username: str | None = None,
            password: Incomplete | None = None,
            institution: Incomplete | None = None,
            ticket: Incomplete | None = None,
            service: Incomplete | None = None,
            **kwargs: Any,
    ) -> AbstractBaseUser | None: ...

class LinkedEmailBackend(ModelBackend):
    def authenticate(
            self,
            request: HttpRequest | None,
            username: str | None = None,
            password: Incomplete | None = None,
            email: Incomplete | None = None,
            **kwargs: Any,
    ) -> AbstractBaseUser | None: ...

class UsernameOrLinkedEmailBackend(LinkedEmailBackend): ...
