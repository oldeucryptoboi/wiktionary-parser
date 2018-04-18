from parser.en.components.ENBlockHandler import ENBlockHandler
from parser.util import StringUtils
from api.entry.WikiString import WikiString


class ENEtymologyHandler(ENBlockHandler):
    """ Parser component for extracting etymological information from
        the English Wiktionary. """

    def __init__(self):
        self.contentBuffer = None

    SPELLINGS = ["etymology", "etymolgy", "eytomology", "etmology", "eymology"]

    def canHandle(self, blockHeader):
        return StringUtils.strip(blockHeader, "{}=: 1234567890").lower() in ENEtymologyHandler.SPELLINGS
    
    def processHead(self, textLine, context):
        self.contentBuffer = ""
        return True
    
    def processBody(self, textLine, context):
        if bool(textLine) and not textLine.startswith("==="):
            self.contentBuffer += textLine
        
        return False
    
    def fillContent(self, context):
        if bool(self.contentBuffer.strip()):
            context.setEtymology(WikiString(self.contentBuffer.strip()))
        else:
            context.setEtymology(None)
