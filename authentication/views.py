from django.urls import reverse
from django.template.loader import render_to_string
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from .models import User
from .forms import RegisterForm

from card.models import Card

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm

    template_name = 'authentication/register.html'

    def get_success_url(self) -> str:
        return reverse('dashboard')
    
    def form_valid(self, form):
        res = super().form_valid(form)
        user = self.object
        url = self.request.build_absolute_uri(reverse('dashboard'))
        html_message = render_to_string('email/register.html', {'user': user, 'url': url})
        send_mail(
            subject='Bienvenido a Ferreprodac, ' + user.first_name + ' ' + user.last_name,
            message='',
            from_email=None,
            html_message=html_message,
            recipient_list=[user.email]
        )
        return res

class SigninView(LoginView):

    def form_valid(self, form: None):
        res = super().form_valid(form)
        user = form.get_user()
        if not getattr(user, 'card', None):
            Card.objects.create(user=user)
        return res