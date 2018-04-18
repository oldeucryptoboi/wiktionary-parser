class IBlockHandler:
    """ A handler encapsulated the extraction of the information items encoded in
        a certain article constituent. There might be, for example, a handler
        for extracting pronunciation information. """

    def canHandle(self, blockHeader):
        """ Return <code>True</code> if the handler requests to process the article
            constituent starting at the given line of text. """
        pass

    def processHead(self, line, context):
        """ If the handler requested to process this constituent, this hotspot
            will be called for processing the section header of this
            article constituent. Return <code>True</code> if the handler
            requests to handle also the body of this constituent. """
        pass

    def processBody(self, line, context):
        """ If the handler requested to process the body of this constituent, this
            hotspot will be called for processing each line of the constituent's
            body. Return <code>True</code> if the handler requests to handle also
            the next line using this handler. """
        pass

    def fillContent(self, context):
        """ This hotspot is invoked if the parser releases this handler. It can be
            used to store the extracted information to the Wiktionary data
            objects stored in the parsing context. """
        pass
