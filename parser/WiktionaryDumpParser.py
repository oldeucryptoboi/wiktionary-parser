from errors import WiktionaryException, ParseException, IOException
from compat import Logger
from parser.util import DumpInfo
from api.util import Language
from datetime import datetime

from parser import *


class WiktionaryDumpParser(XMLDumpParser, IWiktionaryMultistreamDumpParser):
    """ Extension of the :@link XMLDumpParser that reads the different XML tags
        of the Wiktionary XML dump file format and provides hotspots for each
        type of information. A number of :@link IWiktionaryPageParsers can
        be registered for this dump parser. The page parsers are called whenever
        a certain information has been read. Different page parsers can, for
        example, handle different page types or namespaces. """

    logger = Logger.getLogger("WiktionaryDumpParser")

    def __init__(self, pageParsers=None):
        """ Initializes the dump parser and registers the given page parsers. """
        self.timestampFormat = datetime.utcnow()
        self.parserRegistry = list()
        if bool(pageParsers):
            for pageParser in pageParsers:
                self.register(pageParser)

        self.dumpInfo = None
        self.inPage = None

    def register(self, pageParser):
        self.parserRegistry.append(pageParser)
    
    def getPageParsers(self):
        return self.parserRegistry
    
    def parseFile(self, dumpFile):  # throws WiktionaryException :
        self.dumpInfo = DumpInfo(dumpFile, self)
        super().parseFile(dumpFile)
        self.onClose()
    
    def parseMultistream(self, multistreamDumpFile, indexFile, filter_):  # throws WiktionaryException :
        self.dumpInfo = DumpInfo(multistreamDumpFile, self)
        try:
            MultistreamXMLDumpParser(self).parseMultistream(multistreamDumpFile, indexFile, filter_)
            self.onClose()
        except IOException as e:
            raise WiktionaryException(e)
        
    def onParserStart(self):
        super().onParserStart()
        self.inPage = False
        self.dumpInfo.reset()
        for pageParser in self.parserRegistry:
            pageParser.onParserStart(self.dumpInfo)

    def onSiteInfoComplete(self):
        for pageParser in self.parserRegistry:
            pageParser.onSiteInfoComplete(self.dumpInfo)
    
    def onParserEnd(self):
        super().onParserEnd()
        for pageParser in self.parserRegistry:
            pageParser.onParserEnd(self.dumpInfo)
    
    def onClose(self):
        for pageParser in self.parserRegistry:
            pageParser.onClose(self.dumpInfo)
    
    def onElementStart(self, name, handler):
        if "page" == name:
            self.inPage = True
            self.onPageStart()
        
    def onElementEnd(self, name, handler):
        # Check URL.
        if "base" == name:
            self.setBaseURL(handler.getContents())
        elif "namespace" == name and handler.hasContents():
            self.addNamespace(handler.getContents())
        elif "siteinfo" == name:
            self.onSiteInfoComplete()
        elif "page" == name:
            self.inPage = False
            self.onPageEnd()
        
        # Article contents.
        if self.inPage:
            if "page" == handler.getParent():
                if "id" == name:
                    self.setPageId(int(handler.getContents()))
                elif "title" == name:
                    self.setTitle(handler.getContents())
            elif "revision" == handler.getParent():
                if "id" == name:
                    self.setRevision(int(handler.getContents()))
                elif "timestamp" == name:
                    try:
                        self.setTimestamp(self.parseTimestamp(handler.getContents()))
                    except ParseException:
                        self.setTimestamp(None)
                    
                elif "text" == name:
                    self.setText(handler.getContents())
                
            elif "contributor" == handler.getParent():
                if "username" == name:
                    self.setAuthor(handler.getContents())

    def onPageStart(self):
        for pageParser in self.parserRegistry:
            pageParser.onPageStart()

    def onPageEnd(self):
        for pageParser in self.parserRegistry:
            pageParser.onPageEnd()

        self.dumpInfo.incrementProcessedPages()
        # if self.dumpInfo.getProcessedPages() % 25000 == 0:
        #     WiktionaryDumpParser.logger.info("Parsed " + str(self.dumpInfo.getProcessedPages()) + " pages")
        pass

    def setBaseURL(self, baseURL):
        self.dumpInfo.setDumpLanguage(self.resolveLanguage(baseURL))

    # noinspection PyMethodMayBeStatic
    def resolveLanguage(self, baseURL):
        idx = baseURL.find("://")
        language = baseURL[idx + 3: idx + 5]
        return Language.findByCode(language)

    def addNamespace(self, namespace):
        self.dumpInfo.addNamespace(namespace)

    def setAuthor(self, author):
        for pageParser in self.parserRegistry:
            pageParser.setAuthor(author)

    def setRevision(self, revisionId):
        for pageParser in self.parserRegistry:
            pageParser.setRevision(revisionId)

    def setTimestamp(self, timestamp):
        for pageParser in self.parserRegistry:
            pageParser.setTimestamp(timestamp)

    def setPageId(self, pageId):
        for pageParser in self.parserRegistry:
            pageParser.setPageId(pageId)

    def setTitle(self, title):
        namespace = None
        idx = title.find(':')
        if idx >= 0:
            namespace = title[0: idx]
            if not self.dumpInfo.hasNamespace(namespace):
                namespace = None
            else:
                title = title[idx + 1:]
        
        for pageParser in self.parserRegistry:
            pageParser.setTitle(title, namespace)

    def setText(self, text):
        for pageParser in self.parserRegistry:
            pageParser.setText(text)

    def parseTimestamp(self, dateString):  # throws ParseException :
        return self.timestampFormat.strftime(dateString)

    def getDumpInfo(self):
        """ Returns information on the current dump file and its parsing
         *  progress. The result is <code>None</code> if the parser has not
         *  yet been started (i.e., the :@link #parse(File) method has not
         *  been called). """
        return self.dumpInfo
