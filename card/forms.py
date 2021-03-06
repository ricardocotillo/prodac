from django import forms
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=100, label=_('Full name'))
    email = forms.EmailField(max_length=100)
    phone = forms.CharField(max_length=15, label=_('Phone'))
    message = forms.CharField(widget=forms.Textarea, label=_('Message'))