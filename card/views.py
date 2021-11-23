from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.shortcuts import render
from django.views.generic import DetailView
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Card
from .forms import ContactForm

from dashboard.mixins import JsonResponseMixin

def home(req):
    if req.method == 'GET':
        return render(req, 'card/base.html')

class CardDetailView(DetailView):
    model = Card

    template_name = 'card/card_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        contact_form = ContactForm()
        ctx['contact_form'] = contact_form
        ctx['vapid_key'] = settings.VAPIDKEY
        ctx['card_url'] = self.request.build_absolute_uri(reverse('card', kwargs={'pk': self.object.pk})) 
        return ctx

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

class CreateRegistration(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        t = request.POST.get('token')
        card = Card.objects.get(pk=pk)
        token, created = card.tokens.get_or_create(token=t)
        return JsonResponse({'token': token.token, 'card': token.card_id})

class ManifestView(DetailView):
    model = Card
    template_name = "card/manifest.json"
