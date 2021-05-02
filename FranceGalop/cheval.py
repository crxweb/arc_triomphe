from pprint import pprint

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
    """
    France Galop : service liste chevaux (html>li>a) en fonction du nom de cheval
    :param name:
    :return:
    """
    url = "https://www.france-galop.com/fr/horses-and-people/search-ajax?mot=" + name + "&type=chevaux"
    payload = {}
    headers = {
        'Cookie': utils.cookie
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return response.text


def performance(cheval_id):
    url = "https://www.france-galop.com/fr/frglp-global/ajax?module=cheval_performances&id_cheval="+cheval_id +\
          "&specialty=4&year=%20&jockey=%20&proprietaire=%20&entraineur=%20&nbResult=1000"
    payload = {}
    headers = {
        'Cookie': utils.cookie
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return response.text


def scrap_searchbyname(search_name, search_id, filename=None):
    """
    Web Scrapping du retour HTML de la fonction search_by_name
    :param search_name:
    :param search_id:
    :param filename:
    :return:

    exemple:
    info = cheval.scrap_searchbyname(
    filename='brouillons/search_cheval.txt',
    search_name='LANDO SPORT',
    search_id='RVF4bENvemM5eWZuLyswdXZzaXBJdz09')
    """
    if filename is not None:
        page_content = BeautifulSoup(open(filename, 'r'), "html.parser")
    else:
        page_content = BeautifulSoup(search_by_name(search_name), "html.parser")

    res = None
    for items in page_content.find_all('li'):
        data = [item for item in items.find_all(['a'])]
        data_href = data[0]['href']
        data_txt = data[0].get_text(strip=True)
        data_id = data_href.replace('/fr/cheval/', '')
        if data_id == search_id:
            info = {
                'pays': None,
                'sexe': None,
                'naissance': 0,
                'race': None
            }
            data_info = data_txt.replace(search_name, '').split(' ')
            data_info = list(filter(None, data_info))
            info['pays'], info['race'], info['sexe'], info['naissance'] = data_info[0], data_info[1], data_info[2], int(
                data_info[3])
            res = info

    return res


def fiche_detail(id):
    """
    France Galop : retour HTML fiche détail d'un cheval
    :param id:
    :return:
    """
    url = 'https://www.france-galop.com/fr/cheval/' + id
    headers = utils.get_header()
    r = requests.get(url, headers=headers)
    return r.content


def info_bystring(info_str, year):
    """
    Extraire informations d'un cheval en fonction de la chaine France Galop (ex: "new bay gb m.ps. 3 a." )
    >> nom: new bay, pays: gb, sexe:m, race: ps, age: 3 à la date year
    A cet instant, n'extrait que le nom du cheval
    :param info_str:
    :param year:
    :return:
    """
    info = {
        "nom": None,
        "age": None,
        "race": None,
        "pays": None,
        "naissance": 0
    }

    block_words = utils.country + utils.sexe_race
    block_words = block_words + list(map(lambda x: x.lower(), block_words))
    country_list = utils.country
    country_list = country_list + list(map(lambda x: x.lower(), country_list))
    racesexe_list = utils.sexe_race
    racesexe_list = racesexe_list + list(map(lambda x: x.lower(), racesexe_list))

    if year == 2000:
        pass
    # Extraction nom cheval
    else:
        make_name = []
        for item in info_str.split(' '):
            if item not in block_words:
                if item.isdigit():
                    break
                make_name.append(item)
        cheval_nom = " ".join(make_name).strip()
        if len(cheval_nom):
            info['nom'] = cheval_nom
        # print('extraction nom',cheval_nom)
        info_str = info_str.replace(cheval_nom, '').strip()
        # print('str without nom', info_str)

    return info


def make_csv_from_course():
    """
    Utilisé pour créer csv chevaux en fonction des courses et sur la base du fichier datas/production/chevaux
    pour retrouver informations déjà saisies (suite fin du service France Galop json search by name)
    :return:
    """
    print('** make csv from course FRANCE GALOP')
    s_id, s_nom, s_sexe, s_naissance, s_race, s_pays, s_info, s_infoyear = ([] for _ in range(8))
    csv_course = glob.glob(utils.course_folder + "arc_triomphe/" + "/*.csv")
    for filename in csv_course:
        year = filename.split(utils.course_folder + "arc_triomphe/")[1][:4]
        df_course = pd.read_csv(filename, index_col=None, header=0)
        for row_course in df_course.itertuples():
            new_cheval = {
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
            new_cheval['info'], new_cheval['id'], new_cheval['infoyear'] = col_info, cheval_id, year
            cheval_nom = info_bystring(col_info, year).get('nom')
            if cheval_nom is not None:
                new_cheval['nom'] = cheval_nom.upper()
                df_production_chevaux = pd.read_csv(utils.cheval_production_csv)
                search = df_production_chevaux.loc[(df_production_chevaux['id_francegalop'] == cheval_id)]
                if not search.empty:
                    search_nom = list(search.nom)[0].strip()
                    search_sexe = list(search.sexe)[0].strip()
                    search_naissance = list(search.naissance)[0]
                    search_race = list(search.race)[0].strip()
                    search_pays = list(search.pays)[0].strip()
                    if search_nom.lower() == cheval_nom.lower():
                        new_cheval['sexe'] = search_sexe
                        new_cheval['naissance'] = search_naissance
                        new_cheval['race'] = search_race
                        new_cheval['pays'] = search_pays
            if new_cheval.get('id') not in s_id:
                s_id.append(new_cheval.get('id'))
                s_nom.append(new_cheval.get('nom'))
                s_sexe.append(new_cheval.get('sexe'))
                s_naissance.append(new_cheval.get('naissance'))
                s_race.append(new_cheval.get('race'))
                s_pays.append(new_cheval.get('pays'))
                s_info.append(new_cheval.get('info'))
                s_infoyear.append(new_cheval.get('infoyear'))

    data = {'id': s_id, 'nom': s_nom, 'sexe': s_sexe, 'naissance': s_naissance,
            'race': s_race, 'pays': s_pays, 'info': s_info, 'infoyear': s_infoyear}
    df_cheval = pd.DataFrame.from_dict(data)
    df_cheval.to_csv(utils.cheval_folder + utils.cheval_from_course_csv, index=None)


def retrieve_undefined_csv():
    """
    Utilise pour créer nouveau csv en complétant les features manquantes
    Retrouve les informations d'un cheval en fonction du nom et de son id via service France Galop search_by_name
    :return:
    """
    print('Attention france galop request -- comment return ')
    return
    df_from_course = pd.read_csv(utils.cheval_folder + utils.cheval_from_course_csv, index_col=None, header=0)
    df_from_course.to_csv(utils.cheval_folder + utils.cheval_retrieve_undefined)

    df_cheval = pd.read_csv(utils.cheval_folder + utils.cheval_retrieve_undefined, index_col=None, header=0)
    #df_undefined = df_cheval[(df_cheval['race'].isna()) & (df_cheval['infoyear'] != 2000)]
    df_undefined = df_cheval[df_cheval['race'].isna()]
    for row in df_undefined.itertuples():
        print(row.id, row.nom)
        info = scrap_searchbyname(
            #filename='brouillons/search_cheval.txt',
            search_name=row.nom,
            search_id=row.id)
        if info is not None:
            print(info)
            df_cheval.loc[df_cheval['id'] == row.id, 'naissance'] = info['naissance']
            df_cheval.loc[df_cheval['id'] == row.id, 'race'] = info['race']
            df_cheval.loc[df_cheval['id'] == row.id, 'pays'] = info['pays']
            df_cheval.loc[df_cheval['id'] == row.id, 'sexe'] = info['sexe']
    df_cheval.to_csv(utils.cheval_folder + utils.cheval_retrieve_undefined, index=None)


def scrap_carriere(cheval_id, filename=None):
    """
    :param cheval_id:
    :param filename:
    :return:
    """
    s_id, s_chevalid, s_date, s_hippodrome, s_place, s_distance, s_spe, s_cat,\
        s_cat_bt, s_poids, s_prop, s_entra, s_jock, s_alloc, s_primep, s_primee,\
        s_valeur = ([] for _ in range(17))
    if filename is not None:
        page_content = BeautifulSoup(open(filename, 'r'), "html.parser")
    else:
        page_content = BeautifulSoup(performance(cheval_id), "html.parser")

    res = None
    for items in page_content.find_all('tr'):
        data = [item for item in items.find_all(['td'])]
        row_perf = {
            'id': None,
            'cheval_id': None,
            'date': None,
            'hippodrome': None,
            'place': None,
            'distance': None,
            'specialite': None,
            'categorie': None,
            'categorie_blacktype': None,
            'poids': None,
            'proprietaire': None,
            'entrainneur': None,
            'jockey': None,
            'allocation_totale': None,
            'prime_proprietaire': None,
            'prime_eleveur': None,
            'valeur': None,
        }

        row_perf['id'] = None
        link_course = data[0].find('a')
        if link_course.has_attr('href'):
            if len(link_course['href']):
                row_perf['id'] = link_course['href'].split('/')[-1]
        row_perf['cheval_id'] =  cheval_id
        row_perf['date'] = data[0].get_text(strip=True)
        row_perf['hippodrome'] = data[1].get_text(strip=True)
        row_perf['place'] = data[2].get_text(strip=True)
        row_perf['distance'] = data[3].get_text(strip=True)
        row_perf['specialite'] = data[4].get_text(strip=True)
        row_perf['categorie'] = data[5].get_text(strip=True) if len(data[5].get_text(strip=True)) else None
        row_perf['categorie_blacktype'] = data[6].get_text(strip=True) if len(data[6].get_text(strip=True)) else None
        row_perf['poids'] = data[7].get_text(strip=True)
        row_perf['proprietaire'] = data[8].get_text(strip=True) if len(data[8].get_text(strip=True)) else None
        row_perf['entrainneur'] = data[9].get_text(strip=True) if len(data[9].get_text(strip=True)) else None
        row_perf['jockey'] = data[10].get_text(strip=True) if len(data[10].get_text(strip=True)) else None
        row_perf['allocation_totale'] = data[11].get_text(strip=True)
        row_perf['prime_proprietaire'] = data[12].get_text(strip=True)
        row_perf['prime_eleveur'] = data[13].get_text(strip=True)
        row_perf['valeur'] = data[14].get_text(strip=True) if len(data[14].get_text(strip=True)) else None

        s_id.append(row_perf.get('id'))
        s_chevalid.append(row_perf.get('cheval_id'))
        s_date.append(row_perf.get('date'))
        s_hippodrome.append(row_perf.get('hippodrome'))
        s_place.append(row_perf.get('place'))
        s_distance.append(row_perf.get('distance'))
        s_spe.append(row_perf.get('specialite'))
        s_cat.append(row_perf.get('categorie'))
        s_cat_bt.append(row_perf.get('categorie_blacktype'))
        s_poids.append(row_perf.get('poids'))
        s_prop.append(row_perf.get('proprietaire'))
        s_entra.append(row_perf.get('entrainneur'))
        s_jock.append(row_perf.get('jockey'))
        s_alloc.append(row_perf.get('allocation_totale'))
        s_primep.append(row_perf.get('prime_proprietaire'))
        s_primee.append(row_perf.get('prime_eleveur'))
        s_valeur.append(row_perf.get('valeur'))

        pprint(row_perf)
        print('-----------------------------')

    data = {'id': s_id, 'cheval_id': s_chevalid, 'date': s_date, 'hippodrome': s_hippodrome, 'place': s_place,
            'distance': s_distance, 'specialite': s_spe, 'categorie': s_cat, 'categorie_backtype': s_cat_bt,
            'poids': s_poids, 'proprietaire': s_prop, 'entrainneur': s_entra, 'jockey': s_jock,
            'allocation_totale': s_alloc, 'prime_proprietaire': s_primep, 'prime_eleveur': s_primee, 'valeur': s_valeur}
    df_perf = pd.DataFrame.from_dict(data)
    return df_perf
    #df_perf.to_csv(utils.perf_folder + utils.performance_from_fg_csv, index=None, mode="a")


def make_perf_csv():
    """
    Utilisé pour création fichier csv performance de tous les chevaux
    Exemple: cheval.scrap_carriere(cheval_id="dFhkeERHK0JNRWpQUnQzdTE3dmp4dz09", filename="brouillons/performance_cheval.txt")
    :return:
    """
    perf_list = []
    df_cheval = pd.read_csv(utils.cheval_folder + utils.cheval_retrieve_undefined, index_col=None, header=0)
    cpt_cheval = 1

    # on récupère pour les 299 1ers chevaux : cookie semble ne plus être valable
    """
    for row in df_cheval.itertuples():
        if cpt_cheval < 300:
            cheval_id = row.id
            print(cpt_cheval, cheval_id)
            #cheval_perf = scrap_carriere(cheval_id=cheval_id, filename="brouillons/performance_cheval.txt")
            cheval_perf = scrap_carriere(cheval_id=cheval_id)
            perf_list.append(cheval_perf)
            cpt_cheval += 1

    if len(perf_list):
        perf_list = pd.concat(perf_list, ignore_index=True)
        perf_list.to_csv(utils.perf_folder + "make_csv_francegalop_part1.csv", index=None)    
    """
    # on récupère les chevaux à partir du 300ème : cookie semble ne plus être valable
    """
    for row in df_cheval.itertuples():
        cheval_id = row.id
        if cpt_cheval > 300:
            print(cpt_cheval, cheval_id)
            #cheval_perf = scrap_carriere(cheval_id=cheval_id, filename="brouillons/performance_cheval.txt")
            cheval_perf = scrap_carriere(cheval_id=cheval_id)
            perf_list.append(cheval_perf)
        cpt_cheval += 1

    if len(perf_list):
        perf_list = pd.concat(perf_list, ignore_index=True)
        perf_list.to_csv(utils.perf_folder + "make_csv_francegalop_part2.csv", index=None)
    """
    # Merge des 2 fichiers
    df_part1 = pd.read_csv(utils.perf_folder + "make_csv_francegalop_part1.csv", index_col=None, header=0)
    df_part2 = pd.read_csv(utils.perf_folder + "make_csv_francegalop_part2.csv", index_col=None, header=0)
    frames = [df_part1, df_part2]
    df_performance = pd.concat(frames)
    df_performance.to_csv(utils.perf_folder + "performance.csv", index=None)