from parser.components.BlockHandler import BlockHandler


class ENBlockHandler(BlockHandler):
    """ Abstract base class for all parser components for the English Wiktionary. """

    def __init__(self, *labels):
        """ Initializes the block handler for parsing all sections starting with
            one of the specified labels. """
        super().__init__(*labels)
