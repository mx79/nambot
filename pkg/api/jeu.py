import webbrowser
from googlesearch import search


def get_jeu(jeu: str):
    # for j in search(query, tld="co.in", num=10, stop=10, pause=2):
    link = search(jeu, tld="co.in", num=10, stop=1, pause=2)
    webbrowser.open(link)
