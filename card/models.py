from django.contrib import messages
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext_lazy as _

from authentication.utils import make_file_path

class Template(models.Model):
    name = models.CharField(max_length=300, verbose_name=_('name'))
    slug = AutoSlugField(populate_from='name', separator='_')

    def __str__(self) -> str:
        return self.name

class Card(models.Model):

    ICON_512 = (512, 512)
    ICON_192 = (192, 192)

    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='card')
    slug = AutoSlugField(populate_from=['user__first_name', 'user__last_name'], editable=True)
    color = models.CharField(max_length=15, default='#8BB53C', help_text=_('Determine the primary color of your Identicard'))
    logo = models.ImageField(upload_to=make_file_path, null=True, blank=True)
    icon = models.ImageField(upload_to=make_file_path, null=True, blank=True, help_text=_('This icon will show as app icon. 512x512 px'), verbose_name=_('icon'))
    icon_small = models.ImageField(upload_to=make_file_path, null=True, blank=True, help_text=_('This icon will show as app icon. 192x192 px'), verbose_name=_('icon small'))
    background = models.ImageField(upload_to=make_file_path, null=True, blank=True, help_text=_('Suggested size: 1920x1080 px'))
    external_catalog_link = models.URLField(null=True, blank=True, verbose_name=_('external catalog link'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    featured_image = models.ImageField(upload_to=make_file_path, null=True, blank=True, verbose_name=_('featured image'))
    featured_text = models.TextField(null=True, blank=True, verbose_name=_('featured text'))
    video = models.URLField(null=True, blank=True, help_text=_('This fields only accepts Youtube links'))
    podcast = models.URLField(null=True, blank=True, help_text=_('Paste spotify link to playlist'))
    qrcode = models.FileField(upload_to=make_file_path, null=True, blank=True, verbose_name=_('qr code'))
    registration_ids = ArrayField(models.CharField(max_length=500), blank=True, default=list)
    contact_messages_count = models.IntegerField(default=0)
    permission = models.ForeignKey('authentication.Permission', related_name='cards', on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.user.email

class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    image = models.ImageField(upload_to=make_file_path, null=True, blank=True, verbose_name=_('image'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, verbose_name=_('price'))
    card = models.ForeignKey('card.Card', on_delete=models.CASCADE, related_name='services')
    active = models.BooleanField(default=True, verbose_name=_('active'))

    def __str__(self) -> str:
        return self.name

class Landing(models.Model):
    card = models.OneToOneField('card.Card', on_delete=models.CASCADE, related_name='landing')
    image = models.ImageField(upload_to=make_file_path, null=True, blank=True, help_text=_('Suggested proportion: 9:16'))
    message = models.CharField(max_length=150, null=True, blank=True, help_text=_('Maximun characters: 150'))