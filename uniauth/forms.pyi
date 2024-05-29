from typing import Any, Dict

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm as AuthPasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm as AuthPasswordResetForm
from django.contrib.auth.forms import SetPasswordForm as AuthSetPasswordForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpRequest

from uniauth.models import LinkedEmail as LinkedEmail
from uniauth.utils import get_setting as get_setting

class AddLinkedEmailForm(forms.Form):
    email: forms.EmailField
    user: User
    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None: ...
    def clean_email(self) -> str: ...
    def clean(self) -> Dict[str, Any]: ...

class ChangePrimaryEmailForm(forms.Form):
    user: User
    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None: ...
    def clean_email(self) -> str: ...

class LinkedEmailActionForm(forms.Form):
    delete_pk: int
    resend_pk: int

class LoginForm(AuthenticationForm):
    def __init__(
            self,
            request: HttpRequest | None = None,
            *args: Any,
            **kwargs: Any,
    ) -> None: ...

class SetPasswordForm(AuthSetPasswordForm):
    def clean_new_password1(self) -> str: ...

class PasswordChangeForm(AuthPasswordChangeForm):
    def clean_new_password1(self) -> str: ...

class PasswordResetForm(AuthPasswordResetForm):
    def get_users(self, email: str) -> tuple[User, ...]: ...

class SignupForm(UserCreationForm):
    email: forms.EmailField
    class Meta:
        model: User
        fields: tuple[str, ...]
    def clean_email(self) -> str: ...
    def clean_password1(self) -> str: ...
