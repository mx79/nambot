import requests
import datetime

from random import choice
from bs4 import BeautifulSoup
from typing import Dict


def get_edt() -> str:
    """It opens the timetable of th promotion P4BDIA in a new browser tab.
    """
    return '<a href="https://qrc.gescicca.net/Planning.aspx?id=JIQmJi9xPenYP9j1da6bMA%3d%3d&annsco=2022&typepersonne=AUDITEUR">Emploi du temps</a>'


def get_news() -> str:
    """It gives the last news from the website `Le Monde`.

    :return: A list of news as a formatted string
    """
    res = "Titres :\n"
    response = requests.get('https://www.lemonde.fr')
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find('body').find_all('h3')
    for x in headlines:
        res += x.text.strip() + "\n"

    return res


def get_meteo(ville: str) -> str:
    """It gives the meteorological condition for a given city.

    :param ville: The city from which we want to get meteorological information
    :return: Meteorological information as a formatted string
    """
    url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={ville}&APPID=beb97c1ce62559bba4e81e28de8be095"
    r_forecast = requests.get(url_forecast)
    data = r_forecast.json()
    meteo = data["list"][1]
    t = meteo['main']['temp']
    humidity = meteo['main']['humidity']
    temps = meteo['weather'][0]['description']

    return f"{ville.strip()} :\nLa température moyenne est de {round(t - 273.15)} degrés Celsius\nTaux d'humidité {humidity}%\nConditions climatiques {temps}\n\n"


def bot_response(entities: Dict, intent: str, previous_intent: str = None) -> str:
    """Orchestration of the Cnambot responses.
    """
    response = ""
    # Previous intent
    if previous_intent == "METEO" and "VILLE" in entities.keys():
        intent = "METEO"

    # Entities
    # User say something like "hello"
    if "YO" in entities.keys():
        response += choice(["Yo", "Salut", "Hey"]) + "\n"
    # User say something like "T'es un batard le bot"
    if "AGGRO" in entities.keys():
        response += choice(["Ce n'est pas très gentil !", "Pas sympa...", "T'es pas cool !",
                            "Je ne te permets pas de me parler comme cela."]) + "\n"
        return response

    # Intents
    # User say something like "Tu sais faire quoi ?"
    if intent == "UTILITY":
        response += "Je peux aider sur les domaines suivants :" \
                    "\n-Date du jour\n-Emploi du temps\n-Meteo\n-News du jour\n-Pire logiciel" \
                    "\n-Meilleur logiciel\n-Meilleur Chatbot"
    # User say something like "Comment tu vas ?"
    elif intent == "CCV":
        response += choice(["Ça va très bien et toi ?", "Impeccable et toi ?",
                            "Ça roule et toi ?"])
    # User say something like "Il est"
    elif intent == "DATE":
        response += datetime.date
    # API "edt"
    elif intent == "EDT":
        response += f"Le voici : {get_edt()}"
    # API "meteo"
    elif intent == "METEO":
        if "VILLE" in entities.keys():
            if type(entities["VILLE"]) == list:
                for city in entities["VILLE"]:
                    response += get_meteo(city)
            else:
                response += get_meteo(entities["VILLE"])
        else:
            response += "Pour quelle ville ?"
    # API "news"
    elif intent == "NEWS":
        response += get_news()
    # User say something like "quel est le pire logiciel"
    elif intent == "PIRELOGICIEL":
        response += "Hadoop c'est pas top"
    # User say something like "tu connais le meilleur logiciel"
    elif intent == "MEILLEURLOGICIEL":
        response += "MyDataBall bien évidemment"
    # User say something like "tu sais qui est le meilleur chatbot"
    elif intent == "MEILLEURCHATBOT":
        response += "Je suis un très bon ChatBot, mais pour être honnête, " \
                    "je vous recommande plutôt Alexa ou Siri."
    # Default response from the Cnambot, if no intent or entity has been detected
    else:
        response += "Désolé, je n'ai pas compris ce que tu m'as dit."

    return response
