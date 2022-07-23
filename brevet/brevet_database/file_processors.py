from datetime import datetime, timedelta

import xlrd


def read_xls_protocol(file):
    """Reads *.xls file returned by ACP"""
    exception = None
    content = {}
    try:
        book = xlrd.open_workbook(file_contents=file.read(), ignore_workbook_corruption=True)
        sheet = book.sheet_by_index(0)
        rows = sheet.nrows

        date = sheet.cell_value(rowx=1, colx=5)
        distance = sheet.cell_value(rowx=1, colx=6)
        code = sheet.cell_value(rowx=1, colx=4)      

        content["date"] = datetime.strptime(date, "%d/%m/%Y").date()
        content["distance"] = int(distance[:-2].strip())
        content["code"] = int("".join(x for x in code if x.isdigit()))
        content["results"] = []

        row = 3
        col_homologation = 0
        col_surname = 1
        col_name = 2
        col_code = 5
        col_time = 6
        col_medal = 7
        col_female = 8

        while row < rows:

            # Read data
            homologation = sheet.cell_value(rowx=row, colx=col_homologation)
            surname = sheet.cell_value(rowx=row, colx=col_surname)
            name = sheet.cell_value(rowx=row, colx=col_name)
            code = sheet.cell_value(rowx=row, colx=col_code)
            time = sheet.cell_value(rowx=row, colx=col_time)
            medal = sheet.cell_value(rowx=row, colx=col_medal)
            female = sheet.cell_value(rowx=row, colx=col_female)
            
            # Format data
            homologation = str(int(homologation))
            surname = surname.title()
            name = name.title()
            code = int(code)
            h,m = time.split(":")
            time = timedelta(hours=int(h), minutes=int(m))
            medal = medal != ""
            female = female != ""
            
            result = {
                'homologation' : homologation,
                'surname' : surname,
                'name' : name,
                'code' : code,
                'time' : time,
                'medal' : medal,
                'female' : female,
            }
            content["results"].append(result)

            row +=1 
            book.release_resources()

            
    except Exception as e:
        exception = str(e)

    return content, exception