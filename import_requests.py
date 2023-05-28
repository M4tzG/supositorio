import requests
from bs4 import BeautifulSoup
import time
import json
import os
import datetime
import pytz

folder_path = 'K:\\spirit_data\\'
DELAY_PER_CAP = 2
DELAY_PER_PAGE = 2


def get_pages_amount(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        div = soup.find('div', class_='numeros')
        a = div.find_all('a')
        number = int(a[len(a) -1].text)

        return number

    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro: {e}")
        return 0

def grab_and_concat(urls):
    grabbed = []
    concated = ''
    done = 0
    errors = 0
    for url in urls:
        print(f"Reading URL: {url} |")
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            box = soup.find('section', class_="boxConteudo")
            box_div = box.find_all('div')

            cap_content = box_div[1].find('div', class_="texto-capitulo")

            author_notes = cap_content.find('div', class_="texto-capitulo-notas")
            author_notes_h2 = cap_content.find_all('h2')
            picture = cap_content.find('div', class_="text-center")
            hasNotes = True if author_notes else False
            hasPicture = True if picture else False
            index_title = 1 if hasNotes else 0
            index_text = 2 if hasNotes else 1
            # print('NOTAS: ', author_notes, 'H2S: ', author_notes_h2)
            if not author_notes:
                index_title = 0
            elif(len(author_notes) == 2):
                index_title = 1
            elif(author_notes_h2):
                if(len(author_notes_h2) > 0):
                        if(author_notes and author_notes_h2[0].text == 'Notas do Autor'):
                            index_title = 1
                        elif(author_notes and author_notes_h2[0].text == 'Notas Finais'):
                            index_title = 0
                        else:
                            index_title = 0
            
            if(not hasNotes and not hasPicture):
                index_text = 0
            elif(not hasNotes or not hasPicture):
                index_text = 1
            else:
                index_text = 2

            # print('HERE: ', cap_content.find_all('h2')[1], cap_content.find_all('div')[2])
            # print(hasNotes, hasPicture, index_title, index_text)
            cap_title = cap_content.find_all('h2')[index_title].text
            cap_text = cap_content.find_all('div')[index_text].text
            data = f"{cap_title}\n{cap_text}"
            grabbed.append(data)

            done = done + 1
            print(f"Successfully grabbed '{cap_title}' | {done} / {len(urls)} [{done / len(urls) * 100}%] | Errors: {errors}")

        except requests.exceptions.RequestException as e:
            errors = errors + 1
            print(f"Failed grabbing {done + 1} / {len(urls)} | Errors: {errors}")
            print(f"Ocorreu um erro: {e}")
            continue
        time.sleep(DELAY_PER_CAP)
    
    return concated.join(grabbed)

def write_to_json(dictionary, relative_path, file_name):
    if not os.path.exists(relative_path):
        os.makedirs(relative_path)

    file_path = os.path.join(relative_path, file_name)

    with open(file_path, 'w') as file:
        json.dump(dictionary, file)


def parse_metadata(raw):
    to_remove = [
        'Iniciado', 'Atualizada ',
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
    i = 0
    for line in result:
        if not (i+1 > len(parsed)-1):
            p = parsed[i+1].split(to_remove[i])
            text = []
            for c in range(len(p)):
                if c != 0:
                    text.append(p[c].strip())
            result[line] = ''.join(text).encode().decode('utf-8')
            # print("TMNC: ", ''.join(text).encode().decode('utf-8'), text)
            i = i + 1
    return result


def extract_fic_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        print(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        box = soup.find('section', class_="boxConteudo")

        box_div = box.find_all('div')
        title = box_div[1].find('h1', class_="tituloPrincipal").text
        info = box_div[1].find_all('div')
        synopsis = info[3].text
        metadata = info[4].text

        table = box.find("table", class_="listagemCapitulos")
        caps = table.find_all("tr", class_="listagem-textoBg1")
        cap_links = []
        for tr in caps:
            a = tr.find("a")
            cap_links.append(a.get("href"))
        
        data = {
            "downloaded_in": str(datetime.datetime.now(pytz.timezone('America/New_York'))),
            "url": url,
            "title": title, 
            "synopsis": synopsis, 
            "metadata": parse_metadata(metadata),
            "chapter_urls": cap_links,
            "history": grab_and_concat(cap_links)
        }
    
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

# print(grab_and_concat(["https://www.spiritfanfiction.com/historia/a-conquista-do-trono-5340076/capitulos/8399828"]))
div_id = "meio"
num_pag = (9)
total_pages = get_pages_amount("https://www.spiritfanfiction.com/recentes")
from_ = 1
to_ = round(total_pages/2)
print(to_)
# to_ = round(total_pages - (total_pages / 2))

for i in range(from_, to_):
    if num_pag == 1:
        url = f"https://www.spiritfanfiction.com/recentes"
    else:
        url = f"https://www.spiritfanfiction.com/recentes?pagina={num_pag}"

    links = extrair_links_pagina(url, div_id)
    if links:
        current = 1
        print(f"Links extraídos da página em {url}, dentro da div com ID '{div_id}', na pag{num_pag}:")
        for link in links:
            print("\n------------\n")
            print(f"[ pag[{num_pag}]_story[{current}]_fanfic.json ] : \n")

            write_to_json(
            extract_fic_info(link), 
            folder_path, 
            f"pag[{num_pag}]_story[{current}]_fanfic.json")

            print("\n\n------------\n\n")

            current = current + 1
            time.sleep(DELAY_PER_PAGE)
    num_pag += 1

write_to_json(
    extract_fic_info("https://www.spiritfanfiction.com/historia/brands-of-tomorrow-24538184"), 
    folder_path, 
    'file_name2.json')

# https://www.spiritfanfiction.com/historia/um-amor-proibido-toshiruz-x-mei-ling-24887152
meta = {
    'title': 'História Um amor proibido toshiruz x mei-ling', 
    'synopsis': '\nSinopse:\r\nNa mansão neo está toshiruz que decide fazer uma festa com todos os seus amigos só que acontece que toshiruz começa a gostar de mei-ling e mei-ling também mais eles não sabem que eles se gostam.\r\n', 
    'metadata': 
    '\r\nIniciado há 5 dias às 21:55\r\nAtualizada 47 minutos atrás\r\nIdioma Português\r\nVisualizações 8\r\nFavoritos 1\r\nComentários 0\r\nListas de leitura 0\r\nPalavras 3.319\r\nConcluído Não\r\nCategorias Histórias Originais\r\nPersonagens Personagens Originais\r\nTags Romance Luta Engraçado\n'
    }


# print(extract_fic_info("https://www.spiritfanfiction.com/historia/complicated-24741568"))
# print(parse_metadata(meta["metadata"]))

# print(grab_and_concat(["https://www.spiritfanfiction.com/historia/as-presas-do-submundo-jinx-x-you-24447852/capitulos/24447860"]))
