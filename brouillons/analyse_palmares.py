import pandas as pnd
pnd.set_option('display.max_columns',None)
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from utils import (
    setTempSecondePalmares
)
dataframe_palmares = pnd.read_csv('datas/arc-palmares.csv')


# Ajout colonne Sexe et Age
dataframe_palmares['Sexe'] = dataframe_palmares['S/A'].astype(str).str[0]
dataframe_palmares['Age'] = dataframe_palmares['S/A'].astype(str).str[2].astype(int)
dataframe_palmares['Is_male'] = (dataframe_palmares['Sexe']=='M').astype(int)

# supprimer la colonne 'S/A'
del dataframe_palmares['S/A']

# renommer certaines colonnes
dataframe_palmares.rename(columns = {'Vainqueur' : 'Gagnant', 'Année' : 'Annee'}, inplace = True)

# ajouter colonne Temps_sec
setTempSecondePalmares(dataframe_palmares)

dataframe_palmares.info()

dataframe_palmares.to_csv('datas/arc-arrivees.csv')

"""

print(dataframe_palmares.head(50))

axe_X = sns.countplot(x="Age", data=dataframe_palmares)
plt.xticks(rotation= 90)
plt.xlabel('Age')
plt.ylabel('Total ')
plt.title("Age cheveaux ayant gagné l'Arc de Triomphe")
plt.show()

"""
























if False:

    def setTempsSec(Annee):
        with open("datas/arc-palmares.csv", newline='') as csvfile:
            palmares = csv.reader(csvfile)
            next(palmares)
            for palm in palmares:
                secondes = 0
                if palm[0]==Annee:
                    chrono = palm[12];
                    print(chrono)
                    print(type(chrono))
                    if len(chrono[0]):
                        secondes += int(chrono[0]) * 60
                    if len(chrono[0]):
                        secondes += int(chrono[2:4])
                    if len(chrono[5:]):
                        secondes += float('0.' + chrono[5:])
            return secondes

    dataframe_palmares['Temps_sec'] = ((dataframe_palmares['Temps'].astype(str).str[0].astype(int)*60) + dataframe_palmares['Temps'].astype(str).str[2:4].astype(int) ) * 1.0
