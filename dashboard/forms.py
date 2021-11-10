from django import forms
from django.contrib.postgres import fields
from django.utils.translation import gettext_lazy as _
from organizations.forms import OrganizationAddForm
from card.models import Landing
from .models import Appointment

class OrganizationCreateForm(OrganizationAddForm):
    email = forms.EmailField(
        required=True,
        max_length=75,
        help_text=_("The email address for the account owner"),
        widget=forms.EmailInput(attrs={'readonly': True})
    )

class AppointmentCreateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('date', 'slot', 'name', 'email', 'phone', 'description',)
        widgets = {
            'slot': forms.Select(choices=[], attrs={})
        }

class NotificationForm(forms.Form):
    title = forms.CharField(max_length=50, help_text=_('Maximun characters: 50'))
    message = forms.CharField(max_length=126, help_text=_('Maximun characters: 126'))
    link = forms.URLField(required=False, help_text=_('You can provide a link to redirect your users upon clicking on notification'))