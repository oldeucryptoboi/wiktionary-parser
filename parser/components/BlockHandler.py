from parser.util import IBlockHandler


class BlockHandler(IBlockHandler):
    """ Abstract parser component for processing article constituents. The handler
        can be initialized with a set of fixed labels that denote the header of
        an article constituent that is to be parsed by this handler. """

    """ Default implementation of the :@link IBlockHandler interface that serves 
        as a base class for parsing any article constituent. """

    def __init__(self, *labels):
        """ Initializes the block handler for parsing all sections starting with
            one of the specified labels. """
        self.labels = list(labels)

    def canHandle(self, blockHeader):
        blockHeader = blockHeader.strip("{}=: ")
        for label in self.labels:
            if label == blockHeader:
                return True

        return False

    def processHead(self, text, context):
        return True

    def processBody(self, textLine, context):
        return False

    def fillContent(self, context):
        pass

    def getLabels(self):
        return self.labels
