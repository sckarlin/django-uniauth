from _typeshed import Incomplete
from typing import Any

from django.conf import settings as settings
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user: models.OneToOneField
    def get_display_id(self) -> str: ...

def create_user_profile(
        sender: Any,
        instance: User,
        created: bool,
        **_kwargs: Any,
) -> None: ...

def clear_old_tmp_users(
        sender: Any,
        instance: Any,
        created: bool,
        **_kwargs: Any,
) -> None: ...

class LinkedEmail(models.Model):
    profile: Incomplete
    address: Incomplete
    is_verified: Incomplete
    def clean(self) -> None: ...

class Institution(models.Model):
    name: Incomplete
    slug: Incomplete
    cas_server_url: Incomplete

class InstitutionAccount(models.Model):
    profile: Incomplete
    institution: Incomplete
    cas_id: Incomplete
    class Meta:
        unique_together: Incomplete
