from django.contrib import admin
from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path("events/", views.event_index, name="event_index"),
    path("event/<int:distance>/<str:date>/register", views.event_register, name="event_register"),
    path("event/<int:distance>/<str:date>/cancel_registration", views.event_cancel_registration, name="event_cancel_registration"),
    path("event/<int:distance>/<str:date>/dnf", views.event_dnf, name="event_dnf"),
    path("event/<int:distance>/<str:date>/", views.event, name="event"),


    path("protocols/", views.protocol_index, name="protocol_index"),
    path("protocols/<int:year>", views.protocol_index, name="protocol_index_pages"),
    path("protocol/<int:distance>/<str:date>/success/", views.protocol, kwargs={'upload_success' : True}, name="protocol_upload_success"),
    path("protocol/<int:distance>/<str:date>/", views.protocol, name="protocol"),
    path("protocol/<int:distance>/<str:date>/<str:form>", views.protocol, name="protocol_f"),

    path("routes/", views.route_index, name="route_index"), 
    path("routes/<int:distance>/", views.route_index, name="route_index_distance"),

    path("route/<int:route_id>/", views.route, name="route_id"), 
    path("route/<str:slug>/", views.route, name="route"), # Alternative route url

    path("stats/route/<int:route_id>/", views.route_stats, name="stats_route_id"), 
    path("stats/route/<str:slug>/", views.route_stats, name="stats_route"), # Alternative route url

    path("stats/club/total/", views.statistics_total, name="statistics_total"),    
    path("stats/club/total/<str:form>/", views.statistics_total, name="statistics_total_f"), 
    path("stats/club/", views.statistics, name="statistics_default"),
    path("stats/club/<int:year>/", views.statistics, name="statistics"),
    path("stats/club/<str:form>/", views.statistics, name="statistics_default_f"),    
    path("stats/club/<int:year>/<str:form>/", views.statistics, name="statistics_f"),

    path("stats/user/", views.personal_stats_index, name = "personal_stats_index"),
    path("stats/user/<int:uid>/", views.personal_stats, name="personal_stats"), 
    path("stats/user/<int:uid>/<str:form>/", views.personal_stats, name="personal_stats_f"), 
    path("stats/user/<str:surname>_<str:name>/", views.personal_stats, name="person_by_name"), 
]
