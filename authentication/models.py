from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .utils import make_file_path

class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to=make_file_path, null=True, verbose_name=_('image'))
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('title'))
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('phone'))
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    web = models.URLField(blank=True, null=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('address'))

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username',]

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

class Permission(models.Model):
    LEVEL_STANDARD = 1
    LEVEL_ADVANCED = 2
    LEVEL_PRO = 3
    LEVELS = (
        (LEVEL_STANDARD, 'Standard'),
        (LEVEL_ADVANCED, 'Advanced'),
        (LEVEL_PRO, 'Professional'),
    )
    level = models.IntegerField(choices=LEVELS, default=LEVEL_STANDARD)
    name = models.CharField(max_length=255)
    default = models.BooleanField(default=False)
    allow_booking = models.BooleanField(default=False)
    allow_notifications = models.BooleanField(default=False)
    allow_landing = models.BooleanField(default=False)
    allow_services = models.BooleanField(default=False)
    allow_podcast = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name