from django.contrib import admin

from .models import Club, Randonneur, Route, Event, Result, Application

admin.site.register(Club)
admin.site.register(Randonneur)
admin.site.register(Route)
admin.site.register(Event)
admin.site.register(Result)
admin.site.register(Application)


# Register your models here.
