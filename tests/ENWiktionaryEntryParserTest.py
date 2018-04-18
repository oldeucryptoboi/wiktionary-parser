from compat import *
import os

from api.entry import WiktionaryPage
from parser.en import ENWiktionaryEntryParser
from parser.en.components import ENEntryFactory
from parser.util import ParsingContext


class ENWiktionaryEntryParserTest:
    """ Abstract test case for English Wiktionary parsers. """

    # noinspection PyMethodMayBeStatic
    def parse(self, fileName):  # throws IOException
        text = ""
        reader = FileReader(File(os.path.join(os.getcwd(), "resources/articles-en/"), fileName))

        for line in reader.readLines():
            text += line.rstrip('\n') + "\n"
        reader.close()
        result = WiktionaryPage()
        result.setTitle(fileName.replace(".txt", ""))
        parser = ENWiktionaryEntryParser()
        parser.parse(result, text)
        return result

    # noinspection PyMethodMayBeStatic
    def process(self, handler, *body):
        context = ParsingContext(WiktionaryPage(), ENEntryFactory())

        handler.processHead("testing", context)
        for line in body:
            handler.processBody(line, context)

        handler.fillContent(context)

        return context.findEntry()
