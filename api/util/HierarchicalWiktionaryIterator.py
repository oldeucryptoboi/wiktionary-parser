from .WiktionaryIterator import WiktionaryIterator


class HierarchicalWiktionaryIterator(WiktionaryIterator):
    """ Generic implementation for an iterator of iterators. That is, an object,
        which is initialized with an iterator of type OuterType. This iterator is
        being iterated an converted into an iterator of type IterableType. For each
        element of the outer iterator, all elements of the inner iterator are then
        traversed. For example, a hierarchical iterator of outer type
        WiktionaryEntry and inner type WiktionarySense enumerates all senses of
        entry1, then all senses of entry2, etc.
        @param <IterableType> The type the inner iterator.
        @param <OuterType> The type the outer iterator. """

    def __init__(self, outerIterator):
        """ Initialize the iterator for the given outer type. """
        super().__init__()
        self.outerIterator = outerIterator
        self.innerIterator = None

    def fetchNext(self):
        if self.innerIterator is not None and self.innerIterator.hasNext():
            return self.innerIterator.next()
        if not self.outerIterator.hasNext():
            return None

        outer = self.outerIterator.next()
        self.innerIterator = self.getInnerIterator(outer)
        if self.innerIterator is not None and self.innerIterator.hasNext():
            return self.innerIterator.next()
        else:
            return None

    # noinspection PyMethodMayBeStatic
    def getInnerIterator(self, outer):
        return outer

    def doClose(self):
        if self.innerIterator is not None:
            self.innerIterator.close()
