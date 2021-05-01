import pandas as pnd
from bs4 import BeautifulSoup
from utils import (
    searchChevalByName,
    getChevalDetail,
)

incap_session_name = 'incap_ses_1177_1885728'
incap_session_value = 'k9Hsbm+2DnDFoaptkItVECKVhWAAAAAAE6flKnvdwMFjf5L/RWu1Ng==';

pnd.set_option('display.max_columns', None)
df_chevaux = pnd.read_csv('datas/output/chevaux.csv')
# print(df_chevaux.head())
df_historique = pnd.read_csv('datas/output/arc_triomphe_historique.csv')
df_performance = pnd.read_csv('datas/output/cheval_performance.csv')
# df_historique.info()
df_2008 = df_historique[df_historique['Année'] == 2008]
df_2008_subset = df_2008[['Cheval']]
df_subset = df_historique[['Cheval']]

df_perf_avant_2008 = df_performance[df_performance['Annee'] < 2008]
df_perf_avant_2008_count = df_perf_avant_2008.groupby('Annee').size()
#print(df_perf_avant_2008_count)

df_perf_arc_2007 = df_performance[df_performance['DateReunion'] == 20071007]
#print(df_perf_arc_2007)
df_perf_arc_2006 = df_performance[df_performance['DateReunion'] == 20061001]
print(df_perf_arc_2006)

# Récupération des chevaux manquant (present dans historique et pas dans chevaux : pour non partants par ex
def repriseDonneeChevauxByHistorique():
    production_chevaux = pnd.read_csv('datas/production/chevaux.csv')
    last_id = int(production_chevaux.tail(1).id)
    manquant = 0
    for row in df_subset.itertuples():
        # print(row.Cheval)
        nom_cheval = df_chevaux.loc[df_chevaux['NumSire'] == row.Cheval, 'NomCheval'].values
        if nom_cheval.size == 0:
            manquant += 1
            # print('manquant: ',row.Cheval)
            detail_request = getChevalDetail(row.Cheval, incap_session_name, incap_session_value)
            page_content = BeautifulSoup(detail_request, "html.parser")
            titre_nom = page_content.find('h1').getText()
            resultwords = [word for word in titre_nom.split() if word not in ['BRZ', 'FR', 'GB', 'GER', 'IRE', 'ITY', 'JPN', 'NZ', 'SPA', 'SWI', 'USA']]
            cheval_nom = ' '.join(resultwords)

            print(cheval_nom)
            if len(cheval_nom):
                if True:
                    search_fg = searchChevalByName(cheval_nom, incap_session_name, incap_session_value, fake=False)
                    if search_fg:
                        data = pnd.DataFrame.from_records(search_fg, index=[0])
                        format_df = data.rename(columns={"AnneeNaissance": "naissance", "NomCheval": "nom", "NumSire": "id_francegalop","Suffixe": "pays", "Race": "race", "Sexe": "sexe"})
                        format_df = format_df.drop(['link'], axis=1)
                        format_df['id'] = last_id+1
                        format_df = format_df[['id', 'nom', 'sexe', 'naissance', 'race', 'pays', 'id_francegalop']]
                        with open('datas/production/chevaux.csv', 'a') as f:
                            format_df.to_csv(f, header=False)
                        last_id += 1
                    else:
                        print('search fg failed for ', cheval_nom)
                        for item in ['(BRZ)', '(FR)', '(GB)', '(GER)', '(IRE)', '(ITY)', '(JPN)', '(NZ)', '(SPA)','(SWI)', '(USA)']:
                            cheval_nom = cheval_nom.replace(item, '')
                        print('clean name', cheval_nom)
                        search_fg = searchChevalByName(cheval_nom, incap_session_name, incap_session_value, fake=False)
                        if search_fg:
                            data = pnd.DataFrame.from_records(search_fg, index=[0])
                            format_df = data.rename(columns={"AnneeNaissance": "naissance", "NomCheval": "nom", "NumSire": "id_francegalop","Suffixe": "pays", "Race": "race", "Sexe": "sexe"})
                            format_df = format_df.drop(['link'], axis=1)
                            format_df['id'] = last_id+1
                            format_df = format_df[['id', 'nom', 'sexe', 'naissance', 'race', 'pays', 'id_francegalop']]
                            with open('datas/production/chevaux.csv', 'a') as f:
                                format_df.to_csv(f, header=False)
                            last_id += 1


            else:
                print('nom cheval', nom_cheval, 'est vide')


                print('-----------------------')

        """
            print(nom_cheval)
        print(type(nom_cheval))
        print('count', nom_cheval.size)
        print(type(nom_cheval.size))
        print('-----------')
        """

        # nom_cheval = df_chevaux[df_chevaux['NumSire'] == row.Cheval]['NomCheval'].values.tolist()
        # nom_cheval = df_chevaux.loc[df_chevaux['NumSire'] == row.Cheval, 'NomCheval'].values[0]
        # print(nom_cheval)

cheval_nom = "MIGWAR(IRE)"
removable_list = ['(BRZ)', '(FR)', '(GB)', '(GER)', '(IRE)', '(ITY)', '(JPN)', '(NZ)', '(SPA)', '(SWI)', '(USA)', 'BRZ', 'FR', 'GB', 'GER', 'IRE', 'ITY', 'JPN', 'NZ', 'SPA', 'SWI', 'USA']
for item in ['(BRZ)', '(FR)', '(GB)', '(GER)', '(IRE)', '(ITY)', '(JPN)', '(NZ)', '(SPA)', '(SWI)', '(USA)', 'BRZ', 'FR', 'GB', 'GER', 'IRE', 'ITY', 'JPN', 'NZ', 'SPA', 'SWI', 'USA']:
    cheval_nom = cheval_nom.replace(item,'')

print(cheval_nom)

