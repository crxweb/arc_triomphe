

url_ex = 'https://www.iturf.fr/programme/resultats.php?date=2017-10-06'

def generate_url_targets(input):
    urls = []
    for date in input:
        urls.append('https://www.iturf.fr/programme/resultats.php?date='+str(date))

    return urls
