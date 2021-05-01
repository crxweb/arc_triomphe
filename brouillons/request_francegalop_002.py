import json
import pandas as pnd
from utils import (
    searchChevalByName,
    getChevauxDepart,
    getChevalPerformance,
)
incap_session_name = 'incap_ses_1184_1885728'
incap_session_value = 'BjlnGZTAaHsA7yK1BGpuEHDAe2AAAAAAqVLRKqBhnQyYdMqsijUgbw==';

# Génère CSV liste chevaux / identifiant FranceGalop
def makeCsvIdentificationChevaux():

    # Liste des chevaux figurant au départ de 2008 à 2020 (source ITURF)
    chevaux_depart = getChevauxDepart()
    print(chevaux_depart)

    """"
    value_test = [{'NumSire': 'NnhGZ1B4bXkxSGtiYVFyMG9pN0cyQT09', 'NomCheval': 'YOUMZAIN                 ', 'Suffixe': 'IRE', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2003', 'link': '/fr/cheval/NnhGZ1B4bXkxSGtiYVFyMG9pN0cyQT09'}, {'NumSire': 'L1Z1bVhvZ3VMNlQ5eDdOYVJVRXU2dz09', 'NomCheval': 'ZAMBEZI SUN              ', 'Suffixe': 'GB ', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2004', 'link': '/fr/cheval/L1Z1bVhvZ3VMNlQ5eDdOYVJVRXU2dz09'}, {'NumSire': 'TUlnUHpYTm15RUo2Q2NVSjFqU0pDUT09', 'NomCheval': 'ASK                      ', 'Suffixe': 'GB ', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2003', 'link': '/fr/cheval/TUlnUHpYTm15RUo2Q2NVSjFqU0pDUT09'}, {'NumSire': 'R2VpNXlyd0cyYzBzbWVhY0dLUk8zUT09', 'NomCheval': 'SCHIAPARELLI             ', 'Suffixe': 'FR ', 'Race': 'AR   ', 'Sexe': 'F', 'AnneeNaissance': '2016', 'link': '/fr/cheval/R2VpNXlyd0cyYzBzbWVhY0dLUk8zUT09'}, {'NumSire': 'czMzdVMvOTdNaTU4V1cvaHFUeU5kZz09', 'NomCheval': 'MEISHO SAMSON            ', 'Suffixe': 'JPN', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2003', 'link': '/fr/cheval/czMzdVMvOTdNaTU4V1cvaHFUeU5kZz09'}, {'NumSire': 'TlVwdUJtc1N6SEFGZk1aTThYYVRGdz09', 'NomCheval': 'SOLDIER OF FORTUNE       ', 'Suffixe': 'IRE', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2004', 'link': '/fr/cheval/TlVwdUJtc1N6SEFGZk1aTThYYVRGdz09'}, {'NumSire': 'NUd5ZTFPNUQwNmp4OGlsY0hwOVliQT09', 'NomCheval': 'DUKE OF MARMALADE        ', 'Suffixe': 'IRE', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2004', 'link': '/fr/cheval/NUd5ZTFPNUQwNmp4OGlsY0hwOVliQT09'}, {'NumSire': 'OHRGVnJJcVBuaExzMGxtQld4ckRJQT09', 'NomCheval': 'PAPAL BULL               ', 'Suffixe': 'GB ', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2003', 'link': '/fr/cheval/OHRGVnJJcVBuaExzMGxtQld4ckRJQT09'}, {'NumSire': 'MjlMSlBkbnpHN0NCNXZ3aklVbG5jQT09', 'NomCheval': "IT'S GINO                ", 'Suffixe': 'GER', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2003', 'link': '/fr/cheval/MjlMSlBkbnpHN0NCNXZ3aklVbG5jQT09'}, {'NumSire': 'VERWUENCaGRhQUNZY1drMjdFNEJtZz09', 'NomCheval': 'RED ROCK CANYON          ', 'Suffixe': 'IRE', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2004', 'link': '/fr/cheval/VERWUENCaGRhQUNZY1drMjdFNEJtZz09'}, {'NumSire': 'OWEvTkFId2VXV0hCOG9oaERMTXE1Zz09', 'NomCheval': 'GETAWAY                  ', 'Suffixe': 'GER', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2003', 'link': '/fr/cheval/OWEvTkFId2VXV0hCOG9oaERMTXE1Zz09'}, {'NumSire': 'RkdjY3JKQldKa3lmQjkxaTkxNGYxUT09', 'NomCheval': "VISION D'ETAT            ", 'Suffixe': 'FR ', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2005', 'link': '/fr/cheval/RkdjY3JKQldKa3lmQjkxaTkxNGYxUT09'}, {'NumSire': 'Zk1YYWM4TmhwNHVqUkdzZjNsNEpEUT09', 'NomCheval': 'KAMSIN                   ', 'Suffixe': 'ITY', 'Race': 'PS   ', 'Sexe': 'H', 'AnneeNaissance': '1983', 'link': '/fr/cheval/Zk1YYWM4TmhwNHVqUkdzZjNsNEpEUT09'}, {'NumSire': 'bXN4Y3dmQ1FiOFpPUEU5TU1ZV2xRZz09', 'NomCheval': 'BLUE BRESIL              ', 'Suffixe': 'FR ', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2005', 'link': '/fr/cheval/bXN4Y3dmQ1FiOFpPUEU5TU1ZV2xRZz09'}, {'NumSire': 'aUtYaVhKMkJzQzFEblB5Q0NsU09hZz09', 'NomCheval': 'CIMA DE TRIOMPHE         ', 'Suffixe': 'IRE', 'Race': 'PS   ', 'Sexe': 'M', 'AnneeNaissance': '2005', 'link': '/fr/cheval/aUtYaVhKMkJzQzFEblB5Q0NsU09hZz09'}, {'NumSire': 'YWNmUDA5eEQ3dFgyNElBa3B0MlRJQT09', 'NomCheval': 'ZARKAVA                  ', 'Suffixe': 'IRE', 'Race': 'PS   ', 'Sexe': 'F', 'AnneeNaissance': '2005', 'link': '/fr/cheval/YWNmUDA5eEQ3dFgyNElBa3B0MlRJQT09'}]
    with open('list_chevaux_francegalop.json', 'w') as fp:
        json.dump(value_test, fp)
    df = pnd.read_json('list_chevaux_francegalop.json')
    df.to_csv('list_chevaux_francegalop.csv')
    
    
    search_fg = searchChevalByName('YOUMZAIN',incap_session_name,incap_session_value)
    if search_fg:
        # print(search_fg)
        print(type(search_fg))
    """
    horses_search = []
    if False:
        for horse in chevaux_depart:
            search_fg = searchChevalByName(horse,incap_session_name,incap_session_value)
            if search_fg:
                horses_search.append(search_fg)
        with open('list_chevaux_francegalop.json', 'w') as fp:
            json.dump(horses_search, fp)
        df = pnd.read_json('list_chevaux_francegalop.json')
        df.to_csv('list_chevaux_francegalop.csv')
    if True:
        for horse in chevaux_depart:
            search_fg = searchChevalByName(horse,incap_session_name,incap_session_value)
            if search_fg:
                data = pnd.DataFrame.from_records(search_fg)
                horses_search.append(data)
        horses_search = pnd.concat(horses_search, ignore_index=True)
        horses_search.to_csv('performance_chevaux.csv')



def makeCsvPerformanceCheval(cheval_id):
    fg_perf = getChevalPerformance(cheval_id,incap_session_name,incap_session_value)
    print(type(fg_perf))
    df = pnd.DataFrame.from_records(fg_perf)
    #df['fg_id'] = cheval_id
    df.insert(0, "fg_id", cheval_id, True)
    df.info()
    df.to_csv('performance_chevaux.csv')

"""
appended_data = []
for infile in glob.glob("*.xlsx"):
    data = pandas.read_excel(infile)
    # store DataFrame in list
    appended_data.append(data)
# see pd.concat documentation for more info
appended_data = pd.concat(appended_data)
# write DataFrame to an excel sheet 
appended_data.to_excel('appended.xlsx')
"""
appended_data = []
for i in range(3):
    cheval_id = 'id_cheval_x'+str(i)
    fg_perf = getChevalPerformance(cheval_id,incap_session_name,incap_session_value,fake=True)
    data = pnd.DataFrame.from_records(fg_perf)
    data.insert(0, "fg_id", cheval_id, True)
    appended_data.append(data)

appended_data = pnd.concat(appended_data,ignore_index=True)
appended_data.to_csv('performance_chevaux.csv')
#makeCsvPerformanceCheval('id_cheval_x'+str(i))