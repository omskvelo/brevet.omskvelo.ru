from datetime import datetime

from django.http import HttpResponse, Http404
from django.http.request import RAISE_ERROR
from django.shortcuts import get_object_or_404, get_list_or_404, render

from .models import Club, Randonneur, Route, Event, Result, Application, DEFAULT_CLUB_ID

def index(request, year=datetime.now().year):
    events = get_list_or_404(Event, finished=True, club=DEFAULT_CLUB_ID, date__year=year)
    events = sorted(events, key=lambda x: (x.date))
    for event in events:
        event.date_ = datetime.strftime(event.date, "%d.%m.%Y")

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
    return render(request, "brevet_database/index.html", context)

def event(request, distance, date):
    try:
        date = datetime.strptime(date, "%Y%m%d")
    except Exception:
        raise Http404

    event = get_object_or_404(Event, route__distance=distance, date=date, )
    route = event.route

    controls = route.controls.split("\n")
    if controls == [""]:
        controls = None

    context = {
        'event' : event,
        'date' : datetime.strftime(event.date, "%d.%m.%Y"),
        'time' : event.time.strftime("%H:%M"),
        'route' : route,
        'controls' : controls,
        'text' : event.text.split("\n"),
        }  

    return render(request, "brevet_database/event.html", context)  

def route(request, slug=None, route_id=None):
    # Render any active route. 
    if slug:
        route = get_object_or_404(Route, slug=slug)
    if route_id:
        route = get_object_or_404(Route, pk=route_id)

    controls = route.controls.split("\n")
    if controls == [""]:
        controls = None

    context = {
        'route' : route,
        'controls' : controls,
        'text' : route.text.split("\n"),
        }  
    return render(request, "brevet_database/route.html", context)       

def protocol(request, distance, date):
    try:
        date = datetime.strptime(date, "%Y%m%d")
    except Exception:
        raise Http404

    event = get_object_or_404(Event, route__distance=distance, date=date, )
    route = event.route
    results = get_list_or_404(Result, event=event)
    for r in results:
        r.time_ = "{:02d}:{:02d}".format(r.time.days*24 + r.time.seconds//3600, r.time.seconds%3600//60)
    results = sorted(results, key=lambda x: x.randonneur.russian_surname)

    context = {
        'event' : event,
        'route' : route,
        'results' : results,
        'date' : datetime.strftime(date, "%d.%m.%Y"),
        }      
    return render(request, "brevet_database/protocol.html", context)    

def get_sr(b):
    sr = 0
    brevets = b.copy()
    while True:
        if 600 in brevets:
            del brevets[brevets.index(600)]
        else:
            return sr
        if 400 in brevets:
            del brevets[brevets.index(400)]
        else:
            if 600 in brevets:
                del brevets[brevets.index(600)]
            else:
                return sr
        if 300 in brevets:
            del brevets[brevets.index(300)]
        else:
            if 400 in brevets:
                del brevets[brevets.index(400)]
            else:
                if 600 in brevets:
                    del brevets[brevets.index(600)]
                else:        
                    return sr
        if 200 in brevets:
            del brevets[brevets.index(200)]
        else:
            if 300 in brevets:
                del brevets[brevets.index(300)]
            else:
                if 400 in brevets:
                    del brevets[brevets.index(400)]
                else:
                    if 600 in brevets:
                        del brevets[brevets.index(600)]
                    else:        
                        return sr
        sr += 1   

def personal_stats(request, surname, name):
    surname = surname.lower().capitalize()
    name = name.lower().capitalize()
    randonneur = get_object_or_404(Randonneur, name=name, surname=surname)
    results = get_list_or_404(Result, randonneur=randonneur)
    for r in results:
        r.date_ = datetime.strftime(r.event.date, "%d.%m.%Y")
        r.time_ = "{:02d}:{:02d}".format(r.time.days*24 + r.time.seconds//3600, r.time.seconds%3600//60) 

    results = sorted(results, key=lambda x: x.event.date, reverse=True)

    best_200 = None
    best_300 = None
    best_400 = None
    best_600 = None
    by_year = {}
    total_distance = 0
    for result in results:
        # Count total distance
        total_distance += result.event.route.distance
        # Prepare data to calculate sr years and years active
        if result.event.route.brm:
            if result.event.date.year not in by_year:
                by_year[result.event.date.year] = [result.event.route.distance]
            else:
                by_year[result.event.date.year].append(result.event.route.distance)
        # Select best results
        if result.event.route.distance == 200:
            if best_200 is None:
                best_200 = result
            if best_200.time > result.time:
                best_200 = result
        if result.event.route.distance == 300:
            if best_300 is None:
                best_300 = result
            if best_300.time > result.time:
                best_300 = result
        if result.event.route.distance == 400:
            if best_400 is None:
                best_400 = result
            if best_400.time > result.time:
                best_400 = result
        if result.event.route.distance == 600:
            if best_600 is None:
                best_600 = result
            if best_600.time > result.time:
                best_600 = result  

    # Count SR qualifications
    sr = []
    for key in by_year:
        for _ in range (get_sr(by_year[key])):
            sr.append(str(key))  
    sr.sort()

    years_active = list(by_year.keys())
    years_active.sort()

    context = {
        'randonneur' : randonneur,
        'results' : results,
        'best_200' : best_200,
        'best_300' : best_300,
        'best_400' : best_400,
        'best_600' : best_600,
        'years_active' : ", ".join([str(y) for y in years_active]),
        'sr' :  ", ".join(sr),
        'total_distance' : total_distance,
        }  
    return render(request, "brevet_database/personal.html", context)   


    # surname = surname.lower().capitalize()
    # name = name.lower().capitalize()
    # randonneur = get_object_or_404(Randonneur, name=name, surname=surname)
    # results = []
    # for r in get_list_or_404(Result, randonneur=randonneur):
    #     results.append({
    #             'homologation' : r.homologation,
    #             'date' : datetime.strftime(r.event.date, "%d.%m.%Y"),
    #             'date_': r.event.date,
    #             'distance' : r.event.route.distance,
    #             'route' : r.event.route.name,
    #             'club' : r.event.club,
    #             'time' : "{:02d}:{:02d}".format(r.time.days*24 + r.time.seconds//3600, r.time.seconds%3600//60),
    #             'time_': r.time,
    #             'brm'  : r.event.route.brm
    #     })    

    # results = sorted(results, key=lambda row: (row['date_']), reverse=True)

    # best_200 = None
    # best_300 = None
    # best_400 = None
    # best_600 = None
    # by_year = {}
    # total_distance = 0
    # for result in results:
    #     # Count total distance
    #     total_distance += result['distance']
    #     # Prepare data to calculate sr years and years active
    #     if result['brm']:
    #         if result['date_'].year not in by_year:
    #             by_year[result['date_'].year] = [result['distance']]
    #         else:
    #             by_year[result['date_'].year].append(result['distance'])
    #     # Select best results
    #     if result['distance'] == 200:
    #         if best_200 is None:
    #             best_200 = result
    #         if best_200['time_'] > result ['time_']:
    #             best_200 = result
    #     if result['distance'] == 300:
    #         if best_300 is None:
    #             best_300 = result
    #         if best_300['time_'] > result ['time_']:
    #             best_300 = result
    #     if result['distance'] == 400:
    #         if best_400 is None:
    #             best_400 = result
    #         if best_400['time_'] > result ['time_']:
    #             best_400 = result
    #     if result['distance'] == 600:
    #         if best_600 is None:
    #             best_600 = result
    #         if best_600['time_'] > result ['time_']:
    #             best_600 = result  

    # # Count SR qualifications
    # sr = []
    # for key in by_year:
    #     for _ in range (get_sr(by_year[key])):
    #         sr.append(str(key))  
    # sr.sort()

    # years_active = list(by_year.keys())
    # years_active.sort()

    # context = {
    #     'randonneur' : randonneur,
    #     'results' : results,
    #     'best_200' : best_200,
    #     'best_300' : best_300,
    #     'best_400' : best_400,
    #     'best_600' : best_600,
    #     'years_active' : ", ".join([str(y) for y in years_active]),
    #     'sr' :  ", ".join(sr),
    #     'total_distance' : total_distance,
    #     }  
    # return render(request, "brevet_database/personal.html", context)   