import re

from django.contrib import admin
from django import forms

from .models import Club, Randonneur, Route, Event, Result, Application

result_pattern = re.compile("^\d\d\:\d\d$")

class AdminResultForm(forms.ModelForm):
    def __init__(self, data=None, *args, **kwargs):
        if data:
            data = data.copy()
            data['time'] = data['time'].strip()
            if result_pattern.match(data['time']):
                data['time'] += ":00"
        super().__init__(data, *args, **kwargs)

    class Meta:
        model = Randonneur
        exclude = []

class ResultAdmin(admin.ModelAdmin):
    form = AdminResultForm
    autocomplete_fields = ['randonneur']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        default_event = Event.objects.filter(finished=False).order_by("date").first()
        if default_event:
            form.base_fields['event'].initial = default_event
        return form        

class RandonneurAdmin(admin.ModelAdmin):
    search_fields = ['russian_surname', 'russian_name']

class ApplicationAdmin(admin.ModelAdmin):
    raw_id_fields = ['result']

admin.site.register(Club)
admin.site.register(Randonneur, RandonneurAdmin)
admin.site.register(Route)
admin.site.register(Event)
admin.site.register(Result, ResultAdmin)
admin.site.register(Application, ApplicationAdmin)