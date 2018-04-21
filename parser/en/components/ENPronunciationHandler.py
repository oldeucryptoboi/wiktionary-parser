import re

from api import IPronunciation
from api.entry import Pronunciation
from api.util import TemplateParser
from parser.en.components import ENBlockHandler
from parser.util import StringUtils


class ENPronunciationHandler(ENBlockHandler):
    """ Parser component for extracting pronunciations from the English Wiktionary. """

    PRONUNCIATION_CONTEXT = re.compile("\\{\\{(?:a|sense)\\|([^}|]+?)}}")
    PRONUNCIATION = re.compile("\\{\\{(?:IPA|SAMPA)\\|.+?}}")
    PRONUNCIATION_AUDIO = re.compile("\\{\\{audio\\|([^}|]+?)(?:\\|([^}|]+?)(?:\\|lang=[^}|]+)?)?}}")
    PRONUNCIATION_RYHME = re.compile("\\{\\{rhymes\\|([^}|]+?)}}")
    PRONUNCIATION_RAW = re.compile("\\{\\{\\w+-(?:IPA|pron)(?:\\|.*?)?}}")

    def __init__(self):
        self.pronunciations = None

    def canHandle(self, blockHeader):
        blockHeader = StringUtils.strip(blockHeader, "{}=: 1234567890").lower()

        if "pronunciation" == blockHeader or "pronuncaition" == blockHeader \
                or "pronunceation" == blockHeader or "pronunciaton" == blockHeader:
            return True

        return False

    def processHead(self, textLine, context):
        self.pronunciations = list()
        return super().processHead(textLine, context)

    def processBody(self, textLine, context):
        ctx = ""
        for matcher in re.finditer(ENPronunciationHandler.PRONUNCIATION_CONTEXT, textLine):
            ctx += " " + matcher.group(1)

        this = self

        # noinspection PyShadowingNames,PyUnusedLocal
        def handle(self, template):
            pronun_type = IPronunciation.PronunciationType[template.getName()]
            for i in range(template.getNumberedParamsCount()):
                pronunciation = template.getNumberedParam(i)
                if pronunciation.strip():
                    this.pronunciations.append(Pronunciation(pronun_type, pronunciation, str(ctx).strip()))
            return None

        for pronunMatcher in re.finditer(ENPronunciationHandler.PRONUNCIATION, textLine):
            handler = type("_TemplateHandler", (TemplateParser.ITemplateHandler,), {"handle": handle})
            TemplateParser.parse(pronunMatcher.group(), handler())

        for matcher in re.finditer(ENPronunciationHandler.PRONUNCIATION_RAW, textLine):
            self.pronunciations.append(Pronunciation(Pronunciation.PronunciationType.RAW, matcher.group(0), None))

        # TODO: english pronunciation key/AHD
        # TODO: separate property for sense
        for matcher in re.finditer(ENPronunciationHandler.PRONUNCIATION_AUDIO, textLine):
            note = ctx + " " + matcher.group(2)
            self.pronunciations.append(
                Pronunciation(Pronunciation.PronunciationType.AUDIO, matcher.group(1), note.strip()))

        matcher = re.search(ENPronunciationHandler.PRONUNCIATION_RYHME, textLine)
        if matcher is not None:
            self.pronunciations.append(
                Pronunciation(Pronunciation.PronunciationType.RHYME, matcher.group(1), str(ctx).strip()))

        return False

    def fillContent(self, context):
        """ There is no PosEntry yet - store the pronunciations in the context
            and add them later on (in ENWordLanguageHandler). """
        context.setPronunciations(self.pronunciations)

    def getPronunciations(self):
        """ Returns the list of all extracted pronunciations. """
        return self.pronunciations
