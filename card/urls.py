from django.urls import path
from .views import CardDetailView, ProcessContact, ManifestView

urlpatterns = [
    path('<int:pk>/', CardDetailView.as_view(), name='card'),
    path('<int:pk>/contact/', ProcessContact.as_view(), name='contact'),
    path('<int:pk>/manifest/', ManifestView.as_view(), name='manifest'),
]
