from django.urls import re_path
from uniauth import views

app_name = "uniauth"

urlpatterns = [
    re_path(r"^login/$", views.login, name="login"),
    re_path(
        r"^cas-login/(?P<institution>[a-z0-9\-]+)/$",
        views.cas_login,
        name="cas-login",
    ),
    re_path(r"^logout/$", views.logout, name="logout"),
    re_path(r"^signup/$", views.signup, name="signup"),
    re_path(r"^settings/$", views.settings, name="settings"),
    re_path(r"^link-to-profile/$", views.link_to_profile, name="link-to-profile"),
    re_path(
        r"^link-from-profile/(?P<institution>[a-z0-9\-]+)/$",
        views.link_from_profile,
        name="link-from-profile",
    ),
    re_path(
        r"^verify-token/(?P<pk_base64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$",
        views.verify_token,
        name="verify-token",
    ),
    re_path(
        r"^password-reset/",
        views.PasswordReset.as_view(),
        name="password-reset",
    ),
    re_path(
        r"^password-reset-done/",
        views.PasswordResetDone.as_view(),
        name="password-reset-done",
    ),
    re_path(
        r"^password-reset-verify/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/",
        views.PasswordResetVerify.as_view(),
        name="password-reset-verify",
    ),
    re_path(
        r"^password-reset-verify-done/",
        views.PasswordResetVerifyDone.as_view(),
        name="password-reset-verify-done",
    ),
    re_path(r"^jwt-tokens/", views.get_jwt_tokens_from_session, name="jwt-tokens"),
]
