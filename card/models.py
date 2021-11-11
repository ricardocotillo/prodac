from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.utils import make_file_path

class Card(models.Model):
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='card')
    name = models.CharField(max_length=250, default='FerreProdac')
    email = models.EmailField()
    logo = models.ImageField(upload_to=make_file_path, null=True, blank=True)
    background = models.ImageField(upload_to=make_file_path, null=True, blank=True, help_text=_('Suggested size: 1920x1080 px'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    google_map = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('phone'))
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('address'))

    def __str__(self) -> str:
        return self.user.email

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    image = models.ImageField(upload_to=make_file_path, null=True, blank=True, verbose_name=_('image'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, verbose_name=_('price'))
    card = models.ForeignKey('card.Card', on_delete=models.CASCADE, related_name='services')

    def __str__(self) -> str:
        return self.name
