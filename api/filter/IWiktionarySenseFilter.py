class IWiktionarySenseFilter:
    """ Interface for implementing a filter for :@link IWiktionarySenses.
        That is, a possibility for selecting which senses are to be processed
        (i.e., accepted) or skipped (i.e., filtered out). """

    def accept(self, sense):
        """ Return <code>True</code> if the given sense should be accepted or
            <code>False</code> if it should be filtered out. """
        pass
