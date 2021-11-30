import requests
from bs4 import BeautifulSoup as Bs
import re
from model import Coins
import time
import winsound
import json
######################################################################################################################
######################################################################################################################


def get_free_proxies():
    url = "https://free-proxy-list.net/"

    soup = Bs(requests.get(url).content, 'html.parser')

    proxies = []
    for row in soup.find("table", attrs={"class": "table table-striped table-bordered"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            proxies.append("http://" + str(ip) + ":" + str(port))
        except IndexError:
            continue
    return proxies


######################################################################################################################
######################################################################################################################

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
    'If-Modified-Since': 'Fri, 19 Nov 2021 22:05:03 GMT',
    'TE': 'trailers',
}

params = (
    ('listing_status', 'active'),
    ('cryptoAux', 'is_active,status'),
    ('start', '1'),
    ('limit', '10000'),
)


url = 'https://api.coinmarketcap.com/data-api/v3/map/all'


# '''sn rukno coine manually nt'''
# for coin_name in first_2000: 
# for coin_name in after_2000_names: 
#     shramba.add_coin(coin_name)
# 
# shramba.shrani_stanje(DATA)
#first_2000 = [match[1] for match in matches[0:2000]]
#+ time.asctime().split(" ")[1] + " " + time.asctime().split(" ")[2]) datum če ga rabim
#########################################################################################################


def searching_for_new_coin():

    clock = time.asctime().split(" ")[3] + " "

    ############################################################
    proxies = get_free_proxies()

    for i in range(50):
        print(f"request number: ({i})")
        proxy = proxies[i]
        try:
            response = requests.get(url, headers=headers, params=params, proxies={"http":proxy, "https":proxy}, timeout=0.5)
            break
        except:
            continue

    ############################################################

    #response = requests.get(url, headers=headers, params=params)
    fulltext = response.text

    sample = r'"symbol":"(.*?)","slug":"(.*?)"'
    matches = re.findall(sample, fulltext)
    after_2000_names = [match[1] for match in matches[1998:]]


    for name in after_2000_names:
        if name not in shramba.coins_in_names:
            with open(f"{name}.txt", "w") as f:
                print(f"coin {name} has arrived at: " + clock, file=f)
                shramba.add_coin(name)
    print(lightgreen("done searching"))




def searching():

    clock = time.asctime().split(" ")[3] + " "
    response = requests.get(url, headers=headers, params=params, timeout=1) 
    fulltext = response.text
    #with open("scan.html", "w") as f:
    #    print(soup, file=f)
    sample = r'"symbol":"(.*?)","slug":"(.*?)"'
    sample2= r'"symbol":"(.*?)","slug":"(.*?)","is_active":1,"status":"active"'
    matches = re.findall(sample2, fulltext)
    after_2000_names = [match[1] for match in matches[1998:]]
    for name in after_2000_names:
        if name not in shramba.coins_in_names:
            text = f"coin {name} has arrived at: " + clock
            #winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
            send_message(text, 1047104075)
            with open("newcoins.txt", "a") as f:
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
    



i=1
while True:

    try:
        searching()
        shramba.shrani_stanje(DATA)
        print(lightgreen("done searching " + str(i)))
        i+=1
        time.sleep(120)
    except:
        print(pink("didnt work this time"))
        i+=1     



