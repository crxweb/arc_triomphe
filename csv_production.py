import pandas as pd
import uuid

pd.set_option('display.max_columns',None)

df_chevaux = pd.read_csv('datas/output/chevaux.csv', index_col=0)
#df_chevaux.info()


renamed_df = df_chevaux.rename(columns={"AnneeNaissance": "naissance", "NomCheval": "nom", "NumSire": "id_francegalop", "Suffixe": "pays","Race": "race", "Sexe": "sexe"})
renamed_df = renamed_df.drop(['link'], axis=1)
renamed_df['id'] = renamed_df.index + 1
renamed_df = renamed_df[['id','nom','sexe','naissance','race','pays','id_francegalop']]
renamed_df.info()
print(renamed_df.head(5))

pays = renamed_df.groupby('pays').size()
print(pays)
#for row in renamed_df.itertuples():
    #print(row.naissance)
    #print(row[0])


#renamed_df.to_csv('datas/production/chevaux.csv')
