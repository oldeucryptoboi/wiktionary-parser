from parser.en.components.ENRelationHandler import ENRelationHandler
from parser.en.components.WordList import WordList
from api import RelationType


class ENDescendantRelationHandler(ENRelationHandler):
    def __init__(self, *labels):
        super().__init__(RelationType.DESCENDANT, *labels)

    def parseWordList(self, text):
        list_ = super().parseWordList(text)
        if list_:
            return WordList(list_.comment, self.fixDescendantWordList(list_.words))
        else:
            return list_

    @classmethod
    def fixDescendantWordList(cls, wordList):
        firstWord = wordList[0]
        colon = -1 if firstWord is None else firstWord.find(':')
        if colon != -1:
            fixed = list()
            fixed.append(firstWord)

            language = firstWord[0:colon]
            for i in range(1, len(wordList)):
                word = wordList[i]
                if word.find(':') == -1:
                    fixed.append(language + ": " + word)
                else:
                    fixed.append(word)

            return fixed
        else:
            return wordList
