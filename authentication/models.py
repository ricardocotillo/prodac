from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username',]

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
