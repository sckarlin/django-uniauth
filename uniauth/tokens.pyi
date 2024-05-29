from typing import Any

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator): ...

token_generator: EmailVerificationTokenGenerator

def get_jwt_tokens_for_user(
        user: User,
        **_kwargs: Any,
) -> tuple[RefreshToken, AccessToken]: ...
