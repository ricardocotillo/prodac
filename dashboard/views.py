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
from card.models import Card, Landing, Service, Template
from dashboard.models import AvailableSlots
from .forms import NotificationForm, OrganizationCreateForm
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
        'title',
        'phone',
        'whatsapp',
        'telegram',
        'address',
        'linkedin',
        'facebook',
        'twitter',
        'instagram',
        'youtube',
        'web',
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
        'qrcode',
        'color',
        'background',
        'logo',
        'icon',
        'icon_small',
        'description',
        'featured_image',
        'featured_text',
        'video',
    ]
    
    template_name = 'dashboard/card.html'

    def set_success_messages(self):
        return messages.success(self.request, _('Identicard updated successfully'))

    def get_success_url(self):
        return reverse('config')

    def get_form_class(self):
        if self.object.permission.allow_podcast:
            self.fields = self.fields[:9] + ['podcast'] + self.fields[9:]
        return super().get_form_class()

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
        try:
            card = self.request.user.card
            return card
        except ObjectDoesNotExist:
            templ = Template.objects.get(slug='first_template')
            card = Card.objects.create(user=self.request.user, template=templ)
            card.save()
        return self.request.user.card

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        services = self.object.services.all()
        ServiceFormSet = modelformset_factory(Service, exclude=('card',), extra=3, max_num=3, validate_max=True, min_num=1)
        ctx['formset'] = ServiceFormSet(queryset=services)
        ctx['card_url'] = self.request.build_absolute_uri(reverse('card', kwargs={'slug': self.object.slug}))
        return ctx

class UpdateServiceView(View):
    def get_response_messages(self):
        msgs = []
        storage = get_messages(self.request)
            
        for m in storage:
            msgs.append({
                'message': m.message,
                'level': m.level,
                'tags': m.tags,
                'extra_tags': m.extra_tags,
                'level_tag': m.level_tag,
            })

        return msgs

    def post(self, request):
        ctx = {}
        services = self.request.user.card.services.all()
        ServiceFormSet = modelformset_factory(Service, extra=3, exclude=('card',), max_num=3, validate_max=True, min_num=1)
        formset = ServiceFormSet(request.POST, request.FILES, queryset=services)
        if formset.is_valid():
            services = formset.save(commit=False)
            data = {}
            for form in formset:
                if form.has_changed():
                    if form.instance.pk is None:
                        service = form.save(commit=False)
                        service.card =  self.request.user.card
                        service.save()
                        data[form.prefix + '-id'] = service.pk
                    else:
                        form.save()
            messages.success(request, _('Services updated successfully'))
            ctx['messages'] = self.get_response_messages()
            ctx['data'] = data
        else:
            ctx['errors'] = formset.errors
            
        return JsonResponse(ctx)

def resize_image(image, size):
    img = Image.open(image)
    resized_img = img.resize(size)
    buffer = BytesIO()
    resized_img.save(buffer, format='JPEG')
    cf = ContentFile(buffer.getvalue())
    f = File(cf)
    return f

class UpdateImage(LoginRequiredMixin, JsonResponseMixin, UpdateView):
    login_url = '/authentication/login/'
    model = User
    fields = ['image',]
    template_name = 'components/alerts/form_errors.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self) -> str:
        return reverse('update')

    def set_success_messages(self):
        messages.success(self.request, _('Image updated successfully'))

    def get_response_data(self):
        return {'image': self.object.image.url}
    
    def form_valid(self, form):
        image = form.cleaned_data.get('image')
        card = self.object.card
        if not card.icon:
            icon_512 = resize_image(image, Card.ICON_512)
            self.object.card.icon.save(image.name, icon_512)

        if not card.icon_small:
            icon_192 = resize_image(image, Card.ICON_192)
            self.object.card.icon_small.save(image.name, icon_192)

        return super().form_valid(form)

class OrganizationDetailView(OrganizationDetail):
    template_name = 'dashboard/organization/organization.html'

    def get_context_data(self, **kwargs):
        context = {}
        organization_users = self.organization.organization_users.all()
        paginator = Paginator(organization_users, 10)
        page = self.request.GET.get('page', '1')
        context["organization_users"] = paginator.get_page(int(page))
        context["organization"] = self.organization
        is_admin = self.organization.is_admin(self.request.user)
        context['is_admin'] = is_admin
        if is_admin:
            context['form'] = OrganizationUserAddForm(self.request, self.organization)
        
        return context

    @cached_property
    def organization(self):
        org = Organization.objects.get_for_user(self.request.user).first()

        if org:
            return org
        else:
            raise Http404

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            return render(self.request, self.template_name, {'organization': False})

class OrganizationListView(ListView):
    template_name = 'dashboard/organization/organization_members.html'

    model = OrganizationUser

    paginate_by = 10


    context_object_name = 'organization_users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = self.organization.is_admin(self.request.user)
        return context

    @cached_property
    def organization(self):
        org = Organization.objects.get_for_user(self.request.user).first()
        if org:
            return org
        else:
            raise Http404
    
    def get_queryset(self):
        return self.organization.organization_users.all()
    

class OrganizationCreateView(OrganizationCreate):
    
    template_name = 'dashboard/organization/organization_create.html'
    form_class = OrganizationCreateForm

    def get_success_url(self):
        return reverse('organization')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            kwargs.update({"request": self.request})
        else:
            kwargs.update({'initial': {'email': self.request.user.email}})
        return kwargs


class OrganizationUserCreateView(AdminRequiredMixin, BaseOrganizationUserCreate):
    def get_success_url(self):
        return reverse('organization')
    @cached_property
    def organization(self):
        org = Organization.objects.get_for_user(self.request.user).first()
        if org:
            return org
        raise Http404

class BookingUpdateView(LoginRequiredMixin, JsonResponseMixin, UpdateView):
    model = AvailableSlots
    fields = [
        'range',
        'num_days',
        'holidays',
    ]

    template_name = 'dashboard/booking.html'

    def set_success_messages(self):
        messages.success(self.request, _('Booking settings updated successfully'))

    def get_object(self):
        available_slots, _ = AvailableSlots.objects.get_or_create(card=self.request.user.card)
        return available_slots

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['holidays'].widget = MultipleDatesWidget()
        return form

    def get_success_url(self) -> str:
        return reverse('booking')

class RemoveOrgUserView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        user_pk = kwargs.get('pk')
        user = User.objects.get(pk=user_pk)
        org = Organization.objects.get_for_user(self.request.user).first()
        org.remove_user(user)
        return redirect('organization')

class NotificationsView(LoginRequiredMixin, JsonResponseMixin, FormView):

    form_class = NotificationForm
    fields = '__all__'
    template_name = 'dashboard/notifications.html'

    firebase_app = firebase_admin.initialize_app()

    def get_success_url(self) -> str:
        return reverse('notifications')

    def form_valid(self, form):
        res = super().form_valid(form)
        registration_tokens = self.request.user.card.registration_ids
        icon = self.request.user.card.icon.url
        if settings.DEBUG:
            icon = self.request.build_absolute_uri(icon)
        link = form.cleaned_data.get('link')
        path = link if link else reverse('card', kwargs={'slug': self.request.user.card.slug})
        url = self.request.build_absolute_uri(path)
        badge = self.request.build_absolute_uri(static('icons/badge.png'))
        if len(registration_tokens) > 0:
            message = fcm.MulticastMessage(
                data={
                    'url': url,
                    'title':form.cleaned_data.get('title'),
                    'body':form.cleaned_data.get('message'),
                    'icon':icon,
                    'badge': badge,
                },
                tokens=registration_tokens,
            )
            fcm.send_multicast(message)
            messages.success(self.request, _('Notification sent successfully'))
        else:
            messages.info(self.request, _('No device to send to'))
        return res

class LandingUpdateView(LoginRequiredMixin, JsonResponseMixin, UpdateView):
    model = Landing
    fields = ['card', 'image']
    template_name = 'dashboard/landing.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['landing_url'] = self.request.build_absolute_uri(reverse('landing', kwargs={'pk': self.object.pk}))
        return ctx

    def get_object(self, queryset=None):
        landing, created = Landing.objects.get_or_create(card=self.request.user.card)
        if created:
            messages.info(self.request, _('We have created a new landing page for you'))
        return landing

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['card'].widget = HiddenInput()
        return form

    def set_success_messages(self):
        messages.success(self.request, 'Landing page updated correctly')
    
    def get_success_url(self) -> str:
        return reverse('landing_update')