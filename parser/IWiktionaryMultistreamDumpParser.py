from parser import *


class IWiktionaryMultistreamDumpParser(IWiktionaryDumpParser):

    def parseMultistream(self, multistreamDumpFile, indexFile,  filter_):   # throws WiktionaryException
        """ Parses a multistream XML dump file

            @param multistreamDumpFile the dumpfile (<code>*-pages-articles-multistream-index.txt.bz2</code>)
            @param indexFile           the matching index file (<code>*-pages-articles-multistream.xml.bz2</code>)
            @param filter_              the filter to use to constrain the parsed pages
            @throws WiktionaryException """
        pass
