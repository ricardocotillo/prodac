from django.core.mail import mail_admins, send_mail
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from card.forms import ContactForm

class Contactview(FormView):
    template_name = 'web/contact.html'
    form_class = ContactForm

    def form_valid(self, form = None):
        html_message = render_to_string('email/new_contact.html', {'contact': form.cleaned_data})
        send_mail(
            subject=_('Your message has been received'),
            message=_('I have received your message and I will contact you as soon as possible.'),
            from_email=None,
            recipient_list=[form.cleaned_data['email']]
        )
        mail_admins(
            subject='Contacto',
            message='',
            html_message=html_message,
        )
        return super().form_valid(form)
