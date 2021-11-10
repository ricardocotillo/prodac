from django.template.loader import render_to_string
from dashboard.models import AvailableSlots
from django.utils.timezone import datetime, timedelta
from django.utils.translation import gettext as _
from typing import Any, Dict
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, CreateView
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail

from .models import Card, Landing
from .forms import ContactForm

from dashboard.models import Appointment
from dashboard.forms import AppointmentCreateForm
from dashboard.mixins import JsonResponseMixin

def home(req):
    if req.method == 'GET':
        return render(req, 'card/base.html')

class CardDetailView(DetailView):
    model = Card

    template_name = 'card/card_detail.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx['services'] = self.object.services.filter(active=True)
        form = AppointmentCreateForm()
        contact_form = ContactForm()
        ctx['form'] = form
        ctx['contact_form'] = contact_form
        ctx['card_url'] = self.request.build_absolute_uri(reverse('card', kwargs={'slug': self.object.slug})) 
        return ctx

class ServiceWorker(DetailView):
    model = Card
    template_name = 'card/pwa/serviceworker.js'
    content_type = 'application/javascript'

class Manifest(DetailView):
    model = Card
    template_name = 'card/pwa/manifest.json'
    content_type = 'application/json'

class RegistrationId(View):
    
    def post(self, request, *args, **kwargs):
        card_pk = kwargs.get('pk')
        registration_id = request.POST.get('registration_id')
        card = Card.objects.get(pk=card_pk)

        if registration_id not in card.registration_ids:
            card.registration_ids.append(registration_id)
            card.save()

        return JsonResponse({ 'registration_id': registration_id })

class Slots(View):
    def get(self, request, *args, **kwargs):
        card_pk = kwargs.get('pk')
        date = request.GET.get('date')
        date = datetime.fromisoformat(date).date()
        card = Card.objects.get(pk=card_pk)
        appointments = card.appointments.filter(date=date)
        available_slots, created = AvailableSlots.objects.get_or_create(card=card)
        holidays = available_slots.holidays
        is_holiday = date in holidays
        time_range = available_slots.range
        slots = {
            _('Slots available'): False
        }
        slots_range = int(10 // (time_range / 60))
        start = timedelta(hours=9)
        for t in range(9, 9 + slots_range):
            end = start + timedelta(minutes=time_range)
            start_str = str(start)
            end_str = str(end)
            slot_str = start_str[:len(start_str) - 3] + '-' + end_str[:len(end_str) - 3]
            slots[slot_str] = not is_holiday and not appointments.filter(slot=slot_str).exists()
            start = end
        return JsonResponse({'slots': slots})

class BookingCreateView(JsonResponseMixin, CreateView):
    model = Appointment
    fields = ('date', 'slot', 'name', 'email', 'phone', 'description', 'card')

    def get_success_url(self) -> str:
        return reverse('update')

    def set_success_messages(self):
        messages.success(self.request, _('Date booked successfully'))

class ProcessContact(JsonResponseMixin, View):

    def set_success_messages(self):
        return messages.success(self.request, _('Your message has been sent successfully'))

    def post(self, request, *args, **kwargs):
        card_pk = kwargs.get('pk')
        card = Card.objects.get(pk=card_pk)
        form = ContactForm(request.POST)
        if form.is_valid():
            html_message = render_to_string('email/new_contact.html', {'contact': form.cleaned_data})
            send_mail(
                subject=_('Your message has been received'),
                message=_('I have received your message and I will contact you as soon as possible.'),
                from_email=None,
                recipient_list=[form.cleaned_data['email']]
            )
            send_mail(
                subject=form.cleaned_data['full_name'] + _(' wants to contact you'),
                html_message=html_message,
                message='',
                from_email=None,
                recipient_list=[card.user.email]
            )
            card.contact_messages_count = card.contact_messages_count + 1
            card.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class LandingView(DetailView):
    model = Landing
    template_name = 'card/landing.html'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = ContactForm()
        return ctx

    def get(self, request, *args, **kwargs):
        res = super().get(request, *args, **kwargs)
        if self.object.card.permission.allow_landing:
            return res
        url = reverse('card', kwargs={'slug': self.object.card.slug})
        return redirect(url)