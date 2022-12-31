import requests
import webbrowser

from random import choice
from bs4 import BeautifulSoup
from googlesearch import search
from typing import List, Dict, Any

news_url = 'https://www.lemonde.fr'


def get_edt():
    """It opens the timetable of th promotion P4BDIA in a new browser tab.
    """
    webbrowser.open(
        "https://qrc.gescicca.net/Planning.aspx?id=JIQmJi9xPenYP9j1da6bMA%3d%3d&annsco=2022&typepersonne=AUDITEUR"
    )


def get_jeu(jeu: str):
    """It opens the entered game in a new browser tab.

    :param jeu: The game to launch in a new browser tab.
    """
    # TODO: Change this function
    links = search(jeu, num=10)
    webbrowser.open(links[0])


def get_news() -> str:
    """It gives the last news from the website `Le Monde`.

    :return: A list of news as a formatted string
    """
    res = "Titres :\n"
    response = requests.get(news_url)
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
    # Météo
    meteo = data["list"][1]
    t = meteo['main']['temp']
    humidity = meteo['main']['humidity']
    temps = meteo['weather'][0]['description']

    return f"{ville.strip()} :\nLa température moyenne est de {round(t - 273.15)} degrés Celsius\nTaux d'humidité {humidity}%\nConditions climatiques {temps}\n\n"


class Transcript:

    def __init__(
            self,
            user_id: str,
            msg: str,
            intent: str = None,
            entities: Dict = None,
            response: Any = None
    ):
        """The transcript class will contain a sentence and information related to it.
        It will implement methods to extract information.

        :param user_id: The CNAM user id
        :param msg: The message entered by the CNAM user
        :param intent: The intention related to the sentence
        :param entities: The dictionary of entities related to the sentence
        :param response: The tip that the whisperer will send back
        """
        self.user_id = user_id
        self.msg = msg
        if intent is None:
            self.intent = ""
        self.intent = intent
        if entities is None:
            self.entities = {}
        self.entities = entities
        if response is None:
            self.response = ""
        self.resp()

    def as_dict(self):
        """The method that displays the Transcript object as a dictionary with additional information.

        :return: The dictionary object representing the conversation
        """
        return {
            "user_id": self.user_id,
            "msg": self.msg,
            "infos": {
                "intent": self.intent,
                "entities": self.entities,
                "response": self.response
            }
        }

    def resp(self):
        """Orchestration of the Cnambot responses.
        """
        # Entities
        # User say something like "hello"
        if "YO" in self.entities.keys():
            self.response += choice(["Yo", "Salut", "Hey"]) + "\n"
        # User say something like "T'es un batard le bot"
        if "AGGRO" in self.entities.keys():
            self.response += choice(["Ce n'est pas très gentil !", "Pas sympa...", "T'es pas cool !",
                                     "Je ne te permets pas de me parler comme cela."]) + "\n"
            return

        # Intents
        # User say something like "Comment tu vas ?"
        if self.intent == "CCV":
            self.response += choice(["Ça va très bien et toi ?", "Impeccable et toi ?",
                                     "Ça roule et toi ?"])
        # API "edt"
        elif self.intent == "EDT":
            get_edt()
            self.response += "Voici ton emploi du temps"
        # API "meteo"
        elif self.intent == "METEO":
            if "VILLE" in self.entities.keys():
                if type(self.entities["VILLE"]) == list:
                    for city in self.entities["VILLE"]:
                        self.response += get_meteo(city)
                else:
                    self.response += get_meteo(self.entities["VILLE"])
        # API "news"
        elif self.intent == "NEWS":
            self.response += get_news()
        # User say something like "quel est le pire logiciel"
        elif self.intent == "PIRELOGICIEL":
            self.response += "Hadoop c'est pas top"
        # User say something like "tu connais le meilleur logiciel"
        elif self.intent == "MEILLEURLOGICIEL":
            self.response += "MyDataBall bien évidemment"
        # User say something like "tu sais qui est le meilleur chatbot"
        elif self.intent == "MEILLEURCHATBOT":
            self.response += "Je suis un très bon ChatBot, mais pour être honnête, " \
                             "je vous recommande plutôt Alexa ou Siri."
        # User say something like ""
        elif self.intent == "GEOGUESSR":
            get_jeu(self.intent)
            self.response += "Voici Geoguessr"
        # Default response from the Cnambot, if no intent or entity has been detected
        else:
            self.response += "Désolé, je n'ai pas compris ce que tu m'as dit."


class Conversation:

    def __init__(self, conv_id: str, transcript_list: List[Transcript] = None):
        """Creation of our conversation object which will contain a list of Transcript objects
        and indications about the conversation in general.

        :param conv_id: The ID of our conversation
        :param transcript_list: The list of transcripts that we will fill in during a conversation
        """
        self.conv_id = conv_id
        if transcript_list is None:
            transcript_list = []
        self.transcript_list = transcript_list

    def old_infos(self) -> List:
        """This method retrieves information from past transcripts of the current conversation.

        :return: Information from previous transcripts
        """
        return [t.as_dict()["infos"] for idx, t in enumerate(self.transcript_list)
                if idx != len(self.transcript_list) - 1]

    def add_transcript(self, transcript: Transcript):
        """The method that adds a Transcript object to the current conversation.

        :param transcript: The Transcript object we give to our Conversation object
        """
        self.transcript_list.append(transcript)
