import json
import pandas as pnd
from utils import (
    searchChevalByName,
    getChevauxDepart,
    getChevalPerformance,
    getChevalCarriere,
    getChevalEngagement,
    getArcTriompheHistorique,
)
incap_session_name = 'incap_ses_1177_1885728'
incap_session_value = 'k9Hsbm+2DnDFoaptkItVECKVhWAAAAAAE6flKnvdwMFjf5L/RWu1Ng==';



# [ok] Génère CSV liste chevaux
def makeCsvChevaux():

    # Liste des chevaux figurant au départ de 2008 à 2020 (source ITURF)
    chevaux_depart = getChevauxDepart()
    #chevaux_depart = ['TALISMANIC'];

    horses_list = []
    for horse in chevaux_depart:
        search_fg = searchChevalByName(horse, incap_session_name, incap_session_value, fake=False)
        if search_fg:
            data = pnd.DataFrame.from_records(search_fg,index=[0])
            horses_list.append(data)
    if len(horses_list):
        horses_list = pnd.concat(horses_list, ignore_index=True)
        horses_list.to_csv('datas/output/chevaux_brute.csv')

# [ok] Génère CSV liste chevaux_performance
def makeCsvChevauxPerformance():
    perf_list = []
    df = pnd.read_csv('datas/output/chevaux.csv')
    for row in df.itertuples():
        #print('Cheval: ', row.NomCheval, 'id: ', row.NumSire)
        cheval_id = row.NumSire
        cheval_nom = row.NomCheval
        fg_perf = getChevalPerformance(cheval_id,incap_session_name,incap_session_value,fake=False)
        data = pnd.DataFrame.from_records(fg_perf)
        data.insert(0, "fg_id", cheval_id, True)
        data.insert(1, "NomCheval", cheval_nom, True)
        perf_list.append(data)
    if len(perf_list):
        perf_list = pnd.concat(perf_list,ignore_index=True)
        perf_list.to_csv('datas/output/cheval_performance.csv')

# [ok] Génère CSV liste chevaux_carriere
def makeCsvChevauxCarriere():
    carriere_list = []
    df = pnd.read_csv('datas/output/chevaux.csv')
    for row in df.itertuples():
        #print('Cheval: ', row.NomCheval, 'id: ', row.NumSire)
        cheval_id = row.NumSire
        cheval_nom = row.NomCheval
        fg_carriere = getChevalCarriere(cheval_id,incap_session_name,incap_session_value,fake=False)
        data = pnd.DataFrame.from_records(fg_carriere)
        data.insert(0, "fg_id", cheval_id, True)
        data.insert(1, "NomCheval", cheval_nom, True)
        carriere_list.append(data)
    if len(carriere_list):
        carriere_list = pnd.concat(carriere_list,ignore_index=True)
        carriere_list.to_csv('datas/output/cheval_carriere.csv')

# [ok] Génère CSV liste chevaux_engagement
def makeCsvChevauxEngagement():
    engagement_list = []
    df = pnd.read_csv('datas/output/chevaux.csv')
    for row in df.itertuples():
        print('Cheval: ', row.NomCheval, 'id: ', row.NumSire)
        cheval_id = row.NumSire
        cheval_nom = row.NomCheval
        fg_engagement = getChevalEngagement(cheval_id,incap_session_name,incap_session_value,fake=False)
        data = pnd.DataFrame.from_records(fg_engagement)
        data.insert(0, "fg_id", cheval_id, True)
        data.NomCheval = cheval_nom
        data.NumSire = cheval_id
        engagement_list.append(data)
    if len(engagement_list):
        engagement_list = pnd.concat(engagement_list,ignore_index=True)
        engagement_list.to_csv('datas/output/cheval_engagement.csv')

# [ok] Génère CSV historique Prix Arc de Triomphe
def makeCsvArcTriompheHistorique():
    getArcTriompheHistorique(incap_session_name,incap_session_value)

# Make csv files BRUT/FranceGalop
makeCsvChevaux()
#makeCsvChevauxPerformance()
#makeCsvChevauxCarriere()
#makeCsvChevauxEngagement()
#makeCsvArcTriompheHistorique()





