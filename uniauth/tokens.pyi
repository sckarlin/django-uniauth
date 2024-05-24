from _typeshed import Incomplete
from typing import Any

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator): ...

token_generator: Incomplete

def get_jwt_tokens_for_user(
        user: Incomplete,
        **kwargs: Any,
) -> tuple[RefreshToken, AccessToken]: ...
