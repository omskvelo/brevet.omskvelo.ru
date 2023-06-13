import re

from django.contrib import admin
from django import forms
from django.http import HttpResponseRedirect

from .models import *

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
    change_form_template = 'admin/change_randonneur.html'

    def response_change(self, request, obj):
        if "_update_stats" in request.POST:
            if (obj.update_stats()):
                self.message_user(request, "Статистика успешно обновлена")
                return super().response_change(request, obj)
            else:
                self.message_user(request, "Что-то пошло не так", level="ERROR")
                return HttpResponseRedirect(".")

        return super().response_change(request, obj)

class ApplicationAdmin(admin.ModelAdmin):
    raw_id_fields = ['result']
    autocomplete_fields = ['user', 'event']

class EventAdmin(admin.ModelAdmin):
    search_fields = ['route__name']

admin.site.register(Club)
admin.site.register(Randonneur, RandonneurAdmin)
admin.site.register(Route)
admin.site.register(Event, EventAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(PaymentInfo)
admin.site.register(ClubStatsCache)
admin.site.register(PersonalStatsChart)