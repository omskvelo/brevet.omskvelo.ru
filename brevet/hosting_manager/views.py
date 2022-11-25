from datetime import datetime, timedelta

from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

from .ruvds import rudvs_get_server_info, ruvds_get_balance, ruvds_get_payment_url


@login_required
@never_cache
def hosting(request):
    exception = ""
    try:
        balance = ruvds_get_balance()
    except Exception as e:
        balance = "Ошибка! {e}"

    try:
        server_info = rudvs_get_server_info()[0]
    except Exception as e:
        server_info = None
        exception = e

    context = {
        'balance': balance,
        'server_info': server_info,
        'payment_url': ruvds_get_payment_url(),
        'exception': exception,
        }      
    return render(request, "hosting_manager/hosting.html", context)   