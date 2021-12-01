from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from authentication.models import User
from card.models import Card
from .widgets import CropperWidget
from .mixins import JsonResponseMixin
from .forms import OrderForm

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
        'name',
        'email',
        'logo',
        'background',
        'description',
        'phone',
        'whatsapp',
        'facebook',
        'address',
    ]
    
    template_name = 'dashboard/card.html'

    def set_success_messages(self):
        return messages.success(self.request, 'Actualizado correctamente')

    def get_success_url(self):
        return reverse('config')

    def get_object(self):
        return self.request.user.card

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['card_url'] = self.request.build_absolute_uri(reverse('card', kwargs={'pk': self.object.pk}))
        return ctx

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields.get('logo').widget = CropperWidget()
        return form

class OrderView(LoginRequiredMixin, JsonResponseMixin, FormView):
    template_name = 'dashboard/order.html'

    form_class = OrderForm

    def set_success_messages(self):
        messages.success(self.request, 'Tu orden ha sido enviada con éxito')

    def get_success_url(self):
        return reverse('order')

    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = self.request.user.first_name + ' ' + self.request.user.last_name
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form=None):
        html_message = render_to_string('email/order.html', {'order': form.cleaned_data})
        send_mail(
            subject='Tu pedido ha sido enviado con éxito',
            message='Prodac ha recibido tu pedido y se contactará contigo a la brevedad.',
            from_email=None,
            recipient_list=[form.cleaned_data.get('email')],
            fail_silently=False,
        )
        send_mail(
            subject='Haz recibido un nuevo Pedido',
            message='',
            html_message=html_message,
            from_email=None,
            recipient_list=['ricardo.cotillo@gmail.com'],
            fail_silently=False,
        )
        return super().form_valid(form)