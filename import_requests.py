import requests
from bs4 import BeautifulSoup
import time
import json
import os

folder_path = './dataset/'

def write_to_json(dictionary, relative_path, file_name):
    if not os.path.exists(relative_path):
        os.makedirs(relative_path)

    file_path = os.path.join(relative_path, file_name)

    with open(file_path, 'w') as file:
        json.dump(dictionary, file)


def parse_metadata(raw):
    to_remove = [
        'Iniciado há ', 'Atualizada ',
        'Idioma ','Visualizações ', 'Favoritos ',
        'Comentários ','Listas de leitura', 'Palavras',
        'Concluído', 'Categorias', 'Personagens', 'Tags'
    ]
    result = {
        'StartDate': '', 
        'LastUpdate' : '', 'Language': '', 
        'Views' : '', 'Stars' :'', 
        'Comments' :'', 'Listed' :'', 
        'Words' :'', 'Finished' :'', 
        'Categories' :'', 'Characters' :'', 
        'Tags' :''}
    
    parsed = raw.split('\r\n')
    i = 1
    for line in result:
        p = parsed[i].split(to_remove[i-1])
        text = []
        for c in range(len(p)):
            if c != 0:
                text.append(p[c].strip())
        result[line] = ''.join(text)
        i = i + 1
    return result


def extract_fic_info(url):
    try:

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        box = soup.find('section', class_="boxConteudo")
        box_div = box.find_all('div')
        title = box_div[1].find('h1', class_="tituloPrincipal").text
        info = box_div[1].find_all('div')
        synopsis = info[3].text
        metadata = info[4].text
        
        data = {"title": title, "synopsis": synopsis, "metadata": parse_metadata(metadata)}
    
        return data

    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro: {e}")

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

write_to_json(
    extract_fic_info("https://www.spiritfanfiction.com/historia/um-amor-proibido-toshiruz-x-mei-ling-24887152"), 
    folder_path, 
    'file_name.json')


# meta = {
#     'title': 'História Um amor proibido toshiruz x mei-ling', 
#     'synopsis': '\nSinopse:\r\nNa mansão neo está toshiruz que decide fazer uma festa com todos os seus amigos só que acontece que toshiruz começa a gostar de mei-ling e mei-ling também mais eles não sabem que eles se gostam.\r\n', 
#     'metadata': 
#     '\r\nIniciado há 5 dias às 21:55\r\nAtualizada 47 minutos atrás\r\nIdioma Português\r\nVisualizações 8\r\nFavoritos 1\r\nComentários 0\r\nListas de leitura 0\r\nPalavras 3.319\r\nConcluído Não\r\nCategorias Histórias Originais\r\nPersonagens Personagens Originais\r\nTags Romance Luta Engraçado\n'
#     }


# print(parse_metadata(meta["metadata"]))
