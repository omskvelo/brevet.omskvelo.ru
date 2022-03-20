import os.path
from datetime import datetime, time, timedelta

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from django.core.management.base import BaseCommand
from brevet_database.models import *


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print ("Accessing Google Sheelts...")
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        SPREADSHEET_ID = '14BVUTzB-7KYsxwDrKHi4W96XJUxXIbFntL5_6r9z1gI'

        creds = None
        if os.path.exists('D:/token.json'):
            creds = Credentials.from_authorized_user_file('D:/token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'D:/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('D:/token.json', 'w') as token:
                token.write(creds.to_json())
        service = build('sheets', 'v4', credentials=creds)

        print ("Access granted. Reading data...")

        sheet = service.spreadsheets()
        gsheet_values = []
        for r in range(2010,2022):
            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=str(r)+"!A2:F").execute()
            gsheet_values += result.get('values', [])
            
        print ("Data acquired. Reading db...")

        randonneurs = Randonneur.objects.all()
        
        # Read existing events to prevent duplicates
        events = []
        for event in Event.objects.all():
            events.append([datetime.strftime(event.date, "%d.%m.%Y"), str(event.route.distance)])

        # Create generic routes as placeholders for further edit
        generic_route = {}
        for route in Route.objects.all():
            if route.name == "":
                generic_route[route.distance] = route     
        
        # Read existing results to prevent duplicates
        results = []
        for result in Result.objects.all():
            results.append([
                result.homologation,
                result.randonneur.surname,
                result.randonneur.name,
                datetime.strftime(result.event.date, "%d.%m.%Y"),
                str(result.event.route.distance),
                "{:d}:{:02d}".format(
                    result.time.days*24 + result.time.seconds//3600, 
                    result.time.seconds%3600//60
                    )
                ])
        
        print ("Creating Events...")

        counter = 0
        for entry in gsheet_values:
            date = entry[3]
            distance = entry[4]
            event = [date, distance]
            if event[1] in ['200','300','400','600'] and event not in events:
                new_event = Event(
                    date=datetime.strptime(event[0],"%d.%m.%Y"),
                    route=generic_route[int(event[1])])
                new_event.save()
                counter += 1
                events.append(event)

        print (f"Events created: {counter}.")

        print ("Populating events...")

        counter = 0
        for entry in gsheet_values:
            if entry not in results:
                try:
                    t = [int(x) for x in entry[5].split(":")]
                    new_result = Result(
                        event=Event.objects.get(
                            date=datetime.strptime(entry[3],"%d.%m.%Y"),
                            route__distance=int(entry[4])),
                        homologation=entry[0],
                        randonneur=Randonneur.objects.get(
                            name=entry[2].strip(),
                            surname=entry[1].strip()),
                        time=timedelta(hours=t[0],minutes=t[1])
                    )
                    new_result.save()
                    counter += 1
                    results.append(entry)
                except Exception: 
                    print (f"Can't add result of {entry[2]} {entry[1]} at date {entry[3]}.")

        print (f"Results transferred: {counter}.")

