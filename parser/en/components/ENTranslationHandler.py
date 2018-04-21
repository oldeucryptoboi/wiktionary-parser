import re
from collections import OrderedDict as TreeMap

from api.entry import WikiString, WiktionaryTranslation
from parser.en.components import ENBlockHandler, ENSemanticRelationHandler
from api.util import Language, TemplateParser
from parser.util import StringUtils


class ENTranslationHandler(ENBlockHandler):
    """ Parser component for extracting translations from the English Wiktionary. """

    LANGUAGE = re.compile("^\\*:?\\s*(.*?):\\s*")  
    SEPARATOR = re.compile("(?:]]|}}|\\))\\s*([;,])")  

    WIKILINK_TRANSLATION = "(?:\\[\\[.*?]]\\s*)+"  
    TEMPLATE_TRANSLATION = "\\{\\{t.*?}}"  

    TRANSLATION = re.compile(  
        "^" +
        "(?P<prefix>.*\\s+)??" +
        "(?P<content>" + WIKILINK_TRANSLATION + "|" + TEMPLATE_TRANSLATION + ")" +
        "(?P<postfix>.*)" +
        "$"
    )

    def __init__(self):
        """ Initializes the block handler for parsing all sections starting with
         *  one of the specified labels. """
        super().__init__("Translations")

        self.currentSense = None
        self.sensNum2trans = None

    def processHead(self, text, context):
        self.currentSense = ""
        self.sensNum2trans = TreeMap()
        return True

    def processBody(self, text, context):
        text = text.strip()

        if text.startswith("{{trans-mid}}") or text.startswith("{{mid}}"):
            return True
        if text.startswith("{{trans-top|") and ("}}" in text):
            template = TemplateParser.parseTemplate(text[2: text.find("}}")])
            if template is not None and template.getNumberedParamsCount() >= 1:
                self.currentSense = template.getNumberedParam(0)

            return True

        if text.startswith("{{top}}"):
            self.currentSense = ""
            return True

        if text.startswith("{{trans-bottom}}") or text.startswith("{{bottom}}"):  # This template indicates the end of the translation block
            return False
        if text.startswith("{{") or text.startswith("=="):  # Indicates that a new block has just started.
            return False

        matcher = re.search(ENTranslationHandler.LANGUAGE, text)
        if matcher is None:
            return False

        languageText = WikiString.removeWikiLinks(matcher.group(1).strip())
        language = Language.findByName(languageText)

        endOffSet = matcher.end()
        if endOffSet > len(text) - 1:
            return False

        remainingText = text[endOffSet:]

        for part in self.splitTranslationParts(remainingText):
            translation = self.parseTranslation(language, part)
            if translation is not None:
                # Save the translation
                if self.currentSense not in self.sensNum2trans:
                    self.sensNum2trans[self.currentSense] = list()
                translations = self.sensNum2trans[self.currentSense]
                translations.append(translation)

        return True

    def parseTranslation(self, languageHeader, text):
        matcher = re.search(ENTranslationHandler.TRANSLATION, text)
        if matcher is None:
            return None

        prefix = matcher.group("prefix")
        content = matcher.group("content")
        postfix = matcher.group("postfix")

        if content.startswith("{{"):
            translation = self.parseTemplate(content)
        else:
            translation = WiktionaryTranslation(languageHeader, StringUtils.cleanText(WikiString.removeWikiLinks(content)))

        if translation is not None:
            additionalInformation = ""
            if prefix is not None:
                additionalInformation += prefix.strip()

            if translation.getGender() is not None:
                additionalInformation += " {{" + translation.getGender() + "}} "

            additionalInformation += postfix
            translation.setAdditionalInformation(StringUtils.cleanText(additionalInformation.strip()))
            if self.currentSense is not None and len(self.currentSense.strip()) > 0:
                translation.setRawSense(self.currentSense.strip())

            return translation
        else:
            return None

    @staticmethod
    def splitTranslationParts(text):
        results = list()
        lastStart = 0
        for m in re.finditer(ENTranslationHandler.SEPARATOR, text):
            candidate = text[lastStart: m.start(1)].strip()
            if re.search(ENTranslationHandler.TRANSLATION, candidate) is not None:
                results.append(candidate)
                lastStart = m.end(1)

        results.append(text[lastStart:].strip())
        return results

    # noinspection PyMethodMayBeStatic
    def parseTemplate(self, templateString):
        template = TemplateParser.parseTemplate(templateString[2:-2])
        if template is None or template.getNumberedParamsCount() <= 1:
            return None

        translationText = StringUtils.cleanText(WikiString.removeWikiLinks(template.getNumberedParam(1)))
        if not translationText:
            return None

        languageCode = template.getNumberedParam(0)
        transliteration = template.getNamedParam("tr")
        translation = WiktionaryTranslation(Language.findByCode(languageCode), translationText)
        if template.getNumberedParamsCount() > 2 and "=" not in template.getNumberedParam(2):
            translation.setGender(template.getNumberedParam(2))

        translation.setCheckNeeded("check" in template.getName())
        if transliteration is not None:
            translation.setTransliteration(StringUtils.cleanText(transliteration))

        return translation

    def fillContent(self, context):
        """
         * Add parsed translation into senseEntry. If no mapping is found, the translation is added to posEntry.
        """
        posEntry = context.findEntry()
        if posEntry is not None:
            for key, value in self.sensNum2trans.items():
                targetSense = self.findSense(posEntry, key)

                for translation in value:
                    targetSense.addTranslation(translation)

    # noinspection PyMethodMayBeStatic
    def findSense(self, entry, marker):
        sense = ENSemanticRelationHandler.findMatchingSense(entry, marker)
        if sense is not None:
            return sense
        else:
            return entry.getUnassignedSense()
