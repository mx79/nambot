import re
import json
import random
import pickle
import numpy as np
from typing import Dict, List, Union
from os import getenv
from os.path import join
from pkg.bot.clean import clean_text

# Paths
dir_name = getenv("PKG_DIR")
data_dir = join(dir_name, "bot", "data")
model_dir = join(dir_name, "bot", "models")


class UnknownModelError(Exception):

    def __init__(
            self,
            message: str
    ):
        super().__init__(message)


class IntentClassifier:

    def __init__(
            self,
            model: str,
    ):
        """
        Description: Instantiation of an intention classification object based on Keras Sequential
        :param model: The path where the model is stored
        """
        self.model = pickle.load(open(join(model_dir, model), "rb"))
        try:
            with open(join(data_dir, "nlu.json"), "r") as f:
                intent_json = json.load(f)
                f.close()
        except FileNotFoundError:
            raise UnknownModelError("The model name entered is not stocked in models path or does not exist")
        words = []
        for liste in intent_json.values():
            for sent in liste:
                tokens = clean_text(sent, no_accent=False)
                words.extend(tokens)
        self.vocab = sorted(set(words))
        self.classes = sorted(set([intent for intent in intent_json.keys()]))

    def bag_of_words(
            self,
            text: str
    ) -> np.array:
        """
        Description: The method that applies the bag of words technique
        :param text: The sentence on which to apply the function
        :return: An array numpy with the number of occurrences of each word in the input sentence
        """
        tokens = clean_text(text, no_accent=False)
        bow = [0] * len(self.vocab)
        for w in tokens:
            for idx, word in enumerate(self.vocab):
                if word == w:
                    bow[idx] = 1
        return np.array([np.array(bow)])

    def get_intent(
            self,
            text: str,
    ) -> str:
        """
        Description: The method that allows us to recover the intention of a given sentence
        :param text: The sentence whose intention we want to detect
        :return: The intent, if any
        """
        res = {}
        thresh = 0.7
        result = self.model.predict(self.bag_of_words(text))[0]
        y_pred = [[idx, res] for idx, conf in enumerate(result) if conf > thresh]
        y_pred.sort(key=lambda x: x[1], reverse=True)
        for r in y_pred:
            res.update({self.classes[r[0]]: r[1]})
        for key, val in res.copy().items():
            if val != max([val for val in res.copy().values()]):
                res.pop(key, None)
        while len(res) > 1:
            res.pop(random.choice(list(res.keys())), None)
        if len(res) == 0:
            return ""
        return list(res.keys())[0]


class EntityExtractor:

    def __init__(
            self,
            file: str,
            regex_dict: Dict[str, List[str]] = None
    ):
        """
        Description: Instantiation of the RegexEntityExtractor object with a dictionary of entities and patterns
        :param regex_dict: The dictionary that contains the entities and their corresponding pattern as a regex
        """
        self.regex_dict = regex_dict
        try:
            if regex_dict is None:
                f = open(join(data_dir, file), "r")
                self.regex_dict = json.load(f)
                f.close()
        except FileNotFoundError as e:
            raise e

    def get_entity(
            self,
            text: str
    ) -> Dict[str, Union[str, List[str]]]:
        """
        Description: The method that returns a match dictionary based on the entities found in the input sentence
        :param text: The text or sentence that we pass to the extractor
        :return: A match dictionary based on the entities found
        """
        cleaned_text = " " + clean_text(text, no_accent=False, lowercase=False, lemmatize_text=False, tokenize_text=False) + " "
        res = {}
        pattern_list = []
        for key, value in self.regex_dict.items():
            for pattern in value:
                m = re.search(pattern, cleaned_text)
                if m:
                    pattern_list.append(m.group())
                    pattern_list = sorted(set(pattern_list))
                    if len(pattern_list) > 1:
                        res.update({key: pattern_list})
                    else:
                        res.update({key: m.group()})
            pattern_list = []
        return res
