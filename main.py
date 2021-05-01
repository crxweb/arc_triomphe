# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
    import datetime
    from utils import (
        next_weekday,
        arctriomphe_date,
        generate_url_targets
    )

    """"
    # Liste des 6 dernières dates du Prix de l'Arc de Triomphe
    last_6_arc_dates = arctriomphe_date(6)
    for date in last_6_arc_dates:
        print(date)

    url_to_scrap = generate_url_targets(last_6_arc_dates)
    for url in url_to_scrap:
        print(url)    
    """

    import requests

    session = requests.Session()
    url = 'https://www.france-galop.com/fr/frglp_global/ajax?id=VmpxdVlzR1R1VGNtdUxJOGVxL0VGZz09&module=cheval_engagements&nbResult=100&racetrack=0'
    url = 'https://www.france-galop.com/fr/frglp_global/ajax?module=search&mot=youmzain&type=IsRechercheCheval'

    # On effectue première requête pour tenter de récupérer les cookies nécessaires
    response = session.get(url)
    session_cookies = session.cookies
    my_cookies = session_cookies.get_dict()
    #print(my_cookies)
    # {'incap_ses_1371_1885728': 'nQepNJNb1mGX0mhiZsUGE/GCemAAAAAAZ6Tary4xGU80eocSWWM3gg==', 'visid_incap_1885728': 'Ns0AbLVISS2RsaClbyv4/fGCemAAAAAAQUIPAAAAAAAPbb0dxttiBA//7hyQLWvj'}

    my_cookie_list = []
    for cookie in session_cookies:
        #print (cookie.name, cookie.value, cookie.domain)
        #my_cookie_headerstring += cookie.name+'='+cookie.value+'; '
        my_cookie_list.append(cookie.name+'='+cookie.value)

    #print(my_cookie_list);
    my_cookie_headerstring = '; '.join(my_cookie_list)
    print(my_cookie_headerstring)
    # ci-dessous valeurs cookie importe depuis navigateur (semble que valeurs plus haut ne soient pas valides)
    header_cookies = 'visid_incap_1885728=6zjN+v8BRMCSLqxIdVrKbynUeWAAAAAAQUIPAAAAAABh59Z2g9R8PRccZTGDptTu; incap_ses_1371_1885728=jOTHUHq3vES5ZltiZsUGE052emAAAAAAsRHmWkqBbpiklBQ2p15JgA=='
    print(header_cookies);
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Cookie': header_cookies,
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }
    r = requests.get(url, headers=headers)
    # print(r.text)
    print(r.json())







    if False:

        if False:
            header_cookies = 'visid_incap_1885728=6zjN+v8BRMCSLqxIdVrKbynUeWAAAAAAQUIPAAAAAABh59Z2g9R8PRccZTGDptTu; francegalop=fcgl-front-02; nlbi_1885728=NVyYHbzKYTuoCWqe1vWh3wAAAAAVOLjRSW9EUCnDwn6ULArM; incap_ses_1371_1885728=jOTHUHq3vES5ZltiZsUGE052emAAAAAAsRHmWkqBbpiklBQ2p15JgA==; has_js=1; _ga=GA1.2.1557203614.1618639991; _gid=GA1.2.981817766.1618639991; _gcl_au=1.1.775057217.1618639991'
            # print(header_cookies.split('; '))

            my_cookie_list = [
                'visid_incap_1885728=6zjN+v8BRMCSLqxIdVrKbynUeWAAAAAAQUIPAAAAAABh59Z2g9R8PRccZTGDptTu',
                # 'francegalop=fcgl-front-02',
                # 'nlbi_1885728=NVyYHbzKYTuoCWqe1vWh3wAAAAAVOLjRSW9EUCnDwn6ULArM',
                'incap_ses_1371_1885728=jOTHUHq3vES5ZltiZsUGE052emAAAAAAsRHmWkqBbpiklBQ2p15JgA==',
                # 'has_js=1',
                # '_ga=GA1.2.1557203614.1618639991',
                # '_gid=GA1.2.981817766.1618639991',
                # '_gcl_au=1.1.775057217.1618639991'
            ]
            print(my_cookie_list)
            my_cookie_headerstring = '; '.join(my_cookie_list)
            print(my_cookie_headerstring)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Cookie': my_cookie_headerstring,
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }
        r = requests.get(url, headers=headers)
        # print(r.text)
        print(r.json())
