from django.urls import path
from . import views

urlpatterns = [
    path('', views.UpdateUserView.as_view(), name='dashboard'),
    path('config/', views.UpdateCardView.as_view(), name='config'),
]
