class MultistreamFilter:

    def accept(self, pageId, pageTitle):
        """ @return whether to include the page with pageId and pageTitle in the parse """
        pass


class IncludingNames(MultistreamFilter):
    """ A filter which includes only page titles contained in  the specified list """

    def __init__(self, pageNames):
        self.pageNames = pageNames

    def accept(self, pageId, pageTitle):
        return pageTitle in self.pageNames
