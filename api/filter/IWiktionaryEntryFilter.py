class IWiktionaryEntryFilter:
    """ Interface for implementing a filter for :@link IWiktionaryEntrys.
        That is, a possibility for selecting which entries are to be processed
        (i.e., accepted) or skipped (i.e., filtered out). """

    def accept(self, entry):
        """ Return <code>True</code> if the given entry should be accepted or
            <code>False</code> if it should be filtered out. """
        pass
