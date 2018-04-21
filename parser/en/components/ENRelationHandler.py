from parser.en.components.ENBlockHandler import ENBlockHandler
from errors import RuntimeException
from api.entry import WiktionaryRelation
from parser.en.components.WordList import WordList


class ENRelationHandler(ENBlockHandler):
    """ Parser component for extracting relations from the English Wiktionary. """

    def __init__(self, relationType, *labels):
        """  Initializes the block handler for the given relation type and
            section headers. """
        super().__init__(*labels)
        self.relationType = relationType

        self.relationList = None

    def processHead(self, textLine, context):
        self.relationList = list()
        return super().processHead(textLine, context)

    def processBody(self, text, context):
        """ Extract word list from the given text line """
        line = text.strip()
        if line and line.startswith("*"):
            self.relationList.append(self.parseWordList(line[1:]))

        return False

    def fillContent(self, context):
        """ Add word list to senseEntry. """
        posEntry = context.findEntry()
        if posEntry is None:
            raise RuntimeException("posEntry is None " + context.getPartOfSpeech())

        for wordList in self.relationList:
            matchingSense = self.findMatchingSense_(posEntry, wordList)
            for target in wordList:
                matchingSense.addRelation(WiktionaryRelation(target, self.relationType))

    def findMatchingSense_(self, posEntry, wordList):
        """  @return the target sense to use for this wordList. Defaults to the unassigned sense, subclasses
            should override if needed. """
        return posEntry.getUnassignedSense()

    def parseWordList(self, text):
        """ @return the parsed word list """
        return WordList.parse(text)
