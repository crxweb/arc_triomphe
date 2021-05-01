import json
import pandas as pnd
pnd.set_option('display.max_columns',None)
import requests
import csv
from bs4 import BeautifulSoup
from utils import (
    getHeader
)

incap_session_name = 'incap_ses_8218_1885728'
incap_session_value = '/RnCQsfu3S0fYNufmDMMclOEfGAAAAAAydcOpdA78L1myMlq17icIQ==';


df_perf = pnd.read_csv('datas/output/cheval_performance.csv')
#df_perf.info()
#print(df_perf.head(50))
search_prix_at = df_perf[df_perf['Prix'].str.strip() == "QATAR PRIX DE L'ARC DE TRIOMPHE"]
#print(search_prix_at.meetingDate)
prix = search_prix_at['meetingDate'].unique().tolist()

urls = []
for p in prix:
    link = json.loads(p.replace("'", '"'))['link']
    urls.append('https://www.france-galop.com'+link)

"""
urls = [
    'https://www.france-galop.com/fr/course/detail/2019/P/c0xHRGZBeWkzcDhqa1orc0xLRjdQZz09',
    'https://www.france-galop.com/fr/course/detail/2020/P/dXdodlJzTFVzMUFRT0FrOERIWDIyQT09'
]
"""
url_cpt = 0
for url in urls:
    print('url',url)
    headers = getHeader(incap_session_name, incap_session_value)
    res = requests.get(url, headers=headers)
    page_content = BeautifulSoup(res.content, "html.parser")
    print(page_content)
    with open('datas/output/arc_triomphe_historique.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        row_cpt = 0
        for items in page_content.find('table').find_all(['tr', 'thead']):
            data = [item.get_text(strip=True) for item in items.find_all(['th', 'td'])]
            if row_cpt == 0:
                year = 'Année'
            else:
                year = url.split('https://www.france-galop.com/fr/course/detail/')[1][:4]
            data.append(year)
            # print(data)
            # print(type(data))
            tag_link = items.select_one('a')
            if tag_link is not None:
                link = str(tag_link)
                cheval_id = link.split('<a href="/fr/cheval/')[1].split('">')[0]
                data[1] = cheval_id
            if row_cpt == 0:
                if url_cpt == 0:
                    writer.writerow(data)
            else:
                writer.writerow(data)
            row_cpt += 1
            url_cpt += 1
