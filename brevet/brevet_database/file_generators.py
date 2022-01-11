from io import BytesIO

import xlsxwriter

from django.http import HttpResponse

def get_xlsx_protocol(event, results, filename):
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

        worksheet.write(row, 0, result.homologation, text_format)
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

    response = HttpResponse(file, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f"attachment; filename={filename}.xlsx"
    file.close()

    return response

def get_xlsx_personal_stats(
        randonneur, 
        years_active, 
        sr, 
        total_distance, 
        total_brevets, 
        results, 
        elite_dist, 
        best_200, 
        best_300, 
        best_400, 
        best_600,
        filename):
    """Generates xlsx file with all user stats for download"""

    file = BytesIO()
    workbook = xlsxwriter.Workbook(file,  {'in_memory': True})
    worksheet_total = workbook.add_worksheet("Общие сведения")
    worksheet_results = workbook.add_worksheet("Все результаты")
    worksheet_elite = workbook.add_worksheet("LRM, 1000, SR600")
    worksheet_200 = workbook.add_worksheet("200")
    worksheet_300 = workbook.add_worksheet("300")
    worksheet_400 = workbook.add_worksheet("400")
    worksheet_600 = workbook.add_worksheet("600")

    # Set formats
    text_format = workbook.add_format({'align':'left'})
    int_format = workbook.add_format({'align':'right', 'num_format' : '0'})
    time_format = workbook.add_format({'align':'center', 'num_format' : '[h]:mm:ss;@'})
    date_format = workbook.add_format({'align':'center', 'num_format' : 'DD.MM.YYYY;@'})

    # ==== TOTAL STATS SHEET ====
    worksheet = worksheet_total

    # Set colomn width
    worksheet.set_column(0,2, width=16)

    # Write static data
    worksheet.write(0, 0, "Фамилия", text_format)
    worksheet.write(1, 0, "Имя", text_format)
    worksheet.write(2, 0, "Клуб", text_format)
    worksheet.write(3, 0, "Всего км", text_format)
    worksheet.write(4, 0, "Всего бреветов", text_format)
    worksheet.write(5, 0, "Годы активности", text_format)
    worksheet.write(6, 0, "Суперрандоннёр", text_format)

    # Write dynamic data
    worksheet.write(0, 1, randonneur.russian_surname, text_format)
    worksheet.write(0, 2, randonneur.surname, text_format)
    worksheet.write(1, 1, randonneur.russian_name, text_format)
    worksheet.write(1, 2, randonneur.name, text_format)
    worksheet.write(2, 1, randonneur.club.name, text_format)
    worksheet.write(2, 2, randonneur.club.ACP_code, text_format)
    worksheet.write(3, 1, total_distance, int_format)
    worksheet.write(4, 1, total_brevets, int_format)
    worksheet.write(5, 1, years_active, text_format)
    worksheet.write(6, 1, sr, text_format)

    # ==== RESULT SHEETS ====
    write_results_sheet(worksheet_results, results, time_format, text_format, date_format, int_format)
    write_results_sheet(worksheet_200, best_200, time_format, text_format, date_format, int_format)
    write_results_sheet(worksheet_300, best_300, time_format, text_format, date_format, int_format)
    write_results_sheet(worksheet_400, best_400, time_format, text_format, date_format, int_format)
    write_results_sheet(worksheet_600, best_600, time_format, text_format, date_format, int_format)
    write_results_sheet(worksheet_elite, elite_dist, time_format, text_format, date_format, int_format)

    workbook.close()
    file.seek(0)

    response = HttpResponse(file, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f"attachment; filename={filename}.xlsx"
    file.close()

    return response

def get_xlsx_club_stats(
        total_distance,
        total_randonneurs,
        total_sr,
        sr,
        distance_rating,
        best_200,
        best_300,
        best_400,
        best_600,
        elite_dist,
        year,
        years,
        filename):
    """Generates xlsx file with club stats for download"""

    file = BytesIO()
    workbook = xlsxwriter.Workbook(file,  {'in_memory': True})
    worksheet_total = workbook.add_worksheet("Общие сведения")
    worksheet_rating = workbook.add_worksheet("Рейтинг по дистанции")
    worksheet_elite = workbook.add_worksheet("LRM, 1000, SR600")
    worksheet_200 = workbook.add_worksheet("200")
    worksheet_300 = workbook.add_worksheet("300")
    worksheet_400 = workbook.add_worksheet("400")
    worksheet_600 = workbook.add_worksheet("600")

    # Set formats
    text_format = workbook.add_format({'align':'left'})
    int_format = workbook.add_format({'align':'right', 'num_format' : '0'})
    time_format = workbook.add_format({'align':'center', 'num_format' : '[h]:mm:ss;@'})
    date_format = workbook.add_format({'align':'center', 'num_format' : 'DD.MM.YYYY;@'})

    # ==== TOTAL STATS SHEET ====
    worksheet = worksheet_total

    # Set colomn width
    worksheet.set_column(0,2, width=24)

    # Write static data
    worksheet.write(0, 0, "Показатели за год", text_format)
    worksheet.write(1, 0, "Общая дистанция", text_format)
    worksheet.write(2, 0, "Всего участников", text_format)
    worksheet.write(3, 0, "Суперрандоннёры:", text_format)

    # Write dynamic data
    if year:
        worksheet.write(0, 1, year, int_format)
    else:
        worksheet.write(0, 1, f"{years[-1]} - {years[0]}", text_format)
    worksheet.write(1, 1, total_distance, int_format)
    worksheet.write(2, 1, total_randonneurs, int_format)
    worksheet.write(3, 1, total_sr, int_format)

    row = 3
    for s in sr:
        worksheet.write(row, 1, f"{s.russian_surname} {s.russian_name} {s.sr_string}", text_format)
        row += 1

    # ==== RESULT SHEETS ====
    write_results_sheet(worksheet_200, best_200, time_format, text_format, date_format, int_format)
    write_results_sheet(worksheet_300, best_300, time_format, text_format, date_format, int_format)
    write_results_sheet(worksheet_400, best_400, time_format, text_format, date_format, int_format)
    write_results_sheet(worksheet_600, best_600, time_format, text_format, date_format, int_format)
    write_results_sheet(worksheet_elite, elite_dist, time_format, text_format, date_format, int_format)

    # ==== RATINGS SHEET ====
    worksheet = worksheet_rating

    # Set colomn width
    worksheet.set_column(0,0, width=24)
    worksheet.set_column(1,2, width=14)

    # Write static data
    worksheet.write(0, 0, "Рандоннер", text_format)    
    worksheet.write(0, 1, "Всего км", text_format)
    worksheet.write(0, 2, "Всего бреветов", text_format)

    # Write dynamic data
    row = 1
    for result in distance_rating:
        worksheet.write(row, 0, f"{result[0].russian_surname} {result[0].russian_name}" , text_format)
        worksheet.write(row, 1, result[1], int_format)
        worksheet.write(row, 2, result[2], int_format)
        row += 1

    workbook.close()
    file.seek(0)

    response = HttpResponse(file, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f"attachment; filename={filename}.xlsx"
    file.close()

    return response

def write_results_sheet(worksheet, results, time_format, text_format, date_format, int_format):
    # Set colomn width
    worksheet.set_column(0,0, width=24)
    worksheet.set_column(1,2, width=12)
    worksheet.set_column(3,3, width=30)    
    worksheet.set_column(4,4, width=22)
    worksheet.set_column(5,5, width=12)
    worksheet.set_column(6,6, width=14)

    # Write static data
    worksheet.write(0, 0, "Рандоннер", text_format)    
    worksheet.write(0, 1, "Дистанция", text_format)
    worksheet.write(0, 2, "Дата", text_format)
    worksheet.write(0, 3, "Маршрут", text_format)
    worksheet.write(0, 4, "Клуб-организатор", text_format)
    worksheet.write(0, 5, "Время", text_format)
    worksheet.write(0, 6, "Омологация", text_format)


    # Write dynamic data
    row = 1
    for result in results:
        worksheet.write(row, 0, f"{result.randonneur.russian_surname} {result.randonneur.russian_name}", text_format)
        worksheet.write(row, 1, result.event.route.distance, int_format)
        worksheet.write(row, 2, result.event.get_date(), date_format)
        worksheet.write(row, 3, result.event.route.name, text_format)
        worksheet.write(row, 4, result.event.club.name, text_format)
        worksheet.write(row, 5, result.get_time(), time_format)
        worksheet.write(row, 6, result.homologation, text_format)
        row += 1