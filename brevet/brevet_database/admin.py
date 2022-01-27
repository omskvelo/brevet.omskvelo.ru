from re import search
from django.contrib import admin

from .models import Club, Randonneur, Route, Event, Result, Application

class ResultAdmin(admin.ModelAdmin):
    autocomplete_fields = ['randonneur']

class RandonneurAdmin(admin.ModelAdmin):
    search_fields = ['russian_surname', 'russian_name']

admin.site.register(Club)
admin.site.register(Randonneur, RandonneurAdmin)
admin.site.register(Route)
admin.site.register(Event)
admin.site.register(Result, ResultAdmin)
admin.site.register(Application)

