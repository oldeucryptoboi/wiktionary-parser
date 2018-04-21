from api.util import Language
from parser.en.components.ENBlockHandler import ENBlockHandler
from api.entry import WikiString


class ENReferenceHandler(ENBlockHandler):
    """ Parser component for extracting references and external links from
        the English Wiktionary. """

    def __init__(self):
        """ Initializes the block handler for parsing all sections starting with
         *  one of the specified labels. """
        super().__init__("References", "External links", "External lnks")

        self.references = None
        self.inTemplate = None

    def processHead(self, textLine, context):
        self.references = list()
        self.inTemplate = False
        return True

    def processBody(self, textLine, context):
        textLine = textLine.strip()
        if textLine.startswith("{{quote-"):
            self.inTemplate = True
        elif self.inTemplate or textLine.startswith("|"):
            if "}}" not in textLine:
                self.inTemplate = False
        elif textLine.startswith("{{"):
            self.references.append(WikiString(textLine.strip()))
        elif textLine.startswith("*"):
            textLine = textLine[1:]
            self.references.append(WikiString(textLine.strip()))
        else:
            return False

        return True

    def fillContent(self, context):
        """
         * Add external links to WordEntry
         """
        # Add references to all previous entries of the same language.
        entry = context.findEntry()

        for unassignedSense in [e.getUnassignedSense() for e in context.getPage().entries if
                                e.getWordLanguage() == entry.getWordLanguage()]:
            for reference in self.references:
                unassignedSense.addReference(reference)

        return


