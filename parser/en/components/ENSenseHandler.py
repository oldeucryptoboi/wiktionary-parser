import re

from api.entry.WiktionaryRelation import WiktionaryRelation
from api.util import Language
from api.util import TemplateParser
from api import PartOfSpeech
from api.entry.WikiString import WikiString
from api.entry.WiktionaryExample import WiktionaryExample
from api import RelationType

from parser.en.components.ENBlockHandler import ENBlockHandler
from parser.en.components.ENWordFormHandler import ENWordFormHandler
from parser.en.components.ENEntryFactory import ENEntryFactory
from parser.en.components.ENQuotationHandler import ENQuotationHandler
from parser.en.components.ENNonEngWordFormHandler import ENNonEngWordFormHandler
from parser.en.components.EnGlossEntry import EnGlossEntry
from parser.util import StringUtils


class ENSenseHandler(ENBlockHandler):
    """ Extract POS, gloss and inner-definition quotations. It checks if a string is in a predefined pos set,
        if it is, the section is the pos section. """

    EXAMPLE_PATTERN = re.compile("^#+:+")  
    POS_PATTERN = re.compile(  
        "^====?\\s*(?:"
        + "\\{\\{([^\\}\\|]+)(?:\\|[^\\}\\|]*)?\\}\\}|"
        + "\\[\\[(?:[^\\]\\|]+\\|)?([^\\]\\|]+)\\]\\]|"
        + "([^=]+?)"
        + ")\\s*\\d*\\s*=?===$"
    )

    def __init__(self):
        """ Init attributes """
        self.entryFactory = ENEntryFactory()
        self.quotationHandler = ENQuotationHandler()

        self.partOfSpeech = None
        self.glossEntryList = None
        self.takeControl = False
        self.wordFormHandler = None
        self.lastPrefix = None

    def canHandle(self, blockHeader):
        """
         * Check if the label of section is a predefined POS label.
         """
        self.partOfSpeech = None
        posLabel = blockHeader.strip()
        if not posLabel.startswith("===") or not posLabel.endswith("==="):
            return False

        matcher = re.search(ENSenseHandler.POS_PATTERN, blockHeader)
        if not matcher:
            return False

        if matcher.group(1) is not None:
            posLabel = matcher.group(1)
        elif matcher.group(2) is not None:
            posLabel = matcher.group(2)
        else:
            posLabel = matcher.group(3)

        self.partOfSpeech = PartOfSpeech.findByName(posLabel, ENEntryFactory.posMap)
        return self.partOfSpeech is not None

    def processHead(self, text, context):
        """
         * Process head
         """
        context.setPartOfSpeech(self.partOfSpeech)
        self.glossEntryList = list()
        self.wordFormHandler = self.getWordFormHandler(context)
        self.takeControl = True
        self.quotationHandler.processHead(text, context)
        self.lastPrefix = None
        return True

    # noinspection PyMethodMayBeStatic
    def getWordFormHandler(self, context):
        if Language.ENGLISH == context.getLanguage():
            return ENWordFormHandler(context.getPage().getTitle())
        else:
            return ENNonEngWordFormHandler()

    def processBody(self, text, context):
        """
         * Extract example, gloss and in-definition quotation
         """
        line = text.strip()
        if not len(line):
            return self.takeControl

        additionalLine = False
        if self.lastPrefix is not None and not line.startswith("#") and not line.startswith("{"):
            line = self.lastPrefix + line
            additionalLine = True

        exampleMatcher = re.search(ENSenseHandler.EXAMPLE_PATTERN, line)
        if exampleMatcher is not None:
            self.processExampleLine(line, exampleMatcher.group(), additionalLine)
        elif line.startswith("#*"):
            # Quotation.
            self.quotationHandler.extractQuotation(line[1:], additionalLine, context)
            self.lastPrefix = "#*"
            self.takeControl = False

        elif line.startswith("##"):
            # Subsense.
            subsense = line[2:].strip()
            if self.glossEntryList:
                glossEntry = self.glossEntryList[-1]
                if subsense.startswith("*"):
                    self.quotationHandler.extractQuotation(subsense, additionalLine, context)
                    self.lastPrefix = "##*"
                else:
                    glossEntry.setGloss(glossEntry.getDefinition() + "\n" + subsense)
                    self.lastPrefix = "##"

            self.takeControl = False

        elif line.startswith("#") and len(line) > 2:
            # Sense definition.
            self.saveQuotations()
            gloss = line[1:].strip()
            glossEntry = EnGlossEntry(gloss)
            self.glossEntryList.append(glossEntry)
            self.lastPrefix = "#"
            self.takeControl = False

        elif self.wordFormHandler.parse(line):
            self.lastPrefix = None
            self.takeControl = True

        return self.takeControl

    def saveQuotations(self):
        quotations = self.quotationHandler.getQuotations()
        if not quotations or not self.glossEntryList:
            return

        glossEntry = self.glossEntryList[-1]
        for quotation in quotations:
            glossEntry.getQuotations().append(quotation)
        self.quotationHandler.getQuotations().clear()

    def fillContent(self, context):
        """
         * Store POS (a.k.a. part-of-speech), examples, quotations in WordEntry object
         """
        self.saveQuotations()

        # In the special case when article constituents have been found before
        # the first entry, do not create a new entry, but use the automatically
        # created one.
        if context.getPage().getEntryCount() == 1 and context.getPage().getEntry(0).getPartOfSpeech() is None:
            entry = context.getPage().getEntry(0)
            entry.setWordLanguage(context.getLanguage())
            entry.addPartOfSpeech(context.getPartOfSpeech())
            if context.getHeader() is not None:
                entry.setHeader(context.getHeader())
            entry.setWordEtymology(context.getEtymology())
        else:
            entry = self.entryFactory.createEntry(context)
            context.getPage().addEntry(entry)

        pronunciations = context.getPronunciations()
        if pronunciations is not None:
            for pronunciation in pronunciations:
                entry.addPronunciation(pronunciation)

        for senseEntry in self.glossEntryList:
            sense = entry.createSense()
            sense.setGloss(WikiString(senseEntry.getDefinition()))
            for exp in senseEntry.getExampleList():
                translation = senseEntry.getExampleTranslation(exp)
                sense.addExample(WiktionaryExample(WikiString(exp), None if translation is None else WikiString(translation)))

            for quotation in senseEntry.getQuotations():
                sense.addQuotation(quotation)

            entry.addSense(sense)

            for relation in [WiktionaryRelation(target, key) for key, value in senseEntry.getRelations() for target in value]:
                sense.addRelation(relation)

            # for relation in flatMap([WiktionaryRelation(target, key) for key, value in senseEntry.getRelations() for target in value]):
            #     sense.addRelation(relation)

        for form in self.wordFormHandler.getWordForms():
            entry.addWordForm(form)

        entry.setRawHeadwordLine(self.wordFormHandler.getRawHeadwordLine())

        genders = self.wordFormHandler.getGenders()
        if genders is not None:
            for gender in genders:
                entry.addGender(gender)

    @staticmethod
    def isNym(line):
        return "{{syn" in line or "{{ant" in line

    def processExampleLine(self, line, currentPrefix, additionalLine):
        lineContent = line[len(currentPrefix):].strip()
        if self.glossEntryList:
            glossEntry = self.glossEntryList[-1]
            if self.isNym(lineContent):
                self. parseNym(lineContent, glossEntry)
            else:
                self.parseExample(lineContent, currentPrefix, additionalLine, glossEntry)

        self.lastPrefix = currentPrefix
        self.takeControl = False

    def parseExample(self, lineContent, currentPrefix, additionalLine, glossEntry):
        translatedExample = self.lastPrefix is not None and \
                             re.search(ENSenseHandler.EXAMPLE_PATTERN, self.lastPrefix) is not None and \
                             len(currentPrefix) > len(self.lastPrefix)

        if additionalLine:
            glossEntry.appendExample(lineContent, " ")
        elif translatedExample:
            glossEntry.appendExampleTranslation(lineContent)
        else:
            glossEntry.addExample(lineContent)

    def parseNym(self, line, glossEntry):

        this = self

        # noinspection PyShadowingNames,PyUnusedLocal
        def handle(self, template):
            relation_type = this.getRelationType(template)
            if relation_type is not None:
                for i in range(1, template.getNumberedParamsCount()):
                    glossEntry.addRelation(relation_type, StringUtils.cleanText(template.getNumberedParam(i)))
            return None

        handler = type("_TemplateHandler", (TemplateParser.ITemplateHandler,), {"handle": handle})
        TemplateParser.parse(line, handler())

    @classmethod
    def getRelationType(cls, template):
        # https://en.wiktionary.org/wiki/Template:synonyms
        # https://en.wiktionary.org/wiki/Template:antonyms
        case = template.getName()
        if case == "syn" or case == "synonyms":
            return RelationType.SYNONYM
        if case == "ant" or case == "antonyms":
            return RelationType.ANTONYM

        return None
