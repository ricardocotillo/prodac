from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('update/', views.UpdateUserView.as_view(), name='update'),
    path('config/', views.UpdateCardView.as_view(), name='config'),
]
