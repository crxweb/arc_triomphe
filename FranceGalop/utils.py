incap_session_name = "incap_ses_1095_1885728";
incap_session_value = "gSGaEinhP3gaZsQ5LjkyD0rniGAAAAAAMJsJNikFbq7rfIm7Rgu5FA=="
cookie = 'francegalop=fcgl-web-01; visid_incap_1885728=f4q5iFCjQ3KLw/sMm7VJt/LrjGAAAAAAQUIPAAAAAADBBhoxYAy+g8Nu/enRLo3D; incap_ses_8218_1885728=2qwUZOTgdypRcBbcmjMMcvLrjGAAAAAADc3jB1DPinscPB3QDNqMTQ==; _ga=GA1.2.2023099979.1619848180; _gid=GA1.2.2024350857.1619848180; _gcl_au=1.1.1166768797.1619848180; cookiefirst-consent=%7B%22necessary%22%3Atrue%2C%22functional%22%3Atrue%2C%22performance%22%3Atrue%2C%22advertising%22%3Atrue%2C%22timestamp%22%3A1619848184%7D; incap_ses_456_1885728=lgtLIuoIeCHdGpP2+wlUBhAejWAAAAAAAgSQIaFPB0CObYk0yLHU+Q==; _gat=1; _dc_gtm_UA-110792996-1=1; visid_incap_1885728=plxOrVzCSAS4Vd7/9HoZo8jdemAAAAAAQUIPAAAAAABf9TigOEzv1YLzkfVwhHUi'
base_url = 'https://www.france-galop.com';

country = ['AUS', 'CAN', 'BRZ', 'FR', 'GB', 'GER', 'IRE', 'ITY', 'JPN', 'NZ', 'SPA', 'SWI', 'USA', '(AUS)', '(CAN)',
           '(BRZ)', '(FR)', '(GB)', '(GER)', '(IRE)', '(ITY)', '(JPN)', '(NZ)', '(SPA)', '(SWI)', '(USA)', '(ARG)',
           'ARG']
sexe_race = ['M.PS.', 'F.PS.', 'H.PS.', 'M.PS.+', 'F.PS.+', 'H.PS.+']
course_folder = 'collecte/france_galop/courses/'
cheval_folder = 'collecte/france_galop/chevaux/'
# csv généré depuis fonction search_by_name utilisant service ajax FRANGE GALOP (service arrêté) reto
cheval_production_csv = 'collecte/france_galop/chevaux/chevaux_2008_2020.csv'
cheval_from_course_csv = 'make_csv_from_course.csv'
cheval_retrieve_undefined = 'retrieve_undefined.csv'

def get_header():
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
