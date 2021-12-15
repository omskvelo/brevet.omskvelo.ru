from io import BytesIO

import xlsxwriter

# Assortment of tools that did not fit neatly into views.py

def get_xlsx_protocol(event, results):
    """Generates a protocol file that can be submitted to ACP"""
    results = sorted(results, key=lambda x: x.randonneur.surname)   

    file = BytesIO()
    workbook = xlsxwriter.Workbook(file,  {'in_memory': True})
    worksheet = workbook.add_worksheet(f"{event.route.distance} - {event.get_date()}")

    # Set formats
    text_format = workbook.add_format({'border': True, 'align':'center'})
    name_format = workbook.add_format({'border': True, 'align':'left'})
    time_format = workbook.add_format({'border': True, 'align':'center', 'num_format' : '[h]:mm:ss;@'})
    date_format = workbook.add_format({'border': True, 'align':'center', 'num_format' : 'DD.MM.YYYY;@'})

    # Set colomn width
    worksheet.set_column(0,0, width=12)
    worksheet.set_column(1,1, width=19)
    worksheet.set_column(2,2, width=12)
    worksheet.set_column(3,3, width=15)
    worksheet.set_column(4,8, width=12)

    # Merge cells
    worksheet.merge_range('B1:D1', "", text_format)
    worksheet.merge_range('H1:I1', "", text_format)
    worksheet.merge_range('B2:D2', "", text_format)
    worksheet.merge_range('D3:E3', "", text_format)

    # Write static header data
    worksheet.write(0, 0, "", text_format)
    worksheet.write(0, 1, "CLUB ORGANISATEUR", text_format)
    worksheet.write(0, 4, "code ACP", text_format)
    worksheet.write(0, 5, "DATE", text_format)
    worksheet.write(0, 6, "DISTANCE", text_format)
    worksheet.write(0, 7, "INFORMATIONS", text_format)

    worksheet.write(1, 0, "'N° de brevet ", text_format)
    worksheet.write(1, 7, "Médaille", text_format)
    worksheet.write(1, 8, "Sexe", text_format)

    worksheet.write(2, 0, "", text_format)
    worksheet.write(2, 1, "NOM", text_format)
    worksheet.write(2, 2, "PRENOM", text_format)
    worksheet.write(2, 3, "CLUB DU PARTICIPANT", text_format)
    worksheet.write(2, 5, "CODE ACP", text_format)
    worksheet.write(2, 6, "TEMPS", text_format)
    worksheet.write(2, 7, "(x)", text_format)
    worksheet.write(2, 8, "(F)", text_format)

    # Write dynamic header data
    worksheet.write(1, 1, event.club.french_name, text_format)
    worksheet.write(1, 4, event.club.ACP_code, text_format)
    worksheet.write(1, 5, event.get_date(), date_format)
    worksheet.write(1, 6, f"{event.route.distance} km", text_format)

    # Write results data
    row = 3
    for result in results:
        worksheet.merge_range(row, 3, row, 4, "", text_format)

        worksheet.write(row, 0, "", text_format)
        worksheet.write(row, 1, result.randonneur.surname, name_format)
        worksheet.write(row, 2, result.randonneur.name, name_format)
        worksheet.write(row, 3, result.randonneur.club.french_name, text_format)
        worksheet.write(row, 5, result.randonneur.club.ACP_code, text_format)
        worksheet.write(row, 6, result.get_time(), time_format)
        worksheet.write(row, 7, "x" if result.medal else "", text_format)
        worksheet.write(row, 8, "F" if result.randonneur.female else "", text_format)

        row += 1

    workbook.close()
    file.seek(0)

    return file



def get_sr(results):
    """Returns the number of SR qualifications over a list of results for the season."""
    sr = 0
    brevets = [result.event.route.distance for result in results if result.event.route.brm]
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