from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import RegisterView, SigninView

urlpatterns = [
    path('login/', SigninView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
