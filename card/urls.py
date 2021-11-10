from django.urls import path
from .views import CardDetailView, ProcessContact

urlpatterns = [
    path('<int:pk>/', CardDetailView.as_view(), name='card'),
    path('<int:pk>/contact/', ProcessContact.as_view(), name='contact'),
]
