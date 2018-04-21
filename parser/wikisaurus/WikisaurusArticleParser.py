from api import PartOfSpeech
from api import RelationType
from api.util import Language
from errors import IOException, RuntimeException
from parser import IWiktionaryPageParser

from compat import StringReader
from parser.en.components import ENSemanticRelationHandler
from .WikisaurusEntry import WikisaurusEntry


class WikisaurusArticleParser(IWiktionaryPageParser):
    """ (Yet experimental) parser for the Wikisaurus entries (i.e., wiki pages
        in the Wikisaurus namespace that contain thesaurus-like information). """

    # noinspection PyMissingConstructor
    def __init__(self,  wiktionaryDB):
        """ Instantiates the parser for the given database. """
        self.wiktionaryDB = wiktionaryDB
        self.entryQueue = list()

        self.currentTitle = None
        self.currentNamespace = None

        self.notFoundRelation = dict()
        self.relTypeMap = dict()
        self.relTypeMap["synonyms"] = RelationType.SYNONYM
        self.relTypeMap["synonym"] = RelationType.SYNONYM
        self.relTypeMap["ambiguous synonyms"] = RelationType.SYNONYM
        self.relTypeMap["antonyms"] = RelationType.ANTONYM
        self.relTypeMap["antonym"] = RelationType.ANTONYM
        self.relTypeMap["hyponyms"] = RelationType.HYPONYM
        self.relTypeMap["instances"] = RelationType.HYPONYM
        self.relTypeMap["hypernym"] = RelationType.HYPERNYM
        self.relTypeMap["hypernyms"] = RelationType.HYPERNYM
        self.relTypeMap["descendants"] = RelationType.DESCENDANT
        self.relTypeMap["holonyms"] = RelationType.HOLONYM
        self.relTypeMap["meronyms"] = RelationType.MERONYM
        self.relTypeMap["troponyms"] = RelationType.TROPONYM
        self.relTypeMap["coordinate terms"] = RelationType.COORDINATE_TERM
        self.relTypeMap["pseudo-synonyms"] = RelationType.SEE_ALSO
        self.relTypeMap["near synonyms"] = RelationType.SEE_ALSO
        self.relTypeMap["near antonyms"] = RelationType.SEE_ALSO
        self.relTypeMap["related terms"] = RelationType.SEE_ALSO
        self.relTypeMap["various"] = RelationType.SEE_ALSO
        self.relTypeMap["see also"] = RelationType.SEE_ALSO
        self.relTypeMap["idiomatic synonyms"] = RelationType.SYNONYM
        self.relTypeMap["idioms/phrases"] = RelationType.SYNONYM
        self.relTypeMap["idioms"] = RelationType.SYNONYM

    def onParserStart(self, dumpInfo):
        pass

    def onSiteInfoComplete(self, dumpInfo):
        pass

    def onClose(self, dumpInfo):
        pass

    def onPageStart(self):
        pass

    def onPageEnd(self):
        pass

    def setAuthor(self, author):
        pass

    def setRevision(self, revisionId):
        pass

    def setTimestamp(self, timestamp):
        pass

    def setPageId(self, pageId):
        pass

    def setTitle(self, title, namespace=None):
        self.currentTitle = title
        self.currentNamespace = namespace

    def setText(self, text):
        if "Wikisaurus" != self.currentNamespace:
            return

        for entry in self.parseWikisaurusEntries(self.currentTitle, text):
            self.saveWikisaurusEntry(entry, True)

    def parseWikisaurusEntries(self, title, text):
        result = set()
        reader = StringReader(text)
        currentLang = None
        currentPos = None
        currentRelType = None
        inList = False
        inRelation = False
        inSense = False
        wikisaurusSense = None
        try:
            for line in reader.readLines():
                line = line.strip()
                if not len(line):
                    continue

                countSectionIdentifier = 0
                while countSectionIdentifier < len(line) and line[countSectionIdentifier] == '=':
                    countSectionIdentifier += 1
                line = line.replace("=", "")

                if wikisaurusSense is not None and 2 <= countSectionIdentifier < 4 \
                        or (countSectionIdentifier == 4 and line.startswith("{{ws sense")):
                    result.add(wikisaurusSense)
                    wikisaurusSense = None

                if countSectionIdentifier == 2:  # Language
                    currentLang = Language.findByName(line)
                    inRelation = False
                    inSense = False
                elif countSectionIdentifier == 3:   # POS
                    currentPos = PartOfSpeech.findByName(line)  # TODO: language-specific POS tags?
                    inRelation = False
                    inSense = False
                elif countSectionIdentifier == 4 and line.startswith("{{ws sense"):  # Sense
                    senseDef = self.extractSenseDefinition(line)
                    wikisaurusSense = WikisaurusEntry(title, currentPos, currentLang, senseDef)
                    inRelation = False
                    inSense = True
                elif (countSectionIdentifier == 5 or countSectionIdentifier == 4) and inSense:  # Relation type
                    currentRelType = self.relTypeMap.get(line.strip().lower())
                    inRelation = True
                    if currentRelType is None:
                        print(title + " RELATION NOT FOUND: " + line)
                        if line in self.notFoundRelation:
                            self.notFoundRelation[line] = self.notFoundRelation[line] + 1
                        else:
                            self.notFoundRelation[line] = 1
                elif line.startswith("{{ws beginlist"):
                    inList = True
                elif line.startswith("{{ws endlist"):
                    inList = False
                elif line.startswith("{{ws|") and inRelation and inList:
                    target = self.extractRelTarget(line)
                    if currentRelType is not None:
                        wikisaurusSense.addRelation(target[0], target[1], currentRelType)

            if wikisaurusSense is not None:
                result.add(wikisaurusSense)
        except IOException as e:
            raise RuntimeException("Error while parsing text of Wikisaurus page " + title, e)

        return result

    def onParserEnd(self,  dumpInfo):
        # Save the remaining entries.
        for entry in self.entryQueue:
            self.saveWikisaurusEntry(entry, False)
        self.entryQueue.clear()

    def saveWikisaurusEntry(self, wikisaurusEntry, allowCaching):
        # Find the Wiktionary page for this Wikisaurus entry.
        page = self.wiktionaryDB.getPageForWord(wikisaurusEntry.getTitle())
        if page is None:
            if allowCaching:
                self.entryQueue.append(wikisaurusEntry)
            else:
                print("PAGE NOT FOUND: " + wikisaurusEntry.getTitle())
            return

        # Find the Wiktionary entry within the Wiktionary page.
        for entry in page.entries:
            if entry.getWordLanguage() != wikisaurusEntry.getLanguage():
                continue
            if entry.getPartOfSpeech() != wikisaurusEntry.getPartOfSpeech():
                continue

            sense = ENSemanticRelationHandler.findMatchingSense(entry, wikisaurusEntry.getSenseDefinition())
            if sense is None:
                print("Unable to find source word sense: " + wikisaurusEntry)
                continue

            for relation in wikisaurusEntry.getRelations():
                sense.addRelation(relation)

        self.wiktionaryDB.savePage(page)

    # noinspection PyMethodMayBeStatic
    def extractSenseDefinition(self, wsSense):
        """ Extracts sense definition from Wikisaurus line. """
        wsSense = wsSense.replace("}", "").replace("{", "")
        parts = wsSense.split("\\|")
        if len(parts) > 1:
            return parts[1]
        else:
            return ""

    # noinspection PyMethodMayBeStatic
    def extractRelTarget(self, wsRel):
        """ Extracts relation target and target sense definition (if exists). """
        result = ["", ""]

        lastBracket = wsRel.lastIndexOf('')
        if lastBracket > 0:
            wsRel = wsRel[0:lastBracket]
        else:
            return result

        wsRel = wsRel.replace("", "").replace(":", "")
        parts = wsRel.split("\\|")
        if len(parts) > 2:
            result[0] = parts[1]
            if parts[2] != "-":
                result[1] = parts[2]
        elif len(parts) > 1:
            result[0] = parts[1]

        return result
