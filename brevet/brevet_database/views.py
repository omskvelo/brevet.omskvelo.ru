from datetime import datetime, timedelta

from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render
from django.views.decorators.cache import cache_page, never_cache

import babel.dates

from .models import *
from .forms import *
from . import file_generators

TIME_LIMITS = {
    200 : timedelta(hours=13, minutes=30),
    300 : timedelta(hours=20),
    400 : timedelta(hours=27),
    600 : timedelta(hours=40),
    1000 : timedelta(hours=75),
}

MIN_TIME_LIMITS = {
    200 : timedelta(hours=5, minutes=53),
    300 : timedelta(hours=9, minutes=0),
    400 : timedelta(hours=12, minutes=8),
    600 : timedelta(hours=18, minutes=48),
    1000 : timedelta(hours=35, minutes=5),
}

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


def statistics_total(request, form="html"):
    return statistics(request, year=None, form=form)


def statistics(request, year=datetime.now().year, form="html"):    
    years = get_event_years()
    if year:
        if year not in years:
            year = max(years)
        results = list(Result.objects.filter(event__finished=True, event__date__year=year))
    else:
        results = list(Result.objects.filter(event__finished=True))
   
    # LRM, SR600, 1000
    elite_dist = [x for x in results if x.event.route.lrm or x.event.route.sr600 or x.event.route.distance == 1000] 
    elite_dist = sorted(elite_dist, key=lambda x: x.event.date, reverse=True)

    # Personal stats 
    randonneurs = get_randonneurs(year)

    distance_rating = []
    if year:
        distance_rating = [[randonneur, randonneur.get_total_distance(year=year), randonneur.get_total_brevets(year=year)] for randonneur in randonneurs]
        distance_rating = sorted(distance_rating, key=lambda x: x[1], reverse=True)
    else:
        sorted_by_distance = Randonneur.objects.filter(total_distance__gt=0).order_by("-total_distance")
        distance_rating = [[randonneur, randonneur.total_distance, randonneur.total_brevets] for randonneur in sorted_by_distance]
        
    

    # Get SR status
    sr = []
    for randonneur in randonneurs:
        if year:
            randonneur_sr = randonneur.sr.get(str(year)) or 0
        else:
            randonneur_sr = sum(randonneur.sr.get(str(y)) or 0 for y in years)
        if randonneur_sr:
            sr.append(randonneur)
            if randonneur_sr > 1:
                randonneur.sr_string = f" (x{randonneur_sr})"
            else:
                randonneur.sr_string = ""
    sr = sorted(sr, key=lambda x: x.sr_string, reverse=True)

    # Find best results
    best_200 = get_best(200, year=year, limit=10)
    best_300 = get_best(300, year=year, limit=10)
    best_400 = get_best(400, year=year, limit=10)
    best_600 = get_best(600, year=year, limit=10)

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
            "year" : year,
            "years" : years,
            "year_min_to_max": str(years[-1]) + " - " + str(years[0])
        }
        if year is not None:
            context.update({
                "distance_rating" : distance_rating,
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
    default_club = event.club.pk == DEFAULT_CLUB_ID
    route = event.route

    form, application, errors = event_result_time_form(request, event)

    context = {
        'event' : event,
        'route' : route,
        'default_club' : default_club,
        'form' : form,
        'application' : application,
        'errors' : errors,
        }  
    return render(request, "brevet_database/event.html", context)  

def event_result_form(request, event):
    """ Process result form with manual time calculation. Deprecated. """
    errors = []
    if request.user.is_authenticated:
        randonneur = request.user.randonneur
        application = Application.objects.filter(event=event, user=request.user).first()
        result = Result.objects.filter(event=event, randonneur=randonneur)

        if request.method == 'POST':
            form = AddResultForm(request.POST)
            if form.is_valid():
                if not randonneur:
                    raise Http404 
                if application and not result:
                    result_time = form.cleaned_data['result']
                    if result_time > TIME_LIMITS[event.route.distance]:
                        errors.append(f"Лимит времени - {timedelta_to_str(TIME_LIMITS[event.route.distance])}.")
                    else:
                        result = Result()
                        result.time = result_time
                        result.medal = form.cleaned_data['medal']
                        result.event = event
                        result.randonneur = randonneur
                        result.save()
                        application.result = result
                        application.save()
            else:
                errors = form.errors
        else:
            form = AddResultForm()
    else:
        form = None
        application = None

    return form, application, errors

def event_result_time_form(request, event):
    """ Process result form with automatic result time calculation"""
    errors = []
    if request.user.is_authenticated and request.user.randonneur:
        randonneur = request.user.randonneur
        application = Application.objects.filter(event=event, user=request.user).first()
        result = Result.objects.filter(event=event, randonneur=randonneur)

        if request.method == 'POST':
            
            form = AddResultTimeForm(request.POST)

            if form.is_valid():
                if application and not result:
                    start = datetime(
                        year=event.date.year, 
                        month=event.date.month, 
                        day=event.date.day, 
                        hour=event.time.hour, 
                        minute=event.time.minute
                        )

                    limit = start + TIME_LIMITS[event.route.distance]

                    # First assume finish has the same date as limit
                    finish = datetime(
                        year=limit.year, 
                        month=limit.month, 
                        day=limit.day, 
                        hour=form.cleaned_data['result'].hour, 
                        minute=form.cleaned_data['result'].minute
                        )

                    # If not - finish either happened on the prevoius date...              
                    if finish > limit:
                        finish -= timedelta(days=1)

                    # Or is invalid
                    if (finish > limit 
                        or finish < start
                        or finish - start < MIN_TIME_LIMITS[event.route.distance]
                        ):
                        errors.append(f"Лимит времени - {timedelta_to_str(TIME_LIMITS[event.route.distance])}.")

                    if not errors:
                        result = Result()
                        result.time = finish - start
                        result.medal = form.cleaned_data['medal']
                        result.event = event
                        result.randonneur = randonneur
                        result.save()
                        application.result = result
                        application.save()
            else:
                errors = form.errors
                if 'result' in errors:
                    errors = ["Введите корректное время."]
        else:
            form = AddResultTimeForm()
    else:
        form = None
        application = None

    return form, application, errors  


def event_register(request, distance, date):
    if request.user.is_authenticated:
        try:
            date = datetime.strptime(date, "%Y%m%d")
        except Exception:
            raise Http404
        event = get_object_or_404(Event, route__distance=distance, date=date)

        conflict = Application.objects.filter(user=request.user, event__date=date)
        if conflict:
            return redirect(request.META.get('HTTP_REFERER'))

        if not event.application_allowed():
            return Http404

        application = Application()
        application.event = event
        application.user = request.user
        application.save()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        raise Http404


def event_cancel_registration(request, distance, date):
    if request.user.is_authenticated:
        try:
            date = datetime.strptime(date, "%Y%m%d")
        except Exception:
            raise Http404
        event = get_object_or_404(Event, route__distance=distance, date=date, )

        application = get_object_or_404(Application, event=event, user=request.user )
        application.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        raise Http404


def event_dnf(request, distance, date):
    if request.user.is_authenticated:
        try:
            date = datetime.strptime(date, "%Y%m%d")
        except Exception:
            raise Http404
        event = get_object_or_404(Event, route__distance=distance, date=date, )

        application = get_object_or_404(Application, event=event, user=request.user )
        application.dnf = True
        if application.result:
            application.result.delete()
            application.result = None
        application.save() 

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        raise Http404

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
def route_stats(request, slug=None, route_id=None):
    if slug:
        route = get_object_or_404(Route, slug=slug)
    elif route_id:
        route = get_object_or_404(Route, pk=route_id)
    else:
        raise Http404
    
    events = Event.objects.filter(route=route, finished=True).order_by("date")
    results = Result.objects.filter(event__route=route, event__finished=True).order_by("time")

    first_event = events.first()
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


def personal_stats_index(request):
    randonneurs = get_randonneurs()

    rating = []
    for randonneur in randonneurs:
        sr = []
        for year in randonneur.sr:
            sr_times = randonneur.sr[year] 
            if sr_times > 1:
                sr.append (f"{year} (x{sr_times})")
            elif sr_times:
                sr.append (f"{year}")
        sr = ", ".join(sr)

        rating.append({
            'randonneur': randonneur, 
            'total_distance': randonneur.total_distance, 
            'total_brevets': randonneur.total_brevets,
            'sr': sr,
            }) 
    rating = sorted(rating, key=lambda x: x['total_distance'], reverse=True)


    context = {
        "rating" : rating,
    }
    return render(request, "brevet_database/stats_personal_index.html", context)    

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
    
    first_brevet = results[-1] if results else None
    
    total_distance = randonneur.total_distance
    total_brevets = randonneur.total_brevets
    
    elite_dist = [x for x in results if x.event.route.lrm or x.event.route.sr600 or x.event.route.distance == 1000] 
    
    best_200 = get_best(200, randonneur)
    best_300 = get_best(300, randonneur)
    best_400 = get_best(400, randonneur)
    best_600 = get_best(600, randonneur)

    years_active = randonneur.get_active_years()

    # Get SR status
    sr = []
    for year in randonneur.sr:
        sr_times = randonneur.sr[year] 
        if sr_times > 1:
            sr.append (f"{year} (x{sr_times})")
        elif sr_times:
            sr.append (f"{year}")

    sr = ", ".join(sr)
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
            'first_brevet' : first_brevet,
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
def index(request):

    # Select latest finished events (there can be more than one event on a single date)
    finished_events = Event.objects.filter(finished=True).order_by("-date")
    prev_event_date = finished_events[0].date
    prev_events = []
    for event in finished_events:
        if event.date == prev_event_date:
            prev_events.append(event)
        else:
            break
            
    prev_events = [
        {
        'event': event,
        'results': Result.objects.filter(event=event).order_by("randonneur__russian_surname","randonneur__russian_name"),
        } for event in prev_events
    ]


    # Select next upcoming events (there can be more than one event on a single date)
    upcoming_events = Event.objects.filter(finished=False).order_by("date")
    next_event_date = upcoming_events[0].date
    next_events = []   

    for event in upcoming_events:
        if event.date == next_event_date:
            form, application, errors = event_result_time_form(request, event)
            next_events.append({
                    'event' : event,
                    'application' : application,
                    'form' : form,
                    'errors' : errors,
                })
        else:
            break

    context = {
        'next_events' : next_events,
        'prev_events' : prev_events,
    }
    return render(request, "brevet_database/index.html", context)