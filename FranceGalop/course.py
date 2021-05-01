from pprint import pprint

import requests
import sys
import json
import os
import pandas as pd
import csv
from bs4 import BeautifulSoup
from FranceGalop import (
    utils,
    cheval
)
import urllib.parse as urlparse

pd.set_option('display.max_columns', None)


def save_fiche_course(url, destination_folder):
    """
    Attention en 2000 France Galop n'a pas enregistré toutes les données : uniquement le 3 premiers chevaux
    2000_arc_triomphe_aEdrbGdqZ1N1SEpncmJwUXdDUnJYUT09.csv est donc à reconstituer ou à ignorer
    :param url:
    :return:
    """
    return False # Attention à sauvegarder le fichier pour année 2000
    parsed = urlparse.urlparse(url)
    path = parsed.path
    year = path[path.find('detail') + len('detail') + 1:path.find('detail') + len('detail') + 1 + 4]
    num_programme = path[path.find('P') + len('P') + 1:]
    csv_file = year + '_arc_triomphe_' + num_programme + '.csv'
    with open(destination_folder + csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        headers = utils.get_header()
        res = requests.get(url, headers=headers)
        page_content = BeautifulSoup(res.content, "html.parser")
        row_cpt = 0
        for items in page_content.find('table').find_all(['tr', 'thead']):
            data = [item.get_text(strip=True) for item in items.find_all(['th', 'td'])]
            if row_cpt == 0:
                data.append('ChevalId')
            else:
                tag_link = items.select_one('a')
                if tag_link is not None:
                    link = str(tag_link)
                    cheval_id = link.split('<a href="/fr/cheval/')[1].split('">')[0]
                    data.append(cheval_id)
            writer.writerow(data)
            row_cpt += 1
        print('File ' + destination_folder + csv_file + ' saved')


def reorder_fiche_course(directory):
    for filename in os.listdir(directory):
        fieldnames = ['Place', 'Cheval', 'ChevalId', 'N°', 'Père/Mère', 'Écart au précédent', 'Couleurs',
                      'Propriétaire',
                      'Entraîneur', 'Jockey', 'Poids', 'Gain', 'Prim. prop.', 'Prim. elev.', 'Suppl.', 'Œil.',
                      'Écurie.',
                      'Éleveurs']
        df = pd.read_csv(directory + filename)
        df_reorder = df[fieldnames]  # rearrange column here
        df_reorder.to_csv(directory + filename, index=False)
        print('File ' + directory + filename + ' reordered')


def add_columns_info_cheval(directory):
    """
    il faut extraire le bon résultat en fonction de ChevalId
    quand ne passe pas et ne voit pas pourquoi retenter avec une portion de chaine ne moins (cas nothin'leica dane aus: nom extrait correctement mais recherche accepte que "nothin'leica dane"
    donc sans le suffix "aus" qui correspond à la nationalité du cheval

    attention à session non valide
    :return:
    """
    block_words = utils.country + utils.sexe_race
    print(block_words)
    block_words_lowercase = map(lambda x: x.lower(), block_words)
    print(block_words_lowercase)
    for filename in os.listdir(directory):
        print('####  Course: ',filename)
        with open(directory + filename , newline='') as f:
            course_rows = csv.reader(f)
            next(course_rows)
            for course in course_rows:
                col_cheval = course[1]
                col_chevalId = course[2]
                cheval_data = None
                make_name = []
                for item in col_cheval.split(' '):
                    if item not in block_words and item not in map(lambda x: x.lower(), block_words):
                        if item.isdigit():
                            break
                        make_name.append(item)
                cheval_nom = " ".join(make_name)

                # --- debug
                if col_chevalId == "RkdjY3JKQldKa3lmQjkxaTkxNGYxUT09":
                    print('col_cheval',col_cheval)
                    print('nom:', cheval_nom)                

                if False:
                    if len(cheval_nom):
                        print(cheval_nom)
                        search_horses = cheval.search_by_name(cheval_nom)
                        for horse in search_horses:
                            if horse.get('NumSire') == col_chevalId:
                                cheval_data = horse
                                break
                    if cheval_data is not None:
                        # vérifier si n'existe pas déjà
                        print('OK')
                        #print("Success reception data for {cheval_nom} | {cheval_id} | ({col_cheval}) from {csv_file}".format(col_cheval=col_cheval, cheval_nom=cheval_nom, cheval_id=col_chevalId, csv_file=directory + filename))
                        #pprint(cheval_data)
                    else:
                        print('NOK')
                        print("FAILED reception data for {cheval_nom} | {cheval_id} | ({col_cheval}) from {csv_file}".format(col_cheval=col_cheval, cheval_nom=cheval_nom, cheval_id=col_chevalId, csv_file=directory + filename))
                        pprint(cheval_data)
                    print('---------------')
                #break
        #break


