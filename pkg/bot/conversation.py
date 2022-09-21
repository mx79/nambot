from typing import List, Dict, Any
from random import choice
from pkg.api import meteo, news, edt, jeu


class Transcript:

    def __init__(
            self,
            user_id: str,
            msg: str,
            intent: str = None,
            entities: Dict = None,
            response: Any = None
    ):
        """
        Description: The transcript class will contain a sentence and information related to it.
        It will implement methods to extract information
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
        """
        Description: The method that displays the Transcript object as a dictionary with additional information
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
        """
        Description: Orchestration of the Nambot responses
        """
        # Entities
        # User say something like "hello"
        if "YO" in self.entities.keys():
            self.response += choice(["Yo", "Salut", "Hey"]) + "\n"
        # User say something like "comment ça va"
        if "AGGRO" in self.entities.keys():
            self.response += choice(["Ce n'est pas très gentil", "Pas sympa", "T'es pas cool"]) + "\n"
            return

        # Intents
        if self.intent == "CCV":
            self.response += choice(["Ça va très bien et toi ?", "Impeccable et toi ?",
                                     "Ça roule et toi ?"])
        # API "edt"
        elif self.intent == "EDT":
            edt.get_edt()
            self.response += "Voici ton emploi du temps"
        # API "meteo"
        elif self.intent == "METEO":
            if "VILLE" in self.entities.keys():
                if type(self.entities["VILLE"]) == list:
                    for city in self.entities["VILLE"]:
                        self.response += meteo.get_meteo(city)
                else:
                    self.response += meteo.get_meteo(self.entities["VILLE"])
        # API "news"
        elif self.intent == "NEWS":
            self.response += news.get_news()
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
        #
        elif self.intent == "GEOGUESSR":
            jeu.get_jeu(self.intent)
            self.response += "Voici Geoguessr"


class Conversation:

    def __init__(
            self,
            conv_id: str,
            transcript_list: List = None,
    ):
        """
        Description: Creation of our conversation object which will contain a list of Transcript objects
        and indications about the conversation in general
        :param conv_id: The ID of our conversation
        :param transcript_list: The list of transcripts that we will fill in during a conversation
        """
        self.conv_id = conv_id
        if transcript_list is None:
            transcript_list = []
        self.transcript_list = transcript_list

    def old_infos(self):
        """
        Description: This method retrieves information from past transcripts of the current conversation
        :return: Information from previous transcripts
        """
        return [t.as_dict()["infos"] for idx, t in enumerate(self.transcript_list)
                if idx != len(self.transcript_list) - 1]

    def add_transcript(self, transcript: Transcript):
        """
        Description: The method that adds a Transcript object to the current conversation
        :param transcript: The Transcript object we give to our Conversation object
        """
        self.transcript_list.append(transcript)
