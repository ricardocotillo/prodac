from django.contrib import admin
from .models import Card, Product, RegistrationToken

class CardAdmin(admin.ModelAdmin):
    autocomplete_fields = ('products',)

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(Card, CardAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(RegistrationToken)