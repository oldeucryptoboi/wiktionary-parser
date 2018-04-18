from api.filter import *


class WiktionarySenseFilter(WiktionaryEntryFilter, IWiktionarySenseFilter):
    """ Default implementation of the :@link IWiktionarySenseFilter interface
        which inherits all filter options of the :@link WiktionaryEntryFilter """

    def __init__(self):
        """ Initializes a page filter without any filter restrictions. """
        super().__init__()

    def accept(self, sense):
        if not self.accept(sense.getEntry()):
            return False

        return True
