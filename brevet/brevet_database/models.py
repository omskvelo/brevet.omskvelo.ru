from datetime import datetime, time, timedelta
from uuid import uuid4
from pathlib import Path

from django.db import models
from django.urls import reverse
from django.dispatch import receiver

from transliterate import translit

from . import file_processors

DEFAULT_CLUB_ID = 1

def gpx_path(instance, filename):
    path = Path(filename)
    id = uuid4()
    return f"gpx/{id}{path.suffix}"

def img_path(instance, filename):
    path = Path(filename)
    id = uuid4()
    return f"img/{id}{path.suffix}"

def pdf_path(instance, filename):
    path = Path(filename)
    id = uuid4()
    return f"pdf/{id}{path.suffix}"

class AbstractModel(models.Model):
    def get_admin_url_change(self):
        return f"/admin/{self._meta.app_label}/{self._meta.object_name.lower()}/{self.pk}/change/"

    def get_admin_url_add(self):
        return f"/admin/{self._meta.app_label}/{self._meta.object_name.lower()}/add/"

    def get_admin_url_delete(self):
        return f"/admin/{self._meta.app_label}/{self._meta.object_name.lower()}/{self.pk}/delete/"

    class Meta:
        abstract = True

class Club(AbstractModel):
    name = models.CharField(max_length=50, blank=False, unique=True)
    ACP_code = models.IntegerField(blank=False, unique=True)
    french_name = models.CharField(max_length=50, blank=False, unique=True)
    
    def __str__(self):
        return f"{self.name} {self.ACP_code}"

class Randonneur(AbstractModel):
    name = models.CharField(max_length=50, blank=False)
    surname = models.CharField(max_length=50, blank=False)
    russian_name = models.CharField(max_length=50, blank=False)
    russian_surname = models.CharField(max_length=50, blank=False)
    club = models.ForeignKey(Club, on_delete=models.PROTECT, default=DEFAULT_CLUB_ID)
    female = models.BooleanField(default=False)
    sr = models.JSONField(null=True, blank=True, default=dict)
    total_distance = models.IntegerField(default=0)
    total_brevets = models.IntegerField(default=0)

    class Meta:
        ordering = ['russian_surname']

    def get_absolute_url(self):
        return reverse('personal_stats', kwargs={'uid' : self.pk})

    def get_xlsx_url(self):
        return reverse('personal_stats_f', kwargs={'uid' : self.pk, 'form' : 'xlsx'})

    def get_results(self, year=None):
        q = Result.objects.filter(randonneur=self, event__finished=True)
        if year:
            q = q.filter(event__date__year=year)
        return q

    def get_active_years(self):
        years = set()
        q = list(Result.objects.filter(event__finished=True, randonneur=self))
        for result in q:
            years.add(str(result.event.date.year))
        return sorted(list(years))

    def get_sr(self, year):
        """Calculate Super Randonneur status"""
        sr = 0
        brevets = list(self.get_results(year).filter(event__route__brm=True).values_list('event__route__distance', flat=True))
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
        """ Deprecated """
        sr = 0
        for year in years:
            sr += self.get_sr(year)
        if sr > 1:
            self.sr_string = f" (x{sr})"
        else:
            self.sr_string = ""
        return sr

    def get_total_distance(self, year=None):
        distance = self.get_results(year).filter(event__route__fleche=False).aggregate(models.Sum('event__route__distance'))['event__route__distance__sum'] or 0
        distance += self.get_results(year).filter(event__route__fleche=True).aggregate(models.Sum('event__fleche_distance'))['event__fleche_distance__sum'] or 0
        return distance

    def get_total_brevets(self, year=None):
        return self.get_results(year).count()

    def update_stats(self):
        years = self.get_active_years()
        self.sr = dict()
        for year in years:
            sr_buffer = self.get_sr(str(year))
            if sr_buffer:
                self.sr[str(year)] = sr_buffer

        self.total_brevets = self.get_total_brevets()
        self.total_distance = self.get_total_distance()
        self.save()

        return True

    def from_user(user):
        r = Randonneur()
        r.russian_name = user.first_name
        r.russian_surname = user.last_name
        r.name = translit(user.first_name, 'ru', reversed=True)
        r.surname = translit(user.last_name, 'ru', reversed=True)
        return r

    def __str__(self):
        return f"{self.russian_surname} {self.russian_name}"

class Route(AbstractModel):
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
    image = models.ImageField(upload_to=img_path, blank=True)
    gpx = models.FileField(upload_to=gpx_path, blank=True)
    pdf = models.FileField(upload_to=pdf_path, blank=True)
    orvm = models.FileField(upload_to=pdf_path, blank=True)

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

    def get_stats_url(self):
        if self.slug:
            return reverse('stats_route', kwargs={'slug' : self.slug})
        else:
            return reverse('stats_route_id', kwargs={'route_id' : self.pk})

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/brevet/img/route_default.jpg"

    def __str__(self):
        club = str(self.club) if self.club.id != DEFAULT_CLUB_ID else ""
        return f"{self.distance} км {self.name} {club}"     

class PaymentInfo(models.Model):
    text = models.TextField(max_length=1000, blank=False, null=False)

    def __str__(self):
        return self.text

class Event(AbstractModel):
    name = models.CharField(max_length=50, blank=True) 
    route = models.ForeignKey(Route, on_delete=models.PROTECT, blank=False)
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
    fleche_distance = models.IntegerField(null=True, blank=True, verbose_name="Actual distance (Fleche only)")
    payment_info = models.ForeignKey(PaymentInfo, on_delete=models.SET_NULL, null=True, default=1)

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        date = datetime.strftime(self.date, "%Y%m%d")
        return reverse('event', kwargs={'distance' : self.route.distance, 'date' : date})

    def get_protocol_url(self):
        date = datetime.strftime(self.date, "%Y%m%d")
        return reverse('protocol', kwargs={'distance' : self.route.distance, 'date' : date})

    def get_dnf_url(self):
        date = datetime.strftime(self.date, "%Y%m%d")
        return reverse('event_dnf', kwargs={'distance' : self.route.distance, 'date' : date})

    def get_protocol_xlsx_url(self):
        date = datetime.strftime(self.date, "%Y%m%d")
        return reverse('protocol_f', kwargs={'distance' : self.route.distance, 'date' : date, "form" : "xlsx"})  

    def get_protocol_upload_success_url(self):
        date = datetime.strftime(self.date, "%Y%m%d")
        return reverse("protocol_upload_success", kwargs={'distance' : self.route.distance, 'date' : date})

    def get_applications(self):
        return Application.objects.filter(event=self).order_by(
            'dns',
            'dnf',
            'otl',
            'dsq',
            'result__is_null',
            'date',
        )

    def get_applicants(self):
        applications = list(Application.objects.filter(event=self))
        applicants = [application.user for application in applications]
        return applicants

    def get_same_date_applicants(self):
        same_date_events = Event.objects.filter(date=self.date).exclude(pk=self.pk)
        return [x for event in same_date_events for x in event.get_applicants()]

    def started(self):
        datetime_start = datetime.combine(self.date, self.time)
        return datetime_start < datetime.now()

    def application_allowed(self):
        timedelta_block = timedelta(hours = 12)
        datetime_start = datetime.combine(self.date, self.time)
        return datetime_start - timedelta_block > datetime.now()

    def get_add_application_url(self):
        date = datetime.strftime(self.date, "%Y%m%d")
        return reverse('event_register', kwargs={'distance' : self.route.distance, 'date' : date})

    def get_cancel_application_url(self):
        date = datetime.strftime(self.date, "%Y%m%d")
        return reverse('event_cancel_registration', kwargs={'distance' : self.route.distance, 'date' : date})

    def get_finisher_count(self):
        return Result.objects.filter(event=self).count()

    def get_moving_count(self):
        return Application.objects.filter(
            event=self, 
            dnf=False,
            dns=False,
            dsq=False,
            otl=False,
            result=None, 
            ).count()

    def get_dnf_count(self):
        return Application.objects.filter(event=self, dnf=True).count()

    def get_dns_count(self):
        return Application.objects.filter(event=self, dns=True).count()

    def get_dsq_count(self):
        return Application.objects.filter(event=self, dsq=True).count()

    def get_otl_count(self):
        return Application.objects.filter(event=self, otl=True).count()    

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
                        if (entry['name'].lower() == name.lower()
                            and entry['surname'].lower() == surname.lower()):
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
        return [x for x in self.text.split("\n") if x]

    def __str__(self):
        club = str(self.club) if self.club.id != DEFAULT_CLUB_ID else ""
        return f"{self.get_date()} {self.route.distance} км {self.route.name} {club}"  

@receiver(models.signals.post_save, sender=Event)
def update_randonneur_stats(sender, instance, created, **kwargs):
    if instance.finished:
        # Update stats of participants
        applications = Application.objects.filter(event=instance)
        results = [a.result for a in applications if a.result]
        randonneurs = [result.randonneur for result in results]

        for randonneur in randonneurs:
            randonneur.update_stats()

        # Delete old applications
        applications.delete()
           

class Result(AbstractModel):
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


class Application(AbstractModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    dnf = models.BooleanField(default=False)
    dns = models.BooleanField(default=False)
    dsq = models.BooleanField(default=False)
    otl = models.BooleanField(default=False)
    result = models.ForeignKey(Result, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    payment = models.BooleanField(default=False)
    
    def __str__(self):
        datestring = datetime.strftime(self.date, "%H:%M %d.%m.%Y")
        return f"{datestring} - заявка от {self.user.get_display_name()} на бревет {self.event}"


def get_event_years(reverse=True, finished=True):
    """Returns a list of event years for use in selectors"""
    years = {x.date.year for x in Event.objects.filter(finished=finished, club=DEFAULT_CLUB_ID)}
    return sorted(list(years), reverse=reverse)


def get_best(distance, randonneur=None, year=None, limit=None, unique_randonneurs=False):
    """Returns best results on brm distance for randonneur 
    (or all randonneurs if None) for a given year (or all years if None)
    """
    query = Result.objects.filter(event__route__distance=distance, event__route__brm=True)
    
    if randonneur:
        query = query.filter(randonneur=randonneur)
    
    if year:
        query = query.filter(event__date__year=year)
    
    query = query.order_by("time", "event__date")

    if unique_randonneurs:
        for q in query:
            query = query.exclude(randonneur=q.randonneur, time__gt=q.time)

    if limit and len(query) > limit:
        while query[limit-1].time == query[limit].time:
            limit += 1
        query = query[:limit]
    return query


def get_randonneurs(year=None):
    """Returns a list of randonneurs for a given year (or all randonneurs if None). 
    NOTE: randonneurs with no results are omitted on purpose."""
    randonneurs = set()
    results = Result.objects.filter(event__finished=True)
    if year:
        results = results.filter(event__date__year=year)
    for result in list(results):
        randonneurs.add(result.randonneur)
    return randonneurs


def timedelta_to_str(t:timedelta):
    return "{:02d}:{:02d}".format(t.days*24 + t.seconds//3600, t.seconds%3600//60)