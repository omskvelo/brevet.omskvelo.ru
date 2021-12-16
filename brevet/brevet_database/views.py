from datetime import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.views.decorators.cache import cache_page, never_cache

import babel.dates

from .models import Club, Randonneur, Route, Event, Result, Application, DEFAULT_CLUB_ID
from .toolbox import brevet_tools

@never_cache
def protocol(request, distance, date):
    try:
        date = datetime.strptime(date, "%Y%m%d")
    except Exception:
        raise Http404

    event = get_object_or_404(Event, route__distance=distance, date=date)
    route = event.route
    results = get_list_or_404(Result.objects.order_by("randonneur__russian_surname","randonneur__russian_name"), event=event)

    context = {
        'event' : event,
        'route' : route,
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

    file = brevet_tools.get_xlsx_protocol(event,results)

    response = HttpResponse(file.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f"attachment; filename={date.year}-{date.month}-{date.day}_{distance}.xlsx"

    file.close()

    return response

def protocol_index(request, year=datetime.now().year):
    events = get_list_or_404(Event.objects.order_by("date"), finished=True, club=DEFAULT_CLUB_ID, date__year=year)

    #Check available years
    years = set()
    for event in get_list_or_404(Event, finished=True, club=DEFAULT_CLUB_ID):
        years.add(event.date.year)
    years = sorted(list(years), reverse=True)

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
    if year is not None:
        results = get_list_or_404(Result, event__finished=True, event__date__year=year)
    else:
        results = get_list_or_404(Result, event__finished=True)

    # Check available years
    years = set()
    for event in get_list_or_404(Event, finished=True, club=DEFAULT_CLUB_ID):
        years.add(event.date.year)
    years = sorted(list(years), reverse=True)

    # Prepare data to calculate personal stats 
    randonneurs = {}
    for result in results:
        r = str(result.randonneur)
        if r not in randonneurs:
            randonneurs[r] = {"randonneur":result.randonneur, "results":[]}
        randonneurs[r]["results"].append(result)

    # LRM, SR600, 1000
    elite_dist = [x for x in results if x.event.route.lrm or x.event.route.sr600 or x.event.route.distance == 1000] 
    elite_dist = sorted(elite_dist, key=lambda x: x.event.date)

    # Calculate personal stats
    sr = []
    for _,randonneur in randonneurs.items():
        randonneur["total_brevets"] = len(randonneur["results"])
        randonneur["total_distance"] = sum([result.event.route.distance for result in randonneur["results"]])
        r_sr = brevet_tools.get_sr(randonneur["results"])
        if (r_sr):
            if r_sr > 1:
                sr_string = f"(x{r_sr})"
            else:
                sr_string = ""
            randonneur["randonneur"].sr_string = sr_string
            sr.append(randonneur["randonneur"])
    sr = sorted(sr, key=lambda x: x.sr_string, reverse=True)

    distance_rating = [
        [randonneur[1]["randonneur"],
        randonneur[1]["total_distance"],
        randonneur[1]["total_brevets"]] 
        for randonneur in randonneurs.items()]
    distance_rating = sorted(distance_rating, key=lambda x: x[1], reverse=True)

    # Find best results
    best_200 = [x for x in results if x.event.route.distance == 200]
    best_300 = [x for x in results if x.event.route.distance == 300]
    best_400 = [x for x in results if x.event.route.distance == 400]
    best_600 = [x for x in results if x.event.route.distance == 600]
    best_200 = sorted(best_200, key=lambda x: x.time)[:10]
    best_300 = sorted(best_300, key=lambda x: x.time)[:10]
    best_400 = sorted(best_400, key=lambda x: x.time)[:10]
    best_600 = sorted(best_600, key=lambda x: x.time)[:10]

    # Calculate total stats
    total_sr = len(sr)
    total_randonneurs = len(randonneurs)
    total_distance = 0
    for result in results:
        total_distance += result.event.route.distance

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
        file = brevet_tools.get_xlsx_club_stats(
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
        years)

        response = HttpResponse(file.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f"attachment; filename={year if year else 'total'}.xlsx"

        file.close()

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

def route_index(request, distance=200):
    r = get_list_or_404(Route, distance=distance, club=DEFAULT_CLUB_ID)
    routes = []
    for route in r:
        if route.slug != "":
            routes.append(route)

    context = {
        'routes' : routes,
        'distance' : distance,
        'distances' : [200,300,400,600,1000],
    } 
    return render(request, "brevet_database/route_index.html", context)         


def personal_stats(request, surname=None, name=None, uid=None, form="html"):
    if uid:
        randonneur = get_object_or_404(Randonneur, pk=uid)
    elif surname and name:
        surname = surname.lower().capitalize()
        name = name.lower().capitalize()
        randonneur = get_object_or_404(Randonneur, name=name, surname=surname)
    else:
        raise Http404

    results = get_list_or_404(Result.objects.order_by("-event__date"), randonneur=randonneur)

    # Total stats
    total_distance = sum([x.event.route.distance for x in results])
    total_brevets = len(results)

    # LRM, SR600, 1000
    elite_dist = [x for x in results if x.event.route.lrm or x.event.route.sr600 or x.event.route.distance == 1000] 

    # Best BRM results
    best_200 = [x for x in results if x.event.route.distance == 200]
    best_300 = [x for x in results if x.event.route.distance == 300]
    best_400 = [x for x in results if x.event.route.distance == 400]
    best_600 = [x for x in results if x.event.route.distance == 600 and x.event.route.brm]
    best_200 = sorted(best_200, key=lambda x: x.time)
    best_300 = sorted(best_300, key=lambda x: x.time)
    best_400 = sorted(best_400, key=lambda x: x.time)
    best_600 = sorted(best_600, key=lambda x: x.time)

    # Count years active and SR qualifications
    by_year = {}
    for result in results:
        if result.event.route.brm:
            if result.event.date.year not in by_year:
                by_year[result.event.date.year] = []
            by_year[result.event.date.year].append(result)

    sr = []
    for key in by_year:
        for _ in range (brevet_tools.get_sr(by_year[key])):
            sr.append(str(key))  
    sr.sort()
    sr =  ", ".join(sr)

    years_active = list(by_year.keys())
    years_active.sort()
    years_active = ", ".join([str(y) for y in years_active])

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
        file = brevet_tools.get_xlsx_personal_stats(
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
            best_600)

        response = HttpResponse(file.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f"attachment; filename={randonneur.surname} {randonneur.name}.xlsx"

        file.close()

        return response
    else:
        raise Http404


