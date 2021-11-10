from django.contrib import admin
from .models import AvailableSlots, Appointment

admin.site.register(AvailableSlots)
admin.site.register(Appointment)