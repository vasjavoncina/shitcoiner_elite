import requests
import re
from coins_coin_class import Coins
import time
import json
from funkcija_za_iskanje_po_id import searching_with_id
from bs4 import BeautifulSoup
from funkcija_za_zamik_eno_ure import eno_uro_nazaj
#########################################################################################################

def krepko(niz):
    return f'\033[01m{niz}\033[0m'
def modro(niz):
    return f'\033[1;94m{niz}\033[0m'
def rdece(niz):
    return f'\033[1;91m{niz}\033[0m'
def zeleno(niz):
    return f'\033[0;32m{niz}\033[0m'
def rumeno(niz):
    return f'\033[0;33m{niz}\033[0m'
def lightcyan(niz):
    return f'\033[0;96m{niz}\033[0m'
def pink(niz):
    return f'\033[0;95m{niz}\033[0m'
def lightgreen(niz):
    return f'\033[0;92m{niz}\033[0m'

#########################################################################################################

DATA = "shramba.json"
try:
    shramba = Coins.nalozi_stanje(DATA)
except FileNotFoundError:
    shramba = Coins()

#########################################################################################################

def API():
    gmt = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    zamakjen = eno_uro_nazaj(gmt)
    print(lightgreen(gmt))
    print(lightgreen(zamakjen))
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://coinmarketcap.com/',
    'Origin': 'https://coinmarketcap.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'If-Modified-Since': zamakjen,
    'TE': 'trailers',
    }
    params = (
        ('listing_status', 'active'),
        ('cryptoAux', 'is_active,status'),
        ('start', '1'),
        ('limit', '10000'),
    )
    params2 = (
        ('listing_status', 'active'),
        ('cryptoAux', 'is_active,status'),
        ('start', '10001'),
        ('limit', '10000'),
    )
    url = 'https://api.coinmarketcap.com/data-api/v3/map/all'

    return headers, params, params2, url


def searching():

    headers, params, params2, url = API()

    date = time.asctime().split(" ")
    clock = date[3] + ' ' + date[1] + ', ' + date[4]

    response_1 = requests.get(url, headers=headers, params=params, timeout=1) 
    response_2 = requests.get(url, headers=headers, params=params2, timeout=1) 

    fulltext_1 = response_1.text
    fulltext_2 = response_2.text

    #with open("scan.txt", "w", encoding="utf-8") as f:
    #    print(fulltext_1, file=f)
        
    #sample = r'"symbol":"(.*?)","slug":"(.*?)"'
    sample2= r'"symbol":"(.*?)","slug":"(.*?)","is_active":1,"status":"active"'

    matches_1 = re.findall(sample2, fulltext_1)
    matches_2 = re.findall(sample2, fulltext_2)
    
    
    
    
    names = [match[1] for match in matches_1] + [match[1] for match in matches_2]
    
    for name in names:
        if name not in shramba.coins_in_names:
            text = f"coin {name} has arrived at: " + clock
            #winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
            send_message(text, 1047104075)
            #833164394 julijan chat id
            with open("txt_datoteke/newcoins.txt", "a") as f:
                print(text, file = f)
            shramba.add_coin(name)


###########################################################################
# telegram
###########################################################################


TOKEN = "2105035703:AAH8UNfNXEHC3LsH0u9QLjw1meGRL_sgv9g"
URL = f"https://api.telegram.org/bot{TOKEN}/"



def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf-8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    





if __name__ == '__main__':

    i=1
    while True:

        try:
            ### all listed detector ###
            searching()
            shramba.shrani_stanje(DATA)
            print(rumeno("number: " + str(i)) + lightgreen('\nlist detector search status: complete.'))
            i+=1


            ### id detector ###
            new_name = searching_with_id()
            if new_name != None:
                text = f"ID_SEARCH: {new_name}"
                send_message(text, 1047104075)
                #833164394 julijan chat id
            print(lightcyan('id detector search status: complete.'))


            time.sleep(60)
        except:
            print(pink("didnt work this time"))
            i+=1     



