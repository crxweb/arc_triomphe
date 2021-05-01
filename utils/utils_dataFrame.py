import os
import pandas as pnd
pnd.set_option('display.max_columns',None)
import csv


def setTempSecondePalmares(dataframe_palmares):
    with open("datas/arc-palmares.csv", newline='') as csvfile:
        palmares = csv.reader(csvfile)
        next(palmares)
        for palm in palmares:
            secondes = 0
            chrono = palm[12]
            minute = int(chrono.split("'")[0])
            secondes += minute * 60
            seconde = int(chrono.split("'")[1].split('"')[0])
            secondes += seconde
            mseconde = float('0.' + chrono.split("'")[1].split('"')[1])
            secondes += mseconde
            dataframe_palmares.loc[dataframe_palmares.Annee == int(palm[0]), 'Temps_sec'] = secondes

def getChevauxDepart(year = None):
    if year:
        df = pnd.read_csv('datas/input/departs/iturf/arc-depart-'+str(year)+'.csv')
        chevaux = df['Cheval'].unique()
    else:
        list = []
        listeDeFichiers = os.listdir("datas/input/departs/iturf")
        for fichier in listeDeFichiers:
            df = pnd.read_csv('datas/input/departs/iturf/'+fichier)
            list.extend(df['Cheval'].unique())
        chevaux = set(list)

    return chevaux




"""
group_by_sexe = dataframe_palmares.groupby('Sexe').count()
print(group_by_sexe)

group_by_age = dataframe_palmares.groupby('Age').count()
print(group_by_age)

group_by_jockey = dataframe_palmares.groupby('Jockey').count().sort_values(by = "Age",ascending = False)
print(group_by_jockey)

search_dettori = dataframe_palmares[dataframe_palmares['Jockey']=='Lanfranco Dettori']
print(search_dettori)
"""
