from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.module_loading import import_string
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Creates tokens for linked email verification.
    """
    def _make_hash_value(self, email, timestamp):
        return str(email.pk) + str(email.is_verified) + str(timestamp)


token_generator = EmailVerificationTokenGenerator()


def get_jwt_tokens_for_user(user, **_kwargs):
    """
    Generates a refresh token for the valid user
    """
    try:
        serializer = import_string(jwt_settings.TOKEN_OBTAIN_SERIALIZER)
        refresh_token = serializer.get_token(user)
    except (AttributeError, ImportError) as _error:
        # simplejwt defines a default token serializer that uses
        # RefreshToken, but this is here as a fallback in case something
        # is weirdly configured, or the installed simplejwt package is
        # too old to support custom serializers
        refresh_token = RefreshToken.for_user(user)

    return refresh_token, refresh_token.access_token
