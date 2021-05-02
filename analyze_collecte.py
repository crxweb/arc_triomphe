import statistics
import pandas as pd
from FranceGalop import (
    utils,
)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

"""
pouvoir faire corrélation entre probabilite de faire partie des x premiers si :
- à déjà concurru pour l'arc
- age (on sais déjà que entre 3-4 ans c'est le standard)
- jockey ayant déjà gagné l'ar
- entrainneur ayant déjà gagné l'arc
- musique du cheval à générer puis retraiter en numérique

pour perf + course de l'arc : prendre en considération l'état du terrain (attention cette donnée n'est dispo que pour 
les courses se déroulant sur hippodrome francais (scrap detail course)


rafiner

df_course_arc = pd.read_csv(utils.course_folder + "arc_triomphe.csv", index_col=None, header=0)
search = df_course_arc[df_course_arc['Place'] == "3"]
search = df_course_arc.loc[df_course_arc['Place'] == "3", ['annee','Place']]
print(search.groupby('annee').size())
"""

# Cheval Stats
if False:
    df_arc_liste = pd.read_csv(utils.course_folder + 'arc_triomphe_list.csv', index_col=None, header=0)
    arc_course_id = list(df_arc_liste['id'])
    df_perf = pd.read_csv(utils.perf_folder + 'performance.csv', index_col=None, header=0)
    df_chevaux = pd.read_csv(utils.cheval_folder + 'retrieve_undefined.csv', index_col=None, header=0)

    s_id, s_nom, s_participation, s_bestplace, s_worstplace, s_avgplace = ([] for _ in range(6))
    for cheval in df_chevaux.itertuples():
        cheval_perf_arc = df_perf[
            (df_perf['id'].isin(arc_course_id))
            & (df_perf['cheval_id'] == cheval.id)
            ].shape[0]
        cheval_places = list(df_perf.loc[
                                 (df_perf['id'].isin(arc_course_id))
                                 & (df_perf['cheval_id'] == cheval.id)
                                 & ~(df_perf['place'].isin(['99', 'DI', 'AR', 'DB', 'RP', 'TB']))
                                 , 'place'].astype(int))
        avg_place, worst_place, best_place = None, None, None
        if len(cheval_places):
            cheval_places.sort(key=int)
            worst_place = cheval_places[len(cheval_places)-1]
            if worst_place == 99:
                print(cheval_places)
            best_place = cheval_places[0]
            avg_place = statistics.mean(cheval_places)

        s_id.append(cheval.id)
        s_nom.append(cheval.nom)
        s_participation.append(cheval_perf_arc)
        s_bestplace.append(best_place)
        s_worstplace.append(worst_place)
        s_avgplace.append(avg_place)
        #print('---------------')

    data = {'id': s_id, 'nom': s_nom, 'arc_participation': s_participation, 'arc_best_place': s_bestplace,
            'arc_worst_place': s_worstplace, 'arc_avg_place': s_avgplace}
    df_chevaux_stat = pd.DataFrame.from_dict(data)
    df_chevaux_stat = df_chevaux_stat.sort_values(['arc_participation', 'arc_avg_place'], ascending=[False, True])
    df_chevaux_stat.info()
    print(df_chevaux_stat[['nom', 'arc_participation', 'arc_best_place', 'arc_worst_place', 'arc_avg_place']].head(200))
    df_chevaux_stat.to_csv(utils.processing_folder + "chevaux/stats.csv", index=None)

# Générer musique cheval / performance
df_perf = pd.read_csv(utils.perf_folder + 'performance.csv', index_col=None, header=0)
distinc_specialite = df_perf.groupby('specialite').size()
print(distinc_specialite)
cheval_id = "SHpmdDVUam5PNDMyOTJuWDJBVUFidz09" # golden horn
df_collecte_perf = pd.read_csv(utils.perf_folder + 'performance.csv', index_col=None, header=0)
df_collecte_perf.info()
cheval_perf = df_perf.loc[df_collecte_perf['cheval_id'] == cheval_id, ['date','place','specialite']]
cheval_perf['date'] = pd.to_datetime(cheval_perf.date, format="%d/%m/%Y")
cheval_perf = cheval_perf.sort_values(by='date', ascending=False)
print(cheval_perf.head(100))
musique = ""
for perf in cheval_perf.itertuples():
    musique += perf.place + perf.specialite

print(musique)


