from django.urls import path
from .views import CardDetailView, ProcessContact

urlpatterns = [
    path('<slug:slug>/', CardDetailView.as_view(), name='card'),
    path('<int:pk>/contact/', ProcessContact.as_view(), name='contact'),
]
