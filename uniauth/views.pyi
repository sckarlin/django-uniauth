from typing import Any, Dict, List, Optional

from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetView
from django.http import HttpResponseBadRequest as HttpResponseBadRequest
from uniauth.decorators import login_required as login_required
from uniauth.forms import PasswordResetForm, SetPasswordForm
from uniauth.merge import merge_model_instances as merge_model_instances
from rest_framework.request import Request
from django.http import JsonResponse, HttpResponse, HttpResponseBase
from django.forms.forms import BaseForm

from uniauth.models import UserProfile


def _get_global_context(request: Request) -> Dict[str, Any]: ...
def _login_success(
        request: Request,
        user: str,
        next_url: str,
        drop_params: Optional[List[str]] = None,
) -> HttpResponse: ...

def login(request: Request) -> HttpResponse: ...
def cas_login(request: Request, institution: str) -> HttpResponse: ...
def logout(request: Request) -> HttpResponse: ...

def _send_verification_email(
        request: Request,
        to_email: str,
        verify_email: str,
) -> None: ...

def signup(request: Request) -> HttpResponse: ...
def settings(request: Request) -> HttpResponse: ...

def _add_institution_account(
        profile: UserProfile,
        slug: str,
        cas_id: int,
) -> None: ...

def link_to_profile(request: Request) -> HttpResponse: ...
def link_from_profile(request: Request, institution: str) -> HttpResponse: ...
def verify_token(request: Request, pk_base64: str, token: str) -> HttpResponse: ...

class PasswordReset(PasswordResetView):
    email_template_name: str
    form_class = PasswordResetForm
    from_email: str
    success_url: str
    template_name: str
    extra_email_context: Dict[str, Any]
    def form_valid(self, form: BaseForm) -> HttpResponse: ...

class PasswordResetDone(PasswordResetDoneView):
    template_name: str

class PasswordResetVerify(PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url: str
    template_name: str
    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponseBase: ...
    def form_valid(self, form: BaseForm) -> HttpResponse: ...

class PasswordResetVerifyDone(PasswordResetCompleteView):
    template_name: str
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]: ...

def get_jwt_tokens_from_session(request: Request) -> JsonResponse: ...




