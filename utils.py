import requests
from bs4 import BeautifulSoup

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