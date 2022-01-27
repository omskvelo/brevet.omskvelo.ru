from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class UserAdmin(admin.ModelAdmin):
    autocomplete_fields = ['randonneur']


admin.site.register(User, UserAdmin)