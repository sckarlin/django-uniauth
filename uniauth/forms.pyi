from _typeshed import Incomplete
from typing import Any

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm as AuthPasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm as AuthPasswordResetForm
from django.contrib.auth.forms import SetPasswordForm as AuthSetPasswordForm
from django.contrib.auth.forms import UserCreationForm
from uniauth.models import LinkedEmail as LinkedEmail
from uniauth.utils import get_setting as get_setting

# FIXME
class AddLinkedEmailForm(forms.Form):
    email: forms.EmailField
    user: Incomplete
    def __init__(self, user: Incomplete, *args: Any, **kwargs: Any) -> None: ...
    def clean_email(self) -> str: ...
    def clean(self) -> Incomplete: ...

class ChangePrimaryEmailForm(forms.Form):
    user: Incomplete
    def __init__(self, user: Incomplete, *args: Any, **kwargs: Any) -> None: ...
    def clean_email(self) -> str: ...

class LinkedEmailActionForm(forms.Form):
    delete_pk: Incomplete
    resend_pk: Incomplete

class LoginForm(AuthenticationForm):
    def __init__(
            self,
            request: Incomplete | None = None,
            *args: Any,
            **kwargs: Any,
    ) -> None: ...

class SetPasswordForm(AuthSetPasswordForm):
    def clean_new_password1(self) -> str: ...

class PasswordChangeForm(AuthPasswordChangeForm):
    def clean_new_password1(self) -> str: ...

class PasswordResetForm(AuthPasswordResetForm):
    def get_users(self, email: str) -> tuple[Incomplete, ...]: ...

class SignupForm(UserCreationForm[Incomplete]):
    email: forms.EmailField
    class Meta:
        model: Incomplete
        fields: tuple[str, ...]
    def clean_email(self) -> str: ...
    def clean_password1(self) -> str: ...
