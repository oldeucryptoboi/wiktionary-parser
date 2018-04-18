import re
from parser.util import IBlockHandler
from parser.en.components.ENBlockHandler import ENBlockHandler
from api.util.Language import Language


class ENWordLanguageHandler(ENBlockHandler, IBlockHandler):
    """ Parser component for extracting a words language from the English Wiktionary. """

    LANGUAGE_HEADER = re.compile("^\\s*=+\\s*\\[*\\s*(.*?)\\s*\\]*\\s*=+")  

    def __init__(self):
        self.language = None

    def canHandle(self, blockHeader):
        if "----" == blockHeader:
            self.language = None
            return True
        
        self.language = None

        # print(textLine)
        matcher = re.search(ENWordLanguageHandler.LANGUAGE_HEADER, blockHeader)
        if not matcher:
            return False
                
        # print(matcher.group(1))
        self.language = Language.findByName(matcher.group(1))
        return bool(self.language)

    def processHead(self, textLine, context):
        return True

    def processBody(self, textLine, context):
        return False

    def fillContent(self, context):
        context.setLanguage(self.language)
