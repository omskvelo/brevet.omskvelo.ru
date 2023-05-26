from django.contrib import admin

from inventory.models import Medal


class MedalAdmin(admin.ModelAdmin):
    autocomplete_fields = ['randonneur']
 
    
admin.site.register(Medal, MedalAdmin)