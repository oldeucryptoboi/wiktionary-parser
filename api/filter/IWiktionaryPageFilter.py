class IWiktionaryPageFilter:
    """ Interface for implementing a filter for :@link IWiktionaryPages.
        That is, a possibility for selecting which pages are to be processed
        (i.e., accepted) or skipped (i.e., filtered out). """

    def accept(self, page):
        """ Return <code>True</code> if the given page should be accepted or
         *  <code>False</code> if it should be filtered out. """
        pass
