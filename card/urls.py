from django.urls import path
from .views import BookingCreateView, CardDetailView, LandingView, Manifest, ProcessContact, RegistrationId, Slots

urlpatterns = [
    path('<slug:slug>/', CardDetailView.as_view(), name='card'),
    path('<int:pk>/manifest.json', Manifest.as_view(), name='manifest'),
    path('<int:pk>/registration_id/', RegistrationId.as_view(), name='registration_id'),
    path('<int:pk>/card_available_slots/', Slots.as_view(), name='card_available_slots'),
    path('<int:pk>/book_date/', BookingCreateView.as_view(), name='book_date'),
    path('<int:pk>/contact/', ProcessContact.as_view(), name='contact'),
    path('<int:pk>/landing/', LandingView.as_view(), name='landing'),
]
