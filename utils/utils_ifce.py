import requests
from bs4 import BeautifulSoup

def search(nom,annee_naissance,sexe):
    """

    :param nom: STR
    :param annee_naissance: INT YYYY
    :param sexe: [ "MALE","HONGRE","FEMELLE" ]
    :return:
    """
    base_url = 'https://infochevaux.ifce.fr';
    url = base_url + "/fr/info-chevaux"
    payload={'recherche': '{"recherche":"'+nom+'","page":1,"nbResultat":"10","facettes":{"annee_naissance_cheval":["'+str(annee_naissance)+'"],"sexe_cheval":["'+sexe+'"]},"filtres":{}}'}
    files=[

    ]
    headers = {
      'Cookie': 'PHPSESSID=8mske76mn67df44813jpeqbij7; visid_incap_2474039=UIheFbIERb2jg1xiX/n30IL+hGAAAAAAQUIPAAAAAAAIMjFVpjUOpJ5j2JlkHotp; incap_ses_9218_2474039=ZajGF9GY2QEfhHgjTOrsf4L+hGAAAAAA1jjJysZqZP1ByJIbB6nMew==; _ga=GA1.2.1369964116.1619328647; _gid=GA1.2.1747399075.1619328648; dtCookie=1$14B86D62DB46F1D3E9AB53C081C96900|111efffa471a14ee|1; visid_incap_2474042=5V5cfzjWTa2DNpiijRGcuTUAhWAAAAAAQUIPAAAAAACJlD6+yDDy332a0T1DkXOT; incap_ses_9218_2474042=Du2+dzQIJyw/UXkjTOrsfzUAhWAAAAAAKJBw9GVxxvARC//ICxUSBw==; rxVisitor=1619329078200M3ED4B5V1R70ILHA9J5K2T1GTJBAA1ME; dtLatC=2; rxvt=1619330900471|1619329078203; dtPC=1$529098335_973h-vMRUMLPHDDLQRPEHHHLFPGFORIPSAAGUG-0e3; dtSa=true%7CC%7C-1%7CSIRE-info-chevaux-1%7C-%7C1619329101071%7C529098335_973%7Chttps%3A%2F%2Fwww.ifce.fr%2Fifce%2Fsire-demarches%2F%7CSIRE%20%26%20D%C3%A9marches%20-%20Ifce%7C%7C%7C; _gat=1'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    json = response.json()
    resultats = json.get('resultats')
    #print(resultats)
    with open("../datas/test/output1.html", "w") as file:
        #file.write(resultats)
        soup = BeautifulSoup(resultats, "html.parser")
        #link = soup.find("a", href=True)["href"]
        #print(link)
        for link in soup.find_all("a", class_="strong text-uppercase"):
            cheval_url = base_url + str(link["href"])
            print(cheval_url)
            res = requests.get(cheval_url, headers=headers)
            page_content = BeautifulSoup(res.content, "html.parser")
            file.write(str(page_content))
            test_numsire = page_content.body.find_all(text='Numéro SIRE')
            print(test_numsire)
            for colordemarche in page_content.find_all("span", class_="color-demarches"):
                print(colordemarche)



#search("chachnak",2017,"MALE")
#search("GHAIYYATH",2015,"MALE")
search("LA BOUM",2003,"FEMELLE")
#search("HIRUNO D'AMOUR",2007,"MALE")

# trouver URL : https://infochevaux.ifce.fr/fr/chachnak-Z2QpRsmFQDSNFc0ezD4I_A/infos-generales
# parser cette url pour trouver info utiles
"""
Numéro SIRE : 17750245E
Numéro UELN : 2500FR17750245E
Date de naissance : 30/03/2017
Pays de naissance : FRANCE
Stud-book de naissance : STUD BOOK FRANCAIS CHEVAL DE PUR SANG
Stud-book adulte : STUD BOOK FRANCAIS CHEVAL DE PUR SANG
pour connaitre les races de production, cliquez ici
"""