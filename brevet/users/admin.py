from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect

from .models import User

class UserAdmin(admin.ModelAdmin):
    autocomplete_fields = ['randonneur']
    change_form_template = 'admin/change_user.html'

    def response_change(self, request, obj):
        if "_generate-randonneur" in request.POST:

            if (obj.create_randonneur()):
                obj.save()
                self.message_user(request, "Рандоннёр сгенерирован успешно!")
                return super().response_change(request, obj)
            else:
                self.message_user(request, "Невозможно сгенерировать рандоннёра. К учетной записи уже привязан рандоннёр.", level="ERROR")
                return HttpResponseRedirect(".")

        return super().response_change(request, obj)


admin.site.register(User, UserAdmin)