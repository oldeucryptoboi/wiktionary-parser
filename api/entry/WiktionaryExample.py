from api import IWiktionaryExample


class WiktionaryExample(IWiktionaryExample):

    def __init__(self, example, translation):
        self.example = example
        self.translation = translation

    def getText(self):
        return self.example.getText()

    def getExample(self):
        return self.example

    def getTranslation(self):
        return self.translation
