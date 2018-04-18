import os.path
import bz2
import fileinput
from compat import *

from parser import *


class MultistreamXMLDumpParser:
    """ A parser which can deal with MediaWiki multistreams.

        Multistreams consist of several concatenated bz2 stream which typically only contain
        100 pages. The index file (*-multistream-index.txt.bz2) is an index into this file, in the format
        <code>offset:page_id:page_title</code>, e.g.
        <pre>
        654:6:Wiktionary:Welcome, newcomers
        654:7:Wiktionary:GNU Free Documentation License
        ...
        </pre>
        The actual parsing is delegated to a standard :@link XMLDumpParser. """

    logger = Logger.getLogger("MultistreamXMLDumpParser")

    MEDIAWIKI_OPENING = "<mediawiki>"
    MEDIAWIKI_CLOSING = "</mediawiki>"

    def __init__(self, parser):
        self.parser = parser

    def parseMultistream(self, dumpFile, indexFile, filter_):  # throws IOException :
        self.parse(dumpFile, self.collectOffsets(indexFile, filter_))

    def parse(self, dumpFile, offsets):  # throws IOException :
        if not offsets:
            raise IOException("no valid offsets")

        offsets.add(0)  # make sure header / siteInfo gets parsed
        with open(dumpFile, "r") as file:
            for offset in offsets:
                # logger.fine("parsing contents at offset " + offset)
                self.parser.parseStream(self.getInputStreamAtOffset(file, offset))

    # noinspection PyMethodMayBeStatic
    def collectOffsets(self, indexFile, filter_):  # throws IOException :
        MultistreamXMLDumpParser.logger.fine("parsing index file " + indexFile)
        bufferedReader = None
        try:
            offsets = set()
            bufferedReader = BZip2InputStream(indexFile)
            for line in bufferedReader.readLine():
                split = line.split(":", 3)
                offset = Long.parseLong(split[0])
                pageId = Long.parseLong(split[1])
                pageTitle = split[2]

                if filter_.accept(pageId, pageTitle):
                    offsets.add(offset)
            return offsets

        finally:
            if bufferedReader is not None:
                bufferedReader.close()

    def getInputStreamAtOffset(self, file, offset):  # throws IOException :
        if offset + 2 >= os.path.getsize(file):
            raise IOException("read past EOF")

        file.seek(offset + 2)  # skip past 'BZ' header

        with bz2.BZ2File(file, "rb") as file:
            if offset == 0:
                result = fileinput.FileInput([file, io.StringIO(self.MEDIAWIKI_CLOSING)])
            else:
                result = fileinput.FileInput([io.StringIO(self.MEDIAWIKI_OPENING), file,
                                              io.StringIO(MultistreamXMLDumpParser.MEDIAWIKI_CLOSING)])

        return result
