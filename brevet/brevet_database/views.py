from datetime import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render
from django.views.decorators.cache import cache_page, never_cache
from django.db import connection

import babel.dates

from .models import *
from .forms import *
from . import file_generators


@never_cache
def protocol(request, distance, date, upload_success=None, form="html"):
    try:
        date = datetime.strptime(date, "%Y%m%d")
    except Exception:
        raise Http404
 

    event = get_object_or_404(Event, route__distance=distance, date=date)
    results = get_list_or_404(Result.objects.order_by("randonneur__russian_surname","randonneur__russian_name"), event=event)

    if form == "html":
        upload_exception = None
        if request.method == 'POST':
            form = ProtocolUploadForm(request.POST, request.FILES)
            if form.is_valid():
                upload_status, upload_exception = event.update_protocol_from_xls(request.FILES['xls'])
                if upload_status:
                    return redirect(event.get_protocol_upload_success_url())
        else:
            form = ProtocolUploadForm()

        context = {
            'event' : event,
            'results' : results,
            'form' : form,
            'upload_exception' : upload_exception,
            'upload_success' : upload_success,
            }      
        response = render(request, "brevet_database/protocol.html", context)   

    if form == "xlsx":
        response = file_generators.get_xlsx_protocol(event,results,f"{event.date.year}-{event.date.month}-{event.date.day}_{distance}") 



    return response

@never_cache
def protocol_index(request, year=datetime.now().year):
    years = get_event_years()
    if year not in years:
        year = max(years)
    events = get_list_or_404(Event, finished=True, club=DEFAULT_CLUB_ID, date__year=year)

    context = {
        "events" : events,
        "year" : year,
        "years" : years,
    }


    return render(request, "brevet_database/protocol_index.html", context)

@never_cache
def statistics_total(request, form="html"):
    return statistics(request, year=None, form=form)

# @cache_page(60*60)
@never_cache
def statistics(request, year=datetime.now().year, form="html"):
    years = get_event_years()
    if year:
        if year not in years:
            year = max(years)
        results = get_list_or_404(Result, event__finished=True, event__date__year=year)
    else:
        results = get_list_or_404(Result, event__finished=True)

    # LRM, SR600, 1000
    elite_dist = [x for x in results if x.event.route.lrm or x.event.route.sr600 or x.event.route.distance == 1000] 
    elite_dist = sorted(elite_dist, key=lambda x: x.event.date)

    # Personal stats 
    randonneurs = get_randonneurs(year)

    distance_rating = []
    for randonneur in randonneurs:
        distance_rating.append([randonneur, randonneur.get_total_distance(year=year), randonneur.get_total_brevets(year=year)])
    distance_rating = sorted(distance_rating, key=lambda x: x[1], reverse=True)

    sr = []
    for randonneur in randonneurs:
        if year:
            r = randonneur.set_sr_string([year])
        else:
            r = randonneur.set_sr_string(years)
        if r:
            sr.append(randonneur)            
    sr = sorted(sr, key=lambda x: x.sr_string, reverse=True)

    # Find best results
    best_200 = get_best(200,year=year)[:10]
    best_300 = get_best(300,year=year)[:10]
    best_400 = get_best(400,year=year)[:10]
    best_600 = get_best(600,year=year)[:10]

    # Calculate total stats
    total_sr = len(sr)
    total_randonneurs = len(randonneurs)
    total_distance = sum([result.event.route.distance for result in results])



    if form=="html":
        context = {
            "total_distance" : total_distance,
            "total_randonneurs" : total_randonneurs,
            "total_sr" : total_sr,
            "sr" : sr,
            "distance_rating" : distance_rating[:10],
            "best_200" : best_200,
            "best_300" : best_300,
            "best_400" : best_400,
            "best_600" : best_600,
            "elite_dist" : elite_dist,
            "years" : years,
            "year_min_to_max": str(years[-1]) + " - " + str(years[0])
        }
        if year is not None:
            context.update({
                "distance_rating" : distance_rating,
                "year" : year,
            })
        return render(request, "brevet_database/stats_club.html", context) 
    elif form=="xlsx":
        response = file_generators.get_xlsx_club_stats(
            total_distance,
            total_randonneurs,
            total_sr,
            sr,
            distance_rating,
            best_200,
            best_300,
            best_400,
            best_600,
            elite_dist,
            year,
            years,
            filename=f"{year if year else 'total'}")
        return response     
    else:
        raise Http404     
      

@never_cache
def event(request, distance, date):
    try:
        date = datetime.strptime(date, "%Y%m%d")
    except Exception:
        raise Http404

    event = get_object_or_404(Event, route__distance=distance, date=date, )
    route = event.route

    default_club = event.club.pk == DEFAULT_CLUB_ID

    context = {
        'event' : event,
        'route' : route,
        'default_club' : default_club,
        }  
    return render(request, "brevet_database/event.html", context)  

@never_cache
def event_index(request):
    events = get_list_or_404(Event.objects.order_by("date"), club=DEFAULT_CLUB_ID, finished=False)

    # Allocate events into a dict {year : {month: [events]}}
    years = {}
    for event in events:
        if event.date.year not in years:
            years[event.date.year] = {}
        m = babel.dates.format_date(event.date, "LLLL", locale='ru').capitalize()
        if m not in years[event.date.year]:
             years[event.date.year][m] = []
        years[event.date.year][m].append(event)

    context = {
        'events' : events,
        'years' : years,
    } 
    return render(request, "brevet_database/event_index.html", context)      

@never_cache
def route(request, slug=None, route_id=None):
    if slug:
        route = get_object_or_404(Route, slug=slug)
    elif route_id:
        route = get_object_or_404(Route, pk=route_id)
    else:
        raise Http404

    context = {
        'route' : route,
        }  
    return render(request, "brevet_database/route.html", context)       

@never_cache
def route_index(request, distance=200):
    routes = get_list_or_404(Route, active=True, distance=distance, club=DEFAULT_CLUB_ID)

    context = {
        'routes' : routes,
        'distance' : distance,
        'distances' : [200,300,400,600,1000],
    } 
    return render(request, "brevet_database/route_index.html", context)         

@never_cache
def personal_stats_index(request):
    randonneurs = get_randonneurs()

    distance_rating = []
    for randonneur in randonneurs:
        distance_rating.append([randonneur, randonneur.get_total_distance(), randonneur.get_total_brevets()])
    distance_rating = sorted(distance_rating, key=lambda x: x[1], reverse=True)

    context = {
        "distance_rating" : distance_rating,
    }
    return render(request, "brevet_database/stats_personal_index.html", context)    


@never_cache
def personal_stats(request, surname=None, name=None, uid=None, form="html"):
    if uid:
        randonneur = get_object_or_404(Randonneur, pk=uid)
    elif surname and name:
        surname = surname.lower().capitalize()
        name = name.lower().capitalize()
        randonneur = get_object_or_404(Randonneur, name=name, surname=surname)
    else:
        raise Http404

    results = sorted(randonneur.get_results(), key=lambda x: x.event.date, reverse=True)
    
    total_distance = randonneur.get_total_distance()
    total_brevets = len(results)
    
    elite_dist = [x for x in results if x.event.route.lrm or x.event.route.sr600 or x.event.route.distance == 1000] 
    
    best_200 = get_best(200, randonneur)
    best_300 = get_best(300, randonneur)
    best_400 = get_best(400, randonneur)
    best_600 = get_best(600, randonneur)

    years_active = randonneur.get_active_years()
    sr = []
    for year in years_active:
        for _ in range (randonneur.get_sr(year)):
            sr.append(year)  
    sr =  ", ".join(sr)

    years_active = ", ".join(years_active)

    if form=="html":
        context = {
            'randonneur' : randonneur,
            'results' : results,
            'elite_dist' : elite_dist,
            'best_200' : best_200[0] if best_200 else "",
            'best_300' : best_300[0] if best_300 else "",
            'best_400' : best_400[0] if best_400 else "",
            'best_600' : best_600[0] if best_600 else "",
            'years_active' : years_active,
            'sr' : sr,
            'total_distance' : total_distance,
            'total_brevets' : total_brevets,
            }  
        return render(request, "brevet_database/stats_personal.html", context)   
    if form=="xlsx":
        response =  file_generators.get_xlsx_personal_stats(
            randonneur, 
            years_active, 
            sr, 
            total_distance, 
            total_brevets, 
            results, 
            elite_dist, 
            best_200, 
            best_300, 
            best_400, 
            best_600,
            filename=f"{randonneur.surname} {randonneur.name}")
        return response
    else:
        raise Http404

@never_cache
def route_stats(request, slug=None, route_id=None):
    if slug:
        route = get_object_or_404(Route, slug=slug)
    elif route_id:
        route = get_object_or_404(Route, pk=route_id)
    else:
        raise Http404
    
    events = Event.objects.filter(route=route).order_by("date")
    results = Result.objects.filter(event__route=route).order_by("time")

    first_event = events.first
    total_events = len(events)
    total_results = len(results)

    context = {
        'route' : route,
        'first_event' : first_event,
        'results' : results,
        'total_events' : total_events,
        'total_results' : total_results,
        }  
    return render(request, "brevet_database/stats_route.html", context)  