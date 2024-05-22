"""
URL configuration for testing.
"""

from django.urls import include
from django.urls import re_path

urlpatterns = [
    re_path("accounts/", include("uniauth.urls", namespace="uniauth")),
]
