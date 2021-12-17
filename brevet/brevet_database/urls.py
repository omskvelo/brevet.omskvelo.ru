"""brevet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path("events/", views.event_index, name="event_index"),
    path("event/<int:distance>/<str:date>/", views.event, name="event"),

    path("protocols/", views.protocol_index, name="protocol_index"),
    path("protocols/<int:year>", views.protocol_index, name="protocol_index_pages"),
    path("protocol/<int:distance>/<str:date>/", views.protocol, name="protocol"),
    path("protocol/xlsx/<int:distance>/<str:date>/", views.protocol_xlsx, name="protocol_xlsx"),
    # path("protocol/upload/<int:distance>/<str:date>/", views.protocol_upload, name="protocol_upload"),

    path("routes/", views.route_index, name="route_index"), 
    path("routes/<int:distance>/", views.route_index, name="route_index_distance"),

    path("route/<int:route_id>/", views.route, name="route_id"), 
    path("route/<str:slug>/", views.route, name="route"), # Alternative route url

    path("stats/club/total/", views.statistics_total, name="statistics_total"),    
    path("stats/club/total/<str:form>/", views.statistics_total, name="statistics_total_f"), 
    path("stats/club/", views.statistics, name="statistics_default"),
    path("stats/club/<int:year>/", views.statistics, name="statistics"),
    path("stats/club/<str:form>/", views.statistics, name="statistics_default_f"),    
    path("stats/club/<int:year>/<str:form>/", views.statistics, name="statistics_f"),

    path("stats/user/<int:uid>/", views.personal_stats, name="personal_stats"), 
    path("stats/user/<int:uid>/<str:form>/", views.personal_stats, name="personal_stats_f"), 
    path("stats/user/<str:surname>_<str:name>/", views.personal_stats, name="person_by_name"), 
]
