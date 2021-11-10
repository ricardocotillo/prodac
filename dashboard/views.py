from io import BytesIO
from PIL import Image
import firebase_admin
from django.views.generic.edit import FormView
from django.conf import settings
from firebase_admin import messaging as fcm
from django.contrib.messages.api import get_messages
from django.forms import HiddenInput
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.core.files.base import ContentFile
from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from django.contrib import messages
from django.http.response import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.templatetags.static import static
from organizations.views.default import OrganizationCreate, OrganizationDetail
from organizations.forms import OrganizationUserAddForm
from organizations.models import Organization, OrganizationUser
from organizations.views.base import BaseOrganizationUserCreate
from organizations.views.mixins import AdminRequiredMixin
from authentication.models import User
from card.models import Card
from .widgets import CropperWidget, MultipleDatesWidget, ColorInput, QuillWidget
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
        'background',
        'logo',
        'description',
    ]
    
    template_name = 'dashboard/card.html'

    def set_success_messages(self):
        return messages.success(self.request, _('Identicard updated successfully'))

    def get_success_url(self):
        return reverse('config')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['description'].widget = QuillWidget()
        form.fields['featured_text'].widget = QuillWidget()
        form.fields['color'].widget = ColorInput()
        form.fields['icon'].widget = CropperWidget(attrs={'data-width': 512, 'data-height': 512})
        form.fields['icon_small'].widget = CropperWidget(attrs={'data-width': 192, 'data-height': 192})
        return form
    
    def form_valid(self, form):
        return super().form_valid(form)

    def get_object(self):
        return self.request.user.card

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['card_url'] = self.request.build_absolute_uri(reverse('card', kwargs={'pk': self.object.pk}))
        return ctx
