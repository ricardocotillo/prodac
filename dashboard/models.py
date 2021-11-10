import datetime

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

class Appointment(models.Model):
    card = models.ForeignKey('card.Card', on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField(verbose_name=_('date'))
    slot = models.CharField(max_length=11, verbose_name=_('slot'))
    name = models.CharField(max_length=100, verbose_name=_('name'))
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name=_('phone'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))

    class Meta:
        constraints = [models.UniqueConstraint(fields=['email', 'date', 'slot'], name='unique_booking')]

class AvailableSlots(models.Model):
    START_DEFAULT = datetime.time(9, 00)
    END_DEFAULT = datetime.time(19, 00)
    NUM_DAYS_DEFAULT = 7
    RANGE_30 = 30
    RANGE_40 = 40
    RANGE_50 = 50
    RANGE_60 = 60
    RANGE_90 = 90
    RANGE_120 = 120
    RANGE_CHOICES = (
        (RANGE_30, '30 min'),
        (RANGE_40, '40 min'),
        (RANGE_50, '50 min'),
        (RANGE_60, '60 min'),
        (RANGE_90, '90 min'),
        (RANGE_120, '120 min'),
    )
    card = models.OneToOneField('card.Card', on_delete=models.CASCADE, related_name='slots')
    range = models.IntegerField(choices=RANGE_CHOICES, default=RANGE_60, verbose_name=_('range'), help_text=_('Slots range'))
    num_days = models.IntegerField(default=NUM_DAYS_DEFAULT, verbose_name=_('number of days'), help_text=_('Max number of days in th future allowed'))
    holidays = ArrayField(models.DateField(auto_now=False, auto_now_add=False), default=list, verbose_name=_('holidays'), help_text=_('Holidays or not working days'))
    monday = models.JSONField(default=dict, verbose_name=_('monday'))
    tuesday = models.JSONField(default=dict, verbose_name=_('tuesday'))
    wednesday = models.JSONField(default=dict, verbose_name=_('wednesday'))
    thursday = models.JSONField(default=dict, verbose_name=_('thursday'))
    friday = models.JSONField(default=dict, verbose_name=_('friday'))
    saturday = models.JSONField(default=dict, verbose_name=_('saturday'))
    sunday = models.JSONField(default=dict, verbose_name=_('sunday'))
