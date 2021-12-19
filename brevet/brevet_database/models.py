from datetime import datetime, time

from django.db import models
from django.urls import reverse

from . import file_processors

DEFAULT_CLUB_ID = 1

class Club(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    ACP_code = models.IntegerField(blank=False, unique=True)
    french_name = models.CharField(max_length=50, blank=False, unique=True)
    
    def __str__(self):
        return f"{self.name} {self.ACP_code}"

class Randonneur(models.Model):
    name = models.CharField(max_length=50, blank=False)
    surname = models.CharField(max_length=50, blank=False)
    russian_name = models.CharField(max_length=50, blank=False)
    russian_surname = models.CharField(max_length=50, blank=False)
    image = models.ImageField(upload_to="img/users/", blank=True)
    club = models.ForeignKey(Club, on_delete=models.PROTECT, default=DEFAULT_CLUB_ID)
    female = models.BooleanField(default=False)

    class Meta:
        ordering = ['russian_surname']

    def get_absolute_url(self):
        return reverse('personal_stats', kwargs={'uid' : self.pk})

    def get_xlsx_url(self):
        return reverse('personal_stats_f', kwargs={'uid' : self.pk, 'form' : 'xlsx'})

    def get_active_years(self):
        years = set()
        q = list(Result.objects.filter(event__finished=True, randonneur=self))
        for result in q:
            years.add(str(result.event.date.year))
        return sorted(list(years), reverse=True)

    def get_sr(self, year):
        sr = 0
        results = list(Result.objects.filter( event__route__brm=True, randonneur=self, event__date__year=year))
        brevets = [result.event.route.distance for result in results]
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

    def set_sr_string(self, years):
        sr = 0
        for year in years:
            sr += self.get_sr(year)
        if sr > 1:
            self.sr_string = f" (x{sr})"
        else:
            self.sr_string = ""
        return sr


    def get_results(self, year=None):
        q = Result.objects.filter(randonneur=self)
        if year:
            q = q.filter(event__date__year=year)
        return list(q)

    def get_total_distance(self, year=None):
        results = self.get_results(year)
        return sum([result.event.route.distance for result in results])

    def get_total_brevets(self, year=None):
        results = self.get_results(year)
        return len(results)        

    def __str__(self):
        return f"{self.russian_surname} {self.russian_name}"

class Route(models.Model):
    name = models.CharField(max_length=200, blank=True) 
    slug = models.SlugField(blank=True)
    distance = models.IntegerField(blank=False)
    active = models.BooleanField(default=False)
    controls = models.TextField(blank=True)
    text = models.TextField(blank=True)
    text_brief = models.TextField(max_length=120, blank=True)
    bad_roads = models.BooleanField(default=False)
    brm = models.BooleanField(default=True)
    lrm = models.BooleanField(default=False)
    fleche = models.BooleanField(default=False)
    sr600 = models.BooleanField(default=False)
    club = models.ForeignKey(Club, on_delete=models.PROTECT, blank=True, default=DEFAULT_CLUB_ID)
    external_xref = models.URLField(blank=True)
    map_embed_src = models.CharField(max_length=500, blank=True) 
    image = models.ImageField(upload_to="img/", blank=True)
    gpx = models.FileField(upload_to="gpx/", blank=True)
    pdf = models.FileField(upload_to="pdf/", blank=True)
    orvm = models.FileField(upload_to="orvm/", blank=True)

    class Meta:
        ordering = ['-active', 'distance']

    def get_controls(self):        
        if self.controls == "":
            return None
        else:
            return self.controls.split("\n")

    def get_text(self):
        return self.text.split("\n")

    def get_absolute_url(self):
        if self.slug:
            return reverse('route', kwargs={'slug' : self.slug})
        else:
            return reverse('route_id', kwargs={'route_id' : self.pk})

    def __str__(self):
        club = str(self.club) if self.club.id != DEFAULT_CLUB_ID else ""
        return f"{self.distance} км {self.name} {club}"     

class Event(models.Model):
    name = models.CharField(max_length=50, blank=True) 
    route = models.ForeignKey(Route, on_delete=models.PROTECT, blank = False)
    date = models.DateField(auto_now=False, auto_now_add=False, blank=False)
    time = models.TimeField(auto_now=False, auto_now_add=False, blank=False, default=time(hour = 7))
    text_intro = models.TextField(blank=True)
    text = models.TextField(blank=True)
    warning_text = models.TextField(blank=True)
    lights_required = models.BooleanField(default=False)
    club = models.ForeignKey(Club, on_delete=models.PROTECT, default=DEFAULT_CLUB_ID)
    responsible = models.CharField(max_length=50, blank=True)
    finished = models.BooleanField(default=False)
    omskvelo_xref = models.URLField(blank=True)
    external_xref = models.URLField(blank=True)
    vk_xref = models.URLField(blank=True) 

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        date = datetime.strftime(self.date, "%Y%m%d")
        return reverse('event', kwargs={'distance' : self.route.distance, 'date' : date})

    def get_protocol_url(self):
        date = datetime.strftime(self.date, "%Y%m%d")
        return reverse('protocol', kwargs={'distance' : self.route.distance, 'date' : date})

    def get_protocol_xlsx_url(self):
        date = datetime.strftime(self.date, "%Y%m%d")
        return reverse('protocol_f', kwargs={'distance' : self.route.distance, 'date' : date, "form" : "xlsx"})  

    def get_protocol_upload_success_url(self):
        date = datetime.strftime(self.date, "%Y%m%d")
        return reverse("protocol_upload_success", kwargs={'distance' : self.route.distance, 'date' : date})

    def is_homologated(self):
        results = list(Result.objects.filter(event=self))
        for result in results:
            if result.homologation == "":
                return False
        return True

    def update_protocol_from_xls(self,file):
        results = list(Result.objects.filter(event=self))
        content, exception = file_processors.read_xls_protocol(file)
        
        if not exception:
            if (content["date"] == self.date 
                and content["distance"] == self.route.distance 
                and content["code"] == self.club.ACP_code
                ):
                for result in results:
                    surname = result.randonneur.surname
                    name = result.randonneur.name

                    for entry in content["results"]:
                        if (entry['name'] == name
                            and entry['surname'] == surname):
                            if entry['homologation']:
                                result.homologation = entry['homologation']
                                result.save()
                            else:
                                exception = "Homologation is empty"
                return True, exception
            else:
                exception = "Date, distance or ACP code do not match"
        return False, exception


    def get_date(self):
        return self.date.strftime("%d.%m.%Y")

    def get_time(self):
        return self.time.strftime("%H:%M")

    def get_controls(self):        
        return self.route.get_controls
    
    def get_text(self):
        return self.text.split("\n")

    def __str__(self):
        club = str(self.club) if self.club.id != DEFAULT_CLUB_ID else ""
        return f"{self.get_date()} {self.route.distance} км {self.route.name} {club}"     

class Result(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    homologation = models.CharField(max_length=50, blank=True) 
    randonneur = models.ForeignKey(Randonneur, on_delete=models.CASCADE) 
    time = models.DurationField(blank=True)
    medal = models.BooleanField(default=False)

    class Meta:
        ordering = ['-event__date']

    def get_date(self):
        return self.event.get_date()

    def get_time(self):
        return "{:02d}:{:02d}".format(self.time.days*24 + self.time.seconds//3600, self.time.seconds%3600//60)

    def __str__(self):
        return f"{self.get_date()} {self.event.route.distance} км {self.randonneur} {self.get_time()}"

class Application(models.Model):
    randonneur = models.ForeignKey(Randonneur, on_delete=models.CASCADE, blank=True) 
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    russian_name = models.CharField(max_length=50, blank=True)
    russian_surname = models.CharField(max_length=50, blank=True) 
    club = models.ForeignKey(Club, on_delete=models.PROTECT, blank=True, default=DEFAULT_CLUB_ID)
    female = models.BooleanField(default=False, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    
    def __str__(self):
        datestring = datetime.strftime(self.date, "%H:%M %d.%m.%Y")
        return f"Заявка №{self.id} от {datestring} на бревет {self.event}"

def get_event_years(reverse=True, finished=True):
    """Returns a list of event years for use in selectors"""
    years = set()
    for event in list(Event.objects.filter(finished=finished, club=DEFAULT_CLUB_ID)):
        years.add(event.date.year)
    return sorted(list(years), reverse=reverse)

def get_best(distance, randonneur=None, year=None):
    """Returns best results on brm distance for randonneur 
    (or all randonneurs if None) for a given year (or all years if None)"""
    q = Result.objects.filter(event__route__distance=distance, event__route__brm=True)
    if randonneur:
        q = q.filter(randonneur=randonneur)
    if year:
        q = q.filter(event__date__year=year)
    q=q.order_by("time")
    return list(q)

def get_randonneurs(year=None):
    """Returns a list of randonneurs for a given year (or all randonneurs if None). 
    NOTE: randonneurs with no results are omitted on purpose."""
    randonneurs = set()
    results = Result.objects.filter(event__finished=True)
    if year:
        results = results.filter(event__date__year=year)
    for result in list(results):
        randonneurs.add(result.randonneur)
    return list(randonneurs)

    
def search(object_class, query):
    # NOTE: Since we use SqLite and mostly cyrrilic characters, __icontains does not work as expected: https://docs.djangoproject.com/en/4.0/ref/databases/#sqlite-notes

    if object_class is Randonneur:       

        # Search cyrillic name:
        results = object_class.objects.filter(russian_name__contains=query.capitalize())
        results |= object_class.objects.filter(russian_name__contains=query.lower())
        results |= object_class.objects.filter(russian_surname__contains=query.capitalize())
        results |= object_class.objects.filter(russian_surname__contains=query.lower())

        # Search transliterated name:
        results |= object_class.objects.filter(name__icontains=query)
        results |= object_class.objects.filter(surname__icontains=query)

        # Extras
        if query.lower() in ["девушка", "девушки", "женщина", "женщины"]: # Return women
            results = object_class.objects.filter(female=True)
        if query.lower() in ["парень", "парни", "мужчина", "мужчины", "мужик", "мужики"]: # Return men
            results = object_class.objects.filter(female=False)


    elif object_class is Event:

        # Search cyrillic name:
        results = object_class.objects.filter(name__contains=query.capitalize())
        results |= object_class.objects.filter(name__contains=query.lower())

        try: 
            # Search distance:
            results |= object_class.objects.filter(route__distance=int(query), route__active=True)
            results |= results.exclude(route__name="")

            # Search year
            if int(query) in range (2010,2100):
               results |= object_class.objects.filter(date__year=int(query))
        except ValueError:
            pass 


    elif object_class is Route:

        # Search cyrillic name:
        results = object_class.objects.filter(name__contains=query.capitalize())
        results |= object_class.objects.filter(name__contains=query.lower())
        results |= object_class.objects.filter(name=query.title())

        try: 
            # Search distance:
            results |= object_class.objects.filter(distance=int(query), active=True)
        except ValueError:
            pass   


    return list(results)