from django.contrib import admin
from .models import Service, Appointment

admin.site.register((Service, Appointment))