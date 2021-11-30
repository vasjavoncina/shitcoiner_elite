import requests
from bs4 import BeautifulSoup as bs

######################################################################################################################
######################################################################################################################


def get_free_proxies():
    url = "https://free-proxy-list.net/"

    soup = bs(requests.get(url).content, 'html.parser')

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

url = "https://httpbin.org/ip"
proxies = get_free_proxies()

for i in range(len(proxies)):
    print(f"request number: ({i})")
    proxy = proxies[i]
    try:
        response = requests.get(url, proxies={"http":proxy, "https":proxy}, timeout=0.5)
        print(response.json())
        break
    except:
        continue

######################################################################################################################
######################################################################################################################


