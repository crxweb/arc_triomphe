import requests


session = requests.Session()
url = 'https://www.france-galop.com/fr/frglp_global/ajax?id=VmpxdVlzR1R1VGNtdUxJOGVxL0VGZz09&module=cheval_engagements&nbResult=50&racetrack=0'
url = 'https://www.france-galop.com/fr/frglp_global/ajax?module=search&mot=youmzain&type=IsRechercheCheval'

incap_session_name = 'incap_ses_454_1885728'
incap_session_value = 'ndFfbyriNQQprrgj7O5MBi0Je2AAAAAAK4EPQB/GOghOsGu0H005AA==';

my_cookie_list = [
    #'visid_incap_1885728=iLY/l0mrQ2+lFCXnp6sBRSPfemAAAAAAQUIPAAAAAABFFnSIMuZ/X7knDKukU5R1',
    # 'francegalop=fcgl-front-02',
    # 'nlbi_1885728=NVyYHbzKYTuoCWqe1vWh3wAAAAAVOLjRSW9EUCnDwn6ULArM',
    incap_session_name + '=' + incap_session_value,
    # 'has_js=1',
    # '_ga=GA1.2.1557203614.1618639991',
    # '_gid=GA1.2.981817766.1618639991',
    # '_gcl_au=1.1.775057217.1618639991'
]
print(my_cookie_list)
my_cookie_headerstring = '; '.join(my_cookie_list)
print(my_cookie_headerstring)

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'Cookie': my_cookie_headerstring,
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

if True:
    r = requests.get(url, headers=headers)
    # print(r.text)
    #print(r.json())
    r_json = r.json();
    print(r_json)
    result_chevaux = r_json.get('Chevaux');
    result_chevaux_count = len(result_chevaux)
    searched_horse = 'YOUMZAIN'
    res = next((sub for sub in result_chevaux if sub['NomCheval'].rstrip() == searched_horse), None)
    if res:
        print('le cheval ',searched_horse,'a bien été trouvé')
        print(res)
    else:
        print('le cheval ', searched_horse, "n'a pas été trouvé")

