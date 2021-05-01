import pandas as pd
from FranceGalop import (
    course,
    utils,
    cheval,
)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

course_folder = 'collecte/france_galop/courses/';
cheval_folder = 'collecte/france_galop/chevaux/';

# Enregistre csv / fiche course Arc de Triomphe (source : france galop)
def make_csv_course():
    course_url = [
        "https://www.france-galop.com/fr/course/detail/2020/P/dXdodlJzTFVzMUFRT0FrOERIWDIyQT09",
        "https://www.france-galop.com/fr/course/detail/2019/P/c0xHRGZBeWkzcDhqa1orc0xLRjdQZz09",
        "https://www.france-galop.com/fr/course/detail/2018/P/VWx6R3k1MTVUNWFtY2lac1J1MGRpdz09",
        "https://www.france-galop.com/fr/course/detail/2017/P/aVluMkQ4cXNQS3JEanlXR04vR2Rkdz09",
        "https://www.france-galop.com/fr/course/detail/2016/P/NnJNYW1oY1JuTmNlUi9Wa2NaNXpsQT09",
        "https://www.france-galop.com/fr/course/detail/2015/P/MWlGcFp6YVFvMGRuSURmdUhqeFp5Zz09",
        "https://www.france-galop.com/fr/course/detail/2014/P/ZTlZWnpxR25DVmtNeGVlelFkclBNdz09",
        "https://www.france-galop.com/fr/course/detail/2013/P/THhJSjhIcmx4eEx1Sm1XMy92WWVOdz09",
        "https://www.france-galop.com/fr/course/detail/2012/P/Tmg4UnR3VzdQNEFSVjNqNjBVMlc5QT09",
        "https://www.france-galop.com/fr/course/detail/2011/P/TnJINVNUR1d3WGlCcUM5dUpZVDZwdz09",
        "https://www.france-galop.com/fr/course/detail/2010/P/N3RycGd1V3UxVFB2NjNyOW4yS1FwZz09",
        "https://www.france-galop.com/fr/course/detail/2009/P/YmwwSDJwc1ZINkhOVUQ0d2JvbUFyUT09",
        "https://www.france-galop.com/fr/course/detail/2008/P/N3M4RzZFRmF4T1ZRUW5sVTkzWm44dz09",
        "https://www.france-galop.com/fr/course/detail/2007/P/M2sxMDRKTkMyZkZ2cW1XMFRvdlFEdz09",
        "https://www.france-galop.com/fr/course/detail/2006/P/TVNuUy9QTG8zRis1WWg3bWdHYm5sdz09",
        "https://www.france-galop.com/fr/course/detail/2005/P/eXJuK0wwOUJJSTVvUjdIcUR3ZWtMdz09",
        "https://www.france-galop.com/fr/course/detail/2004/P/TUNYNVg0NEF4Uk9QOGoyUVFFTUhJdz09",
        "https://www.france-galop.com/fr/course/detail/2003/P/dW5WVkFMdVp5dld1cjhNSmNEUUFrdz09",
        "https://www.france-galop.com/fr/course/detail/2002/P/bEJ4OE11dGZUSkIwRWp2RW5BLzZPQT09",
        "https://www.france-galop.com/fr/course/detail/2001/P/SEpJc1NxR3pmNDFoaE9JR2JrODAzZz09",
        "https://www.france-galop.com/fr/course/detail/2000/P/aEdrbGdqZ1N1SEpncmJwUXdDUnJYUT09",
        "https://www.france-galop.com/fr/course/detail/1999/P/R21WbFZRdWs5ZENuRDI4VTA1cVZudz09",
        "https://www.france-galop.com/fr/course/detail/1998/P/Z0lmNEdEek1SS2hQUnpHV083Y2tvZz09",
        "https://www.france-galop.com/fr/course/detail/1997/P/ZThhQWxIcVBmVmFLUGhqSjlVeVNRdz09",
        "https://www.france-galop.com/fr/course/detail/1996/P/VmdtNEFzbExvWVlVNmhsVjJvVndjUT09",
        "https://www.france-galop.com/fr/course/detail/1995/P/MkdmVHpwVWgzODl2SG9PbWk0U0xJdz09",
        "https://www.france-galop.com/fr/course/detail/1994/P/ZHAza0JCa2FHMmZ6bkM1dmtLNXhzUT09",
        "https://www.france-galop.com/fr/course/detail/1993/P/L0x5MXVOQjl5UjdDSWdFZjc2d0ZLZz09",
    ]
    for url in course_url:
        course.save_fiche_course(url, course_folder)


# make_csv_course()
# course.reorder_fiche_course(course_folder)
#course.add_columns_info_cheval(course_folder)

"""
cheval_id = 'bytINmx4MVZBT3Z1cGlVTTEzYUlTQT09'
fiche_detail = cheval.fiche_detail(cheval_id)
print(fiche_detail)
"""

#cheval.make_csv(course_folder, cheval_folder)

"""
cheval.new_make_csv(process="make_csv_by_course" ,input_folder=course_folder, output_folder=cheval_folder)
def new_make_csv(process, input_folder=None, output_folder=None, input_csv=None, output_csv=None):
# appeller fonction process avec paramètre
"""

# test info cheval -- faire un fichier csv pour interpretation (on doit garder historique du traitement)
"""
- faire un csv traitement (pour chaque ressource, version, fonction, total taite sucess/failed % taux ..)
- rajouter une colonne indiquant id du traitement + rapport traitement (on doit pouvoir savoir si le row
est considéré comme complètement traité par l'algo de base ou si doit être retraité)
- 1 on fait un csv avec à minima l'id,le nom du cheval (avec info et infoyear)
- 2 on fait un 2ème csv sur la base du premier en traitant les données manquantes
- 3 un 3ème csv pour traiter les manquant (et ainsi de suite)

df_cheval = pd.read_csv('collecte/france_galop/chevaux/chevaux_from_course.csv')
df_reprise = df_cheval[(df_cheval['race'].isna()) & (df_cheval['infoyear'] != 2000)]
df_reprise = df_reprise[['info', 'infoyear']]
print(df_reprise)
"""

cheval.make_csv_from_course()
#cheval.search_by_name('LANDO')

