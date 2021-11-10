from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('update/', views.UpdateUserView.as_view(), name='update'),
    path('config/', views.UpdateCardView.as_view(), name='config'),
    path('update_image/', views.UpdateImage.as_view(), name='update_image'),
    path('organization/', views.OrganizationDetailView.as_view(), name='organization'),
    path('organization/add_member/', views.OrganizationUserCreateView.as_view(), name='organization_add_member'),
    path('organizations/', views.OrganizationCreateView.as_view(), name='organization_create'),
    path('organization/members/', views.OrganizationListView.as_view(), name='organization_members'),
    path('services/', views.UpdateServiceView.as_view(), name='services'),
    path('booking/', views.BookingUpdateView.as_view(), name='booking'),
    path('notifications/', views.NotificationsView.as_view(), name='notifications'),
    path('landing/', views.LandingUpdateView.as_view(), name='landing_update'),
    path('remove_orguser/<int:pk>/', views.RemoveOrgUserView.as_view(), name='remove_orguser'),
]
