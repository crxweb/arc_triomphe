import requests
import sys
import json
import pandas as pnd
import csv
from bs4 import BeautifulSoup

pnd.set_option('display.max_columns',None)

def getHeader(incap_session_name, incap_session_value):
    """
    Retourne en-tête requête avec le cookie de session obligatoire
    :param incap_session_name:
    :param incap_session_value:
    :return:
    """
    cookie = '; '.join([incap_session_name + '=' + incap_session_value])
    return {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Cookie': cookie,
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

def getChevalDetail(id,incap_session_name,incap_session_value, fake = False):
    url = 'https://www.france-galop.com/fr/cheval/' + id
    headers = getHeader(incap_session_name, incap_session_value)
    r = requests.get(url, headers=headers)
    return r.content


def searchChevalByName(name,incap_session_name,incap_session_value, fake = False):
    """
    Rechercher un cheval par son nom (permet de récupérer identifiant FranceGalop, age, sexe..)
    :param name:
    :param incap_session_name:
    :param incap_session_value:
    :param fake:
    :return:
    """
    if fake:
        print('Fake')
        ex_response = [{'NumSire': 'NnhGZ1B4bXkxSGtiYVFyMG9pN0cyQT09', 'NomCheval': 'YOUMZAIN                 ', 'Suffixe': 'IRE', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2003', 'link': '/fr/cheval/NnhGZ1B4bXkxSGtiYVFyMG9pN0cyQT09'}, {'NumSire': 'L1Z1bVhvZ3VMNlQ5eDdOYVJVRXU2dz09', 'NomCheval': 'ZAMBEZI SUN              ', 'Suffixe': 'GB ', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2004', 'link': '/fr/cheval/L1Z1bVhvZ3VMNlQ5eDdOYVJVRXU2dz09'}, {'NumSire': 'TUlnUHpYTm15RUo2Q2NVSjFqU0pDUT09', 'NomCheval': 'ASK                      ', 'Suffixe': 'GB ', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2003', 'link': '/fr/cheval/TUlnUHpYTm15RUo2Q2NVSjFqU0pDUT09'}, {'NumSire': 'R2VpNXlyd0cyYzBzbWVhY0dLUk8zUT09', 'NomCheval': 'SCHIAPARELLI             ', 'Suffixe': 'FR ', 'Race': 'AR   ', 'Sexe': 'F', 'AnneeNaissance': '2016', 'link': '/fr/cheval/R2VpNXlyd0cyYzBzbWVhY0dLUk8zUT09'}, {'NumSire': 'czMzdVMvOTdNaTU4V1cvaHFUeU5kZz09', 'NomCheval': 'MEISHO SAMSON            ', 'Suffixe': 'JPN', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2003', 'link': '/fr/cheval/czMzdVMvOTdNaTU4V1cvaHFUeU5kZz09'}, {'NumSire': 'TlVwdUJtc1N6SEFGZk1aTThYYVRGdz09', 'NomCheval': 'SOLDIER OF FORTUNE       ', 'Suffixe': 'IRE', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2004', 'link': '/fr/cheval/TlVwdUJtc1N6SEFGZk1aTThYYVRGdz09'}, {'NumSire': 'NUd5ZTFPNUQwNmp4OGlsY0hwOVliQT09', 'NomCheval': 'DUKE OF MARMALADE        ', 'Suffixe': 'IRE', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2004', 'link': '/fr/cheval/NUd5ZTFPNUQwNmp4OGlsY0hwOVliQT09'}, {'NumSire': 'OHRGVnJJcVBuaExzMGxtQld4ckRJQT09', 'NomCheval': 'PAPAL BULL               ', 'Suffixe': 'GB ', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2003', 'link': '/fr/cheval/OHRGVnJJcVBuaExzMGxtQld4ckRJQT09'}, {'NumSire': 'MjlMSlBkbnpHN0NCNXZ3aklVbG5jQT09', 'NomCheval': "IT'S GINO                ", 'Suffixe': 'GER', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2003', 'link': '/fr/cheval/MjlMSlBkbnpHN0NCNXZ3aklVbG5jQT09'}, {'NumSire': 'VERWUENCaGRhQUNZY1drMjdFNEJtZz09', 'NomCheval': 'RED ROCK CANYON          ', 'Suffixe': 'IRE', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2004', 'link': '/fr/cheval/VERWUENCaGRhQUNZY1drMjdFNEJtZz09'}, {'NumSire': 'OWEvTkFId2VXV0hCOG9oaERMTXE1Zz09', 'NomCheval': 'GETAWAY                  ', 'Suffixe': 'GER', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2003', 'link': '/fr/cheval/OWEvTkFId2VXV0hCOG9oaERMTXE1Zz09'}, {'NumSire': 'RkdjY3JKQldKa3lmQjkxaTkxNGYxUT09', 'NomCheval': "VISION D'ETAT            ", 'Suffixe': 'FR ', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2005', 'link': '/fr/cheval/RkdjY3JKQldKa3lmQjkxaTkxNGYxUT09'}, {'NumSire': 'Zk1YYWM4TmhwNHVqUkdzZjNsNEpEUT09', 'NomCheval': 'KAMSIN                   ', 'Suffixe': 'ITY', 'Race': 'PS   ', 'Sexe': 'H', 'AnneeNaissance': '1983', 'link': '/fr/cheval/Zk1YYWM4TmhwNHVqUkdzZjNsNEpEUT09'}, {'NumSire': 'bXN4Y3dmQ1FiOFpPUEU5TU1ZV2xRZz09', 'NomCheval': 'BLUE BRESIL              ', 'Suffixe': 'FR ', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2005', 'link': '/fr/cheval/bXN4Y3dmQ1FiOFpPUEU5TU1ZV2xRZz09'}, {'NumSire': 'aUtYaVhKMkJzQzFEblB5Q0NsU09hZz09', 'NomCheval': 'CIMA DE TRIOMPHE         ', 'Suffixe': 'IRE', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2005', 'link': '/fr/cheval/aUtYaVhKMkJzQzFEblB5Q0NsU09hZz09'}, {'NumSire': 'YWNmUDA5eEQ3dFgyNElBa3B0MlRJQT09', 'NomCheval': 'ZARKAVA                  ', 'Suffixe': 'IRE', 'Race': 'PS   ', 'Sexe': 'F', 'AnneeNaissance': '2005', 'link': '/fr/cheval/YWNmUDA5eEQ3dFgyNElBa3B0MlRJQT09'}]
        ex_response = [{"NumSire":"anptcjdXV2c4dE9DbE1QSGtmQ3Z2Zz09","NomCheval":"MIGWAR ","Suffixe":"FR ","Race":"AR ","Sexe":"M","AnneeNaissance":"2014","link":"\/fr\/cheval\/anptcjdXV2c4dE9DbE1QSGtmQ3Z2Zz09"},{"NumSire":"Rk1Hd2ZZNXgza0VvaHg5S01kZjBkUT09","NomCheval":"MIGWAR ","Suffixe":"IRE","Race":"PS ","Sexe":"M","AnneeNaissance":"2012","link":"\/fr\/cheval\/Rk1Hd2ZZNXgza0VvaHg5S01kZjBkUT09"}]
        return ex_response
    else:
        url = 'https://www.france-galop.com/fr/frglp_global/ajax?module=search&mot='+name+'&type=IsRechercheCheval'
        headers = getHeader(incap_session_name, incap_session_value)
        r = requests.get(url, headers=headers)
        try:
            res_horses = r.json().get('Chevaux', [])
            if len(res_horses):
                res = next((sub for sub in res_horses if sub['NomCheval'].rstrip() == name), None)
                if res:
                    print(res)
                    return res
        except ValueError as e:
            print('!!! JSON RESPONSE NOT AVAILABLE !!!')
            sys.exit()

def getChevalPerformance(id,incap_session_name,incap_session_value, fake = False):
    """
    Retourne liste des performances d'un cheval en fonction de son identifiant FranceGalop
    :param id:
    :param incap_session_name:
    :param incap_session_value:
    :param fake:
    :return:
    """
    if fake:
        ex_response = [{"Annee":"2017","Specialite":0,"DateReunion":"20171001","NomProprietaire":"MME J. MAGNIER\/M.TABOR\/D.SMITH","NbPlace":9,"Gains":"0000000000","Prix":"QATAR PRIX DE L'ARC DE TRIOMPHE                                       ","PrimeProp":"00000000","PrimeEleveur":"00000000","PoidsPorte":"55","NomJockey":"MOORE                         ","Hippodrome":"CHANTILLY","NumProgramme":"aVluMkQ4cXNQS3JEanlXR04vR2Rkdz09","DistanceParcouru":"2400","Discipline":"P","Categorie":"GR.I      ","CategBlackType":"K","NomEntraineur":"O'BRIEN                       ","Valeur":"","NomVideo":"20171001_25564837_00000HR","TypeVideo":0,"meetingDate":{"link":"\/fr\/course\/detail\/2017\/P\/aVluMkQ4cXNQS3JEanlXR04vR2Rkdz09"},"DisciplineLitteral":"Plat"},{"Annee":"2017","Specialite":0,"DateReunion":"20170909","NomProprietaire":"","NbPlace":2,"Gains":"0000066500","Prix":"","PrimeProp":"00000000","PrimeEleveur":"00000000","PoidsPorte":"57","NomJockey":"","Hippodrome":"LEOPARDSTOWN","NumProgramme":"V2ZZd3N3M2JmV1ExeGk0NVkvSWZIdz09","DistanceParcouru":"1600","Discipline":"P","Categorie":"GR.I      ","CategBlackType":"K","NomEntraineur":"","Valeur":"540","NomVideo":"","TypeVideo":1,"meetingDate":{"link":"#"},"DisciplineLitteral":"Plat"},{"Annee":"2017","Specialite":0,"DateReunion":"20170803","NomProprietaire":"","NbPlace":1,"Gains":"0000397407","Prix":"","PrimeProp":"00000000","PrimeEleveur":"00000000","PoidsPorte":"56,5","NomJockey":"","Hippodrome":"GOODWOOD","NumProgramme":"V2ZZd3N3M2JmV1ExeGk0NVkvSWZIdz09","DistanceParcouru":"2000","Discipline":"P","Categorie":"GR.I      ","CategBlackType":"K","NomEntraineur":"","Valeur":"","NomVideo":"","TypeVideo":1,"meetingDate":{"link":"#"},"DisciplineLitteral":"Plat"},{"Annee":"2017","Specialite":0,"DateReunion":"20170623","NomProprietaire":"","NbPlace":1,"Gains":"0000284808","Prix":"","PrimeProp":"00000000","PrimeEleveur":"00000000","PoidsPorte":"57","NomJockey":"","Hippodrome":"ASCOT","NumProgramme":"V2ZZd3N3M2JmV1ExeGk0NVkvSWZIdz09","DistanceParcouru":"1600","Discipline":"P","Categorie":"GR.I      ","CategBlackType":"K","NomEntraineur":"","Valeur":"","NomVideo":"","TypeVideo":1,"meetingDate":{"link":"#"},"DisciplineLitteral":"Plat"},{"Annee":"2017","Specialite":0,"DateReunion":"20170528","NomProprietaire":"","NbPlace":1,"Gains":"0000171000","Prix":"","PrimeProp":"00000000","PrimeEleveur":"00000000","PoidsPorte":"0","NomJockey":"","Hippodrome":"CURRAGH","NumProgramme":"V2ZZd3N3M2JmV1ExeGk0NVkvSWZIdz09","DistanceParcouru":"1600","Discipline":"P","Categorie":"GR.I      ","CategBlackType":"K","NomEntraineur":"","Valeur":"","NomVideo":"","TypeVideo":1,"meetingDate":{"link":"#"},"DisciplineLitteral":"Plat"},{"Annee":"2017","Specialite":0,"DateReunion":"20170507","NomProprietaire":"","NbPlace":1,"Gains":"0000331172","Prix":"","PrimeProp":"00000000","PrimeEleveur":"00000000","PoidsPorte":"0","NomJockey":"","Hippodrome":"NEWMARKET","NumProgramme":"V2ZZd3N3M2JmV1ExeGk0NVkvSWZIdz09","DistanceParcouru":"1600","Discipline":"P","Categorie":"GR.I      ","CategBlackType":"K","NomEntraineur":"","Valeur":"","NomVideo":"","TypeVideo":1,"meetingDate":{"link":"#"},"DisciplineLitteral":"Plat"},{"Annee":"2017","Specialite":0,"DateReunion":"20170408","NomProprietaire":"","NbPlace":2,"Gains":"0000012350","Prix":"","PrimeProp":"00000000","PrimeEleveur":"00000000","PoidsPorte":"57","NomJockey":"","Hippodrome":"LEOPARDSTOWN","NumProgramme":"V2ZZd3N3M2JmV1ExeGk0NVkvSWZIdz09","DistanceParcouru":"1400","Discipline":"P","Categorie":"GR.III    ","CategBlackType":"K","NomEntraineur":"","Valeur":"","NomVideo":"","TypeVideo":1,"meetingDate":{"link":"#"},"DisciplineLitteral":"Plat"},{"Annee":"2016","Specialite":0,"DateReunion":"20160814","NomProprietaire":"","NbPlace":1,"Gains":"0000008600","Prix":"","PrimeProp":"00000000","PrimeEleveur":"00000000","PoidsPorte":"57","NomJockey":"","Hippodrome":"DUNDALK","NumProgramme":"V2ZZd3N3M2JmV1ExeGk0NVkvSWZIdz09","DistanceParcouru":"1400","Discipline":"P","Categorie":"          ","CategBlackType":"D","NomEntraineur":"","Valeur":"","NomVideo":"","TypeVideo":1,"meetingDate":{"link":"#"},"DisciplineLitteral":"Plat"},{"Annee":"2016","Specialite":0,"DateReunion":"20160723","NomProprietaire":"","NbPlace":3,"Gains":"0000001395","Prix":"","PrimeProp":"00000000","PrimeEleveur":"00000000","PoidsPorte":"57","NomJockey":"","Hippodrome":"GOWRAN PARK","NumProgramme":"V2ZZd3N3M2JmV1ExeGk0NVkvSWZIdz09","DistanceParcouru":"1600","Discipline":"P","Categorie":"          ","CategBlackType":"D","NomEntraineur":"","Valeur":"","NomVideo":"","TypeVideo":1,"meetingDate":{"link":"#"},"DisciplineLitteral":"Plat"},{"Annee":"2016","Specialite":0,"DateReunion":"20160511","NomProprietaire":"","NbPlace":3,"Gains":"0000001395","Prix":"","PrimeProp":"00000000","PrimeEleveur":"00000000","PoidsPorte":"57","NomJockey":"","Hippodrome":"NAAS","NumProgramme":"V2ZZd3N3M2JmV1ExeGk0NVkvSWZIdz09","DistanceParcouru":"1200","Discipline":"P","Categorie":"          ","CategBlackType":"D","NomEntraineur":"","Valeur":"","NomVideo":"","TypeVideo":1,"meetingDate":{"link":"#"},"DisciplineLitteral":"Plat"}]
        return ex_response
    else:
        nb_result = 1000
        url = 'https://www.france-galop.com/fr/frglp_global/ajax?entraineur=0&id='+id+'&jockey=0&module=cheval_performances&nbResult='+str(nb_result)+'&proprietaire=0&specialty=4&year=0'
        headers = getHeader(incap_session_name, incap_session_value)
        r = requests.get(url, headers=headers)
        try:
            res_perf = r.json()
            return res_perf
        except ValueError as e:
            print('!!! JSON RESPONSE NOT AVAILABLE !!!')
            sys.exit()

def getChevalCarriere(id,incap_session_name,incap_session_value, fake = False):
    """
    Retourne carrière d'un cheval en fonction de son identifiant FranceGalop
    :param id:
    :param incap_session_name:
    :param incap_session_value:
    :param fake:
    :return:
    """
    if fake:
        ex_response = [{"Annee":"2017","Specialite":"P\/","NbrCourses":"1","NbrVictoires":"0","NbrPlaces":"0","AllocVict":"0","AllocPlc":"0","AllocTotale":"0","AllocPrimeProp":"0","PrimeEleveur":"0","VictPart":"0","PlcPart":"0","MoyenneGainAnnee":"0"},{"Annee":"2016","Specialite":"P\/","NbrCourses":"0","NbrVictoires":"0","NbrPlaces":"0","AllocVict":"0","AllocPlc":"0","AllocTotale":"0","AllocPrimeProp":"0","PrimeEleveur":"0","VictPart":"0","PlcPart":"0","MoyenneGainAnnee":"0"}]
        return ex_response
    else:
        nb_result = 1000
        url = 'https://www.france-galop.com/fr/frglp_global/ajax?id='+id+'&module=cheval_carriere&nbResult='+str(nb_result)+'&specialty=4'
        headers = getHeader(incap_session_name, incap_session_value)
        r = requests.get(url, headers=headers)
        try:
            res_carriere = r.json()
            return res_carriere
        except ValueError as e:
            print('!!! JSON RESPONSE NOT AVAILABLE !!!')
            sys.exit()

def getChevalEngagement(id,incap_session_name,incap_session_value, fake = False):
    """
    Retourne engagement d'un cheval en fonction de son identifiant FranceGalop
    :param id:
    :param incap_session_name:
    :param incap_session_value:
    :param fake:
    :return:
    """
    if fake:
        ex_response = [{"DateReunion":"20210418","Hippodrome":"PARISLONGCHAMP","CodeHippodrome":"dTBtUk50T2Z4NVpwbHI5OFRYazI3QT09","AnneeCourse":"2021","Specialite":"P","LabelCourse":"LORD SEYMOUR ","Prix":"P - 307 - LORD SEYMOUR ","PrixCourt":null,"NumProgramme":"SEVpdXJ6aHVXeWtycFM4TlNHR2Rvdz09","Categorie":null,"NumSire":null,"NomCheval":null,"DistanceParcouru":null,"PoidsPorte":null,"NomProprietaire":null,"Etat":"PARTANT ","ClotSuiv1":"","ClotSuiv2":"","DateClot":"","LibelleJockey":"RONAN THOMAS","Allocation":null,"TypeEngagement":"N","Corde":null,"Discipline":null,"NomEntraineur":null,"NomJockey":null,"ReferenceCourse":null,"price":{"link":"\/fr\/course\/detail\/2021\/P\/SEVpdXJ6aHVXeWtycFM4TlNHR2Rvdz09"},"NumProgrammeDecoded":"307","SpecialiteLabel":"Plat"},{"DateReunion":"20201004","Hippodrome":"PARISLONGCHAMP","CodeHippodrome":"dTBtUk50T2Z4NVpwbHI5OFRYazI3QT09","AnneeCourse":"2020","Specialite":"P","LabelCourse":"ARC DE TRIOMPHE","Prix":"P - 593 - ARC DE TRIOMPHE","PrixCourt":null,"NumProgramme":"c3hUZ091amI2b0tkNVNSenhqcjFBUT09","Categorie":null,"NumSire":null,"NomCheval":null,"DistanceParcouru":null,"PoidsPorte":null,"NomProprietaire":null,"Etat":"PARTANT ","ClotSuiv1":"","ClotSuiv2":"","DateClot":"","LibelleJockey":"RONAN THOMAS","Allocation":null,"TypeEngagement":"N","Corde":null,"Discipline":null,"NomEntraineur":null,"NomJockey":null,"ReferenceCourse":null,"price":{"link":"\/fr\/course\/detail\/2020\/P\/c3hUZ091amI2b0tkNVNSenhqcjFBUT09"},"NumProgrammeDecoded":"593","SpecialiteLabel":"Plat"},{"DateReunion":"20201003","Hippodrome":"PARISLONGCHAMP","CodeHippodrome":"dTBtUk50T2Z4NVpwbHI5OFRYazI3QT09","AnneeCourse":"2020","Specialite":"P","LabelCourse":"CHAUDENAY ","Prix":"P - 588 - CHAUDENAY ","PrixCourt":null,"NumProgramme":"VHIyWUkzK0lLR2tVaFlTN3MxQUN6dz09","Categorie":null,"NumSire":null,"NomCheval":null,"DistanceParcouru":null,"PoidsPorte":null,"NomProprietaire":null,"Etat":"FORFAIT 1 ","ClotSuiv1":"","ClotSuiv2":"","DateClot":"","LibelleJockey":"","Allocation":null,"TypeEngagement":"N","Corde":null,"Discipline":null,"NomEntraineur":null,"NomJockey":null,"ReferenceCourse":null,"price":{"link":"\/fr\/course\/detail\/2020\/P\/VHIyWUkzK0lLR2tVaFlTN3MxQUN6dz09"},"NumProgrammeDecoded":"588","SpecialiteLabel":"Plat"},{"DateReunion":"20200913","Hippodrome":"PARISLONGCHAMP","CodeHippodrome":"dTBtUk50T2Z4NVpwbHI5OFRYazI3QT09","AnneeCourse":"2020","Specialite":"P","LabelCourse":"GD PRIX PARIS ","Prix":"P - 522 - GD PRIX PARIS ","PrixCourt":null,"NumProgramme":"U1JpaWM3c2RuMncyRU8rWjYwSk5WQT09","Categorie":null,"NumSire":null,"NomCheval":null,"DistanceParcouru":null,"PoidsPorte":null,"NomProprietaire":null,"Etat":"PARTANT ","ClotSuiv1":"","ClotSuiv2":"","DateClot":"","LibelleJockey":"RONAN THOMAS","Allocation":null,"TypeEngagement":"N","Corde":null,"Discipline":null,"NomEntraineur":null,"NomJockey":null,"ReferenceCourse":null,"price":{"link":"\/fr\/course\/detail\/2020\/P\/U1JpaWM3c2RuMncyRU8rWjYwSk5WQT09"},"NumProgrammeDecoded":"522","SpecialiteLabel":"Plat"},{"DateReunion":"20200714","Hippodrome":"PARISLONGCHAMP","CodeHippodrome":"dTBtUk50T2Z4NVpwbHI5OFRYazI3QT09","AnneeCourse":"2020","Specialite":"P","LabelCourse":"DU LYS ","Prix":"P - 467 - DU LYS ","PrixCourt":null,"NumProgramme":"QlEya29XVWJoOHdOc3VCUFVPVHRydz09","Categorie":null,"NumSire":null,"NomCheval":null,"DistanceParcouru":null,"PoidsPorte":null,"NomProprietaire":null,"Etat":"FORFAIT 1 ","ClotSuiv1":"","ClotSuiv2":"","DateClot":"","LibelleJockey":"","Allocation":null,"TypeEngagement":"N","Corde":null,"Discipline":null,"NomEntraineur":null,"NomJockey":null,"ReferenceCourse":null,"price":{"link":"\/fr\/course\/detail\/2020\/P\/QlEya29XVWJoOHdOc3VCUFVPVHRydz09"},"NumProgrammeDecoded":"467","SpecialiteLabel":"Plat"},{"DateReunion":"20200606","Hippodrome":"LYON PARILLY","CodeHippodrome":"YkFyQTdZdFNobzlrQzExSEs5cHQxQT09","AnneeCourse":"2020","Specialite":"P","LabelCourse":"GREFFULHE ","Prix":"P - 367 - GREFFULHE ","PrixCourt":null,"NumProgramme":"RjF2RUJnL2d1YUcrQUdxVlZoZnBqZz09","Categorie":null,"NumSire":null,"NomCheval":null,"DistanceParcouru":null,"PoidsPorte":null,"NomProprietaire":null,"Etat":"PARTANT ","ClotSuiv1":"","ClotSuiv2":"","DateClot":"","LibelleJockey":"PIERRE-CHARLES BOUDOT","Allocation":null,"TypeEngagement":"N","Corde":null,"Discipline":null,"NomEntraineur":null,"NomJockey":null,"ReferenceCourse":null,"price":{"link":"\/fr\/course\/detail\/2020\/P\/RjF2RUJnL2d1YUcrQUdxVlZoZnBqZz09"},"NumProgrammeDecoded":"367","SpecialiteLabel":"Plat"},{"DateReunion":"20200604","Hippodrome":"LYON PARILLY","CodeHippodrome":"YkFyQTdZdFNobzlrQzExSEs5cHQxQT09","AnneeCourse":"2020","Specialite":"P","LabelCourse":"COUPE 3 ANS ","Prix":"P - 4837 - COUPE 3 ANS ","PrixCourt":null,"NumProgramme":"OXk5M092VHFpN0VSSHhkRXkzenNrdz09","Categorie":null,"NumSire":null,"NomCheval":null,"DistanceParcouru":null,"PoidsPorte":null,"NomProprietaire":null,"Etat":"N DEC.PART","ClotSuiv1":"","ClotSuiv2":"","DateClot":"","LibelleJockey":"","Allocation":null,"TypeEngagement":"N","Corde":null,"Discipline":null,"NomEntraineur":null,"NomJockey":null,"ReferenceCourse":null,"price":{"link":"\/fr\/course\/detail\/2020\/P\/OXk5M092VHFpN0VSSHhkRXkzenNrdz09"},"NumProgrammeDecoded":"4837","SpecialiteLabel":"Plat"},{"DateReunion":"20200604","Hippodrome":"CLAIREFONTAINE","CodeHippodrome":"dHVHWXlzYXd3YmVNdmJOTENOdFpXUT09","AnneeCourse":"2020","Specialite":"P","LabelCourse":"DES ORFEVRES ","Prix":"P - 653 - DES ORFEVRES ","PrixCourt":null,"NumProgramme":"OWVKMkNkT3JQYURKZzY0TXBYK283dz09","Categorie":null,"NumSire":null,"NomCheval":null,"DistanceParcouru":null,"PoidsPorte":null,"NomProprietaire":null,"Etat":"N DEC.PART","ClotSuiv1":"","ClotSuiv2":"","DateClot":"","LibelleJockey":"","Allocation":null,"TypeEngagement":"N","Corde":null,"Discipline":null,"NomEntraineur":null,"NomJockey":null,"ReferenceCourse":null,"price":{"link":"\/fr\/course\/detail\/2020\/P\/OWVKMkNkT3JQYURKZzY0TXBYK283dz09"},"NumProgrammeDecoded":"653","SpecialiteLabel":"Plat"},{"DateReunion":"20200515","Hippodrome":"LYON PARILLY","CodeHippodrome":"YkFyQTdZdFNobzlrQzExSEs5cHQxQT09","AnneeCourse":"2020","Specialite":"P","LabelCourse":"LOUIS SAULNIER ","Prix":"P - 4193 - LOUIS SAULNIER ","PrixCourt":null,"NumProgramme":"US8vRUlyZFNpYzJPSzZ5enRCYyttZz09","Categorie":null,"NumSire":null,"NomCheval":null,"DistanceParcouru":null,"PoidsPorte":null,"NomProprietaire":null,"Etat":"PARTANT ","ClotSuiv1":"","ClotSuiv2":"","DateClot":"","LibelleJockey":"PIERRE-CHARLES BOUDOT","Allocation":null,"TypeEngagement":"N","Corde":null,"Discipline":null,"NomEntraineur":null,"NomJockey":null,"ReferenceCourse":null,"price":{"link":"\/fr\/course\/detail\/2020\/P\/US8vRUlyZFNpYzJPSzZ5enRCYyttZz09"},"NumProgrammeDecoded":"4193","SpecialiteLabel":"Plat"}]
        return ex_response
    else:
        nb_result = 1000
        url = 'https://www.france-galop.com/fr/frglp_global/ajax?id='+id+'&module=cheval_engagements&nbResult='+str(nb_result)+'&racetrack=0'
        headers = getHeader(incap_session_name, incap_session_value)
        r = requests.get(url, headers=headers)
        try:
            res_engagement = r.json()
            return res_engagement
        except ValueError as e:
            print('!!! JSON RESPONSE NOT AVAILABLE !!!')
            sys.exit()

def getArcTriompheHistorique(incap_session_name,incap_session_value):
    """
    Retourne historique courses prix Arc de Triomphe
    :param incap_session_name:
    :param incap_session_value:
    :return:
    """
    df_perf = pnd.read_csv('datas/output/cheval_performance.csv')
    search_prix_at = df_perf[df_perf['Prix'].str.strip() == "QATAR PRIX DE L'ARC DE TRIOMPHE"]
    prix = search_prix_at['meetingDate'].unique().tolist()
    urls = []
    for p in prix:
        link = json.loads(p.replace("'", '"'))['link']
        urls.append('https://www.france-galop.com' + link)
    url_cpt = 0
    for url in urls:
        print('url', url)
        headers = getHeader(incap_session_name, incap_session_value)
        res = requests.get(url, headers=headers)
        page_content = BeautifulSoup(res.content, "html.parser")
        print(page_content)
        with open('datas/output/arc_triomphe_historique_v01.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            row_cpt = 0
            for items in page_content.find('table').find_all(['tr', 'thead']):
                data = [item.get_text(strip=True) for item in items.find_all(['th', 'td'])]
                if row_cpt == 0:
                    data.append('Année')
                    data.append('fg_id')
                else:
                    year = url.split('https://www.france-galop.com/fr/course/detail/')[1][:4]
                    data.append(year)

                tag_link = items.select_one('a')
                if tag_link is not None:
                    link = str(tag_link)
                    cheval_id = link.split('<a href="/fr/cheval/')[1].split('">')[0]
                    #data[1] = cheval_id
                    data.append(cheval_id)
                if row_cpt == 0:
                    if url_cpt == 0:
                        writer.writerow(data)
                else:
                    writer.writerow(data)
                row_cpt += 1
                url_cpt += 1