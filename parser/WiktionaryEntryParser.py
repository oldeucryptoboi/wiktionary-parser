import re
from compat import StringReader, Logger
from errors import RuntimeException
from enum import Enum

from parser import *


class WiktionaryEntryParser(IWiktionaryEntryParser):
    """ Base implementation for parsing the textual contents of an article page in
        order to construct :@link IWiktionaryEntry and :@link IWiktionarySense
        instances. The parser is based on a finite state machine using a set
        of block handlers that are being asked if they want to process the current
        line of text. If so, the handler is in a position to process the subsequent
        lines until the entire block has been processed and the next line is
        subject to initialize a different block handler. Since there are large
        differences between the individual Wiktionary language editions, there
        should be one subclass of this parser for each language edition, which
        cares about language-specific adaptation and the selection of the
        block handlers used. """

    class ParseStatus(Enum):
        IN_BODY = 1
        IN_HEAD = 2

    logger = Logger.getLogger("WiktionaryEntryParser")

    COMMENT_PATTERN = re.compile("<!--((?!-->)[^\0])*?-->")
    IMAGE_PATTERN = re.compile("\\[\\[Image:([^\\]]+?)\\|[^\\]]+?\\]\\]")
    REFERENCES_PATTERN = re.compile("<ref[^>]*>.+?</ref>")

    def __init__(self, language, redirectName):
        """ Instantiates the entry parser for the given language.
            @param redirectName denotes the language-specific prefix used for
                redirection. """
        self.handlers = list()
        self.language = language
        self.redirectTemplate = "#" + redirectName + " [["
        self.entryId = 0

    def parse(self, page, text):
        # Handle redirects.
        if self.checkForRedirect(page, text):
            return

        LINE_SEPARATOR = "\n"

        # Remove html comments.
        text = re.sub(WiktionaryEntryParser.COMMENT_PATTERN, "", text)
        text = re.sub(WiktionaryEntryParser.IMAGE_PATTERN, "", text)
        text = re.sub(WiktionaryEntryParser.REFERENCES_PATTERN, "", text)
        reader = StringReader(text)
        try:
            # contains information shared by workers.
            context = self.createParsingContext(page)
            line = reader.readLine()
            handler = unfinishedHandler = None

            status = WiktionaryEntryParser.ParseStatus.IN_HEAD

            # Decides if parser take control of the parsing or let a worker object decide if its work is finished.
            parserTakeControl = False
            EOT = not line
            while not EOT:
                line = line.strip()

                lineSep = line + LINE_SEPARATOR
                if status == WiktionaryEntryParser.ParseStatus.IN_HEAD:
                    # HEAD
                    if self.isStartOfBlock(line):
                        handler = self.selectHandler(line)
                        self.logger.fine("pre-processing " + line + " worker is " + str(handler))

                    # continue only when the worker finishes processing head part.
                    if handler is not None and handler.processHead(lineSep, context):
                        self.logger.fine("processing " + line)
                        status = WiktionaryEntryParser.ParseStatus.IN_BODY
                        unfinishedHandler = handler

                    line = reader.readLine()

                elif status == WiktionaryEntryParser.ParseStatus.IN_BODY:
                    # BODY
                    if not parserTakeControl:
                        parserTakeControl = not handler.processBody(lineSep, context)
                        if parserTakeControl:
                            if self.isStartOfBlock(line):
                                handler.fillContent(context)
                                unfinishedHandler = None
                                handler = None
                                status = WiktionaryEntryParser.ParseStatus.IN_HEAD
                                parserTakeControl = False
                            else:
                                line = reader.readLine()
                        else:
                            line = reader.readLine()
                    else:
                        if self.isStartOfBlock(line):
                            handler.fillContent(context)
                            unfinishedHandler = None
                            handler = None
                            status = WiktionaryEntryParser.ParseStatus.IN_HEAD
                            parserTakeControl = False
                        else:
                            handler.processBody(lineSep, context)
                            line = reader.readLine()

                if line is None:
                    if unfinishedHandler is not None:
                        unfinishedHandler.fillContent(context)
                    EOT = True

        except Exception as e:
            # DEBUG
            import traceback
            traceback.print_exc()

            raise RuntimeException("Error while parsing text of article " + page.getTitle(), e)

    def createParsingContext(self, page):
        return None

    def checkForRedirect(self, page, text):
        """ Check if the specified text is a redirect and set the redirect target of
            the given Wiktionary page. """
        if text.endswith("]]") and text.startswith(self.redirectTemplate):
            page.setRedirectTarget(text[len(self.redirectTemplate), text.length() - 2])
            return True
        else:
            return False

    def isStartOfBlock(self, line):
        """ Hotspot for deciding if the given line is a potential start of a new
            article constituent. This may include headlines, templates, or other
            typographic variants. """
        pass

    def selectHandler(self, line):
        """ Find a handler that is willing to handle the given line. """
        for handler in self.handlers:
            if handler.canHandle(line):
                return handler

        return None

    def register(self, handler):
        """ Register the given handler that will be invoked during the parsing. """
        self.handlers.append(handler)

    def getLanguage(self):
        """ Returns the language of this parser's Wiktionary edition. """
        return self.language
