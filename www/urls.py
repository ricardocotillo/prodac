from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from organizations.backends import invitation_backend

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('card/', include('card.urls')),
    path('authentication/', include('authentication.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('organizations.urls')),
    path('invitations/', include(invitation_backend().get_urls())),
    path('firebase-messaging-sw.js', TemplateView.as_view(template_name='card/firebase-messaging-sw.js', content_type='application/javascript'), name='sw'),
    path('', include('web.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)