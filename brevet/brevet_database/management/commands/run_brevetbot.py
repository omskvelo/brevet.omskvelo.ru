import logging
import os
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from base64 import b64encode

from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from brevet_database.models import Event, DEFAULT_CLUB_ID

API_KEY = os.environ.get('INVISION_API_KEY')
URL = "https://omskvelo.ru/api/forums/topics"
FORUM = 54
AUTHOR = 14225
TEMPLATE = "brevet_database/forum_topic.html"


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        logging.info('Starting BrevetBot...')
        events = Event.objects.filter(
            finished=False, 
            club=DEFAULT_CLUB_ID,
            omskvelo_xref='',
            date__lt=now()+timedelta(days=14),
            date__gt=now()
            )
        
        for event in events:
            title = str(event)
            site = Site.objects.get_current()

            context = {
                'site': site.name,
                'event': event
            }

            post = render_to_string(TEMPLATE, context)

            query = urlencode({
                'forum': FORUM,
                'title': title,
                'post': post,
                'author': AUTHOR,
            })

            auth_str = b64encode(f"{API_KEY}:".encode('ascii'))

            request = Request(url=f"{URL}?{query}", data=b'', method='POST')
            request.add_header("Authorization", "Basic %s" % auth_str.decode('ascii'))  
            request.add_header("Content-Length", "0")
            request.add_header("Host", "omskvelo.ru")
            request.add_header("User-Agent", "HTTPie")

            try:
                response = urlopen(request)
                logging.info(f"BrevetBot: Event id{event.pk} posted: {response.status} {response.reason}")
                response_body = json.loads(response.read().decode())
                event.omskvelo_xref = response_body['forum']['url']
                event.save()
                
            except Exception:
                logging.exception("BrevetBot exception")
