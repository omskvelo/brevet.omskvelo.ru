from datetime import datetime
import babel.dates

from django.http import HttpResponse, Http404
from django.http.request import RAISE_ERROR
from django.shortcuts import get_object_or_404, get_list_or_404, render

from .models import Club, Randonneur, Route, Event, Result, Application, DEFAULT_CLUB_ID

def protocol_index(request, year=datetime.now().year):
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
    return render(request, "brevet_database/protocol_index.html", context)

def stats_club_total(request):
    return stats_club(request, year=None)


def stats_club(request, year=datetime.now().year):
    if year is not None:
        # Check available years
        years = set()
        for event in get_list_or_404(Event, finished=True, club=DEFAULT_CLUB_ID):
            years.add(event.date.year)
        years = sorted(list(years), reverse=True)
        # Add total stats
        # years.append(" - ".join([str(years[-1]),str(years[0])]))

        # Collect results
        results = get_list_or_404(Result, event__finished=True, event__date__year=year)
    else:
        results = get_list_or_404(Result, event__finished=True)

    # Add date and time foramtting
    for result in results:
        result.date_ = result.event.date.strftime("%d.%m.%Y")
        result.time_ = "{:02d}:{:02d}".format(result.time.days*24 + result.time.seconds//3600, result.time.seconds%3600//60)

    # Calculate total stats
    total_distance = 0
    for result in results:
        total_distance += result.event.route.distance

    # Prepare data to calculate personal stats 
    randonneurs = {}
    for result in results:
        r = str(result.randonneur)
        if r not in randonneurs:
            randonneurs[r] = {"randonneur":result.randonneur, "results":[]}
        randonneurs[r]["results"].append(result)
    total_randonneurs = len(randonneurs)

    # LRM, SR600
    elite_dist = []
    for result in results:
        if result.event.route.lrm:
            elite_dist.append(result)
        if result.event.route.sr600:
            elite_dist.append(result)
        if result.event.route.distance == 1000:
            elite_dist.append(result)
    elite_dist = sorted(elite_dist, key=lambda x: x.event.date)

    # Calculate personal stats
    sr = []
    for _,randonneur in randonneurs.items():
        randonneur["total_brevets"] = len(randonneur["results"])
        randonneur["total_distance"] = sum([result.event.route.distance for result in randonneur["results"]])
        r_sr = get_sr(randonneur["results"])
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

    total_sr = len(sr)

    # Best results
    best_200 = []
    best_300 = []
    best_400 = []
    best_600 = []
    for result in results:
        if result.event.route.distance == 200:
            best_200.append(result)
        if result.event.route.distance == 300:
            best_300.append(result)
        if result.event.route.distance == 400:
            best_400.append(result)
        if result.event.route.distance == 600:
            best_600.append(result)
    best_200 = sorted(best_200, key=lambda x: x.time)[:10]
    best_300 = sorted(best_300, key=lambda x: x.time)[:10]
    best_400 = sorted(best_400, key=lambda x: x.time)[:10]
    best_600 = sorted(best_600, key=lambda x: x.time)[:10]

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
    return render(request, "brevet_database/stats_club.html", context)        


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

def event_index(request):
    events = get_list_or_404(Event, club=DEFAULT_CLUB_ID, finished=False)
    for event in events:
        event.time_ = event.time.strftime("%H:%M")
        event.date_ = datetime.strftime(event.date, "%d.%m.%Y")
        event.controls_ = event.route.controls.split("\n")
        if event.controls_ == [""]:
            event.controls_ = None

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

def route(request, slug=None, route_id=None):
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
        'time' : event.time.strftime("%H:%M"),
        }      
    return render(request, "brevet_database/protocol.html", context)    

def get_sr(results):
    sr = 0
    brevets = [result.event.route.distance for result in results if result.event.route.brm]
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
                by_year[result.event.date.year] = []
            by_year[result.event.date.year].append(result)
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


