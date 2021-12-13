from datetime import datetime, time

from django.db import models
from django.urls import reverse
from django.utils import timezone

DEFAULT_CLUB_ID = 1

class Club(models.Model):
    name = models.CharField(max_length=50, blank=False)
    ACP_code = models.IntegerField(blank=False)
    
    def __str__(self):
        return " ".join((self.name, str(self.ACP_code)))

class Randonneur(models.Model):
    name = models.CharField(max_length=50, blank=False)
    surname = models.CharField(max_length=50, blank=False)
    russian_name = models.CharField(max_length=50, blank=False)
    russian_surname = models.CharField(max_length=50, blank=False)
    image = models.ImageField(upload_to="img/users/", blank=True)
    club = models.ForeignKey(Club, on_delete=models.PROTECT, default=DEFAULT_CLUB_ID)
    female = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('personal_stats', kwargs={'surname' : self.surname, 'name' : self.name})

    def __str__(self):
        return " ".join((self.russian_surname,self.russian_name))

class Route(models.Model):
    name = models.CharField(max_length=200, blank=True) 
    slug = models.SlugField(blank=True)
    distance = models.IntegerField(blank=False)
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
        distance = str(self.distance)
        name = str(self.name)
        club = str(self.club) if self.club.id != DEFAULT_CLUB_ID else ""
        return "{} км {: <20} {} ".format(distance, name, club)     

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

    def get_absolute_url(self):
        date = datetime.strftime(self.date, "%Y%m%d")
        return reverse('event', kwargs={'distance' : self.route.distance, 'date' : date})

    def get_protocol_url(self):
        date = datetime.strftime(self.date, "%Y%m%d")
        return reverse('protocol', kwargs={'distance' : self.route.distance, 'date' : date})

    def get_date(self):
        return self.date.strftime("%d.%m.%Y")

    def get_time(self):
        return self.time.strftime("%H:%M")

    def get_controls(self):        
        return self.route.get_controls
    
    def get_text(self):
        return self.text.split("\n")

    def __str__(self):
        date = datetime.strftime(self.date, "%Y.%m.%d")
        distance = str(self.route.distance)
        club = str(self.club) if self.club.id != DEFAULT_CLUB_ID else ""
        return f"{date} {distance} км {self.route.name} {club}"     

class Result(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    homologation = models.CharField(max_length=50, blank=True) 
    randonneur = models.ForeignKey(Randonneur, on_delete=models.CASCADE) 
    time = models.DurationField(blank=True)
    success = models.BooleanField(default=True)
    medal = models.BooleanField(default=False)
    comment = models.CharField(max_length=200,blank=True) 

    def get_date(self):
        return self.event.get_date()

    def get_time(self):
        return "{:02d}:{:02d}".format(self.time.days*24 + self.time.seconds//3600, self.time.seconds%3600//60)

    def __str__(self):
        date = datetime.strftime(self.event.date, "%Y.%m.%d")
        randonneur = str(self.randonneur)
        distance = str(self.event.route.distance)
        result = self.get_time()
        success = "" if self.success else str(self.comment)
        return "{} {} км {} {} {}".format(date,  distance, randonneur, result, success)

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
