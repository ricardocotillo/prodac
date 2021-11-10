from django.urls import path
from django.views.generic import TemplateView
from .views import Contactview

urlpatterns = [
    path('', TemplateView.as_view(template_name='web/home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='web/about.html'), name='about'),
    path('contact/', Contactview.as_view(), name='contact'),
]
