from unittest import skipUnless

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from uniauth.tokens import get_jwt_tokens_for_user

try:
    import mock
except ImportError:
    from unittest import mock


MIN_DJANGO_CUSTOM_SERIALIZER_VERSION = "2.0.0"
MIN_SIMPLEJWT_CUSTOM_SERIALIZER_VERSION = "5.1.0"


def custom_serializers_supported():
    """
    Returns whether the installed simplejwt package supports custom
    serializers or not
    """
    import django
    import rest_framework_simplejwt

    # Simple JWT also requires Django 2.0+ in order to work properly,
    # but that is not currently enforced in its requirements
    return (django.__version__ >= MIN_DJANGO_CUSTOM_SERIALIZER_VERSION) and (
        rest_framework_simplejwt.__version__
        >= MIN_SIMPLEJWT_CUSTOM_SERIALIZER_VERSION
    )


if custom_serializers_supported():
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

    class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
        """
        Example TokenObtainPairSerializer subclass that adds custom claims
        """

        @classmethod
        def get_token(cls, user):
            token = super().get_token(user)
            token["foo"] = "bar"
            return token


class GetJWTTokensForUserTests(TestCase):
    """
    Tests the get_jwt_tokens_for_user method in tokens.py
    """

    def setUp(self):
        self.user = User.objects.create(username="johndoe@school.edu")
        self.user2 = User.objects.create(username="janedoe@gmail.com")

    def test_get_jwt_tokens_for_user_success(self):
        """
        Ensure get_jwt_tokens_for_user returns strings that decode
        into valid Refresh and Access tokens
        """
        refresh_token, access_token = get_jwt_tokens_for_user(self.user)
        # str() for Token signs and returns it as a base64 encoded string
        refresh_token_encoded = str(refresh_token)
        access_token_encoded = str(access_token)
        # Use noqa for token parameter for Token() due to
        # https://github.com/jazzband/djangorestframework-simplejwt/issues/787
        refresh_token_validated = RefreshToken(token=refresh_token_encoded)  # noqa
        access_token_validated = AccessToken(token=access_token_encoded)  # noqa
        self.assertEqual(refresh_token_validated["user_id"], self.user.id)
        self.assertEqual(access_token_validated["user_id"], self.user.id)

        refresh_token, access_token = get_jwt_tokens_for_user(self.user2)
        # str() for Token signs and returns it as a base64 encoded string
        refresh_token_encoded = str(refresh_token)
        access_token_encoded = str(access_token)
        # Use noqa for token parameter for Token() due to
        # https://github.com/jazzband/djangorestframework-simplejwt/issues/787
        refresh_token_validated = RefreshToken(token=refresh_token_encoded)  # noqa
        access_token_validated = AccessToken(token=access_token_encoded)  # noqa
        self.assertEqual(refresh_token_validated["user_id"], self.user2.id)
        self.assertEqual(access_token_validated["user_id"], self.user2.id)

    @skipUnless(
        custom_serializers_supported(),
        (
            "django >= '{}' and simple_jwt >= '{}' required "
            "to support custom token serializers"
        ).format(
            MIN_DJANGO_CUSTOM_SERIALIZER_VERSION,
            MIN_SIMPLEJWT_CUSTOM_SERIALIZER_VERSION,
        ),
    )
    @mock.patch(
        "uniauth.tokens.jwt_settings.TOKEN_OBTAIN_SERIALIZER",
        "tests.test_tokens.CustomTokenObtainPairSerializer",
    )
    def test_get_jwt_tokens_for_user_custom_serializer(self):
        """
        If a custom token obtain serializer is defined, ensure
        get_jwt_tokens_for_user uses that custom class
        """
        refresh, access = get_jwt_tokens_for_user(self.user)
        self.assertEqual(refresh["user_id"], self.user.id)
        self.assertEqual(access["user_id"], self.user.id)
        self.assertEqual(refresh["foo"], "bar")
        self.assertEqual(access["foo"], "bar")
