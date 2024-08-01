from django.contrib import admin
from .models import *

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')

