from django.contrib import admin
from .models import Card, Product, RegistrationToken

admin.site.register(Card)
admin.site.register(Product)
admin.site.register(RegistrationToken)