from django.shortcuts import render

from .models import search as db_search

def search_results(request):
    query = request.GET.get('q',"")

    if query:
        events = db_search('Event',query)
        routes = db_search('Route',query)
        randonneurs = db_search('Randonneur',query)

        context = {
        "query" : query,
        "events" : events,
        "routes" : routes,
        "randonneurs" : randonneurs,
        }
    else:
        context = {}


    return render(request, "search/search_results.html", context)
