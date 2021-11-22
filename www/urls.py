from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('card/', include('card.urls')),
    path('authentication/', include('authentication.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('serviceworker', TemplateView.as_view(template_name='card/serviceworker.js'), name='sw'),
    path('', include('web.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)