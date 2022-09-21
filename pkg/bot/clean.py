from os.path import abspath, dirname, join
import nltk
import pandas as pd
from typing import List
from unidecode import unidecode
from nltk.stem import WordNetLemmatizer
nltk.download("wordnet")
nltk.download("punkt")
nltk.download("omw-1.4")

lemmatizer = WordNetLemmatizer()


def clean_text(
        s: str,
        no_punctuation: bool = True,
        no_accent: bool = True,
        no_stopword: bool = True,
        lowercase: bool = True,
        lemmatize_text: bool = True,
        tokenize_text: bool = True
) -> str or List:
    """
    Description: The function that allows to clean a given text in depth by applying several layers of treatment
    :param s: The sentence to clean
    :param no_punctuation: The boolean that indicates if we must remove the punctuation in the text or not
    :param no_accent: The boolean that indicates if we must remove the accent in the text or not
    :param no_stopword: The boolean that indicates if we must remove the stopwords in the text or not
    :param lowercase: The boolean that indicates if we must lower the text or not
    :param lemmatize_text: The boolean that indicates if we must lemmatize the text or not
    :param tokenize_text: The boolean that indicates if we must tokenize the text or not
    :return: The sentence or word list based on boolean values
    """
    if no_punctuation:
        s = remove_punctuation(s)
    if no_accent:
        s = remove_accent(s)
    if no_stopword:
        s = stopword(s)
    if lowercase:
        s = lower(s)
    if lemmatize_text:
        s = lemmatize(s)
    if tokenize_text:
        s = tokenize(s)
    return s


# Enlève la ponctuation
def remove_punctuation(s: str) -> str:
    """
    Description: The function that allows to remove punctuation in a sentence
    :param s: The sentence from which the punctuation must be removed
    :return: The sentence without punctuation
    """
    punctuation = "!@#$%^&*()[]_-+<>?:.,;"
    for c in s:
        s = s.replace(c, "") if c in punctuation else s
    return s


# Enlève les accents dans un texte donné
def remove_accent(s: str) -> str:
    """
    Description: The function that allows you to remove the accents in a sentence
    :param s: The sentence from which the accents must be removed
    :return: The sentence without accents
    """
    return unidecode(s)


# Liste des stopwords français (Personnalisable dans stopwords_fr.xlsx)
def stopword_list() -> List:
    """
    Description: The function that retrieves a list of stopwords, here in French
    :return: The list of stopwords in French
    """
    # "./backend/chucho/data/stopwords_fr.xlsx"
    data = pd.read_excel(join(dirname(abspath(__file__)), "data", "stopwords_fr.xlsx"))
    stopwords = list(data["stopwords"])
    return stopwords


# Supprime les stopwords dans une phrase en français :
def stopword(s: str) -> str:
    """
    Description: The function that removes the stopwords contained in the input sentence
    :param s: The sentence from which the stopwords must be removed
    :return: The sentence without stopwords
    """
    return list_to_str([word for word in s.split() if word not in stopword_list()])


def lower(s: str):
    """
    Description: The function that put words of a sentence in lowercase mode
    :param s: The sentence from which the words must be lowered
    :return: The sentence with words in lowercase
    """
    return list_to_str([word.lower() for word in s.split()])


def lemmatize(s: str) -> str:
    """
    Description: The function that lemmatizes the words of a sentence or a word
    :param s: The sentence containing the words to lemmatize or the word to lemmatize
    :return: The lemmatized sentence or the lemmatized word
    """
    if len(s.split()) > 1:
        return list_to_str([lemmatizer.lemmatize(word) for word in s.split()])
    else:
        return lemmatizer.lemmatize(s)


def tokenize(s: str) -> List:
    """
    Description: The function that separates the words of a sentence to facilitate their study in NLP
    :param s: The sentence whose words must be separated
    :return: The list containing the tokens of the input sentence
    """
    return nltk.word_tokenize(s)


def list_to_str(a_list: List) -> str:
    """
    Description: The function that transforms a list into a string
    :param a_list: The list to transform into a string
    :return: The desired string
    """
    return " ".join(a_list)
