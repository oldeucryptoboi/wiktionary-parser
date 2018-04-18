from parser.WiktionaryEntryParser import WiktionaryEntryParser
from api import RelationType
from api.util import Language

from parser.en.components import *
from parser.components import CategoryHandler, InterwikiLinkHandler
from parser.util import ParsingContext


class ENWiktionaryEntryParser(WiktionaryEntryParser):
    """ An implementation of the :@link IWiktionaryEntryParser interface for
        parsing the contents of article pages from the English Wiktionary. """

    def __init__(self, language=Language.ENGLISH, redirectName="REDIRECT"):
        """ Initializes the English entry parser. That is, the language and the
            redirection pattern is defined, and the handlers for extracting
            the information from the article constituents are registered. """
        super().__init__(language, redirectName)

        # Fixed name content handlers.
        self.register(ENSemanticRelationHandler(RelationType.SYNONYM, "Synonyms", "Synomyms", "Synoynms"))
        self.register(ENSemanticRelationHandler(RelationType.ANTONYM, "Antonyms"))
        self.register(ENSemanticRelationHandler(RelationType.HYPERNYM, "Hypernyms"))
        self.register(ENSemanticRelationHandler(RelationType.HYPONYM, "Hyponyms"))
        self.register(ENSemanticRelationHandler(RelationType.HOLONYM, "Holonyms"))
        self.register(ENSemanticRelationHandler(RelationType.MERONYM, "Meronyms"))
        self.register(ENSemanticRelationHandler(RelationType.TROPONYM, "Troponyms"))
        self.register(ENSemanticRelationHandler(RelationType.COORDINATE_TERM, "Coordinate terms"))
        self.register(ENSemanticRelationHandler(RelationType.SEE_ALSO, "See also"))
        self.register(ENRelationHandler(RelationType.DERIVED_TERM, "Derived terms"))
        self.register(ENRelationHandler(RelationType.ETYMOLOGICALLY_RELATED_TERM, "Related terms"))
        self.register(ENDescendantRelationHandler("Descendants"))
        self.register(ENTranslationHandler())
        self.register(ENEtymologyHandler())
        self.register(ENReferenceHandler())
        self.register(ENQuotationHandler())
        self.register(ENPronunciationHandler())
        self.register(ENUsageNotesHandler())

        # Pattern
        self.register(CategoryHandler("Category"))
        self.register(InterwikiLinkHandler("Category"))
        self.register(ENWordLanguageHandler())
        self.register(ENSenseHandler())

    def createParsingContext(self, page):
        return ParsingContext(page, ENEntryFactory())

    def isStartOfBlock(self, line):
        """ Checks if it is start of section. Symbols are =, [[ """
        line = line.strip()
        if line.startswith("----"):
            return True

        if line.startswith("="):
            return True
        if line.startswith("[[") and line.endswith("]]"):
            return True

        return False
