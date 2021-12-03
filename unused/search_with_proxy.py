import requests
from bs4 import BeautifulSoup as Bs
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

# '''sn rukno coine manually nt'''
# for coin_name in first_2000: 
# for coin_name in after_2000_names: 
#     shramba.add_coin(coin_name)
# 
# shramba.shrani_stanje(DATA)
#first_2000 = [match[1] for match in matches[0:2000]]
#+ time.asctime().split(" ")[1] + " " + time.asctime().split(" ")[2]) datum če ga rabim
#########################################################################################################

#def searching_for_new_coin():
#
#    date = time.asctime().split(" ")
#    clock = date[3] + ' ' + date[1] + ', ' + date[4]
#
#    ############################################################
#    proxies = get_free_proxies()
#
#    for i in range(50):
#        print(f"request number: ({i})")
#        proxy = proxies[i]
#        try:
#            response = requests.get(url, headers=headers, params=params, proxies={"http":proxy, "https":proxy}, timeout=0.5)
#            break
#        except:
#            continue
#
#    ############################################################
#
#    #response = requests.get(url, headers=headers, params=params)
#    fulltext = response.text
#
#    sample = r'"symbol":"(.*?)","slug":"(.*?)"'
#    matches = re.findall(sample, fulltext)
#    after_2000_names = [match[1] for match in matches[1998:]]
#
#
#    for name in after_2000_names:
#        if name not in shramba.coins_in_names:
#            with open(f"{name}.txt", "w") as f:
#                print(f"coin {name} has arrived at: " + clock, file=f)
#                shramba.add_coin(name)
#    print(lightgreen("done searching"))