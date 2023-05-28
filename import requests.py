import requests
from bs4 import BeautifulSoup
import time

def extrair_links_pagina(url, div_id):
    try:

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        div = soup.find('div', id=div_id)
        articles = div.find_all('article')   
        links = []
        for x in articles:
            h2 = x.find('h2') if div else None 
            links.append(h2.find('a').get('href'))

        return links

    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro: {e}")


div_id = "meio"
num_pag = 1

for i in range(2):
    if num_pag == 1:
        url = f"https://www.spiritfanfiction.com/recentes"
    else:
        url = f"https://www.spiritfanfiction.com/recentes?pagina={num_pag}"

    links = extrair_links_pagina(url, div_id)
    if links:
        print(f"Links extraídos da página em {url}, dentro da div com ID '{div_id}', na pag{num_pag}:")
        for link in links:
            print(link)
    time.sleep(5)
    num_pag += 1