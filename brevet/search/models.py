from brevet_database.models import Randonneur, Event, Route

def search(class_name:str, query:str, recursive=False):
    # NOTE: Since we use SqLite and mostly cyrrilic characters, __icontains does not work as expected: https://docs.djangoproject.com/en/4.0/ref/databases/#sqlite-notes

    if not query.isalnum():
        return []

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

    results = list(results)

    if not recursive:
        results = results + search(class_name, query=convert_layout(query), recursive=True)

    return results


layout_pairs = {
    'q' : 'й', 'w' : 'ц', 'e' : 'у', 'r' : 'к', 't' : 'е', 'y' : 'н', 'u' : 'г', 
    'i' : 'ш', 'o' : 'щ', 'p' : 'з', '[' : 'х', ']' : 'ъ', 'a' : 'ф', 's' : 'ы', 
    'd' : 'в', 'f' : 'а', 'g' : 'п', 'h' : 'р', 'j' : 'о', 'k' : 'л', 'l' : 'д', 
    ';' : 'ж','\'' : 'э', 'z' : 'я', 'x' : 'ч', 'c' : 'с', 'v' : 'м', 'b' : 'и', 
    'n' : 'т', 'm' : 'ь', ',' : 'б', '.' : 'ю',

    'й' : 'q', 'ц' : 'w', 'у' : 'e', 'к' : 'r', 'е' : 't', 'н' : 'y', 'г' : 'u', 
    'ш' : 'i', 'щ' : 'o', 'з' : 'p', 'х' : '[', 'ъ' : ']', 'ф' : 'a', 'ы' : 's', 
    'в' : 'd', 'а' : 'f', 'п' : 'g', 'р' : 'h', 'о' : 'j', 'л' : 'k', 'д' : 'l', 
    'ж' : ';', 'э' :'\'', 'я' : 'z', 'ч' : 'x', 'с' : 'c', 'м' : 'v', 'и' : 'b', 
    'т' : 'n', 'ь' : 'm', 'б' : ',', 'ю' : '.', 
}

def convert_layout(s:str):
    """ Converts between ru-RU and rn-US keyboard layouts """
    s = s.lower()
    return "".join([layout_pairs[letter] for letter in s if letter in layout_pairs])
