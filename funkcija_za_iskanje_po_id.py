import requests
import re


def searching_with_id():

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'sl,en-GB;q=0.7,en;q=0.3',
    'Referer': 'https://coinmarketcap.com/',
    'Origin': 'https://coinmarketcap.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'TE': 'trailers',
    }
    with open("txt_datoteke/id.txt", "r") as f:
        id = f.readline().strip()

    params = (
        ('id', id),
        )
    response = requests.get('https://api.coinmarketcap.com/data-api/v3/cryptocurrency/quote/latest', headers=headers, params=params)
    text = response.text 
    
    
    sample_1 = r'"error_code":"500"'
    sample_2 = r'"slug":".*?"'
    
    
    match_1 = re.findall(sample_1, text)
    match_2 = re.findall(sample_2, text)

    if match_1 == match_2 == []:
        print(f"SUCCESS PAGE {id}")
        return
    if match_1 != []:
        return
    
    name = match_2[0].split('"')[3]
    with open("txt_datoteke/id.txt", "w") as f:
        new_id_number = str(int(id) + 1) 
        print(new_id_number, file=f)
    return name

