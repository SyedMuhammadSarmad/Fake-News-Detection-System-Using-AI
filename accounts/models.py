from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Extends Django's built-in User with a 'verified' flag.
    Admin must set verified=True before the user can access the system.
    """
    verified = models.BooleanField(
        default=False,
        help_text='Admin must verify this account before the user can log in.'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.username} ({"verified" if self.verified else "pending"})'
