from django.contrib import admin
from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path("events/", views.event_index, name="event_index"),
    path("event/<int:event_id>/", views.event, name="event"),
    path("event/<int:distance>/<str:date>/", views.event, name="event_by_params"),
    path("event/<int:event_id>/register", views.event_register, name="event_register"),
    path("event/<int:event_id>/cancel_registration", views.event_cancel_registration, name="event_cancel_registration"),
    path("event/<int:event_id>/dnf", views.event_dnf, name="event_dnf"),
    path("hx/event/<int:event_id>/participants/", views.hx_event_load_participants, name="hx_event_load_participants"),
    path("hx/event/<int:event_id>/participants/apply", views.hx_event_create_application, name="hx_event_create_application"),
    path("hx/event/<int:event_id>/participants/cancel", views.hx_event_delete_application, name="hx_event_delete_application"),
    path("hx/event/<int:event_id>/payment_info/", views.hx_event_payment_info, name='hx_event_payment_info'),

    path("protocols/", views.protocol_index, name="protocol_index"),
    path("protocols/<int:year>", views.protocol_index, name="protocol_index_pages"),
    path("hx/protocols/<int:year>", views.hx_protocol_index, name="hx_protocol_index_pages"),

    path("protocol/<int:event_id>/success/", views.protocol, kwargs={'upload_success' : True}, name="protocol_upload_success"),
    path("protocol/<int:event_id>/", views.protocol, name="protocol"),
    path("protocol/<int:event_id>/<str:form>", views.protocol, name="protocol_f"),
    path("protocol/yearly/<int:year>", views.protocol_yearly, name="protocol_yearly"),

    path("routes/", views.route_index, name="route_index"), 
    path("routes/<int:distance>/", views.route_index, name="route_index_distance"),
    path("hx/routes/<int:distance>/", views.hx_route_index, name="hx_route_index_distance"),

    path("route/<int:route_id>/", views.route, name="route_id"), 
    path("route/<str:slug>/", views.route, name="route"), # Alternative

    path("stats/route/<int:route_id>/", views.route_stats, name="stats_route_id"), 
    path("stats/route/<str:slug>/", views.route_stats, name="stats_route"), # Alternative

    path("stats/club/total/", views.statistics_total, name="statistics_total"),    
    path("stats/club/total/<str:form>/", views.statistics_total, name="statistics_total_f"), 
    path("stats/club/", views.statistics, name="statistics_default"),
    path("stats/club/<int:year>/", views.statistics, name="statistics"),
    path("stats/club/<str:form>/", views.statistics, name="statistics_default_f"),    
    path("stats/club/<int:year>/<str:form>/", views.statistics, name="statistics_f"),
    path("hx/stats/club/total", views.hx_statistics, name="hx_statistics_total"),
    path("hx/stats/club/<int:year>", views.hx_statistics, name="hx_statistics"),
    path("hx/stats/club/distance_rating/", views.hx_statistics_distance_rating, name="hx_statistics_distance_rating_total"),
    path("hx/stats/club/distance_rating/<int:year>", views.hx_statistics_distance_rating, name="hx_statistics_distance_rating"),
    path("hx/stats/club/best/<int:distance>/<int:year>", views.hx_statistics_best_x00, name="hx_statistics_best_x00"),
    path("hx/stats/club/best/<int:distance>/", views.hx_statistics_best_x00, name="hx_statistics_best_x00_total"),

    path("stats/user/", views.personal_stats_index, name = "personal_stats_index"),
    path("stats/user/<int:uid>/", views.personal_stats, name="personal_stats"), 
    path("stats/user/<int:uid>/<str:form>/", views.personal_stats, name="personal_stats_f"), 
    path("stats/user/<str:surname>_<str:name>/", views.personal_stats, name="person_by_name"), 
    path("hx/stats/user/<int:line>/", views.hx_personal_stats_page, name = "hx_personal_stats_page"),

]
