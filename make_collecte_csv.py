import pandas as pd
from FranceGalop import (
    course,
    utils,
    cheval,
)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# Enregistre csv / fiche course Arc de Triomphe (source : france galop)
def make_csv_course():
    course_url = utils.fg_arc_course_url
    for url in course_url:
        course.save_fiche_course(url, utils.course_folder + "arc_triomphe/")


# Enregistre csv chevaux
def make_csv_chevaux():
    cheval.make_csv_from_course()
    cheval.retrieve_undefined_csv()


# Enregistre csv carrière des chevaux
def make_csv_carriere():
    cheval.make_perf_csv()


def make_csv_course():
    course.make_arc_triomphe_liste_csv()
    course.make_arc_triomphe_csv()
    course.populate_arc_triomphe_liste_csv()

"""
A utiliser dans l'ordre ci-dessous
"""
#make_csv_chevaux()
#make_csv_carriere()
#make_csv_course()




