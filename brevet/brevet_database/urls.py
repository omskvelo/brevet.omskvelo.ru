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
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("events/", views.event_index, name="event_index"),
    path("event/<int:distance>/<str:date>/", views.event, name="event"),

    path("protocols/", views.protocol_index, name="protocol_index"),
    path("protocols/<int:year>", views.protocol_index, name="protocol_index_pages"),
    path("protocol/<int:distance>/<str:date>/", views.protocol, name="protocol"),
    path("stats/club/total", views.stats_club_total, name="stats_club_total"),    
    path("stats/club/", views.stats_club, name="stats_club_pages"),
    path("stats/club/<int:year>", views.stats_club, name="stats_club_pages"),

    path("routes/", views.route_index, name="route_index"),
    path("routes/<int:distance>/", views.route_index, name="route_index_distance"),
    path("route/<str:slug>/", views.route, name="route"),
    path("route/id/<int:route_id>/", views.route, name="route_id"),

    path("user/<str:surname>_<str:name>/", views.personal_stats, name="personal_stats"),
]
