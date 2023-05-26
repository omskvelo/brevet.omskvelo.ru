from django.contrib import admin

from inventory.models import Medal, Price


class MedalAdmin(admin.ModelAdmin):
    autocomplete_fields = ['randonneur']
 
    
admin.site.register(Medal, MedalAdmin)
admin.site.register(Price)