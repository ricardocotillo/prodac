from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import User
from card.models import Card
from .widgets import QuillWidget
from .mixins import JsonResponseMixin

class DashboardView(LoginRequiredMixin, View):
    login_url = '/authentication/login/'

    def get(self, req):
        return render(req, 'dashboard/dashboard.html', {'user': req.user})

class UpdateUserView(LoginRequiredMixin, JsonResponseMixin, UpdateView):
    login_url = '/authentication/login/'

    model = User
    fields = [
        'first_name',
        'last_name',
        'email',
    ]

    template_name = 'dashboard/update.html'

    def get_success_url(self) -> str:
        return reverse('update')

    def set_success_messages(self):
        messages.success(self.request, _('Profile updated successfully'))

    def get_object(self):
        return self.request.user

class UpdateCardView(LoginRequiredMixin, JsonResponseMixin, UpdateView):
    login_url = '/authentication/login/'

    model = Card
    fields = [
        'logo',
        'background',
        'description',
        'phone',
        'whatsapp',
        'facebook',
    ]
    
    template_name = 'dashboard/card.html'

    def set_success_messages(self):
        return messages.success(self.request, _('Identicard updated successfully'))

    def get_success_url(self):
        return reverse('config')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['description'].widget = QuillWidget()
        return form
    
    def form_valid(self, form):
        return super().form_valid(form)

    def get_object(self):
        return self.request.user.card

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['card_url'] = self.request.build_absolute_uri(reverse('card', kwargs={'pk': self.object.pk}))
        return ctx
