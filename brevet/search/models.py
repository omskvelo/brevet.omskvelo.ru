from brevet_database.models import Randonneur, Event, Route

def search(class_name:str, query:str):
    # NOTE: Since we use SqLite and mostly cyrrilic characters, __icontains does not work as expected: https://docs.djangoproject.com/en/4.0/ref/databases/#sqlite-notes

    if class_name == 'Randonneur':  
        object_class = Randonneur

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


    elif class_name == 'Event':
        object_class = Event

        # Search cyrillic name:
        results = object_class.objects.filter(name__contains=query.capitalize())
        results |= object_class.objects.filter(name__contains=query.lower())

        if query.isdigit():
            try: 
                # Search distance:
                results |= object_class.objects.filter(route__distance=int(query), route__active=True)
                results |= results.exclude(route__name="")

                # Search year
                if int(query) in range (2010,2100):
                    results |= object_class.objects.filter(date__year=int(query))
            except ValueError:
                pass 


    elif class_name == 'Route':
        object_class = Route

        # Search cyrillic name:
        results = object_class.objects.filter(name__contains=query.capitalize())
        results |= object_class.objects.filter(name__contains=query.lower())
        results |= object_class.objects.filter(name=query.title())

        if query.isdigit():
            try: 
                # Search distance:
                results |= object_class.objects.filter(distance=int(query), active=True)
            except ValueError:
                pass   


    return list(results)