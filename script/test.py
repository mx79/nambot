from googletrans import Translator

translator = Translator()

print(translator.translate("I'm doing some tests on this app", dest="fr"))

print(translator.detect("I'm doing some tests on this app"))

