import requests
from bs4 import BeautifulSoup

url = 'https://www.lemonde.fr'


def get_news() -> str:
    """It gives the last news from the website `Le Monde`.

    :return: A list of news as a formatted string
    """
    res = "Titres :\n"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find('body').find_all('h3')
    for x in headlines:
        res += x.text.strip() + "\n"

    return res
