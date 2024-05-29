from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class UserProfile(models.Model):
    """
    Extension of the default User model containing
    extra information necessary for UniAuth to run.
    """

    # User this profile is extending
    user = models.OneToOneField(
        get_user_model(),
        related_name="uniauth_profile",
        on_delete=models.CASCADE,
        null=False,
    )

    def get_display_id(self):
        """
        Returns a display-friendly ID for this User, using their
        username. Users created via CAS authentication will have
        their CAS ID returned (without the cas-institution prefix),
        and Users with an email address for a username will have
        the string preceding the "@" returned. All other users
        will have their raw username returned.

        Note that these IDs are not guaranteed to be unique.
        """
        username = self.user.username  # type: ignore
        if "@" in username:
            return username.split("@")[0]
        if username.startswith("cas-"):
            from uniauth.utils import get_account_username_split

            return get_account_username_split(username)[-1]
        return username

    def __str__(self):
        try:
            return self.user.email or self.user.username  # type: ignore
        except AttributeError:
            return "NULL"


@receiver(post_save, sender=get_user_model())
def create_user_profile(_sender, instance, created, **_kwargs):
    """
    Create a Uniauth profile automatically when a User is created.

    If the User was given an email on creation, add it as a verified
    LinkedEmail immediately.
    """
    if created:
        profile = UserProfile.objects.create(user=instance)
        if profile and instance.email:
            LinkedEmail.objects.create(
                profile=profile, address=instance.email, is_verified=True
            )


@receiver(post_save, sender=get_user_model())
def clear_old_tmp_users(_sender, _instance, created, **_kwargs):
    """
    Deletes temporary users more than PASSWORD_RESET_TIMEOUT_DAYS
    old when a User is created.

    Does nothing if the user model does not have date_joined field.
    """
    if created:
        user_model = get_user_model()
        if hasattr(user_model, "date_joined"):
            from uniauth.utils import get_setting

            timeout_days = timedelta(
                days=get_setting("PASSWORD_RESET_TIMEOUT_DAYS")
            )
            tmp_expire_date = (timezone.now() - timeout_days).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            user_model.objects.filter(
                username__startswith="tmp-", date_joined__lt=tmp_expire_date
            ).delete()


class LinkedEmail(models.Model):
    """
    Represents an email address linked to a user's account.
    """

    # Person owning this email
    profile = models.ForeignKey(
        "UserProfile",
        related_name="linked_emails",
        on_delete=models.CASCADE,
        null=False,
    )

    # The email address
    address = models.EmailField(null=False, blank=False)

    # Whether the linked email is verified
    is_verified = models.BooleanField(default=False)

    def clean(self):
        """
        Ensures an email can't be linked and verified for multiple
        accounts if UNIAUTH_ALLOW_SHARED_EMAILS is False.

        Also ensures a user does not link more than the maximum
        number of linked emails per user.
        """
        from uniauth.utils import get_setting

        # Check for shared emails if necessary
        if (
            not get_setting("UNIAUTH_ALLOW_SHARED_EMAILS")
            and LinkedEmail.objects.filter(
                address=self.address, is_verified=True
            )
            and self.is_verified
        ):
            raise ValidationError(
                "This email address has already been "
                + "linked to another account."
            )

        # Ensure a user doesn't link more than the maximum
        max_linked_emails = get_setting("UNIAUTH_MAX_LINKED_EMAILS")
        if max_linked_emails > 0:
            if self.profile.linked_emails.count() >= max_linked_emails:
                raise ValidationError(
                    f"You can not link more than {max_linked_emails} "
                    f"emails to your account."
                )
        super().clean()

    def __str__(self):
        try:
            return "%s | %s" % (self.profile, self.address)
        except AttributeError:
            return "NULL"


class Institution(models.Model):
    """
    Represents an organization holding a CAS server
    that can be logged into.
    """

    # Name of the institution
    name = models.CharField(max_length=30, null=False, blank=False)

    # Slugified version of name
    slug = models.CharField(
        max_length=30, null=False, blank=False, unique=True
    )

    # CAS server location
    cas_server_url = models.URLField(null=False, blank=False)

    def __str__(self):
        try:
            return self.slug
        except AttributeError:
            return "NULL"


class InstitutionAccount(models.Model):
    """
    Relates users to the accounts they have at
    institutions, and stores any associated data.
    """

    # The person the account is for
    profile = models.ForeignKey(
        "UserProfile",
        related_name="accounts",
        on_delete=models.CASCADE,
        null=False,
    )

    # The institution the account is with
    institution = models.ForeignKey(
        "Institution",
        related_name="accounts",
        on_delete=models.CASCADE,
        null=False,
    )

    # The ID used by the CAS server
    cas_id = models.CharField(max_length=30, null=False, blank=False)

    class Meta:
        unique_together = ("institution", "cas_id")

    def __str__(self):
        try:
            return "%s | %s | account" % (self.profile, self.institution)
        except AttributeError:
            return "NULL"
