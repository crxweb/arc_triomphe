import requests
import sys
import json
import os
import pandas as pd
import csv
from bs4 import BeautifulSoup
import glob
from FranceGalop import (
    utils
)
import numpy as np


def search_by_name(name):
    url = "https://www.france-galop.com/fr/horses-and-people/search-ajax?mot="+name+"&type=chevaux"
    payload = {}
    headers = {
        'Cookie': utils.cookie
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)

def old_search_by_name(name):
    """
    OUPS : plus valable (permettait via dict recup annee, race)
    Retourne réponse requête recherche d'un cheval par son nom
    :param name:
    :return:
    """
    url = utils.base_url + '/fr/frglp_global/ajax?module=search&mot=' + name + '&type=IsRechercheCheval'
    headers = utils.get_header()
    r = requests.get(url, headers=headers)
    try:
        res_horses = r.json().get('Chevaux', [])
        return res_horses
    except ValueError as e:
        print('!!! JSON RESPONSE NOT AVAILABLE !!!')
        sys.exit()


def fiche_detail(id):
    url = 'https://www.france-galop.com/fr/cheval/' + id
    headers = utils.get_header()
    r = requests.get(url, headers=headers)
    return r.content

def info_bystring(info_str, year):
    # attention pour annee 2000, ne pas prendre
    #print('####### info by string: ', info_str)
    info = {
        "nom": None,
        "age": None,
        "race": None,
        "pays": None,
        "naissance": None
    }

    block_words = utils.country + utils.sexe_race
    block_words = block_words + list(map(lambda x: x.lower(), block_words))
    country_list = utils.country
    country_list = country_list + list(map(lambda x: x.lower(), country_list))
    racesexe_list = utils.sexe_race
    racesexe_list = racesexe_list + list(map(lambda x: x.lower(), racesexe_list))

    # Extraction nom cheval
    make_name = []
    for item in info_str.split(' '):
        if item not in block_words:
            if item.isdigit():
                break
            make_name.append(item)
    cheval_nom = " ".join(make_name).strip()
    if len(cheval_nom):
        info.__setitem__('nom', cheval_nom)
    #print('extraction nom',cheval_nom)
    info_str = info_str.replace(cheval_nom, '').strip()
    #print('str without nom', info_str)

    return info

def old_make_csv(course_folder, destination_folder):
    """
    Merger tous les fichiers courses dans collecte/france_galop/merged/
    Faire DataFrame groupby ChevalId
    Vérifier si ChevalId est retrouvé dans datas/production/chevaux.csv
        si oui prendre les données
        sinon extraire le nom, indiquer NumSire, extraire la race et le sexe, générer le lien, trouver le pays,

    :param course_folder:
    :param destination_folder:
    :return:
    """
    print('*** make csv chevaux in ', destination_folder)
    all_files = glob.glob(course_folder + "/*.csv")
    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.info()

    # ex supprimer duplicate value pour colonne ChevalId
    """
    frame.sort_values("ChevalId", inplace = True)
    frame.drop_duplicates(subset="ChevalId", keep=False, inplace=True)
    frame.info()    
    """

    #frame.to_csv(destination_folder + "/chevaux_01.csv")
    df_production_chevaux = pd.read_csv('datas/production/chevaux.csv')
    cpt_failed = 0
    for row in frame.itertuples():
        print(row.ChevalId)
        nom_cheval = df_production_chevaux.loc[(df_production_chevaux['id_francegalop'] == row.ChevalId), 'nom'].values
        if nom_cheval.size == 0:
            print('FAILED')
            cpt_failed += 1
        #else:
            print('Nom : ', nom_cheval)
        print('----------------')

    print('total failed',cpt_failed)


def make_csv(course_folder, destination_folder):
    series_id = []
    series_nom = []
    series_sexe = []
    series_naissance = []
    series_race = []
    series_pays = []
    series_info = []
    series_infoyear = []

    """
    series_id.append('xs55z5e555')
    series_nom.append('ZARKAVA')
    series_sexe.append('M')
    series_naissance.append(None)
    series_race.append('M')
    series_pays.append('M')

    # vérifier que l'id n'existe pas déjà
    cheval_toinstert = {
        'id': 'xs55z5e555',
        'nom': 'Ulysse',
        'sexe': 'M',
        'naissance': 2014,
        'race': 'PS',
        'pays': 'JPN'
    }
    if cheval_toinstert.get('id') not in series_id:
        series_id.append(cheval_toinstert.get('id'))
        series_nom.append(cheval_toinstert.get('nom'))
        series_sexe.append(cheval_toinstert.get('sexe'))
        series_naissance.append(cheval_toinstert.get('naissance'))
        series_race.append(cheval_toinstert.get('PS'))
        series_pays.append(cheval_toinstert.get('FR'))


    data = {'id': series_id, 'nom': series_nom, 'sexe': series_sexe, 'naissance': series_naissance, 'race': series_race, 'pays': series_pays}
    df_test = pd.DataFrame.from_dict(data)
    df_test.info()
    print(df_test)
    """

    cpt_echec = 0
    country_list = utils.country
    country_list = country_list + list(map(lambda x: x.lower(), country_list))
    block_words = utils.country + utils.sexe_race
    block_words = block_words + list(map(lambda x: x.lower(), block_words))
    df_production_chevaux = pd.read_csv('datas/production/chevaux.csv')

    # test - Suivre ce modèle pur insérer les chevaux

    """
    data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
    df_test = pd.DataFrame.from_dict(data)
    print(df_test)

    names = ["Chouette", "Zarkava", "Ducon", "Cacahuette"]
    sexe = ["F", "M", "H", "M"]
    id = ["ze25sdf5", "s988ze77", "5555sdf", "ze95dsdf"]
    year = [1995, 2000, 1945, 1956]

    data = {'cheval_id': id, 'nom': names, 'sexe': sexe, 'naissance': year}
    df_test = pd.DataFrame.from_dict(data)
    df_test.info()
    print(df_test)
    
    df_production_chevaux_merged = pd.read_csv('collecte/france_galop/merged/course_distinct_chevalid.csv')
    df_production_chevaux_merged = df_production_chevaux_merged.groupby('Cheval').count()
    for row in df_production_chevaux_merged.itertuples():
        print(row[0])
    
    df_chevaux = pd.DataFrame([],columns=['id', 'nom', 'age', 'sexe'])
    df_chevaux.info()
    print(df_chevaux.head(10))
    
    id_series = pd.Series([],name="id", dtype="float64")
    name_series = pd.Series([], name="nom", dtype="object")
    sexe_series = pd.Series([], name="sexe", dtype="object")
    naissance_series = pd.Series([], name="annee_naissance", dtype="float64")
    print(type(name_series))
    print(name_series)
    """

    if True:

        print('*** MAKE CSV CHEVAUX ***')
        csv_course = glob.glob(course_folder + "/*.csv")
        for filename in csv_course:
            print('--------------- START ', filename, '-------------------')
            year = filename.split(course_folder)[1][:4]
            #print('Année:',year)
            df_course = pd.read_csv(filename, index_col=None, header=0)
            for row_course in df_course.itertuples():
                cheval_toinstert = {
                    'id': None,
                    'nom': None,
                    'sexe': None,
                    'naissance': None,
                    'race': None,
                    'pays': None,
                    'info': None,
                }

                col_nom = row_course.Cheval
                cheval_id = row_course.ChevalId

                cheval_toinstert.__setitem__('info', col_nom)
                cheval_toinstert.__setitem__('id', cheval_id)
                cheval_toinstert.__setitem__('infoyear', year)
                make_name = []
                for item in col_nom.split(' '):
                    if item not in block_words:
                        if item.isdigit():
                            break
                        make_name.append(item)
                cheval_nom = " ".join(make_name).strip()

                if len(cheval_nom):
                    cheval_toinstert.__setitem__('nom', cheval_nom.upper())
                    process = "[ok]"
                    search = df_production_chevaux.loc[(df_production_chevaux['id_francegalop'] == cheval_id)]
                    #print('>> begin search')
                    if not search.empty:
                        search_nom = list(search.nom)
                        search_sexe = list(search.sexe)
                        search_naissance = list(search.naissance)
                        search_race = list(search.race)
                        search_pays = list(search.pays)

                        search_nom = search_nom[0].strip()
                        # VERIFIER SI NOM CHEVAL CORRESPOND
                        search_sexe = search_sexe[0].strip()
                        search_naissance = search_naissance[0]
                        search_race = search_race[0].strip()
                        search_pays = search_pays[0].strip()
                        if search_nom.lower() == cheval_nom.lower():
                            cheval_toinstert.__setitem__('sexe', search_sexe)
                            cheval_toinstert.__setitem__('naissance', search_naissance)
                            cheval_toinstert.__setitem__('race', search_race)
                            cheval_toinstert.__setitem__('pays', search_pays)

                            #print('search >>> [ ', search_nom, ' vs ', cheval_nom, ' ]  ', search_sexe, search_naissance)
                        else:
                            #print('search ERROR >>> [ ', search_nom, ' vs ', cheval_nom, ' ]  ', search_sexe, search_naissance)
                            process = "[FAILED]"
                            cpt_echec += 1

                    else:
                        #print('search >>> EMPTY')
                        process = "[FAILED]"
                        cpt_echec += 1
                        print('determiner age, sexe, annee naissance en fonction de la colonne nom pour le cheval',cheval_nom.upper())
                        print('ATTENTION : traiter la course 2000 à la mnao')
                        #print(col_nom)
                        col_info = col_nom.replace(cheval_nom, '').strip()
                        if year != 2000:
                            #info = info_bystring(col_info, year)
                            info = info_bystring(col_nom, year)
                else:
                    process = "[FAILED]"
                    cpt_echec += 1

                if cheval_toinstert.get('id') not in series_id:
                    series_id.append(cheval_toinstert.get('id'))
                    series_nom.append(cheval_toinstert.get('nom'))
                    series_sexe.append(cheval_toinstert.get('sexe'))
                    series_naissance.append(cheval_toinstert.get('naissance'))
                    series_race.append(cheval_toinstert.get('race'))
                    series_pays.append(cheval_toinstert.get('pays'))
                    series_info.append(cheval_toinstert.get('info'))
                    series_infoyear.append(cheval_toinstert.get('infoyear'))
                print(cheval_toinstert)

                print(process,' | Nom:',cheval_nom,' | #:',cheval_id,' | col_nom:',col_nom)
                print('*****************************************')
            print('--------------- END ', filename, '---------------------')

        print('Total failed',cpt_echec)
        data = {'id': series_id, 'nom': series_nom, 'sexe': series_sexe, 'naissance': series_naissance,
                'race': series_race, 'pays': series_pays, 'info': series_info, 'infoyear': series_infoyear}
        df_test = pd.DataFrame.from_dict(data)
        df_test.info()
        df_test.to_csv(destination_folder + "chevaux_from_course.csv", index=None)
        print(df_test.head(10))


def make_csv_from_course():
    print('** make csv from course FRANCE GALOP')
    series_id, series_nom, series_sexe, series_naissance, series_race, series_pays, series_info, series_infoyear = ([] for _ in range(8))
    csv_course = glob.glob(utils.course_folder + "/*.csv")
    for filename in csv_course:
        year = filename.split(utils.course_folder)[1][:4]
        df_course = pd.read_csv(filename, index_col=None, header=0)
        for row_course in df_course.itertuples():
            cheval_toinstert = {
                'id': None,
                'nom': None,
                'sexe': None,
                'naissance': 0,
                'race': None,
                'pays': None,
                'info': None,
            }
            col_info = row_course.Cheval
            cheval_id = row_course.ChevalId
            cheval_toinstert.__setitem__('info', col_info)
            cheval_toinstert.__setitem__('id', cheval_id)
            cheval_toinstert.__setitem__('infoyear', year)
            cheval_nom = info_bystring(col_info, year).get('nom')
            if cheval_nom is not None:
                cheval_toinstert.__setitem__('nom', cheval_nom.upper())
                df_production_chevaux = pd.read_csv(utils.cheval_production_csv)
                search = df_production_chevaux.loc[(df_production_chevaux['id_francegalop'] == cheval_id)]
                if not search.empty:
                    search_nom = list(search.nom)[0].strip()
                    search_sexe = list(search.sexe)[0].strip()
                    search_naissance = list(search.naissance)[0]
                    search_race = list(search.race)[0].strip()
                    search_pays = list(search.pays)[0].strip()
                    if search_nom.lower() == cheval_nom.lower():
                        cheval_toinstert.__setitem__('sexe', search_sexe)
                        cheval_toinstert.__setitem__('naissance', search_naissance)
                        cheval_toinstert.__setitem__('race', search_race)
                        cheval_toinstert.__setitem__('pays', search_pays)
            if cheval_toinstert.get('id') not in series_id:
                series_id.append(cheval_toinstert.get('id'))
                series_nom.append(cheval_toinstert.get('nom'))
                series_sexe.append(cheval_toinstert.get('sexe'))
                series_naissance.append(cheval_toinstert.get('naissance'))
                series_race.append(cheval_toinstert.get('race'))
                series_pays.append(cheval_toinstert.get('pays'))
                series_info.append(cheval_toinstert.get('info'))
                series_infoyear.append(cheval_toinstert.get('infoyear'))

    data = {'id': series_id, 'nom': series_nom, 'sexe': series_sexe, 'naissance': series_naissance,
            'race': series_race, 'pays': series_pays, 'info': series_info, 'infoyear': series_infoyear}
    df_cheval = pd.DataFrame.from_dict(data)
    df_cheval.info()
    df_cheval.to_csv(utils.cheval_folder + "make_csv_from_course.csv", index=None)