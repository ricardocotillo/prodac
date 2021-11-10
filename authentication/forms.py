from django.contrib.auth.forms import UserCreationForm
from .models import User, Permission
from card.models import Card


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)
    

    def save(self, commit=True):
        user = super().save(commit=commit)
        perm = Permission.objects.filter(default=True).first()
        Card.objects.create(user=user, permission=perm)
        return user