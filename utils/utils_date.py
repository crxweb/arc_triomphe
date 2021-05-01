"""
Fonctions utiles pour gestion de dates
"""
import datetime

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def next_sunday():
    year, month, day = 2020, 9, 30
    d = datetime.date(year, month, day)
    next_sunday = next_weekday(d, 6) # 0 = Monday, 1=Tuesday, 2=Wednesday...
    print(next_sunday)
    return next_sunday

"""
Retourne x dernières dates du prix de l'arc de triomphe
"""
def arctriomphe_date(nb_years):
    current_year = datetime.date.today().year
    print(current_year)
    range_years = range(current_year-nb_years, current_year)
    print(range_years)

    dates = []
    for year in range_years:
        month, day = 9, 30
        d = datetime.date(year, month, day)
        next_sunday = next_weekday(d, 6)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
        dates.append(next_sunday)

    return dates

