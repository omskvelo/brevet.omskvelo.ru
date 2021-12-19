from django.shortcuts import render

# from blog.models import BlogPost
from brevet_database.models import Event,Route,Randonneur
from brevet_database.models import search as db_search

def search_results(request):
    query = request.GET.get('q',"")

    news = []
    # news = BlogPost.search(query)
    events = db_search(Event,query)
    routes = db_search(Route,query)
    randonneurs = db_search(Randonneur,query)

    context = {
        "query" : query,
        "news" : news,
        "events" : events,
        "routes" : routes,
        "randonneurs" : randonneurs,
    }
    return render(request, "search/search_results.html", context)
