from datetime import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.views.decorators.cache import cache_page, never_cache

import babel.dates

from .models import *
from . import file_generators

@never_cache
def protocol(request, distance, date):
    try:
        date = datetime.strptime(date, "%Y%m%d")
    except Exception:
        raise Http404

    event = get_object_or_404(Event, route__distance=distance, date=date)
    results = get_list_or_404(Result.objects.order_by("randonneur__russian_surname","randonneur__russian_name"), event=event)

    context = {
        'event' : event,
        'results' : results,
        }      
    return render(request, "brevet_database/protocol.html", context)   

@never_cache
def protocol_xlsx(request,distance, date):
    try:
        date = datetime.strptime(date, "%Y%m%d")
    except Exception:
        raise Http404

    event = get_object_or_404(Event, route__distance=distance, date=date, )
    results = get_list_or_404(Result, event=event)
    response = file_generators.get_xlsx_protocol(event,results,f"{date.year}-{date.month}-{date.day}_{distance}") 

    return response

@never_cache
def protocol_index(request, year=datetime.now().year):
    events = get_list_or_404(Event.objects.order_by("date"), finished=True, club=DEFAULT_CLUB_ID, date__year=year)
    years = get_event_years(reverse=True)

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
    if year:
        results = get_list_or_404(Result, event__finished=True, event__date__year=year)
    else:
        results = get_list_or_404(Result, event__finished=True)
    years = get_event_years(reverse=True)

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
            s = randonneur.get_sr(year)
            if s:
                randonneur.sr_string = f"(x{s})" if s > 1 else ""
                sr.append(randonneur)
        else:
            for year in years:
                s = randonneur.get_sr(year)
                if s:
                    randonneur.sr_string = f"(x{s})"
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
            "distance_rating" : distance_rating,
            "best_200" : best_200,
            "best_300" : best_300,
            "best_400" : best_400,
            "best_600" : best_600,
            "elite_dist" : elite_dist,
        }
        if year is not None:
            context.update({
                "year" : year,
                "years" : years,
            })
        return render(request, "brevet_database/statistics.html", context) 
    if form=="xlsx":
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

    context = {
        'event' : event,
        'route' : route,
        }  
    return render(request, "brevet_database/event.html", context)  

@never_cache
def event_index(request):
    events = get_list_or_404(Event, club=DEFAULT_CLUB_ID, finished=False)

    # Get dict with localized month names as keys
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
            'best_200' : best_200[0],
            'best_300' : best_300[0],
            'best_400' : best_400[0],
            'best_600' : best_600[0],
            'years_active' : years_active,
            'sr' : sr,
            'total_distance' : total_distance,
            'total_brevets' : total_brevets,
            }  
        return render(request, "brevet_database/personal.html", context)   
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